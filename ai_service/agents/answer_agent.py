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

GENERAL RULES:
- Do NOT mention internal processing or system roles
- Do NOT hallucinate facts outside provided data
- Prefer higher-score sources when conflicts occur
- If conflicts exist, briefly explain uncertainty
- Use natural, fluent Vietnamese with proper diacritics
- Avoid repetition and meaningless phrasing

----------------------------------------
OUTPUT FORMAT (STRICT)
----------------------------------------

Return ONLY valid JSON with this structure:

{
  "answer": "markdown string",
  "summary": ["bullet 1", "bullet 2", "bullet 3"]
}

----------------------------------------
SUMMARY REQUIREMENTS (KEEP SHORT)
----------------------------------------

- 3–5 bullet points
- Each bullet is ONE complete, concise sentence
- No markdown formatting required
- Focus on key takeaways only

----------------------------------------
DETAILED_REPORT REQUIREMENTS (VERY IMPORTANT)
----------------------------------------

The "answer" MUST be a WELL-DEVELOPED markdown report.

Minimum requirements:
- At least 4–6 paragraphs
- Must be longer than summary
- Must provide explanation, not just listing facts

Structure guideline (flexible but recommended):

# <Title>

## Tổng quan
- Giải thích khái niệm / vấn đề chính

## Phân tích chính
- Diễn giải thông tin từ nhiều nguồn
- So sánh nếu có nhiều đối tượng
- Giải thích điểm khác biệt / nổi bật

## Đánh giá / Nhận định
- Ưu điểm / hạn chế (nếu có)
- Mức độ đáng tin cậy của thông tin

## Kết luận
- Tóm tắt lại insight quan trọng

----------------------------------------
WRITING STYLE
----------------------------------------

- Write like a human expert, not a robot
- Avoid repeating the same sentence patterns
- Use clear, readable paragraphs
- Use bullet points ONLY when helpful
- Do NOT output labels like "answer" or "summary" in the content

----------------------------------------
FAILSAFE
----------------------------------------

If data is insufficient:
- Still produce a structured answer
- Clearly state limitations in analysis
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
            temperature=0.2,
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        data = json.loads(content)

        return {
            "answer": data.get("answer", ""),
            "summary": data.get("summary", []),
            "recommendations": data.get("recommendations", []),
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