package org.example.be.controller;

import org.example.be.service.HistoryService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

/**
 * REST API để FE lấy lịch sử tra cứu theo userId.
 *
 *  GET /api/history/{userId}
 *      → Trả về danh sách query + report của user, mới nhất trước.
 */
@RestController
@RequestMapping("/api/history")
public class HistoryController {

    private final HistoryService historyService;

    public HistoryController(HistoryService historyService) {
        this.historyService = historyService;
    }

    /**
     * Lấy toàn bộ lịch sử tra cứu của một user.
     *
     * @param userId  Supabase Auth UUID của user (gửi từ FE)
     */
    @GetMapping("/{userId}")
    public ResponseEntity<?> getHistory(@PathVariable String userId) {
        try {
            List<Map<String, Object>> history = historyService.getHistory(userId);
            return ResponseEntity.ok(Map.of(
                "success", true,
                "data",    history
            ));
        } catch (Exception e) {
            return ResponseEntity.status(500).body(Map.of(
                "success", false,
                "error",   "Lỗi khi lấy lịch sử: " + e.getMessage()
            ));
        }
    }

    /**
     * Xóa một đoạn chat.
     */
    @DeleteMapping("/{queryId}")
    public ResponseEntity<?> deleteHistory(@PathVariable String queryId) {
        boolean ok = historyService.deleteQuery(queryId);
        return ResponseEntity.ok(Map.of("success", ok));
    }

    /**
     * Đổi tên một đoạn chat.
     */
    @PatchMapping("/{queryId}")
    public ResponseEntity<?> renameHistory(@PathVariable String queryId, @RequestBody Map<String, String> body) {
        String newTitle = body.get("title");
        boolean ok = historyService.renameQuery(queryId, newTitle);
        return ResponseEntity.ok(Map.of("success", ok));
    }
}
