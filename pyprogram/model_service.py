# model_service.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
import akshare as ak
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端，避免图形界面问题
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
import io
import base64
import logging
import sys

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

app = Flask(__name__)
CORS(app)  # 启用CORS，允许所有来源访问

def split_sequence(sequence, n_steps):
    """将时间序列分割为输入和输出对"""
    sequence = np.array(sequence)
    X, y = list(), list()
    for i in range(len(sequence)):
        end_ix = i + n_steps
        if end_ix > len(sequence) - 1:
            break
        seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)

def get_stock_index_daily(symbol, start_date_str, end_date_str):
    """获取股票数据"""
    try:
        logger.info(f"正在获取股票数据: {symbol} 从 {start_date_str} 到 {end_date_str}")
        start_date = pd.to_datetime(start_date_str)
        end_date = pd.to_datetime(end_date_str)
        df_daily = ak.stock_zh_index_daily(symbol=symbol)

        if df_daily is None or len(df_daily) == 0:
            return None, "无法获取股票数据或数据为空"

        df_daily.columns = ['日期', '开盘', '最高价', '最低价', '收盘', '成交量']
        df_daily['日期'] = pd.to_datetime(df_daily['日期'])
        df_daily = df_daily[(df_daily['日期'] >= start_date) & (df_daily['日期'] <= end_date)]

        if len(df_daily) == 0:
            return None, "指定时间范围内没有股票数据"

        # 计算涨跌幅
        df_daily['涨跌幅'] = df_daily['收盘'].pct_change() * 100
        df_daily.dropna(inplace=True)

        logger.info(f"成功获取股票数据: {len(df_daily)} 条记录")
        return df_daily, None
    except Exception as e:
        logger.error(f"获取股票数据失败: {str(e)}")
        return None, f"获取股票数据失败: {str(e)}"

@app.route('/test', methods=['GET'])
def test():
    """测试端点"""
    return jsonify({"status": "success", "message": "Flask模型服务正常运行"})

@app.route('/train/mlp', methods=['POST'])
def train_mlp():
    """训练MLP模型端点"""
    try:
        data = request.json
        logger.info(f"收到训练请求: {data}")

        # 验证输入参数
        required_fields = ['symbol', 'start_date', 'end_date']
        if not all(field in data for field in required_fields):
            logger.error(f"缺少必要参数: {required_fields}")
            return jsonify({"error": "缺少必要参数"}), 400

        symbol = data['symbol']
        start_date_str = data['start_date']
        end_date_str = data['end_date']
        n_steps = int(data.get('n_steps', 7))

        # 获取股票数据
        df_daily, error_msg = get_stock_index_daily(symbol, start_date_str, end_date_str)
        if df_daily is None:
            logger.error(error_msg)
            return jsonify({"error": error_msg}), 400

        # 分割数据集
        train_data, test_data = train_test_split(df_daily, test_size=0.2, shuffle=False)
        logger.info(f"分割数据集: 训练集 {len(train_data)} 条, 测试集 {len(test_data)} 条")

        # 特征工程
        features = ['日期', '最高价', '最低价', '收盘', '成交量', '涨跌幅']

        try:
            # 数据预处理
            def preprocess_data(data):
                processed = data.copy()
                processed['日期'] = processed['日期'].dt.weekday + 1  # 将日期转换为星期几
                processed['涨跌幅'] = processed['涨跌幅'].apply(lambda x: 1 if x > 0.5 else 0)
                return processed

            train_data_processed = preprocess_data(train_data)
            test_data_processed = preprocess_data(test_data)

            # 提取特征和标签
            def extract_features(data, n_steps):
                X_list = []
                for feature in features:
                    feature_data = data[feature].values
                    X, _ = split_sequence(feature_data, n_steps)
                    X_list.append(X)

                # 合并并转置特征
                X_combined = np.hstack(X_list)
                X_reshaped = X_combined.reshape(X_list[0].shape[0], len(features), n_steps)
                X_final = np.transpose(X_reshaped, (0, 2, 1))

                # 提取标签（下一个收盘价）
                _, y = split_sequence(data['收盘'].values, n_steps)

                return X_final, y

            X_train, y_train = extract_features(train_data_processed, n_steps)
            X_test, y_test = extract_features(test_data_processed, n_steps)

            logger.info(f"特征形状: 训练 {X_train.shape}, 测试 {X_test.shape}")

            # 数据归一化
            scaler_x = MinMaxScaler()
            X_train_flat = X_train.reshape(X_train.shape[0] * n_steps, len(features))
            X_train_scaled_flat = scaler_x.fit_transform(X_train_flat)
            X_train_scaled = X_train_scaled_flat.reshape(X_train.shape)

            X_test_flat = X_test.reshape(X_test.shape[0] * n_steps, len(features))
            X_test_scaled_flat = scaler_x.transform(X_test_flat)
            X_test_scaled = X_test_scaled_flat.reshape(X_test.shape)

            scaler_y = MinMaxScaler()
            y_train_scaled = scaler_y.fit_transform(y_train.reshape(-1, 1))
            y_test_scaled = scaler_y.transform(y_test.reshape(-1, 1))

            # 构建MLP模型
            model = Sequential()
            model.add(Input(shape=(n_steps * len(features),)))
            model.add(Dense(200, activation='relu'))
            model.add(Dense(100, activation='relu'))
            model.add(Dropout(0.1))
            model.add(Dense(1))
            model.compile(loss='mean_squared_error', optimizer='adam')

            # 训练模型
            logger.info("开始训练模型...")
            X_train_reshaped = X_train_scaled.reshape(X_train_scaled.shape[0], -1)
            history = model.fit(
                X_train_reshaped, y_train_scaled,
                epochs=100, batch_size=32, verbose=0
            )
            logger.info("模型训练完成")

            # 预测
            X_test_reshaped = X_test_scaled.reshape(X_test_scaled.shape[0], -1)
            y_pred_scaled = model.predict(X_test_reshaped)

            # 反归一化
            y_pred = scaler_y.inverse_transform(y_pred_scaled)
            y_test_actual = y_test.reshape(-1, 1)

            # 计算指标
            mse = mean_squared_error(y_test_actual, y_pred)
            rmse = np.sqrt(mse)
            mae = mean_absolute_error(y_test_actual, y_pred)

            logger.info(f"模型评估: MSE={mse}, RMSE={rmse}, MAE={mae}")

            # 生成图表
            plt.figure(figsize=(12, 6))
            plt.plot(range(len(y_test_actual)), y_test_actual, label='实际收盘价', marker='o')
            plt.plot(range(len(y_pred)), y_pred, label='预测收盘价', marker='x')
            plt.title('实际收盘价 vs 预测收盘价 (MLP)')
            plt.ylabel('价格')
            plt.legend()
            plt.grid(True)

            # 转换图表为base64
            img_buf = io.BytesIO()
            plt.savefig(img_buf, format='png')
            img_buf.seek(0)
            img_data = base64.b64encode(img_buf.read()).decode('utf-8')
            plt.close()

            # 返回结果
            return jsonify({
                'status': 'success',
                'mse': float(mse),
                'rmse': float(rmse),
                'mae': float(mae),
                'chart': img_data
            })

        except Exception as e:
            logger.error(f"处理数据或训练模型时出错: {str(e)}")
            return jsonify({"error": f"处理数据或训练模型时出错: {str(e)}"}), 500

    except Exception as e:
        logger.error(f"训练MLP模型时出错: {str(e)}")
        return jsonify({"error": f"训练MLP模型时出错: {str(e)}"}), 500

if __name__ == '__main__':
    logger.info("启动Flask模型服务，监听端口5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)
