-- ============================================================
-- Phase 3: Persistent Memory - Database Schema
-- Chạy script này trong Supabase SQL Editor
-- ============================================================

-- Bảng 1: Lưu câu hỏi gốc
CREATE TABLE IF NOT EXISTS queries (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL,                      -- Supabase Auth user id
    query_text  TEXT NOT NULL,
    status      VARCHAR(20) NOT NULL DEFAULT 'processing', -- processing | done | error
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index để truy vấn nhanh theo user
CREATE INDEX IF NOT EXISTS idx_queries_user_id ON queries(user_id);
CREATE INDEX IF NOT EXISTS idx_queries_created_at ON queries(created_at DESC);

-- Bảng 2: Lưu nội dung báo cáo (liên kết 1-1 với queries)
CREATE TABLE IF NOT EXISTS reports (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    query_id          UUID NOT NULL REFERENCES queries(id) ON DELETE CASCADE,
    confidence_label  VARCHAR(50),
    quick_summary     JSONB DEFAULT '[]',            -- Mảng string tóm tắt
    detailed_report   TEXT,                          -- Nội dung Markdown đầy đủ
    sources           JSONB DEFAULT '[]',            -- Mảng {url, confidence}
    recommendations   JSONB DEFAULT '[]',            -- Mảng string gợi ý
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_reports_query_id ON reports(query_id);

-- ============================================================
-- Row Level Security (RLS) - Bảo mật theo từng user
-- ============================================================

ALTER TABLE queries ENABLE ROW LEVEL SECURITY;
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;

-- User chỉ đọc được bản ghi của chính mình
CREATE POLICY "Users can view own queries"
    ON queries FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can view own reports"
    ON reports FOR SELECT
    USING (
        query_id IN (
            SELECT id FROM queries WHERE user_id = auth.uid()
        )
    );

-- Backend (service_role) có thể ghi
-- Lưu ý: Spring Boot kết nối bằng postgres user (service_role level),
-- nên không bị giới hạn bởi RLS ở trên.

-- ============================================================
-- (Tuỳ chọn) Seed data để test
-- ============================================================
-- INSERT INTO queries (user_id, query_text, status) VALUES
--     ('<your-user-id>', 'AI năm 2025 có gì mới?', 'done');
