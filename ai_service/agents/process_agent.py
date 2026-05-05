# from typing import List, Dict, Any
# import re

# # =========================
# # CONFIG
# # =========================
# MAX_SNIPPET_LENGTH = 300
# MIN_SNIPPET_LENGTH = 20   # ↓ giảm để không mất dữ liệu tốt

# # =========================
# # CLEAN TEXT
# # =========================
# def clean_text(text: str) -> str:
#     """
#     Làm sạch text nhưng KHÔNG phá nội dung quan trọng
#     """
#     if not text:
#         return ""

#     # 1. Normalize whitespace
#     text = re.sub(r"\s+", " ", text)

#     # 2. Remove markdown noise (nhẹ nhàng)
#     text = re.sub(r"[*#>`_]", "", text)

#     return text.strip()


# # =========================
# # TRUNCATE SNIPPET
# # =========================
# def truncate(text: str, max_len: int) -> str:
#     """
#     Cắt snippet nhưng giữ nguyên word boundary
#     """
#     if len(text) <= max_len:
#         return text

#     truncated = text[:max_len]
#     last_space = truncated.rfind(" ")

#     if last_space > 0:
#         truncated = truncated[:last_space]

#     return truncated + "..."


# # =========================
# # FILTER NOISE
# # =========================
# def is_valid_item(snippet: str, url: str) -> bool:
#     """
#     Filter nhẹ → tránh mất dữ liệu thật
#     """

#     # ❗ chỉ loại nếu QUÁ NGẮN
#     if len(snippet) < MIN_SNIPPET_LENGTH:
#         return False

#     # ❗ chỉ loại video nếu muốn (optional)
#     if "youtube.com" in url:
#         return False

#     return True


# # =========================
# # DEDUPLICATE (improved)
# # =========================
# def deduplicate_content(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#     """
#     Deduplicate thông minh hơn:
#     - Ưu tiên URL (chuẩn nhất)
#     - fallback bằng snippet similarity lite
#     """

#     seen_urls = set()
#     seen_keys = set()
#     unique = []

#     for item in results:
#         url = item["url"]
#         snippet = item["snippet"].lower()

#         # 1. Check URL trước (chính xác nhất)
#         if url in seen_urls:
#             continue

#         # 2. Check nội dung (fallback)
#         key = snippet[:120]

#         if key in seen_keys:
#             continue

#         seen_urls.add(url)
#         seen_keys.add(key)
#         unique.append(item)

#     return unique


# # =========================
# # MAIN PROCESS FUNCTION
# # =========================
# async def process(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#     """
#     Process Agent Pipeline:

#     1. Clean text
#     2. Filter noise (nhẹ)
#     3. Truncate để tiết kiệm token
#     4. Deduplicate
#     5. Sort lại (đảm bảo giữ ranking)
#     """

#     if not results:
#         return []

#     processed = []

#     for item in results:
#         # =========================
#         # 1. CLEAN
#         # =========================
#         title = clean_text(item.get("title", ""))
#         snippet = clean_text(item.get("snippet", ""))
#         url = item.get("url", "")

#         # =========================
#         # 2. FILTER
#         # =========================
#         if not is_valid_item(snippet, url):
#             continue

#         # =========================
#         # 3. TRUNCATE
#         # =========================
#         snippet = truncate(snippet, MAX_SNIPPET_LENGTH)

#         # =========================
#         # 4. BUILD ITEM
#         # =========================
#         processed.append({
#             "title": title,
#             "snippet": snippet,
#             "url": url,
#             "source": item.get("source", "unknown"),
#             "score": item.get("score", 0)
#         })

#     # =========================
#     # 5. DEDUPLICATE
#     # =========================
#     processed = deduplicate_content(processed)

#     # =========================
#     # 6. SORT (GIỮ RANKING)
#     # =========================
#     processed = sorted(processed, key=lambda x: x["score"], reverse=True)

#     return processed

import re
import json
import math
from typing import List, Dict, Any


