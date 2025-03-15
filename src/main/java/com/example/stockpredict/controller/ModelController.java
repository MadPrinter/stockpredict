package com.example.stockpredict.controller;

import com.example.stockpredict.service.ModelService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/models")
@CrossOrigin(origins = "http://localhost:8081") // 允许的前端地址
public class ModelController {

    private final ModelService modelService;

    @Autowired
    public ModelController(ModelService modelService) {
        this.modelService = modelService;
    }

    @PostMapping("/train/mlp")
    public ResponseEntity<?> trainMlpModel(@RequestBody Map<String, Object> requestData) {
        String symbol = (String) requestData.get("symbol");
        String startDate = (String) requestData.get("start_date");
        String endDate = (String) requestData.get("end_date");
        int nSteps = requestData.containsKey("n_steps") ? (int) requestData.get("n_steps") : 7;

        Map<String, Object> result = modelService.trainMlp(symbol, startDate, endDate, nSteps);
        return ResponseEntity.ok(result);
    }

    // 其他模型的训练和预测接口...
}
