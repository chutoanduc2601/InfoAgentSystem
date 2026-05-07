package org.example.be.entity;

import java.time.Instant;

/**
 * Lưu câu hỏi gốc của người dùng, trạng thái và thời điểm tạo.
 * (Đã chuyển sang dùng DTO cho REST API)
 */
public class QueryRecord {

    private String id;
    private String userId;
    private String queryText;
    private String status = "processing";
    private Instant createdAt = Instant.now();

    // ──────────────────────── Getters / Setters ────────────────────────

    public String getId()                   { return id; }
    public void   setId(String id)          { this.id = id; }

    public String getUserId()               { return userId; }
    public void   setUserId(String userId)  { this.userId = userId; }

    public String getQueryText()                  { return queryText; }
    public void   setQueryText(String queryText)  { this.queryText = queryText; }

    public String getStatus()               { return status; }
    public void   setStatus(String status)  { this.status = status; }

    public Instant getCreatedAt()                   { return createdAt; }
    public void    setCreatedAt(Instant createdAt)  { this.createdAt = createdAt; }
}
