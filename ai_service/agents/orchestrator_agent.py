# import os
# import json
# import asyncio
# from typing import Dict, Any
# from openai import AsyncOpenAI  # Sử dụng bản Async
# import logging

# logger = logging.getLogger("orchestrator")

# # Khởi tạo client dùng chung để tối ưu hiệu suất
# def get_client():
#     api_key = os.getenv("OPENAI_API_KEY")
#     base_url = os.getenv("GROQ_BASE_URL")

#     if not api_key: 
#         return None

#     return AsyncOpenAI(api_key=api_key, base_url=base_url) if base_url else AsyncOpenAI(api_key=api_key)

# class Orchestrator:
#     VALID_INTENTS = ["fact", "compare", "recommendation"]

#     @staticmethod
#     def smart_fallback(query: str) -> Dict[str, Any]:
#         q = query.lower()
#         intent = "fact"
#         if "so sánh" in q: intent = "compare"
#         elif any(k in q for k in ["nên", "có nên", "tư vấn"]): intent = "recommendation"

#         return {
#             "intent": intent,
#             "keywords": [query]
#         }

#     @classmethod
#     def validate_plan(cls, plan: Dict[str, Any], original_query: str) -> Dict[str, Any]:
#         if not isinstance(plan, dict):
#             return Orchestrator.smart_fallback(original_query)
        
#         # Chuẩn hóa Intent
#         if plan.get("intent") not in cls.VALID_INTENTS:
#             plan["intent"] = "fact"

#         # Đảm bảo có keywords
#         if not isinstance(plan.get("keywords"), list) or not all(isinstance(k, str) and k.strip() for k in plan["keywords"]):
#             plan["keywords"] = [original_query]
            
#         return plan

# async def call_llm(client, payload, retries=2):
#     for _ in range(retries):
#         try:
#             return await asyncio.wait_for(
#                 client.chat.completions.create(**payload),
#                 timeout=5
#             )
#         except (asyncio.TimeoutError, Exception):
#             continue
#     raise Exception("LLM timeout")

# def safe_json_load(content: str):
#     try:
#         return json.loads(content)
#     except:
#         content = content.replace("```json", "").replace("```", "").strip()
#         return json.loads(content)

# async def orchestrate(query: str) -> Dict[str, Any]:
#     client = get_client()
    
#     if not client:
#         return Orchestrator.smart_fallback(query)

#     system_prompt = """
#     Bạn là Orchestrator Agent.

#     NHIỆM VỤ:
#     - Phân tích câu hỏi
#     - Trả về kế hoạch JSON

#     QUY TẮC BẮT BUỘC:
#     - CHỈ trả JSON hợp lệ
#     - KHÔNG markdown
#     - KHÔNG giải thích
#     - KHÔNG text ngoài JSON

#     FORMAT:
#     {
#     "intent": "fact" | "compare" | "recommendation",
#     "keywords": ["..."]
#     }
#     """

#     model = "llama-3.1-8b-instant" if os.getenv("GROQ_BASE_URL") else "gpt-4o-mini"

#     try:
#         response = await call_llm(client, {
#             "model": model,
#             "messages": [
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": f"Câu hỏi: {query}"}
#             ],
#             "response_format": {"type": "json_object"},
#             "temperature": 0.1
#         })

#         raw_content = response.choices[0].message.content
#         plan = safe_json_load(raw_content)
        
#         # Validate và làm sạch dữ liệu
#         plan = Orchestrator.validate_plan(plan, query)
        
#         # Chỉ ghi đè logic nếu LLM nhận diện sai hoàn toàn các từ khóa nhạy cảm
#         q = query.lower()

#         if any(k in q for k in [
#             "so sánh", "compare", "vs", "khác nhau", "khác gì", "tốt hơn"
#         ]):
#             plan["intent"] = "compare"

#         elif any(k in q for k in [
#             "nên", "có nên", "tư vấn", "chọn", "review", "đáng mua"
#         ]):
#             plan["intent"] = "recommendation"

