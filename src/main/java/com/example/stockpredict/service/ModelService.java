package com.example.stockpredict.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.Map;

@Service
public class ModelService {

    private final RestTemplate restTemplate;

    @Value("${python.model-service.url}")
    private String modelServiceUrl;

    public ModelService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public Map<String, Object> trainMlp(String symbol, String startDate, String endDate, int nSteps) {
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("symbol", symbol);
        requestBody.put("start_date", startDate);
        requestBody.put("end_date", endDate);
        requestBody.put("n_steps", nSteps);

        ResponseEntity<Map> response = restTemplate.postForEntity(
                modelServiceUrl + "/train/mlp", requestBody, Map.class);

        return response.getBody();
    }

    // 其他模型的训练和预测方法...
}
