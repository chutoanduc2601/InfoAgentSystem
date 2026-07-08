package org.example.be.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.example.be.entity.QueryRecord;
import org.example.be.entity.Report;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.time.Instant;
import java.util.*;

/**
 * Service sử dụng Supabase REST API thay vì JDBC.
 * Không cần mật khẩu database, chỉ cần URL và Anon Key.
 */
@Service
public class HistoryService {

    @Value("${supabase.url}")
    private String supabaseUrl;

    @Value("${supabase.key}")
    private String supabaseKey;

    private final RestTemplate restTemplate;
    private final ObjectMapper objectMapper = new ObjectMapper().findAndRegisterModules();

    public HistoryService() {
        // Cấu hình RestTemplate để hỗ trợ PATCH với timeout dùng HttpClient 5
        org.apache.hc.client5.http.config.RequestConfig requestConfig = org.apache.hc.client5.http.config.RequestConfig.custom()
            .setConnectTimeout(org.apache.hc.core5.util.Timeout.ofMilliseconds(10000))
            .setResponseTimeout(org.apache.hc.core5.util.Timeout.ofMilliseconds(15000))
            .build();
        org.apache.hc.client5.http.impl.classic.CloseableHttpClient httpClient = org.apache.hc.client5.http.impl.classic.HttpClients.custom()
            .setDefaultRequestConfig(requestConfig)
            .build();
        org.springframework.http.client.HttpComponentsClientHttpRequestFactory factory = 
            new org.springframework.http.client.HttpComponentsClientHttpRequestFactory(httpClient);
        this.restTemplate = new RestTemplate(factory);
    }

    private HttpHeaders getHeaders() {
        HttpHeaders headers = new HttpHeaders();
        headers.set("apikey", supabaseKey);
        headers.set("Authorization", "Bearer " + supabaseKey);
        headers.set("Content-Type", "application/json");
        headers.set("Prefer", "return=representation");
        return headers;
    }

    // ─────────────────────────────────────────────────────────────
    // Lưu kết quả (Sử dụng REST POST)
    // ─────────────────────────────────────────────────────────────

    public QueryRecord createQuery(String userId, String queryText) {
        try {
            String url = supabaseUrl + "/rest/v1/queries";
            Map<String, Object> body = new HashMap<>();
            body.put("user_id",    userId != null ? userId : "anonymous");
            body.put("query_text", queryText);
            body.put("status",     "processing");

            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(body, getHeaders());
            ResponseEntity<QueryRecord[]> response = restTemplate.postForEntity(url, entity, QueryRecord[].class);
            
            if (response.getBody() != null && response.getBody().length > 0) {
                return response.getBody()[0];
            }
        } catch (Exception e) {
            System.err.println("!!! Lỗi khi tạo Query: " + e.getMessage());
        }
        
        QueryRecord fallback = new QueryRecord();
        fallback.setId(UUID.randomUUID().toString());
        fallback.setStatus("error");
        return fallback;
    }

    public void saveReport(String queryId, Map<String, Object> aiData) {
        try {
            // 1. Cập nhật status -> done
            String patchUrl = supabaseUrl + "/rest/v1/queries?id=eq." + queryId;
            Map<String, Object> patchBody = Map.of("status", "done");
            HttpEntity<Map<String, Object>> patchEntity = new HttpEntity<>(patchBody, getHeaders());
            restTemplate.exchange(patchUrl, HttpMethod.PATCH, patchEntity, String.class);

            // 2. Tạo report mới
            String reportUrl = supabaseUrl + "/rest/v1/reports";
            Map<String, Object> reportBody = new HashMap<>();
            reportBody.put("query_id",         queryId);
            reportBody.put("confidence_label", getString(aiData, "confidence_label"));
            reportBody.put("detailed_report",  getString(aiData, "detailed_report"));
            reportBody.put("quick_summary",    aiData.get("quick_summary"));
            reportBody.put("sources",          aiData.get("sources"));
            reportBody.put("recommendations",  aiData.get("recommendations"));

            HttpEntity<Map<String, Object>> reportEntity = new HttpEntity<>(reportBody, getHeaders());
            restTemplate.postForEntity(reportUrl, reportEntity, String.class);
        } catch (Exception e) {
            System.err.println("!!! Lỗi khi lưu Report: " + e.getMessage());
        }
    }

