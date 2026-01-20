# QWen API 调研项目

本项目包含QWen大模型API的完整调研文档和Python示例代码。

## 📋 项目内容

### 1. 📚 文档

- **Qwen_API_Complete_Guide.md** - 完整的API调研指南，包含：
  - 官方API接口文档和鉴权方式
  - 支持的模型列表和定价
  - 所有接口类型详解
  - Python调用示例代码
  - 最佳实践和性能优化建议
  - 成本控制方案
  - 常见问题解决

### 2. 💻 代码示例

- **qwen_examples.py** - 7个完整的Python示例：
  1. 基本对话 - 最简单的API调用
  2. 流式对话 - 实时显示生成内容
  3. 函数调用 - Function Calling完整演示
  4. 错误处理 - 重试机制和错误恢复
  5. 多轮对话 - 保持对话上下文
  6. 并发调用 - 并发处理多个请求
  7. 成本监控 - 追踪API调用成本

- **requirements.txt** - 项目依赖

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置API Key

方法一：环境变量
```bash
export DASHSCOPE_API_KEY=your-api-key-here
```

方法二：.env文件
```bash
# 在项目根目录创建 .env 文件
echo "DASHSCOPE_API_KEY=your-api-key-here" > .env
```

### 3. 运行示例

```bash
python qwen_examples.py
```

然后选择要运行的示例（1-8）。

## 📖 文档速查

### 常用模型

| 模型 | 输入价格 | 输出价格 | 特点 | 推荐用途 |
|------|---------|---------|------|---------|
| qwen-turbo | ¥0.0003/1K | ¥0.0006/1K | 最便宜、快速 | **简单任务** |
| qwen-plus | ¥0.0008/1K | ¥0.002/1K | 性能平衡 | **大多数场景推荐** |
| qwen-max | ¥0.02/1K | ¥0.06/1K | 最强性能 | 复杂任务 |
| qwen-long | ¥0.0005/1K | ¥0.002/1K | 支持百万token | 长文档处理 |

📅 **价格信息更新时间**：2024年12月31日（官方最新降价）

### 快速代码示例

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="https://dashscope.aliyun.com/compatible-mode/v1"
)

response = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "user", "content": "你好，请介绍一下自己"}
    ]
)

print(response.choices[0].message.content)
```

### 流式输出

```python
stream = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "请写一首诗"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end='', flush=True)
```

## ❓ 常见问题

### Q: API Key在哪里获取？
A: 访问 https://dashscope.aliyun.com/ 登录后创建API Key。

### Q: 如何选择合适的模型？
A: 
- 成本考虑 → qwen-turbo
- 推荐选择 → qwen-plus
- 最高性能 → qwen-max

### Q: 超出限流怎么办？
A: 使用示例4中的重试机制，会自动进行指数退避重试。

### Q: 如何降低成本？
A: 
1. 使用qwen-turbo替代plus（节省成本6倍）
2. 限制max_tokens
3. 使用缓存避免重复调用

## 📞 支持和反馈

- 官方文档: https://dashscope.aliyun.com/
- SDK地址: https://github.com/aliyun/dashscope-python-sdk
- 问题反馈: 在项目issue中提交

## 📝 许可证

本项目为学习和参考用途。

## 🔗 相关链接

- [QWen官方网站](https://qwenlm.github.io/)
- [DashScope API文档](https://help.aliyun.com/zh/dashscope/)
- [OpenAI SDK文档](https://github.com/openai/openai-python)
- [Python异步编程](https://docs.python.org/3/library/asyncio.html)

---

**最后更新**: 2024年1月
