# import httpx
# import os

# TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# async def search(keywords: list, depth: str):
#     async with httpx.AsyncClient() as client:
#         res = await client.post(
#             "https://api.tavily.com/search",
#             json={
#                 "api_key": TAVILY_API_KEY,
#                 "query": query,
#                 "max_results": 5
#             }
#         )
#         data = res.json()

#     return data.get("results", [])