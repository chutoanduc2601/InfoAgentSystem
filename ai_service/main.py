import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
import os

# Ép nạp file .env từ thư mục hiện tại của file main.py
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

# Agents
from agents.orchestrator_agent import orchestrate
from agents.search_agent import search_agent
from agents.process_agent import process_agent
from agents.answer_agent import answer_agent
import time

app = FastAPI(title="InfoAgent System - AI Service")

# =========================
# CACHING LAYER
# =========================
CACHE = {}
CACHE_TTL = 3600  # 1 hour

def get_from_cache(query: str) -> Optional[Dict]:
    if query in CACHE:
        item = CACHE[query]
        if time.time() - item['time'] < CACHE_TTL:
            return item['data']
    return None

def set_cache(query: str, data: Dict):
    CACHE[query] = {
        'time': time.time(),
        'data': data
    }

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
        # CACHE CHECK
        # =====================================================
        cached_result = get_from_cache(request.query)
        if cached_result:
            return ReportResponse(**cached_result)

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
        response_dict = {
            "status": "success",
            "query": request.query,
            "confidence_label": (
                "High Confidence" if answer_result["confidence"] > 0.75
                else "Medium Confidence" if answer_result["confidence"] > 0.4
                else "Low Confidence"
            ),
            "quick_summary": answer_result.get("summary", []),
            "detailed_report": answer_result["answer"],
            "sources": [
                {
                    "url": r.get("url", ""),
                    "confidence": r.get("score", 0.0)
                }
                for r in processed_data.get("results", [])[:5]
            ],
            "recommendations": answer_result.get("recommendations", [])
        }
        
        # Save to cache
        set_cache(request.query, response_dict)
        
        return ReportResponse(**response_dict)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Pipeline error: {str(e)}"
        )