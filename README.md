股票预测系统 README
项目概述
股票预测系统是一个基于Flask和Vue.js的全栈应用，旨在使用机器学习模型（如多层感知机（MLP）、卷积神经网络（CNN）、长短期记忆网络（LSTM））对股票市场数据进行分析和预测。用户可以通过前端界面输入股票代码和日期范围，训练模型并查看预测结果。

系统架构
前端：使用Vue.js构建，提供用户交互界面
后端：使用Flask构建，提供模型训练和预测的API
数据库：通过Akshare库获取股票市场数据
技术栈
前端：

Vue.js
Axios
Vue Router
后端：

Flask
Keras/TensorFlow
Pandas
NumPy
Akshare
Matplotlib
Scikit-learn
项目结构
stockpredict/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/
│   │   │       └── example/
│   │   │           └── stockpredict/
│   │   │               ├── config/
│   │   │               │   ├── SecurityConfig.java
│   │   │               │   └── WebConfig.java
│   │   │               ├── controller/
│   │   │               │   └── ModelController.java
│   │   │               ├── mapper/
│   │   │               │   └── StockPriceMapper.java
│   │   │               ├── model/
│   │   │               │   └── StockPrice.java
│   │   │               └── service/
│   │   │                   └── ModelService.java
│   │   ├── resources/
│   │   │   ├── application.yml
│   │   │   └── mapper/
│   │   │       └── StockPriceMapper.xml
├── model_service.py
├── requirements.txt
└── README.md
环境要求
Python 3.7+
Java 17+
Node.js 14+
MySQL 5.7+
安装与运行
1. 安装后端（Flask部分）
克隆或下载项目代码。

在项目根目录下创建并激活虚拟环境（可选）：

Copypython -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
安装所需的Python库：

Copypip install -r requirements.txt
启动Flask服务：

Copypython model_service.py
默认服务将在 http://localhost:5000 上运行。

2. 安装前端（Vue部分）
进入前端目录：

Copycd stock-predict-frontend
安装依赖：

Copynpm install
启动Vue应用：

Copynpm run serve
默认服务将在 http://localhost:8081 上运行。

3. 启动Spring Boot后端
在Spring Boot项目目录中，运行以下命令：

Copymvn spring-boot:run
默认服务将在 http://localhost:8080 上运行。

使用说明
打开浏览器，访问前端应用 http://localhost:8081。
在“模型训练”页面中，输入股票代码、开始日期和结束日期，以及时间步长（n_steps）。
点击“开始训练”按钮进行模型训练，系统将显示训练结果和预测图表。
在“股价预测”页面中，输入特征数据以进行预测（该功能仍在开发中）。
贡献
欢迎任何对项目的贡献！请提交问题或拉取请求。

许可证
该项目遵循MIT许可证。有关详细信息，请参阅 LICENSE 文件。
