# Scnet 部署说明

## 方式 1: 直接部署（推荐）

1. 登录 Scnet 控制台
2. 创建新应用
3. 选择 Python 3.9 运行时
4. 上传此仓库代码
5. 设置环境变量（见下方）
6. 部署

## 方式 2: Docker 部署

```bash
docker build -t ai-aggregator .
docker run -p 8080:8080 ai-aggregator
```

## 环境变量配置

在 Scnet 控制台设置以下变量：

```
OPENROUTER_KEYS=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
GROQ_KEYS=your_groq_keys
TOGETHER_KEYS=your_together_keys
Google_KEYS=AIzaSyAIRi940QpfoxN27DjNLEy9Hy1ONkUWCaM
DeepSeek_KEYS=sk-cd8b2a27fe634588a99ee317b98496f2
```

## 启动命令

```
gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

## 访问

部署后访问：
```
https://your-app.scnet.io
```

## 特性

- ✅ 多模型调度
- ✅ 自动缓存
- ✅ Web UI
- ✅ 流式输出
- ✅ 高可用

## 支持的 API

- OpenRouter (Llama 3.1 8B)
- Groq (Llama3 70B)
- Together AI (Mixtral 8x7B)
