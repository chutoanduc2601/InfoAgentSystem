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
            # quick_summary=[
            #     answer_result["answer"][:200]
            # ],
            # quick_summary = answer_result["answer"].split("\n")[:3],
            quick_summary=answer_result.get("summary", []),
            detailed_report=answer_result["answer"],
            sources=[
                SourceModel(
                    url=r.get("url", ""),
                    confidence=r.get("score", 0.0)
                )
                for r in processed_data.get("results", [])[:5]
            ],
            recommendations=answer_result.get("recommendations", [])
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Pipeline error: {str(e)}"
        )