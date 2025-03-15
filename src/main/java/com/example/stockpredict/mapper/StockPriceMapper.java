package com.example.stockpredict.mapper;

import com.example.stockpredict.model.StockPrice;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface StockPriceMapper {
    int insert(StockPrice stockPrice);
}