#         if not plan["keywords"]:
#             plan["keywords"] = [query]

#         cleaned = [
#             k.strip() for k in plan["keywords"]
#             if isinstance(k, str) and k.strip()
#         ]

#         plan["keywords"] = cleaned if cleaned else [query]

#         return plan

#     except Exception as e:
#         logger.error(f"Error: {e}", exc_info=True)
#         return Orchestrator.smart_fallback(query)

import os
import json
import asyncio
import logging
from typing import Dict, Any, Optional
from openai import AsyncOpenAI

logger = logging.getLogger("orchestrator")

# 1. Khởi tạo client Singleton
_client: Optional[AsyncOpenAI] = None

def get_client() -> Optional[AsyncOpenAI]:
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("GROQ_BASE_URL")
        if not api_key:
            return None
        _client = AsyncOpenAI(api_key=api_key, base_url=base_url) if base_url else AsyncOpenAI(api_key=api_key)
    return _client

class Orchestrator:
    VALID_INTENTS = ["fact", "compare", "recommendation"]

    @staticmethod
    def smart_fallback(query: str) -> Dict[str, Any]:
        q = query.lower()
        intent = "fact"
        if any(k in q for k in ["so sánh", "compare", "vs", "khác nhau"]): 
            intent = "compare"
        elif any(k in q for k in ["nên", "có nên", "tư vấn", "chọn"]): 
            intent = "recommendation"

        return {
            "intent": intent,
            "keywords": [query]
        }

    @classmethod
    def validate_and_clean(cls, plan: Any, original_query: str) -> Dict[str, Any]:
        # Kiểm tra cấu trúc cơ bản
        if not isinstance(plan, dict):
            return cls.smart_fallback(original_query)
        
        # Chuẩn hóa Intent
        if plan.get("intent") not in cls.VALID_INTENTS:
            # Thay vì gán cứng 'fact', hãy thử dùng fallback logic
            fallback = cls.smart_fallback(original_query)
            plan["intent"] = fallback["intent"]

        # Làm sạch keywords
        keywords = plan.get("keywords")
        if isinstance(keywords, list):
            cleaned = [str(k).strip() for k in keywords if str(k).strip()]
            plan["keywords"] = cleaned if cleaned else [original_query]
        else:
            plan["keywords"] = [original_query]
            
        return plan

async def call_llm(client: AsyncOpenAI, payload: dict, retries=2):
    for i in range(retries):
        try:
            return await asyncio.wait_for(
                client.chat.completions.create(**payload),
                timeout=7  # Tăng lên một chút vì 5s hơi hẹp cho LLM
            )
        except (asyncio.TimeoutError, Exception) as e:
            if i == retries - 1:
                logger.error(f"LLM final failure: {e}")
                raise
            await asyncio.sleep(1) # Nghỉ một chút trước khi retry

def safe_json_load(content: str) -> Optional[Dict[str, Any]]:
    try:
        # Xử lý trường hợp LLM trả về markdown code block
        if "```" in content:
            content = content.split("```json")[-1].split("```")[0].strip()
        return json.loads(content)
    except Exception as e:
        logger.warning(f"JSON parse error: {e}")
        return None

async def orchestrate(query: str) -> Dict[str, Any]:
    client = get_client()
    if not client:
        return Orchestrator.smart_fallback(query)

    system_prompt = """Bạn là Orchestrator Agent. Phân tích câu hỏi và trả về JSON.
QUY TẮC: CHỈ trả JSON, không giải thích.
FORMAT: {"intent": "fact" | "compare" | "recommendation", "keywords": ["keyword1", "keyword2"]}"""

    model = "llama-3.1-8b-instant" if os.getenv("GROQ_BASE_URL") else "gpt-4o-mini"

    try:
        response = await call_llm(client, {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.1
        })

        raw_content = response.choices[0].message.content
        plan = safe_json_load(raw_content)
        
        # Validate kết quả từ LLM
        return Orchestrator.validate_and_clean(plan, query)

    except Exception:
        return Orchestrator.smart_fallback(query)