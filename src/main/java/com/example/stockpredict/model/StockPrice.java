package com.example.stockpredict.model;

import lombok.Data;

@Data
public class StockPrice {
    private Long id;
    private String symbol;
    private String date;
    private Double open;
    private Double high;
    private Double low;
    private Double close;
    private Double volume;
}
