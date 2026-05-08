package org.example.be.entity;

import java.time.Instant;

/**
 * Lưu nội dung báo cáo trả về từ AI.
 * (Đã chuyển sang dùng DTO cho REST API)
 */
public class Report {

    private String id;
    private String queryId;
    private String confidenceLabel;
    private String quickSummary;
    private String detailedReport;
    private String sources;
    private String recommendations;
    private Instant createdAt = Instant.now();

    // ──────────────────────── Getters / Setters ────────────────────────

    public String getId()                         { return id; }
    public void   setId(String id)                { this.id = id; }

    public String getQueryId()                    { return queryId; }
    public void   setQueryId(String queryId)      { this.queryId = queryId; }

    public String getConfidenceLabel()                        { return confidenceLabel; }
    public void   setConfidenceLabel(String confidenceLabel)  { this.confidenceLabel = confidenceLabel; }

    public String getQuickSummary()                     { return quickSummary; }
    public void   setQuickSummary(String quickSummary)  { this.quickSummary = quickSummary; }

    public String getDetailedReport()                       { return detailedReport; }
    public void   setDetailedReport(String detailedReport)  { this.detailedReport = detailedReport; }

    public String getSources()                  { return sources; }
    public void   setSources(String sources)    { this.sources = sources; }

    public String getRecommendations()                        { return recommendations; }
    public void   setRecommendations(String recommendations)  { this.recommendations = recommendations; }

    public Instant getCreatedAt()                   { return createdAt; }
    public void    setCreatedAt(Instant createdAt)  { this.createdAt = createdAt; }
}
