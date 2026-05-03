# agents/orchestrator_agent.py

from openai import OpenAI
import os
import json
from typing import Dict, Any, List

def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("GROQ_BASE_URL")

    if not api_key:
        return None

    # Nếu có GROQ_BASE_URL → dùng Groq
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)

    # fallback OpenAI
    return OpenAI(api_key=api_key)

# =========================
# 1. DEFAULT FALLBACK PLAN
# =========================
def default_plan(query: str) -> Dict[str, Any]:
    """
    Fallback khi LLM lỗi hoặc trả JSON sai.
    """
    return {
        "intent": "fact",
        "needs_search": True,
        "search_depth": "medium",
        "keywords": [query]
    }

def smart_fallback(query: str):
    q = query.lower()

    if "so sánh" in q:
        intent = "compare"
    elif any(k in q for k in ["nên", "có nên"]):
        intent = "recommendation"
    else:
        intent = "fact"

    return {
        "intent": intent,
        "needs_search": True,
        "search_depth": "medium",
        "keywords": [query]
    }

# =========================
# 2. VALIDATE OUTPUT
# =========================
def validate_plan(plan: Dict[str, Any]) -> Dict[str, Any]:
    """
    Đảm bảo JSON đúng format và an toàn.
    """

    valid_intents = ["fact", "compare", "recommendation"]
    valid_depths = ["low", "medium", "high"]

    # intent
    if plan.get("intent") not in valid_intents:
        plan["intent"] = "fact"

    # needs_search
    if not isinstance(plan.get("needs_search"), bool):
        plan["needs_search"] = True

    # search_depth
    if plan.get("search_depth") not in valid_depths:
        plan["search_depth"] = "medium"

    # keywords
    if not isinstance(plan.get("keywords"), list) or len(plan["keywords"]) == 0:
        plan["keywords"] = [plan.get("query", "")]

    return plan

# =========================
# 3. MAIN ORCHESTRATOR
# =========================

async def orchestrate(query: str) -> Dict[str, Any]:
    """
    Orchestrator Agent:
    - Phân tích câu hỏi
    - Quyết định pipeline
    - Trả về kế hoạch thực thi
    """

    system_prompt = """
    Bạn là Orchestrator Agent trong hệ thống InfoAgent.

    Nhiệm vụ:
    1. Phân tích câu hỏi người dùng
    2. Xác định intent:
       - fact (hỏi thông tin)
       - compare (so sánh)
       - recommendation (gợi ý)
    3. Quyết định:
       - có cần search không
    4. Xác định độ sâu search:
       - low (câu hỏi đơn giản)
       - medium (bình thường)
       - high (phức tạp, cần nhiều nguồn)
    5. Trích xuất keyword tìm kiếm (ngắn gọn, rõ ràng)

    QUY TẮC:
    - Không thêm giải thích
    - Chỉ trả JSON hợp lệ
    - keywords phải là list string

    FORMAT:
    {
      "intent": "fact | compare | recommendation",
      "needs_search": true,
      "search_depth": "low | medium | high",
      "keywords": ["..."]
    }
    
    keywords phải:
    - cụ thể, có ý nghĩa tìm kiếm
    - không quá chung chung (ví dụ: "game", "điện thoại" là sai)
    - nên chứa đầy đủ context (ví dụ: "game zombie hay")
    """

    user_prompt = f"Câu hỏi: {query}"

    client = get_client()

    if client is None:
        print("No API key → fallback")
        # return default_plan(query)
        return smart_fallback(query)

    model = "llama-3.1-8b-instant" if os.getenv("GROQ_BASE_URL") else "gpt-4o-mini"

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.2
        )

        DEBUG = os.getenv("DEBUG") == "true"
        if DEBUG:
            print("MODEL:", model)    

        raw_content = response.choices[0].message.content

        # Parse JSON
        plan = json.loads(raw_content)

        # Gắn query để fallback dùng
        plan["query"] = query

        # Validate
        plan = validate_plan(plan)

        q = query.lower()

        if "so sánh" in q:
            plan["intent"] = "compare"

        elif any(k in q for k in ["nên", "có nên", "nên mua", "nên học", "có đáng"]):
            plan["intent"] = "recommendation"
            plan["needs_search"] = True
            plan["search_depth"] = "medium"

        if plan["intent"] == "recommendation":
            plan["keywords"] = [query]

        elif plan["intent"] == "fact" and len(plan["keywords"]) < 2:
            plan["keywords"] = [query]

        return plan

    except json.JSONDecodeError:
        print("JSON decode error từ LLM")
        return default_plan(query)

    except Exception as e:
        print(f"Lỗi orchestrator: {e}")
        return default_plan(query)