    public void markError(String queryId) {
        try {
            String patchUrl = supabaseUrl + "/rest/v1/queries?id=eq." + queryId;
            Map<String, Object> patchBody = Map.of("status", "error");
            HttpEntity<Map<String, Object>> patchEntity = new HttpEntity<>(patchBody, getHeaders());
            restTemplate.exchange(patchUrl, HttpMethod.PATCH, patchEntity, String.class);
        } catch (Exception e) {
            System.err.println("!!! Lỗi khi đánh dấu lỗi Query: " + e.getMessage());
        }
    }

    public List<Map<String, Object>> getHistory(String userId) {
        try {
            // Log để kiểm tra userId đang tìm kiếm
            System.out.println(">>> Đang lấy lịch sử cho user: " + userId);
            
            String url = supabaseUrl + "/rest/v1/queries?select=*,reports(*)&user_id=eq." + userId + "&order=created_at.desc";
            HttpEntity<Void> entity = new HttpEntity<>(getHeaders());
            ResponseEntity<List> response = restTemplate.exchange(url, HttpMethod.GET, entity, List.class);

            List<Map<String, Object>> rawData = response.getBody();
            
            // Log số lượng bản ghi tìm thấy
            System.out.println(">>> Supabase trả về: " + (rawData != null ? rawData.size() : 0) + " bản ghi.");

            List<Map<String, Object>> result = new ArrayList<>();

            if (rawData != null) {
                for (Map<String, Object> q : rawData) {
                    Map<String, Object> item = new LinkedHashMap<>();
                    item.put("queryId",    q.get("id"));
                    item.put("queryText",  q.get("query_text"));
                    item.put("status",     q.get("status"));
                    item.put("createdAt",  q.get("created_at"));

                    Object reportsObj = q.get("reports");
                    if (reportsObj instanceof List) {
                        List<Map<String, Object>> reports = (List<Map<String, Object>>) reportsObj;
                        if (!reports.isEmpty()) {
                            Map<String, Object> r = reports.get(0);
                            Map<String, Object> reportMap = new LinkedHashMap<>();
                            reportMap.put("confidence_label",  r.get("confidence_label"));
                            reportMap.put("quick_summary",     r.get("quick_summary"));
                            reportMap.put("detailed_report",   r.get("detailed_report"));
                            reportMap.put("sources",           r.get("sources"));
                            reportMap.put("recommendations",   r.get("recommendations"));
                            item.put("report", reportMap);
                        }
                    }
                    if (!item.containsKey("report")) {
                        item.put("report", null);
                    }
                    result.add(item);
                }
            }
            return result;
        } catch (Exception e) {
            System.err.println("!!! Lỗi khi lấy lịch sử: " + e.getMessage());
            e.printStackTrace();
            return new ArrayList<>();
        }
    }

    private String getString(Map<String, Object> map, String key) {
        Object v = map.get(key);
        return v != null ? v.toString() : "";
    }

    /**
     * Xóa một đoạn chat (Tự động xóa report nhờ ON DELETE CASCADE).
     */
    public boolean deleteQuery(String queryId) {
        try {
            String url = supabaseUrl + "/rest/v1/queries?id=eq." + queryId;
            HttpEntity<Void> entity = new HttpEntity<>(getHeaders());
            restTemplate.exchange(url, HttpMethod.DELETE, entity, Void.class);
            return true;
        } catch (Exception e) {
            System.err.println("!!! Lỗi khi xóa chat: " + e.getMessage());
            return false;
        }
    }

    /**
     * Đổi tên (nội dung câu hỏi) của đoạn chat.
     */
    public boolean renameQuery(String queryId, String newTitle) {
        try {
            String url = supabaseUrl + "/rest/v1/queries?id=eq." + queryId;
            Map<String, Object> body = Map.of("query_text", newTitle);
            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(body, getHeaders());
            restTemplate.exchange(url, HttpMethod.PATCH, entity, Void.class);
            return true;
        } catch (Exception e) {
            System.err.println("!!! Lỗi khi đổi tên chat: " + e.getMessage());
            return false;
        }
    }
}
