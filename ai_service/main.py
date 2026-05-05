# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import List, Optional
# from openai import OpenAI
# import json
# import os
# from dotenv import load_dotenv
# from agents.search_agent import search_agent
# from agents.process_agent import process_agent
# from agents.orchestrator_agent import orchestrate

# # Load environment variables (API Key)
# load_dotenv()

# app = FastAPI(title="InfoAgent System - AI Service (NGuyễn Thái Bao)")

# # Khởi tạo OpenAI Client.
# #
# # Ví dụ: client = OpenAI(api_key="groq_key", base_url="https://api.groq.com/openai/v1")
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "your-api-key-here"))

# # =====================================================================
# # 1. Định nghĩa chuẩn JSON giao tiếp (API Contract)
# # =====================================================================
# class QueryRequest(BaseModel):
#     query_id: int
#     query: str
#     lang: Optional[str] = "vi"

# class SourceModel(BaseModel):
#     url: str
#     confidence: float

# class ReportResponse(BaseModel):
#     status: str
#     query: str
#     confidence_label: str
#     quick_summary: List[str]
#     detailed_report: str
#     sources: List[SourceModel]
#     recommendations: List[str]

# # =====================================================================
# # (Verification, Summary, Report, Recommendation)
# # =====================================================================
# def process_data_with_llm(user_query: str, raw_data_str: str) -> str:
#     """
#     Hàm này đóng vai trò là "Bộ não" của Người C.
#     Truyền dữ liệu thô (do B tìm được) và câu hỏi của user cho LLM.
#     Ép LLM trả về đúng định dạng JSON.
#     """

#     system_prompt = """
#     Bạn là một AI phân tích thông tin chuyên nghiệp (InfoAgent).
#     Nhiệm vụ của bạn là:
#     1. Đọc dữ liệu thô được cung cấp (từ nhiều nguồn khác nhau).
#     2. Xác thực chéo (Cross-check) xem các nguồn có mâu thuẫn không. Đánh giá độ tin cậy (Confidence).
#     3. Tóm tắt nhanh thành 3-5 ý chính (quick_summary).
#     4. Viết một báo cáo chi tiết bằng Markdown (detailed_report).
#     5. Đưa ra 3 câu hỏi gợi ý liên quan (recommendations).
    
#     BẠN BẮT BUỘC PHẢI TRẢ VỀ CHUẨN JSON VỚI CẤU TRÚC SAU:
#     {
#       "confidence_label": "High Confidence" | "Medium Confidence" | "Conflicting",
#       "quick_summary": ["ý 1", "ý 2"],
#       "detailed_report": "# Báo cáo chi tiết\n...",
#       "sources": [ {"url": "link bài báo", "confidence": 0.9} ],
#       "recommendations": ["câu hỏi 1", "câu hỏi 2"]
#     }
#     Không trả về bất kỳ text nào nằm ngoài JSON.
#     """

#     user_prompt = f"""
#     Câu hỏi của người dùng: "{user_query}"
    
#     Dữ liệu thô thu thập được:
#     {raw_data_str}
#     """

#     try:
#         response = client.chat.completions.create(
#             model="gpt-4o-mini", # Hoặc 'llama3-8b-8192' nếu dùng Groq
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": user_prompt}
#             ],
#             response_format={ "type": "json_object" }, # Ép trả JSON
#             temperature=0.3
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         print(f"Lỗi khi gọi LLM: {e}")
#         # Fallback dữ liệu tĩnh nếu không có API Key hoặc bị lỗi
#         return json.dumps({
#             "confidence_label": "Medium Confidence (Mock)",
#             "quick_summary": ["Đây là dữ liệu test do chưa có API key."],
#             "detailed_report": "Vui lòng cấu hình OPENAI_API_KEY trong file .env",
#             "sources": [],
#             "recommendations": []
#         })

# # =====================================================================
# # 3. API Endpoints
# # =====================================================================
# # @app.post("/ai/generate-report", response_model=ReportResponse)
# # async def generate_report(request: QueryRequest):
# #     print(f"Nhận request từ Spring Boot cho câu hỏi: {request.query}")

# #     # BƯỚC 1: LẤY DỮ LIỆU CỦA NGƯỜI B (Mock Data - Người C không cần đợi B code xong)
# #     try:
# #         # Đường dẫn file json test cùng thư mục
# #         file_path = os.path.join(os.path.dirname(__file__), 'test_data.json')
# #         with open(file_path, 'r', encoding='utf-8') as f:
# #             raw_data = json.load(f)
# #             raw_data_str = json.dumps(raw_data, ensure_ascii=False)
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail="Không tìm thấy file test_data.json của Người B")

