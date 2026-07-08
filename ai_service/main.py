import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
import time
import logging

# Ép nạp file .env từ thư mục hiện tại của file main.py
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

# Agents
from agents.orchestrator_agent import orchestrate
from agents.search_agent import search_agent
from agents.process_agent import process_agent
from agents.answer_agent import answer_agent

# Trained Models
from agents.intent_classifier import classify_intent, load_model as load_intent_model
from agents.lstm_weather_agent import forecast_temperature, load_model as load_weather_model
from agents.lstm_bitcoin_agent import forecast_bitcoin, load_model as load_bitcoin_model

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

app = FastAPI(title="InfoAgent System - AI Service")

# =========================
# LOAD MODELS AT STARTUP
# =========================
@app.on_event("startup")
async def startup_event():
    logger.info("Loading trained models...")
    load_intent_model()
    load_weather_model()
    load_bitcoin_model()
    logger.info("All models loaded.")

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


class ForecastData(BaseModel):
    actual_values: List[float] = []
    actual_labels: List[str] = []
    forecast_values: List[float] = []
    forecast_labels: List[str] = []
    unit: str = ""
    title: str = ""


class ReportResponse(BaseModel):
    status: str
    query: str
    intent: str = "news"
    intent_confidence: float = 0.0
    confidence_label: str
    quick_summary: List[str]
    detailed_report: str
    sources: List[SourceModel]
    recommendations: List[str]
    forecast: Optional[ForecastData] = None


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
        # STEP 1: INTENT CLASSIFICATION (PhoBERT)
        # =====================================================
        intent_result = classify_intent(request.query)
        intent = intent_result["intent"]
        intent_confidence = intent_result["confidence"]

        logger.info(f"Intent: {intent} ({intent_confidence:.2%})")

        # =====================================================
        # STEP 2: DOMAIN-SPECIFIC FORECAST (LSTM)
        # =====================================================
        forecast = None

        if intent == "weather":
            weather_result = await forecast_temperature(steps=24)
            if "error" not in weather_result:
                forecast = ForecastData(
                    actual_values=weather_result.get("actual_temperatures", []),
                    actual_labels=weather_result.get("actual_times", []),
                    forecast_values=weather_result.get("forecast_temperatures", []),
                    forecast_labels=[f"+{i+1}h" for i in range(len(weather_result.get("forecast_temperatures", [])))],
                    unit="°C",
                    title=f"Dự báo nhiệt độ {weather_result.get('location', 'TP.HCM')} (24h tới)"
                )

        elif intent == "bitcoin":
            btc_result = await forecast_bitcoin(steps=24)
            if "error" not in btc_result:
                forecast = ForecastData(
                    actual_values=btc_result.get("actual_prices", []),
                    actual_labels=[str(t) for t in btc_result.get("actual_timestamps", [])],
                    forecast_values=btc_result.get("forecast_prices", []),
                    forecast_labels=[f"+{i+1}h" for i in range(len(btc_result.get("forecast_prices", [])))],
                    unit="USD",
                    title="Dự báo giá Bitcoin BTC/USD (24h tới)"
                )

        # =====================================================
        # STEP 3: ORCHESTRATOR (LLM-based keyword extraction)
        # =====================================================
        plan = await orchestrate(request.query)
        keywords = plan.get("keywords", [request.query])

        # =====================================================
        # STEP 4: SEARCH AGENT
        # =====================================================
        search_input = {
            "keywords": keywords,
            "intent": intent
        }
        search_results = await search_agent(search_input)

        # =====================================================
        # STEP 5: PROCESS AGENT
        # =====================================================
        processed_data = process_agent(search_results["results"])

        # =====================================================
        # STEP 6: ANSWER AGENT (LLM reasoning layer)
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
            "intent": intent,
            "intent_confidence": round(intent_confidence, 4),
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
            "recommendations": answer_result.get("recommendations", []),
            "forecast": forecast.model_dump() if forecast else None
        }
        
        # Save to cache
        set_cache(request.query, response_dict)
        
        return ReportResponse(**response_dict)

    except Exception as e:
        logger.error(f"Pipeline error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Pipeline error: {str(e)}"
        )