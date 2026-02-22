股票预测系统 README
![image](https://github.com/user-attachments/assets/41b15419-4511-4bd2-920a-34c7584e848a)

项目概述<br>
股票预测系统是一个使用机器学习模型预测股票价格的Web应用程序。该系统采用前后端分离架构，使用Flask提供机器学习模型服务，Vue.js构建用户界面。系统支持多层感知机(MLP)、卷积神经网络(CNN)和长短期记忆网络(LSTM)三种模型，用于分析历史股价数据并预测未来趋势。<br>

系统架构<br>
┌─────────────┐      HTTP      ┌─────────────┐<br>
│  Vue.js前端 │ ◀──────────▶  │  Flask后端  │<br>
│  (端口8081) │    请求/响应   │  (端口5000) │<br>
└─────────────┘               └─────────────┘<br>

前端：Vue.js应用 (端口8081)<br>
后端：Flask API服务 (端口5000)<br>
数据源：通过Akshare库获取实时股票数据<br>
技术栈<br>
前端<br>
Vue.js 3<br>
Vue Router<br>
Axios<br>
Chart.js<br>
后端<br>
Flask<br>
Flask-CORS<br>
TensorFlow/Keras<br>
NumPy<br>
Pandas<br>
Matplotlib<br>
Scikit-learn<br>
Akshare (股票数据API)<br>
项目结构<br>
stock-prediction-system/<br>
├── model_service.py            # Flask后端服务主文件<br>
├── requirements.txt            # Python依赖列表<br>
│<br>
└── stock-predict-frontend/     # Vue.js前端项目<br>
    ├── public/                 # 静态资源<br>
    ├── src/                    # 源代码<br>
    │   ├── assets/             # 资源文件<br>
    │   ├── components/         # 组件<br>
    │   ├── router/             # 路由配置<br>
    │   │   └── index.js        # 路由定义<br>
    │   ├── views/              # 页面组件<br>
    │   │   ├── HomePage.vue    # 首页<br>
    │   │   ├── ModelTraining.vue # 模型训练页面<br>
    │   │   └── StockPrediction.vue # 股价预测页面<br>
    │   ├── App.vue             # 主应用组件<br>
    │   └── main.js             # 应用入口<br>
    ├── package.json            # npm配置<br>
    └── vue.config.js           # Vue配置<br>
安装与配置<br>
后端（Flask）<br>
确保已安装Python 3.7+<br>

安装必要的Python包：<br>

Copypip install flask flask-cors numpy pandas matplotlib tensorflow scikit-learn akshare<br>
或者使用requirements.txt：<br>

Copypip install -r requirements.txt<br>
前端（Vue.js）<br>
确保已安装Node.js (14+)和npm<br>

进入前端项目目录并安装依赖：<br>

Copycd stock-predict-frontend<br>
npm install<br>
运行系统<br>
1. 启动Flask后端<br>
Copypython model_service.py<br>
Flask服务将在 http://localhost:5000 上运行<br>

2. 启动Vue前端<br>
Copycd stock-predict-frontend<br>
npm run serve<br>
前端应用将在 http://localhost:8081 上运行<br>

3. 访问应用<br>
在浏览器中打开 http://localhost:8081 访问应用<br>

功能说明<br>
主页<br>
系统状态检查<br>
功能导航<br>
模型训练<br>
输入股票代码（例如：sh000001 - 上证指数）<br>
选择训练数据日期范围<br>
设置时间步长参数<br>
训练模型并查看结果图表和性能指标(MSE, RMSE, MAE)<br>
股价预测<br>
输入特征数据<br>
获取股价预测结果<br>
故障排除<br>
常见问题<br>
"Network Error"错误<br>

检查Flask服务是否正在运行<br>
访问 http://localhost:5000/test 测试API可用性<br>
检查防火墙设置是否阻止了端口通信<br>
获取股票数据失败<br>

确认股票代码格式正确（如：sh000001）<br>
确认选择的日期范围有效<br>
检查网络连接是否正常<br>
训练模型时出错<br>

确保选择的时间范围内有足够的数据点<br>
检查控制台日志获取详细错误信息<br>
开发者说明<br>
Flask API端点<br>
GET /test - API健康检查<br>
POST /train/mlp - 训练MLP模型<br>
POST /train/cnn - 训练CNN模型 (开发中)<br>
POST /train/lstm - 训练LSTM模型 (开发中)<br>

扩展指南<br>

添加新模型：<br>
在Flask后端添加新的训练端点<br>
在前端添加相应的用户界面元素<br>

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=MadPrinter/stockpredict.git&type=date&legend=top-left)](https://www.star-history.com/#MadPrinter/stockpredict.git&type=date&legend=top-left)改进数据源：<br>
可以扩展akshare的使用或集成其他金融数据源<br>
许可证<br>
MIT<br>
