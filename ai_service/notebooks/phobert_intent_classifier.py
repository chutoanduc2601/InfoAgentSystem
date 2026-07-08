# =====================================================================
# KAGGLE NOTEBOOK TEMPLATE: PhoBERT Intent Classifier
# =====================================================================
# Hướng dẫn trên Kaggle:
# 1. Tạo một Notebook mới trên Kaggle, bật GPU T4 x2 hoặc P100 (Settings -> Accelerator).
# 2. Upload file `intent_dataset.csv` lên Kaggle (Add Data -> Upload).
# 3. Copy toàn bộ đoạn code dưới đây vào Notebook và chạy.

import os
import torch
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments

# =====================================================================
# 1. CẤU HÌNH & LOAD DATA
# =====================================================================
# Kaggle input path (thay đổi nếu tên dataset upload của bạn khác)
DATASET_PATH = "/kaggle/input/intent-dataset/intent_dataset.csv"
if not os.path.exists(DATASET_PATH):
    # Fallback nếu bạn upload trực tiếp vào thư mục làm việc
    DATASET_PATH = "intent_dataset.csv"

print(f"Loading dataset from: {DATASET_PATH}")
df = pd.read_csv(DATASET_PATH)

# Đổi tên nhãn thành số
label_map = {"weather": 0, "bitcoin": 1, "news": 2}
df['label'] = df['label'].map(label_map)

# Split Train/Val
train_texts, val_texts, train_labels, val_labels = train_test_split(
    df['text'].tolist(), 
    df['label'].tolist(), 
    test_size=0.2, 
    random_state=42,
    stratify=df['label'].tolist()
)

print(f"Train samples: {len(train_texts)}, Val samples: {len(val_texts)}")

# =====================================================================
# 2. TOKENIZATION
# =====================================================================
# HƯỚNG DẪN KHẮC PHỤC LỖI KẾT NỐI (NAME RESOLUTION ERROR):
# 1. Nếu chạy trên Kaggle: Bạn bắt buộc phải BẬT Internet ở cột cài đặt bên phải:
#    Settings -> Internet -> Gạt nút sang ON (Cần xác thực SĐT để mở khóa tính năng này).
# 2. Nếu chạy Local (ở VN) bị chặn mạng hoặc kết nối chậm: Bỏ comment 2 dòng dưới đây để dùng Mirror Server:
# import os
# os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

MODEL_NAME = "vinai/phobert-base-v2"
print(f"Loading tokenizer: {MODEL_NAME}")
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
except Exception as e:
    print("\n[LỖI] Không thể kết nối tới Hugging Face để tải Tokenizer.")
    print("-> Nếu chạy trên Kaggle: Bật 'Internet' ở panel cài đặt bên phải (Settings -> Internet -> ON).")
    print("-> Nếu chạy Local: Kiểm tra mạng hoặc thử bỏ comment dòng cấu hình 'HF_ENDPOINT' phía trên.\n")
    raise e

train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=64)
val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=64)

class IntentDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = IntentDataset(train_encodings, train_labels)
val_dataset = IntentDataset(val_encodings, val_labels)

# =====================================================================
# 3. KHỞI TẠO MODEL & TRAINING ARGUMENTS
# =====================================================================
print("Loading model...")
try:
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=3)
except Exception as e:
    print("\n[LỖI] Không thể kết nối tới Hugging Face để tải Model.")
    print("-> Nếu chạy trên Kaggle: Bật 'Internet' ở panel cài đặt bên phải (Settings -> Internet -> ON).")
    print("-> Nếu chạy Local: Kiểm tra mạng hoặc thử bỏ comment dòng cấu hình 'HF_ENDPOINT' phía trên.\n")
    raise e

# Đảm bảo sử dụng GPU nếu có
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
print(f"Using device: {device}")

def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='weighted')
    acc = accuracy_score(labels, preds)
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }

training_args = TrainingArguments(
    output_dir='./results',          # Output directory
    num_train_epochs=3,              # Tổng số epoch huấn luyện
    per_device_train_batch_size=16,  # Batch size cho training
    per_device_eval_batch_size=16,   # Batch size cho evaluation
    warmup_steps=100,                # Số bước khởi động learning rate
    weight_decay=0.01,               # Tránh overfitting
    logging_dir='./logs',            # Thư mục chứa log
    logging_steps=10,
    eval_strategy="epoch",     # Đánh giá sau mỗi epoch
    save_strategy="epoch",
    load_best_model_at_end=True,     # Tải model tốt nhất ở cuối
    metric_for_best_model="f1",
    report_to="none"                 # Tắt tích hợp wandb/tensorboard ngoài
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=compute_metrics,
)

# =====================================================================
# 4. TRAINING & EVALUATION
# =====================================================================
print("Starting training...")
trainer.train()

print("Evaluating...")
eval_results = trainer.evaluate()
print("Evaluation results:", eval_results)

# =====================================================================
# 5. LƯU MODEL CHÍNH THỨC
# =====================================================================
SAVE_DIR = "intent-phobert-model"
print(f"Saving final model to {SAVE_DIR}...")
model.save_pretrained(SAVE_DIR)
tokenizer.save_pretrained(SAVE_DIR)

# Nén model lại thành zip để download về máy local dễ dàng
import shutil
shutil.make_archive(SAVE_DIR, 'zip', SAVE_DIR)
print(f"Successfully zipped model to: {SAVE_DIR}.zip")

# =====================================================================
# 6. INFERENCE TEST (TEST THỬ VỚI CÂU HỎI MỚI)
# =====================================================================
def predict_intent(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=64).to(device)
    model.eval()
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.nn.functional.softmax(logits, dim=-1)
        pred_idx = torch.argmax(probs, dim=-1).item()
        
    inv_label_map = {v: k for k, v in label_map.items()}
    return inv_label_map[pred_idx], probs[0][pred_idx].item()

# Test thử vài câu
test_queries = [
    "Thời tiết Sài Gòn chiều nay thế nào?",
    "Giá BTC có biến động gì hôm nay không?",
    "Tin tức mới nhất về cuộc họp hôm nay",
    "Ngày mai có mưa to ở Hà Nội không?"
]

print("\n--- Test thử dự đoán của Model ---")
for query in test_queries:
    label, confidence = predict_intent(query)
    print(f"Query: '{query}' -> Predict: {label} (confidence: {confidence:.2%})")
