package org.example.be.controller;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class QueryController {

    @Value("${ai-service.url:http://localhost:8000}")
    private String aiServiceUrl;

    private final RestTemplate restTemplate = new RestTemplate();

    @PostMapping("/query")
    public ResponseEntity<?> forwardQuery(@RequestBody Map<String, Object> payload) {
        try {
            // Forward request to AI Service (FastAPI)
            // Add a mock query_id since FastAPI expects it
            payload.putIfAbsent("query_id", 1);
            
            String targetUrl = aiServiceUrl + "/ai/generate-report";
            Object response = restTemplate.postForObject(targetUrl, payload, Object.class);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return ResponseEntity.status(500).body(Map.of(
                "error", "Không thể kết nối tới AI Service: " + e.getMessage()
            ));
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