# =========================
# 1. CLEAN HTML / NOISE
# =========================
def clean_text(text: str) -> str:
    if not text:
        return ""

    # remove html tags
    text = re.sub(r"<.*?>", " ", text)

    # remove ads patterns
    ad_keywords = ["advertisement", "sponsored", "ads", "promotion"]
    for k in ad_keywords:
        text = re.sub(k, " ", text, flags=re.IGNORECASE)

    # normalize spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================
# 2. ENTITY EXTRACTION
# =========================
def extract_entities(text: str) -> List[str]:
    # simple heuristic (production có thể dùng NLP/NER model)
    brands = [
        "iphone", "samsung", "xiaomi", "oppo",
        "sony", "fujifilm", "macbook", "windows"
    ]

    text_lower = text.lower()
    found = []

    for b in brands:
        if b in text_lower:
            found.append(b)

    return list(set(found))


# =========================
# 3. PRICE EXTRACTION
# =========================
def extract_price(text: str) -> List[str]:
    # support: 1.000$, $999, 20 triệu, etc.
    patterns = [
        r"\$\s?\d+(?:,\d{3})*(?:\.\d+)?",
        r"\d+(?:\.\d+)?\s?(?:usd|vnd|triệu|k|$)"
    ]

    prices = []
    for p in patterns:
        prices += re.findall(p, text.lower())

    return prices


# =========================
# 4. KEY FACT EXTRACTION
# =========================
def extract_key_facts(text: str) -> List[str]:
    sentences = re.split(r"[.!?]", text)
    facts = []

    keywords = ["feature", "spec", "battery", "camera", "performance", "chip"]

    for s in sentences:
        if any(k in s.lower() for k in keywords):
            facts.append(s.strip())

    return facts


# =========================
# 5. NORMALIZATION
# =========================
def normalize_item(item: Dict[str, Any]) -> Dict[str, Any]:
    text = clean_text(item.get("snippet", ""))

    return {
        "title": clean_text(item.get("title", "")),
        "url": item.get("url"),
        "source": item.get("source", "web"),
        "text": text
    }


# =========================
# 6. SUMMARIZATION (simple heuristic)
# =========================
def summarize(text: str) -> str:
    sentences = text.split(".")
    return ". ".join(sentences[:2]).strip()


# =========================
# 7. CONFLICT DETECTION
# =========================
def detect_conflicts(items: List[Dict[str, Any]]) -> List[str]:
    conflicts = []

    price_map = {}

    for item in items:
        prices = extract_price(item["text"])
        for p in prices:
            price_map.setdefault(item["title"], []).append(p)

    # simple conflict rule
    for k, v in price_map.items():
        if len(set(v)) > 1:
            conflicts.append(f"Price conflict in {k}: {v}")

    return conflicts


# =========================
# 8. SCORING RELIABILITY
# =========================
def score_reliability(item: Dict[str, Any]) -> float:
    score = 0.5  # base

    text = item["text"]

    # length bonus
    if len(text) > 100:
        score += 0.1

    # url quality
    if item["url"] and "wiki" in item["url"]:
        score += 0.2

    # has entities
    if extract_entities(text):
        score += 0.1

    # has key facts
    if extract_key_facts(text):
        score += 0.1

    return round(min(score, 1.0), 3)


# =========================
# 9. MAIN PROCESSOR
# =========================
def process_agent(raw_results: List[Dict[str, Any]]) -> Dict[str, Any]:

    processed = []

    for item in raw_results:
        normalized = normalize_item(item)

        text = normalized["text"]

        enriched = {
            **normalized,
            "entities": extract_entities(text),
            "prices": extract_price(text),
            "key_facts": extract_key_facts(text),
            "summary": summarize(text),
        }

        enriched["score"] = score_reliability(enriched)

        processed.append(enriched)

    # detect conflicts
    conflicts = detect_conflicts(processed)

    # sort by score
    processed.sort(key=lambda x: x["score"], reverse=True)

    return {
        "results": processed,
        "conflicts": conflicts,
        "count": len(processed)
    }