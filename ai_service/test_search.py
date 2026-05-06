import asyncio
from pprint import pprint

from dotenv import load_dotenv
load_dotenv()

# import từ project của bạn
from agents.orchestrator_agent import orchestrate
from agents.search_agent import search_agent


TEST_QUERIES = [
    "iPhone 15 vs Samsung S24",
    "nên mua laptop nào cho lập trình",
    "ChatGPT là gì",
    "so sánh react và vue",
    "có nên học python 2026"
]


async def run_test():
    for query in TEST_QUERIES:
        print("\n" + "="*60)
        print(f"QUERY: {query}")

        # 1. Orchestrator
        plan = await orchestrate(query)
        print("\n[Orchestrator Plan]")
        pprint(plan)

        # 2. Search
        result = await search_agent(plan)

        print("\n[Search Results]")
        print(f"Total: {len(result['results'])}")

        for i, r in enumerate(result["results"], 1):
            print(f"\n--- Result {i} ---")
            print(f"Title  : {r['title']}")
            print(f"Score  : {r['score']}")
            print(f"URL    : {r['url']}")
            print(f"Snippet: {r['snippet'][:120]}...")

        print("="*60)


if __name__ == "__main__":
    asyncio.run(run_test())