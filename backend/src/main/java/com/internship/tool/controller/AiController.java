package com.internship.tool.controller;

import com.internship.tool.service.AiServiceClient;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/ai")
public class AiController {

    private final AiServiceClient aiServiceClient;

    public AiController(AiServiceClient aiServiceClient) {
        this.aiServiceClient = aiServiceClient;
    }

    @PostMapping("/describe")
    public String describe(@RequestBody Map<String, String> request) {
        String text = request.get("text");
        return aiServiceClient.callDescribe(text);
    }

    @PostMapping("/generate-report")
    public String generateReport(@RequestBody Map<String, String> request) {
        String text = request.get("text");
        return aiServiceClient.callGenerateReport(text);
    }
}