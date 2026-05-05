import os
import json
import asyncio
from typing import Dict, Any, List
from openai import AsyncOpenAI

# =========================
# CLIENT
# =========================
def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("GROQ_BASE_URL")

    if not api_key:
        return None

    return AsyncOpenAI(api_key=api_key, base_url=base_url) if base_url else AsyncOpenAI(api_key=api_key)


client = get_client()


# =========================
# FORMAT CONTEXT
# =========================
def build_context(processed_data: Dict[str, Any]) -> str:
    """
    Convert structured data → LLM context
    """

    lines = []

    for i, item in enumerate(processed_data.get("results", []), 1):
        lines.append(f"""
SOURCE {i}:
Title: {item.get('title')}
Summary: {item.get('summary')}
Entities: {item.get('entities')}
Facts: {item.get('key_facts')}
Price: {item.get('prices')}
Score: {item.get('score')}
URL: {item.get('url')}
""")

    if processed_data.get("conflicts"):
        lines.append("\nCONFLICTS:")
        for c in processed_data["conflicts"]:
            lines.append(f"- {c}")

    return "\n".join(lines)


# =========================
# SYSTEM PROMPT
# =========================
SYSTEM_PROMPT = """
You are an Answer Agent in an AI Info System.

Your task:
- Analyze structured multi-source data
- Resolve conflicts between sources
- Produce a final, accurate, helpful answer

RULES:
- Do NOT mention internal processing
- Do NOT hallucinate new facts
- Prefer higher score sources
- If conflict exists, explain uncertainty briefly
- Be concise but informative
- Use Vietnamese unless user context is English

OUTPUT STYLE:
- Clear paragraphs
- Optional bullet points for comparison
- Natural human explanation
"""


# =========================
# ANSWER GENERATION
# =========================
async def answer_agent(
    query: str,
    processed_data: Dict[str, Any]
) -> Dict[str, Any]:

    if not client:
        return {
            "answer": "System not configured (missing API key)",
            "confidence": 0.0
        }

    context = build_context(processed_data)

    user_prompt = f"""
QUESTION:
{query}

DATA:
{context}

TASK:
- Answer the question using ONLY the provided data
- If data is insufficient, say so
"""

    try:
        response = await client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2
        )

        answer = response.choices[0].message.content

        return {
            "answer": answer,
            "sources_used": len(processed_data.get("results", [])),
            "confidence": estimate_confidence(processed_data)
        }

    except Exception as e:
        return {
            "answer": f"Error generating answer: {str(e)}",
            "confidence": 0.0
        }


# =========================
# CONFIDENCE ESTIMATION
# =========================
def estimate_confidence(processed_data: Dict[str, Any]) -> float:
    results = processed_data.get("results", [])

    if not results:
        return 0.0

    avg_score = sum(r.get("score", 0) for r in results) / len(results)

    # boost if multiple sources agree
    if len(results) > 2:
        avg_score += 0.1

    # penalty if conflicts exist
    if processed_data.get("conflicts"):
        avg_score -= 0.1

    return round(min(max(avg_score, 0), 1), 3)