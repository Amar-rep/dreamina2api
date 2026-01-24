# Dreamina API

Dreamina (CapCut) 图像生成 API 服务。

## 功能

- 文生图 (Text-to-Image)
- 图生图 (Image-to-Image)
- 支持多种模型和分辨率

## 支持的模型

| 模型名称 | API Key |
|---------|---------|
| Image 4.5 | `dreamina-4.5` (默认) |
| Image 4.1 | `dreamina-4.1` |
| Image 4.0 | `dreamina-4.0` |

## 支持的比例

- `1:1`, `4:3`, `3:4`, `16:9`, `9:16`, `3:2`, `2:3`, `21:9`

## 获取 Session ID

1. 访问 Dreamina 官网: https://dreamina.capcut.com/ai-tool/home
2. 登录账号
3. 按 F12 打开浏览器开发者工具
4. 切换到 Application (应用) 标签 → Cookies
5. 找到 `sessionid` 字段，复制其值

## 安装

```bash
npm install
```

## 运行

### 本地运行

```bash
npm run build
npm start
```

### Docker 运行

```bash
# docker-compose (推荐)
docker-compose up -d

# 或手动构建
docker build -t dreamina-api .
docker run -d -p 5200:5200 --name dreamina-api dreamina-api
```

服务默认在 `http://localhost:5200` 启动。

## API

### 文生图

```bash
curl -X POST http://localhost:5200/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_SESSION_ID" \
  -d '{
    "prompt": "画一个苹果",
    "model": "dreamina-4.5",
    "ratio": "16:9"
  }'
```

### 参数说明

| 参数 | 必填 | 说明 |
|-----|-----|------|
| `prompt` | ✅ | 图片描述 |
| `model` | ❌ | 模型名称，默认 `dreamina-4.5` |
| `ratio` | ❌ | 图片比例，默认 `1:1` |
| `negative_prompt` | ❌ | 负向提示词 |
| `sample_strength` | ❌ | 精细度 (0-1) |

### 获取历史

```bash
curl -X POST http://localhost:5200/v1/images/history \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_SESSION_ID" \
  -d '{
    "submit_ids": ["your-submit-id"]
  }'
```

## Python 脚本

```bash
cd scripts
python3 generate_image.py --prompt "画一个苹果" --token "YOUR_SESSION_ID" --ratio "16:9"
```

## 环境变量

| 变量 | 说明 | 默认值 |
|-----|------|-------|
| `PORT` | 服务端口 | `5200` |

## 致谢

本项目基于 [jimeng-api](https://github.com/iptag/jimeng-api) 修改而来，感谢原作者的贡献。

## License

MIT
