import os
import asyncio
import logging
import hashlib
import re
from typing import List, Dict, Any, Optional

import httpx
from tavily import AsyncTavilyClient


logger = logging.getLogger("search_agent")


# =========================
# CONFIG
# =========================
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
MAX_RESULTS = 8
MIN_SCORE = 0.2


def get_tavily_client() -> Optional[AsyncTavilyClient]:
    if not TAVILY_API_KEY:
        return None
    return AsyncTavilyClient(api_key=TAVILY_API_KEY)


# =========================
# 1. KEYWORD NORMALIZATION
# =========================
def normalize_keywords(keywords: List[str]) -> List[str]:
    cleaned = []
    for k in keywords:
        if isinstance(k, str):
            k = k.strip().lower()
            if k:
                cleaned.append(k)
    return cleaned


# =========================
# 2. QUERY EXPANSION
# =========================
def expand_queries(keywords: List[str], intent: str) -> List[str]:
    base = " ".join(keywords)
    queries = {base}

    if intent == "compare":
        queries.add(base + " comparison")
        queries.add(base + " vs review")

    elif intent == "recommendation":
        queries.add(base + " nên mua không")
        queries.add(base + " review")

    else:  # fact
        queries.add(base + " là gì")

    return list(queries)


# =========================
# 3. TOKENIZER
# =========================
def tokenize(text: str) -> List[str]:
    return re.findall(r"\w+", text.lower())


# =========================
# 4. SCORING
# =========================
def score_result(keywords: List[str], item: Dict[str, Any]) -> float:
    kw_tokens = set(tokenize(" ".join(keywords)))
    title_tokens = set(tokenize(item["title"]))
    snippet_tokens = set(tokenize(item["snippet"]))

    score = 0
    for w in kw_tokens:
        if w in title_tokens:
            score += 2
        elif w in snippet_tokens:
            score += 1

    max_score = len(kw_tokens) * 2
    return round(score / max_score, 3) if max_score else 0


# =========================
# 5. DEDUPLICATION
# =========================
def hash_content(item: Dict[str, Any]) -> str:
    text = (item["title"] + item["snippet"]).lower()
    return hashlib.md5(text.encode()).hexdigest()


def deduplicate(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    unique = []

    for r in results:
        key = r.get("url") or hash_content(r)
        if key not in seen:
            seen.add(key)
            unique.append(r)

    return unique


# =========================
# 6. URL VALIDATION
# =========================
async def is_url_alive(client: httpx.AsyncClient, url: str) -> bool:
    try:
        r = await client.head(url, timeout=3, follow_redirects=True)
        return r.status_code < 400
    except:
        return False


# =========================
# 7. SEARCH CORE
# =========================
async def search_agent(plan: Dict[str, Any]) -> Dict[str, Any]:

    keywords = normalize_keywords(plan.get("keywords", []))
    intent = plan.get("intent", "fact")

    if not keywords:
        return {"query": "", "results": []}

    queries = expand_queries(keywords, intent)
    client = get_tavily_client()

    if not client:
        logger.warning("No Tavily API key")
        return {"query": " ".join(keywords), "results": []}

    # =========================
    # MULTI QUERY SEARCH
    # =========================
    tasks = [
        client.search(query=q, search_depth="basic", max_results=MAX_RESULTS)
        for q in queries
    ]

    responses = await asyncio.gather(*tasks, return_exceptions=True)

    raw_results = []

    for res in responses:
        if isinstance(res, Exception):
            continue

        for item in res.get("results", []):
            title = item.get("title")
            url = item.get("url")

            if not title or not url:
                continue

            raw_results.append({
                "title": title.strip(),
                "snippet": item.get("content", "").strip(),
                "url": url,
                "source": "web"
            })

    # =========================
    # DEDUP
    # =========================
    results = deduplicate(raw_results)

    # =========================
    # SCORING
    # =========================
    for r in results:
        r["score"] = score_result(keywords, r)

    results = [r for r in results if r["score"] >= MIN_SCORE]
    results.sort(key=lambda x: x["score"], reverse=True)

    # =========================
    # URL CHECK (PARALLEL)
    # =========================
    async with httpx.AsyncClient() as http_client:
        checks = await asyncio.gather(
            *[is_url_alive(http_client, r["url"]) for r in results],
            return_exceptions=True
        )

    final = [
        r for r, ok in zip(results, checks)
        if ok is True
    ]

    return {
        "query": " ".join(keywords),
        "results": final[:MAX_RESULTS]
    }