# #     # BƯỚC 2: NGƯỜI C XỬ LÝ (Verification, Summary, Report)
# #     print("Đang gửi dữ liệu cho LLM xử lý (Người C đang làm việc)...")
# #     llm_json_result = process_data_with_llm(request.query, raw_data_str)

# #     # BƯỚC 3: PARSE JSON VÀ TRẢ VỀ CHO NGƯỜI A (Spring Boot)
# #     try:
# #         result_dict = json.loads(llm_json_result)

# #         return ReportResponse(
# #             status="success",
# #             query=request.query,
# #             confidence_label=result_dict.get("confidence_label", "Unknown"),
# #             quick_summary=result_dict.get("quick_summary", []),
# #             detailed_report=result_dict.get("detailed_report", ""),
# #             sources=result_dict.get("sources", []),
# #             recommendations=result_dict.get("recommendations", [])
# #         )
# #     except json.JSONDecodeError:
# #         raise HTTPException(status_code=500, detail="LLM trả về kết quả không phải là chuẩn JSON")

# @app.post("/ai/generate-report", response_model=ReportResponse)
# async def generate_report(request: QueryRequest):

#     # STEP 0: ORCHESTRATOR
#     plan = await orchestrate(request.query)

#     # STEP 1: SEARCH (có điều kiện)
#     if plan["needs_search"]:
#         search_results = await search_agent(plan["keywords"], plan["search_depth"])
#     else:
#         search_results = []

#     # STEP 2: PROCESS
#     processed_data = await process_agent(search_results)

#     # STEP 3: LLM
#     raw_data_str = json.dumps(processed_data, ensure_ascii=False)
#     llm_json_result = process_data_with_llm(request.query, raw_data_str)

#     result_dict = json.loads(llm_json_result)

#     return ReportResponse(
#         status="success",
#         query=request.query,
#         confidence_label=result_dict.get("confidence_label", "Unknown"),
#         quick_summary=result_dict.get("quick_summary", []),
#         detailed_report=result_dict.get("detailed_report", ""),
#         sources=result_dict.get("sources", []),
#         recommendations=result_dict.get("recommendations", [])
#     )
    
# # Để chạy Server: Mở terminal chạy lệnh
# # uvicorn main:app --reload --port 8000
import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
load_dotenv()

# Agents
from agents.orchestrator_agent import orchestrate
from agents.search_agent import search_agent
from agents.process_agent import process_agent
from agents.answer_agent import answer_agent

app = FastAPI(title="InfoAgent System - AI Service")

# =========================
# API CONTRACT
# =========================
class QueryRequest(BaseModel):
    query: str
    userId: Optional[str] = None
    meta: Optional[Dict[str, Any]] = {}

    class Config:
        extra = "allow"


class SourceModel(BaseModel):
    url: str
    confidence: float


class ReportResponse(BaseModel):
    status: str
    query: str
    confidence_label: str
    quick_summary: List[str]
    detailed_report: str
    sources: List[SourceModel]
    recommendations: List[str]


# =========================
# MAIN PIPELINE
# =========================
@app.post("/ai/generate-report", response_model=ReportResponse)
async def generate_report(request: QueryRequest):

    try:
        # =====================================================
        # STEP 1: ORCHESTRATOR
        # =====================================================
        plan = await orchestrate(request.query)

        # normalize safety
        keywords = plan.get("keywords", [request.query])
        intent = plan.get("intent", "fact")

        # =====================================================
        # STEP 2: SEARCH AGENT
        # =====================================================
        search_input = {
            "keywords": keywords,
            "intent": intent
        }

        search_results = await search_agent(search_input)

        # =====================================================
        # STEP 3: PROCESS AGENT
        # =====================================================
        processed_data = process_agent(search_results["results"])

        # =====================================================
        # STEP 4: ANSWER AGENT (LLM reasoning layer)
        # =====================================================
        answer_result = await answer_agent(
            query=request.query,
            processed_data=processed_data
        )

        # =====================================================
        # RESPONSE MAPPING
        # =====================================================
        return ReportResponse(
            status="success",
            query=request.query,
            confidence_label=(
                "High Confidence" if answer_result["confidence"] > 0.75
                else "Medium Confidence" if answer_result["confidence"] > 0.4
                else "Low Confidence"
            ),
            quick_summary=[
                answer_result["answer"][:200]
            ],
            detailed_report=answer_result["answer"],
            sources=[
                SourceModel(
                    url=r.get("url", ""),
                    confidence=r.get("score", 0.0)
                )
                for r in processed_data.get("results", [])[:5]
            ],
            recommendations=[]
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Pipeline error: {str(e)}"
        )