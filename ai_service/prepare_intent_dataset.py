import os
import pandas as pd
import random

# Output paths
OUTPUT_PATH = "intent_dataset.csv"

# =====================================================================
# DATA GENERATION TEMPLATES
# =====================================================================
WEATHER_TEMPLATES = [
    "thời tiết {location} {time} thế nào",
    "dự báo thời tiết tại {location} {time}",
    "nhiệt độ ở {location} hôm nay là bao nhiêu",
    "{location} {time} có mưa không",
    "thời tiết {location} {time} ra sao",
    "ngày mai {location} có nắng không",
    "dự báo thời tiết {time} của {location}",
    "nhiệt độ {location} lúc này",
    "tình hình thời tiết ở {location} {time}",
    "hôm nay {location} có lạnh không",
    "sài gòn có mưa to không",
    "thời tiết thành phố hồ chí minh ngày mai",
    "dự báo nhiệt độ hcm tuần này"
]

LOCATIONS = ["tp hcm", "sài gòn", "hà nội", "đà nẵng", "nha trang", "đà lạt", "hải phòng", "cần thơ", "quảng ninh"]
TIMES = ["hôm nay", "ngày mai", "tối nay", "tuần này", "cuối tuần", "ngày kia", "ngày mốt", "sáng mai"]

BITCOIN_TEMPLATES = [
    "giá {coin} hôm nay bao nhiêu",
    "tỷ giá {coin} hiện tại",
    "biểu đồ giá {coin} mới nhất",
    "có nên đầu tư vào {coin} không",
    "xu hướng của {coin} sắp tới thế nào",
    "{coin} có tăng giá không",
    "mua {coin} ở đâu uy tín",
    "phân tích kỹ thuật {coin} {time}",
    "{coin} giảm sâu quá",
    "{coin} đạt đỉnh mới",
    "tin tức mới nhất về {coin}",
    "sàn giao dịch {coin} an toàn",
    "halving {coin} là gì",
    "ví lưu trữ {coin} tốt nhất"
]

COINS = ["bitcoin", "btc", "ethereum", "eth", "solana", "sol", "binance coin", "bnb", "crypto", "tiền điện tử"]

# =====================================================================
# 1. GENERATE INTENT DATA
# =====================================================================
def generate_weather_queries(num_samples=1000):
    queries = []
    for _ in range(num_samples):
        tpl = random.choice(WEATHER_TEMPLATES)
        loc = random.choice(LOCATIONS)
        t = random.choice(TIMES)
        
        # Format query
        query = tpl.format(location=loc, time=t)
        # Randomly clean or keep diacritics / lowercase
        if random.random() > 0.8:
            query = query.replace("thời tiết", "thoi tiet").replace("thế nào", "the nao").replace("ngày mai", "ngay mai")
        queries.append((query.strip(), "weather"))
    return queries

def generate_bitcoin_queries(num_samples=1000):
    queries = []
    for _ in range(num_samples):
        tpl = random.choice(BITCOIN_TEMPLATES)
        coin = random.choice(COINS)
        t = random.choice(TIMES)
        
        # Format query
        query = tpl.format(coin=coin, time=t)
        queries.append((query.strip(), "bitcoin"))
    return queries

# =====================================================================
# 2. EXTRACT NEWS DATA (VNTC or generated)
# =====================================================================
def get_news_queries(num_samples=1000):
    """
    Simulates or reads news headlines. Since VNTC needs to be cloned from github,
    this script provides template-based headlines typical of VNTC categories
    (Chính trị, Xã hội, Thể thao, Thế giới, Pháp luật) to bootstrap the dataset.
    """
    news_headlines = [
        "công bố quyết định bổ nhiệm nhân sự mới",
        "tình hình kinh tế xã hội quý 1 năm 2026",
        "hội nghị quốc tế bàn về biến đổi khí hậu toàn cầu",
        "đội tuyển bóng đá nam việt nam giành chiến thắng",
        "kết quả trận chung kết uefa champions league",
        "vụ án lừa đảo chiếm đoạt tài sản bị khởi tố",
        "chính sách thuế mới có hiệu lực từ đầu tháng sau",
        "giá vàng trong nước hôm nay tiếp tục biến động mạnh",
        "phát hiện khảo cổ mới tại hoàng thành thăng long",
        "khánh thành đường cao tốc bắc nam đoạn mới",
        "quan hệ ngoại giao việt nam và các nước đối tác",
        "tổng thống mỹ công bố chiến lược kinh tế mới",
        "tai nạn giao thông nghiêm trọng trên quốc lộ 1a",
        "giải thưởng khoa học công nghệ vinh danh nhà sáng chế",
        "triển lãm nghệ thuật đương đại khai mạc tại hà nội"
    ]
    
    queries = []
    # If a local VNTC dataset exists, you can parse it here
    vntc_path = "VNTC/Data" # Adjust to VNTC local path if cloned
    if os.path.exists(vntc_path):
        print(f"Loading news from local VNTC path: {vntc_path}")
        # Custom logic to parse VNTC text files
        # ...
    else:
        print("VNTC path not found locally. Generating placeholder news queries from template...")
        for _ in range(num_samples):
            headline = random.choice(news_headlines)
            # Add some variations
            prefix = random.choice(["tin tức: ", "thời sự: ", "cập nhật: ", "", ""])
            query = prefix + headline
            queries.append((query.strip(), "news"))
            
    return queries

# =====================================================================
# MAIN RUNNER
# =====================================================================
if __name__ == "__main__":
    print("=== InfoAgent System - Intent Dataset Preparer ===")
    
    weather_data = generate_weather_queries(800)
    bitcoin_data = generate_bitcoin_queries(800)
    news_data = get_news_queries(800)
    
    all_data = weather_data + bitcoin_data + news_data
    random.shuffle(all_data)
    
    df = pd.DataFrame(all_data, columns=["text", "label"])
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")
    
    print(f"Successfully generated {len(df)} samples and saved to '{OUTPUT_PATH}'")
    print("\nDataset label distribution:")
    print(df["label"].value_counts())
    
    print("\nSample records:")
    print(df.head(10))
