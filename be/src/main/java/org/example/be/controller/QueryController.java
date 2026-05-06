package org.example.be.controller;

import org.example.be.DTO.QueryRequest;
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

    @PostMapping("/query")
    public ResponseEntity<?> handleQuery(@RequestBody QueryRequest request) {

        try {
            // =========================
            // 1. VALIDATION LAYER (BE RESPONSIBILITY)
            // =========================
            if (request.getQuery() == null || request.getQuery().isBlank()) {
                return ResponseEntity.badRequest().body(
                    Map.of("error", "Query cannot be empty")
                );
            }

            // =========================
            // 2. BUILD AI PAYLOAD (STRICT CONTRACT)
            // =========================
            Map<String, Object> aiPayload = new HashMap<>();
            aiPayload.put("query", request.getQuery());
            aiPayload.put("user_id", request.getUserId());
            aiPayload.put("meta", request.getMeta());

            // =========================
            // 3. CALL AI SERVICE
            // =========================
            String url = aiServiceUrl + "/ai/generate-report";

            ResponseEntity<Map> response = restTemplate.postForEntity(
                url,
                aiPayload,
                Map.class
            );

            // =========================
            // 4. RESPONSE WRAPPING
            // =========================
            Map<String, Object> body = response.getBody();

            return ResponseEntity.ok(Map.of(
                "success", true,
                "data", body
            ));

        } catch (Exception e) {
            return ResponseEntity.status(500).body(
                Map.of(
                    "success", false,
                    "error", "AI Service error: " + e.getMessage()
                )
            );
        }
    }

    @GetMapping("/health")
    public Map<String, String> health() {
        return Map.of(
            "status", "UP",
            "service", "InfoAgent Gateway"
        );
    }
}
