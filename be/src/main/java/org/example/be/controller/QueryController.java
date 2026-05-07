package org.example.be.controller;

import org.example.be.DTO.QueryRequest;
import org.example.be.entity.QueryRecord;
import org.example.be.service.HistoryService;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class QueryController {

    @Value("${ai-service.url:http://localhost:8000}")
    private String aiServiceUrl;

    private final RestTemplate restTemplate = new RestTemplate();
    private final HistoryService historyService;

    public QueryController(HistoryService historyService) {
        this.historyService = historyService;
    }

    @PostMapping("/query")
    public ResponseEntity<?> handleQuery(@RequestBody QueryRequest request) {

        // =========================
        // 1. VALIDATION LAYER
        // =========================
        if (request.getQuery() == null || request.getQuery().isBlank()) {
            return ResponseEntity.badRequest().body(
                Map.of("error", "Query cannot be empty")
            );
        }

        // =========================
        // 2. TẠO QUERY RECORD (trạng thái: processing)
        // =========================
        QueryRecord queryRecord = historyService.createQuery(
            request.getUserId(),
            request.getQuery()
        );
        String queryId = queryRecord.getId();

        try {
            // =========================
            // 3. BUILD AI PAYLOAD
            // =========================
            Map<String, Object> aiPayload = new HashMap<>();
            aiPayload.put("query",   request.getQuery());
            aiPayload.put("userId",  request.getUserId());
            aiPayload.put("meta",    request.getMeta());

            // =========================
            // 4. CALL AI SERVICE
            // =========================
            String url = aiServiceUrl + "/ai/generate-report";

            @SuppressWarnings("unchecked")
            ResponseEntity<Map> response = restTemplate.postForEntity(url, aiPayload, Map.class);

            @SuppressWarnings("unchecked")
            Map<String, Object> aiBody = response.getBody();

            // =========================
            // 5. LƯU BÁO CÁO VÀO DB
            // =========================
            historyService.saveReport(queryId, aiBody);

            // =========================
            // 6. TRẢ VỀ CHO FE
            // =========================
            return ResponseEntity.ok(Map.of(
                "success", true,
                "queryId", queryId,
                "data",    aiBody
            ));

        } catch (Exception e) {
            historyService.markError(queryId);
            return ResponseEntity.status(500).body(Map.of(
                "success", false,
                "error",   "AI Service error: " + e.getMessage()
            ));
        }
    }

    @GetMapping("/health")
    public Map<String, String> health() {
        return Map.of(
            "status",  "UP",
            "service", "InfoAgent Gateway"
        );
    }
}
