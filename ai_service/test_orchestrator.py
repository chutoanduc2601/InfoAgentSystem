# test_orchestrator.py

import asyncio

from dotenv import load_dotenv
load_dotenv()

from agents.orchestrator_agent import orchestrate

async def main():
    queries = [
        "Game zombie nào hay?",
        "So sánh iPhone 15 và Samsung S24",
        "Thủ đô của Pháp là gì?",
        "Có nên học AI năm 2026 không?"
    ]

    for q in queries:
        result = await orchestrate(q)
        print("\n======================")
        print("Query:", q)
        print("Plan:", result)

if __name__ == "__main__":
    asyncio.run(main())