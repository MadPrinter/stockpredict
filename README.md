股票预测系统 README
项目概述
股票预测系统是一个使用机器学习模型预测股票价格的Web应用程序。该系统采用前后端分离架构，使用Flask提供机器学习模型服务，Vue.js构建用户界面。系统支持多层感知机(MLP)、卷积神经网络(CNN)和长短期记忆网络(LSTM)三种模型，用于分析历史股价数据并预测未来趋势。

系统架构
┌─────────────┐      HTTP      ┌─────────────┐
│  Vue.js前端 │ ◀──────────▶  │  Flask后端  │
│  (端口8081) │    请求/响应   │  (端口5000) │
└─────────────┘               └─────────────┘
前端：Vue.js应用 (端口8081)
后端：Flask API服务 (端口5000)
数据源：通过Akshare库获取实时股票数据
技术栈
前端
Vue.js 3
Vue Router
Axios
Chart.js
后端
Flask
Flask-CORS
TensorFlow/Keras
NumPy
Pandas
Matplotlib
Scikit-learn
Akshare (股票数据API)
项目结构
stock-prediction-system/
├── model_service.py            # Flask后端服务主文件
├── requirements.txt            # Python依赖列表
│
└── stock-predict-frontend/     # Vue.js前端项目
    ├── public/                 # 静态资源
    ├── src/                    # 源代码
    │   ├── assets/             # 资源文件
    │   ├── components/         # 组件
    │   ├── router/             # 路由配置
    │   │   └── index.js        # 路由定义
    │   ├── views/              # 页面组件
    │   │   ├── HomePage.vue    # 首页
    │   │   ├── ModelTraining.vue # 模型训练页面
    │   │   └── StockPrediction.vue # 股价预测页面
    │   ├── App.vue             # 主应用组件
    │   └── main.js             # 应用入口
    ├── package.json            # npm配置
    └── vue.config.js           # Vue配置
安装与配置
后端（Flask）
确保已安装Python 3.7+

安装必要的Python包：

Copypip install flask flask-cors numpy pandas matplotlib tensorflow scikit-learn akshare
或者使用requirements.txt：

Copypip install -r requirements.txt
前端（Vue.js）
确保已安装Node.js (14+)和npm

进入前端项目目录并安装依赖：

Copycd stock-predict-frontend
npm install
运行系统
1. 启动Flask后端
Copypython model_service.py
Flask服务将在 http://localhost:5000 上运行

2. 启动Vue前端
Copycd stock-predict-frontend
npm run serve
前端应用将在 http://localhost:8081 上运行

3. 访问应用
在浏览器中打开 http://localhost:8081 访问应用

功能说明
主页
系统状态检查
功能导航
模型训练
输入股票代码（例如：sh000001 - 上证指数）
选择训练数据日期范围
设置时间步长参数
训练模型并查看结果图表和性能指标(MSE, RMSE, MAE)
股价预测
输入特征数据
获取股价预测结果
故障排除
常见问题
"Network Error"错误

检查Flask服务是否正在运行
访问 http://localhost:5000/test 测试API可用性
检查防火墙设置是否阻止了端口通信
获取股票数据失败

确认股票代码格式正确（如：sh000001）
确认选择的日期范围有效
检查网络连接是否正常
训练模型时出错

确保选择的时间范围内有足够的数据点
检查控制台日志获取详细错误信息
开发者说明
Flask API端点
GET /test - API健康检查
POST /train/mlp - 训练MLP模型
POST /train/cnn - 训练CNN模型 (开发中)
POST /train/lstm - 训练LSTM模型 (开发中)
扩展指南
添加新模型：

在Flask后端添加新的训练端点
在前端添加相应的用户界面元素
改进数据源：

可以扩展akshare的使用或集成其他金融数据源
许可证
MIT

鸣谢
感谢Akshare团队提供的金融数据API
感谢TensorFlow和Keras团队提供的机器学习框架
感谢Vue.js团队提供的前端框架
