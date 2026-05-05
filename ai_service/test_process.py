import asyncio
from colorama import Fore, Style, init

# Khởi tạo màu sắc cho terminal
init(autoreset=True)

# Import hàm process từ file agent của bạn (đảm bảo bạn đã cập nhật bản refactor)
from agents.process_agent import process

# ==========================================
# 1. MOCK DATA (Trích xuất từ Terminal của bạn)
# ==========================================
RAW_SEARCH_RESULTS = [
    # --- CASE 1: Chứa Link Youtube ---
    {
        "title": "TOP 15 NEW Zombie Games coming in 2025 and 2026",
        "snippet": "Take a look at over 15 new anticipated brutal ZOMBIE games releasing in 2025, 2026 and beyond with survival horror...",
        "url": "https://www.youtube.com/watch?v=9E58Aop59Ao",
        "source": "tavily",
        "score": 0.67
    },
    # --- CASE 2: Đoạn văn chuẩn, cần giữ nguyên (có thể truncate nếu quá dài) ---
    {
        "title": "The 15 best zombie games to play in 2025 | TechRadar",
        "snippet": "Here's our picks for the best zombie games to play in 2025. ## Best zombie games 2025. ***Telltale's The Walking Dead*** might be showing its age somewhat, but it's still one of the best zombie games around. No best zombies games list would be complete without Left 4 Dead 2.",
        "url": "https://www.techradar.com/best/best-zombie-games",
        "source": "tavily",
        "score": 0.83
    },
    # --- CASE 3: Rác Markdown & Bảng biểu lộn xộn ---
    {
        "title": "Apple iPhone 15 vs Samsung Galaxy S24 5G : Specs",
        "snippet": "### Release Date\n\n|  |  |\n --- |\n| 13 Sep, 2023 | 18 Jan, 2024 |\n\n### Performance\n\n|  |  |\n --- |\n|  |  |\n| Apple A16 Bionic | Samsung Exynos 2400 |",
        "url": "https://www.91mobiles.com/compare/Apple/...",
        "source": "tavily",
        "score": 1.0
    },
    # --- CASE 4: Ký tự đặc biệt cần giữ lại ($, %, nits) ---
    {
        "title": "Samsung Galaxy S24 vs iPhone 15: Which phone should you buy?",
        "snippet": "Starting price | $799 | $799 | Display | 6.2\" Dynamic LTPO AMOLED 2X, 2600 nits peak | 6.1'' Super Retina XDR OLED, 1000 nits peak. Battery charging to 50% in 30 mins.",
        "url": "https://www.zdnet.com/article/samsung-galaxy-s24-vs-iphone-15/",
        "source": "tavily",
        "score": 0.88
    },
    # --- CASE 5: Nội dung quá ngắn (Noise) ---
    {
        "title": "Short Tech News",
        "snippet": "iPhone 15 is good.",
        "url": "https://example.com/short",
        "source": "tavily",
        "score": 0.5
    }
]

# ==========================================
# 2. HÀM KIỂM TRA (VALIDATOR)
# ==========================================
async def run_process_test():
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== KIỂM TRA PROCESS AGENT (DATA CLEANING) ===\n")
    print(f"Tổng số kết quả đầu vào: {len(RAW_SEARCH_RESULTS)} items\n")

    # Gọi Process Agent
    processed_results = await process(RAW_SEARCH_RESULTS)

    print(f"{Fore.GREEN}{Style.BRIGHT}Số lượng sau khi xử lý: {len(processed_results)} items")
    print(f"{Fore.RED}Số lượng bị loại bỏ: {len(RAW_SEARCH_RESULTS) - len(processed_results)} items\n")
    print("-" * 60)

    # In kết quả đã xử lý để xem "lòng mề"
    for i, item in enumerate(processed_results, 1):
        print(f"{Fore.YELLOW}{Style.BRIGHT}Kết quả #{i}:")
        print(f"  {Fore.BLUE}Title:   {Style.NORMAL}{item['title']}")
        print(f"  {Fore.BLUE}URL:     {Style.NORMAL}{item['url']}")
        
        snippet = item['snippet']
        snippet_len = len(snippet)
        
        # Highlight màu đỏ nếu snippet dài chạm ngưỡng MAX_SNIPPET_LENGTH (chứng tỏ hàm truncate hoạt động)
        len_color = Fore.RED if snippet_len > 290 else Fore.GREEN
        
        print(f"  {Fore.BLUE}Snippet ({len_color}{snippet_len} chars{Fore.BLUE}):")
        print(f"  {Fore.WHITE}{snippet}")
        print("-" * 60)

    # ==========================================
    # 3. TỰ ĐỘNG ASSERT (Tự động bắt lỗi logic)
    # ==========================================
    print(f"\n{Fore.CYAN}=== KIỂM TRA CÁC ĐIỀU KIỆN (ASSERTIONS) ===")
    try:
        urls = [item['url'] for item in processed_results]
        
        # 1. Kiểm tra Video filter
        assert not any("youtube.com" in url for url in urls), "❌ Lỗi: Link YouTube chưa bị loại bỏ!"
        print("✅ Đã loại bỏ thành công các link YouTube (Video).")

        # 2. Kiểm tra Noise filter (Độ dài tối thiểu)
        snippets = [item['snippet'] for item in processed_results]
        assert not any(len(s) < 30 for s in snippets), "❌ Lỗi: Vẫn còn Snippet quá ngắn (<30 chars)!"
        print("✅ Đã loại bỏ thành công các snippet quá ngắn.")

        # 3. Kiểm tra Truncate (Độ dài tối đa)
        assert all(len(s) <= 303 for s in snippets), "❌ Lỗi: Hàm Truncate không hoạt động, có snippet > 300 ký tự!"
        print("✅ Hàm cắt ngắn (Truncate) hoạt động tốt.")

        # 4. Kiểm tra Regex Cleaning (Loại bỏ Markdown table chars như '|')
        # Lưu ý: Nếu trong hàm clean_text của bạn KHÔNG cho phép ký tự '|', nó phải biến mất.
        assert not any("|" in s for s in snippets), "❌ Lỗi: Các ký tự rác (như '|') chưa được dọn sạch!"
        print("✅ Dọn dẹp ký tự rác, markdown thành công.")

        # 5. Giữ lại ký hiệu quan trọng
        zdnet_snippet = next((s for s in snippets if "799" in s), "")
        assert "$" in zdnet_snippet and "%" in zdnet_snippet, "❌ Lỗi: Regex đã xóa mất các ký hiệu quan trọng như $ và %!"
        print("✅ Các ký tự tiền tệ, phần trăm ($, %) được bảo toàn.")

    except AssertionError as e:
        print(f"\n{Fore.RED}{Style.BRIGHT}{e}")

if __name__ == "__main__":
    asyncio.run(run_process_test())