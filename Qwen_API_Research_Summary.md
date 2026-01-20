# Qwen大模型API完整调研总结

## 一、官方API接口文档

### 1.1 基础API调用方法

Qwen API支持**两种调用协议**：

#### **OpenAI兼容协议** （推荐）
- 与OpenAI API格式完全兼容
- 支持多种编程语言的OpenAI SDK
- 请求地址：`POST /chat/completions`
- 优点：无缝迁移、生态成熟

#### **DashScope协议** （阿里云原生）
- 阿里云专门的协议
- 支持专门的DashScope SDK
- 请求地址：`POST /services/aigc/text-generation/generation`

#### **地域端点**
```
华北2（北京）:
  OpenAI兼容: https://dashscope.aliyuncs.com/compatible-mode/v1
  DashScope: https://dashscope.aliyuncs.com/api/v1

新加坡:
  OpenAI兼容: https://dashscope-intl.aliyuncs.com/compatible-mode/v1
  DashScope: https://dashscope-intl.aliyuncs.com/api/v1

美国（弗吉尼亚）:
  OpenAI兼容: https://dashscope-us.aliyuncs.com/compatible-mode/v1
  DashScope: https://dashscope-us.aliyuncs.com/api/v1

金融云:
  OpenAI兼容: https://dashscope-finance.aliyuncs.com/compatible-mode/v1
  DashScope: https://dashscope-finance.aliyuncs.com/api/v1
```

### 1.2 鉴权方式

所有API请求都需要在请求头中包含API Key：

```
Authorization: Bearer {API_KEY}
```

**获取方式：**
- 访问阿里云百炼平台：https://bailian.console.aliyun.com
- 创建API Key
- 建议配置环境变量：`export DASHSCOPE_API_KEY="sk-xxx"`

### 1.3 支持的模型列表

| 模型系列 | 具体模型 | 用途说明 | 特点 |
|---------|--------|--------|------|
| **通用模型** | qwen-max, qwen-max-latest | 高性能通用 | 延时约500ms，性能最强 |
| | qwen-plus, qwen-plus-latest | 通用模型 | 性价比最高，应用最广 |
| | qwen-flash, qwen-flash-latest | 轻量级 | 响应最快，消耗最少 |
| | qwen-turbo, qwen-turbo-latest | 快速响应 | 折中方案 |
| **编程模型** | qwen-coder-plus, qwen-coder-turbo | 代码生成/理解 | 编程能力专强 |
| | qwen-1.8b-chat | 极轻量 | 移动端/边缘部署 |
| **专业模型** | qwen-math-plus, qwen-math-turbo | 数学求解 | 数学推理专长 |
| | qwen-medicine-32b/7b/3b | 医学问题 | 医学领域 |
| | qwen-writing-32b/7b/3b | 写作创意 | 文案生成 |
| **视觉模型** | qwen-vl-max, qwen-vl-plus | 图像/视频理解 | 多模态输入 |
| | qvq-72b-preview | 视觉推理 | 视觉推理专强 |
| **长文本模型** | qwen-long | 长文本理解 | 处理超长文档 |
| **推理模型** | qwq-32b-preview | 深度推理 | 思维链推理 |
| **全模态模型** | qwen-omni-turbo | 文本+音频+视频 | 端到端全模态处理 |
| | qwen2-audio-instruct | 音频理解 | 语音识别和理解 |

### 1.4 请求/响应格式

#### **OpenAI兼容协议 - 请求格式**

```json
{
  "model": "qwen-plus",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "user",
      "content": "你是谁？"
    }
  ],
  "temperature": 0.7,
  "top_p": 0.8,
  "max_tokens": 2000,
  "stream": false
}
```

#### **请求参数详解**

| 参数 | 类型 | 必选 | 说明 | 取值范围 |
|------|------|------|------|---------|
| model | string | ✓ | 模型名称 | qwen-plus/max等 |
| messages | array | ✓ | 对话消息数组 | 每条包括role和content |
| temperature | float | ✗ | 采样温度 | [0, 2) 默认0.7 |
| top_p | float | ✗ | 核采样概率 | (0, 1.0] 默认0.8 |
| max_tokens | integer | ✗ | 最大输出Token数 | 根据模型限制 |
| stream | boolean | ✗ | 是否流式输出 | 默认false |
| enable_search | boolean | ✗ | 启用联网搜索 | 默认false |
| tools | array | ✗ | Function Calling工具列表 | - |
| top_k | integer | ✗ | Top-K采样 | 默认无限制 |
| presence_penalty | float | ✗ | 存在惩罚 | [-2, 2] |
| frequency_penalty | float | ✗ | 频率惩罚 | [-2, 2] |

#### **非流式响应格式**

```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "created": 1735120033,
  "model": "qwen-plus",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "我是阿里云开发的通义千问。"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 3019,
    "completion_tokens": 104,
    "total_tokens": 3123
  }
}
```

#### **流式响应格式**

```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion.chunk",
  "created": 1735113344,
  "model": "qwen-plus",
  "choices": [
    {
      "index": 0,
      "delta": {
        "role": "assistant",
        "content": "我是"
      },
      "finish_reason": null
    }
  ]
}
```

#### **响应字段说明**

| 字段 | 说明 |
|------|------|
| id | 本次调用的唯一标识符 |
| choices | 模型生成内容数组 |
| choices[].message.content | 模型的回复内容 |
| choices[].finish_reason | 停止原因：`stop`（正常）、`length`（超长）、`tool_calls`（工具调用） |
| usage.prompt_tokens | 输入Token数 |
| usage.completion_tokens | 输出Token数 |
| usage.total_tokens | 总Token数 |

---

## 二、主要接口类型

### 2.1 文本生成/对话接口

**基本特点：**
- 支持多轮对话
- 完整的上下文理解
- 支持角色设定

**适用场景：**
- 聊天机器人
- 问答系统
- 内容生成

### 2.2 流式响应接口

**特点：**
- 实时返回数据
- 用户体验好
- 适合UI展示

**关键参数：**
```python
stream=True  # 启用流式
stream_options={"include_usage": True}  # 获取Token统计
```

### 2.3 Function Calling（函数调用）接口

**核心功能：**
- 让模型判断是否需要调用外部工具
- 模型返回工具名和参数
- 支持并行工具调用

**工作流程：**
1. 第一步：发送用户问题+工具清单给模型
2. 第二步：模型返回需要调用的工具和参数
3. 第三步：应用端执行工具，获得结果
4. 第四步：将工具结果回传给模型
5. 第五步：模型整合信息返回最终答案

**支持的模型：**
- qwen-max、qwen-plus、qwen-flash等全系
- 其他厂商：deepseek-v3.2、glm-4.7、kimi-k2等

### 2.4 高级功能

| 功能 | 说明 | 应用场景 |
|------|------|---------|
| 联网搜索 | `enable_search=true` | 实时信息查询 |
| 多模态输入 | 图像、视频、音频 | 内容分析 |
| 长文本处理 | qwen-long模型 | 文档理解、总结 |
| 视觉推理 | qvq模型 | 图表分析、OCR |
| 音频处理 | qwen-omni系列 | 语音识别、转录 |

---

## 三、Python调用示例

### 3.1 SDK安装

```bash
# 方式一：OpenAI SDK（推荐）
pip install -U openai

# 方式二：阿里云DashScope SDK
pip install dashscope

# 方式三：使用LangChain
pip install langchain-community
```

### 3.2 基本调用示例（OpenAI兼容）

```python
import os
from openai import OpenAI

# 初始化客户端
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 从环境变量读取
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 发送请求
response = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "请解释什么是量子计算"}
    ],
    temperature=0.7,
    max_tokens=2000
)

# 获取回复
print(response.choices[0].message.content)

# 获取Token统计
print(f"输入Token: {response.usage.prompt_tokens}")
print(f"输出Token: {response.usage.completion_tokens}")
print(f"总Token: {response.usage.total_tokens}")
```

### 3.3 流式调用示例

```python
import os
import json
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 流式调用
stream = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "user", "content": "写一个快速排序算法"}
    ],
    stream=True,
    stream_options={"include_usage": True}  # 获取最终Token统计
)

# 处理流式响应
print("开始接收流式数据：\n")
total_tokens = 0

for chunk in stream:
    # 检查是否有delta内容
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
    
    # 获取最后的Token统计
    if chunk.usage:
        print(f"\n\n=== 调用统计 ===")
        print(f"输入Token: {chunk.usage.prompt_tokens}")
        print(f"输出Token: {chunk.usage.completion_tokens}")
        print(f"总Token: {chunk.usage.total_tokens}")
```

### 3.4 Function Calling示例

```python
from openai import OpenAI
import json
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 定义工具列表
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "查询指定城市的实时天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名称，如北京、上海等"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "温度单位"
                    }
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行数学计算",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

# 模拟工具执行
def get_current_weather(location, unit="celsius"):
    """模拟天气查询"""
    weather_data = {
        "北京": {"temp": 5, "description": "晴朗"},
        "上海": {"temp": 12, "description": "多云"}
    }
    data = weather_data.get(location, {"temp": 20, "description": "未知"})
    return f"{location}天气：{data['description']}，温度{data['temp']}°{unit[0].upper()}"

def calculate(expression):
    """执行计算"""
    try:
        result = eval(expression)
        return f"计算结果：{result}"
    except Exception as e:
        return f"计算错误：{str(e)}"

# 第一步：发送用户问题和工具列表
messages = [{"role": "user", "content": "北京现在多少度？计算一下2+2等于多少"}]

response = client.chat.completions.create(
    model="qwen-plus",
    messages=messages,
    tools=tools,
)

assistant_message = response.choices[0].message
messages.append(assistant_message)

# 第二步：检查是否需要调用工具
if assistant_message.tool_calls:
    print(f"模型判断需要调用以下工具：")
    
    # 执行所有工具调用
    tool_results = []
    for tool_call in assistant_message.tool_calls:
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)
        
        print(f"\n  - 工具：{tool_name}")
        print(f"    参数：{tool_args}")
        
        # 根据工具名执行相应函数
        if tool_name == "get_current_weather":
            result = get_current_weather(**tool_args)
        elif tool_name == "calculate":
            result = calculate(**tool_args)
        else:
            result = "工具不存在"
        
        print(f"    结果：{result}")
        
        # 保存工具结果
        tool_results.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        })
    
    # 添加工具结果到消息
    messages.extend(tool_results)
    
    # 第三步：再次调用模型获取最终答案
    print("\n正在生成最终答案...")
    final_response = client.chat.completions.create(
        model="qwen-plus",
        messages=messages,
        tools=tools,
    )
    
    print(f"\n最终答案：{final_response.choices[0].message.content}")
else:
    print(f"模型无需调用工具，直接回复：{assistant_message.content}")
```

### 3.5 错误处理示例

```python
from openai import OpenAI, APIError, RateLimitError, APIConnectionError
import os
import time

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

def call_qwen_with_retry(messages, max_retries=3, retry_delay=2):
    """带重试机制的API调用"""
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="qwen-plus",
                messages=messages,
                temperature=0.7,
                max_tokens=2000,
                timeout=30  # 30秒超时
            )
            return response
        
        except RateLimitError as e:
            # 触发限流
            if attempt < max_retries - 1:
                wait_time = retry_delay * (2 ** attempt)  # 指数退避
                print(f"触发限流，等待{wait_time}秒后重试...")
                time.sleep(wait_time)
            else:
                print(f"达到最大重试次数，触发限流：{str(e)}")
                raise
        
        except APIConnectionError as e:
            # 网络连接错误
            if attempt < max_retries - 1:
                print(f"网络连接错误，{retry_delay}秒后重试...")
                time.sleep(retry_delay)
            else:
                print(f"网络连接失败：{str(e)}")
                raise
        
        except APIError as e:
            # 其他API错误
            if "401" in str(e):
                print("错误：API Key无效或已过期")
                raise
            elif "400" in str(e):
                print("错误：请求参数不合法")
                raise
            elif "503" in str(e):
                # 服务器繁忙
                if attempt < max_retries - 1:
                    print(f"服务器繁忙，{retry_delay}秒后重试...")
                    time.sleep(retry_delay)
                else:
                    print("服务器繁忙，无法完成请求")
                    raise
            else:
                print(f"API错误：{str(e)}")
                raise
        
        except Exception as e:
            # 捕获所有其他异常
            print(f"未知错误：{str(e)}")
            raise

# 使用示例
try:
    messages = [
        {"role": "user", "content": "你好"}
    ]
    
    response = call_qwen_with_retry(messages)
    print(f"回复：{response.choices[0].message.content}")
    
except Exception as e:
    print(f"最终失败：{str(e)}")
```

### 3.6 多轮对话示例

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

def multi_turn_conversation():
    """多轮对话示例"""
    
    messages = [
        {
            "role": "system",
            "content": "你是一个专业的Python编程助手，帮助用户解答编程问题。"
        }
    ]
    
    print("开始对话（输入'exit'退出）：\n")
    
    while True:
        # 获取用户输入
        user_input = input("用户：").strip()
        
        if user_input.lower() == "exit":
            print("对话结束")
            break
        
        if not user_input:
            continue
        
        # 添加用户消息
        messages.append({"role": "user", "content": user_input})
        
        # 调用API
        response = client.chat.completions.create(
            model="qwen-plus",
            messages=messages,
            temperature=0.7
        )
        
        # 获取助手回复
        assistant_reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_reply})
        
        # 显示回复
        print(f"助手：{assistant_reply}\n")
        
        # 显示Token消耗
        print(f"[Token消耗] 输入:{response.usage.prompt_tokens} 输出:{response.usage.completion_tokens}")
        print("-" * 60 + "\n")

if __name__ == "__main__":
    multi_turn_conversation()
```

---

## 四、常见用例和最佳实践

### 4.1 提示词优化

#### **原则1：清晰的角色定义**

```python
# ❌ 不好的例子
messages=[
    {"role": "user", "content": "你能帮我吗？"}
]

# ✅ 好的例子
messages=[
    {
        "role": "system", 
        "content": "你是一个资深的数据分析师，拥有10年的行业经验。你的回答需要专业、准确、易懂。"
    },
    {"role": "user", "content": "如何分析用户流失率？"}
]
```

#### **原则2：具体化需求**

```python
# ❌ 不好的例子
{"role": "user", "content": "写一个函数"}

# ✅ 好的例子
{
    "role": "user",
    "content": """
    写一个Python函数，实现快速排序算法，要求：
    1. 输入参数为一个列表
    2. 返回排序后的列表
    3. 添加详细的注释
    4. 包含测试用例
    """
}
```

#### **原则3：提供上下文**

```python
# ❌ 不好的例子
{"role": "user", "content": "这段代码有什么问题？"}

# ✅ 好的例子
{
    "role": "user",
    "content": """
    背景：我们在处理电商订单数据
    问题代码：
    ```python
    orders = [100, 200, 150]
    total = sum(orders) / len(orders)
    ```
    这段代码的问题是什么？如何改进？
    """
}
```

#### **原则4：少量示例（Few-Shot）**

```python
# 使用少量示例引导模型输出格式
messages = [
    {
        "role": "system",
        "content": "你是一个数据标注助手，根据用户输入生成JSON格式的标注。"
    },
    {
        "role": "user",
        "content": "从这句话中提取人物和地点：张三在北京买了一套房子。"
    },
    {
        "role": "assistant",
        "content": '{"person": "张三", "location": "北京", "action": "买房"}'
    },
    {
        "role": "user",
        "content": "从这句话中提取人物和地点：李四在上海找到了一份工作。"
    }
]
```

### 4.2 性能优化建议

#### **1. 选择合适的模型**

| 场景 | 推荐模型 | 理由 |
|------|--------|------|
| 实时对话 | qwen-flash | 延时低，成本低 |
| 复杂任务 | qwen-plus | 平衡性能和成本 |
| 高精度需求 | qwen-max | 性能最强 |
| 代码任务 | qwen-coder-plus | 编程能力强 |
| 移动应用 | qwen-1.8b-chat | 超轻量 |

#### **2. 使用流式输出**

```python
# 优点：
# 1. 用户感受到立即反馈
# 2. 可以提前获取部分结果
# 3. 改进用户体验

stream = client.chat.completions.create(
    model="qwen-plus",
    messages=messages,
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

#### **3. 控制文本长度**

```python
# 使用max_tokens限制输出长度
response = client.chat.completions.create(
    model="qwen-plus",
    messages=messages,
    max_tokens=500  # 限制输出为500 tokens
)
```

#### **4. 并发请求管理**

```python
import asyncio
from openai import AsyncOpenAI

async_client = AsyncOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

async def make_request(prompt, task_id):
    """异步发送单个请求"""
    try:
        response = await async_client.chat.completions.create(
            model="qwen-plus",
            messages=[{"role": "user", "content": prompt}],
            timeout=30
        )
        return task_id, response.choices[0].message.content
    except Exception as e:
        return task_id, f"错误: {str(e)}"

async def batch_requests(prompts):
    """并发处理多个请求"""
    tasks = [
        make_request(prompt, i)
        for i, prompt in enumerate(prompts)
    ]
    results = await asyncio.gather(*tasks)
    return results

# 使用示例
prompts = [
    "简述Python的特点",
    "什么是机器学习",
    "解释什么是REST API"
]

results = asyncio.run(batch_requests(prompts))
for task_id, result in results:
    print(f"任务{task_id}: {result}\n")
```

### 4.3 成本控制建议

#### **1. Token消耗监控**

```python
def estimate_tokens(text):
    """粗略估计Token数（1个中文约1.5 tokens，1个英文单词约1.3 tokens）"""
    chinese_count = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    english_words = len([w for w in text.split() if w.isalpha()])
    
    tokens = chinese_count * 1.5 + english_words * 1.3
    return int(tokens)

# 使用示例
text = "你好，这是一个测试句子。This is a test."
print(f"预估Token数：{estimate_tokens(text)}")
```

#### **2. 成本优化策略**

```python
def optimize_cost():
    """成本优化的最佳实践"""
    
    # 策略1：选择价格低的模型
    # qwen-flash < qwen-plus < qwen-max
    
    # 策略2：减少不必要的上下文
    # 只保留最近的N轮对话（例如最近5轮）
    def trim_messages(messages, max_rounds=5):
        # 保留system消息和最近max_rounds轮对话
        if len(messages) > max_rounds * 2 + 1:
            messages = [messages[0]] + messages[-(max_rounds*2):]
        return messages
    
    # 策略3：使用缓存
    messages_cache = {}
    
    # 策略4：批量处理
    # 合并多个小请求为一个大请求
    
    # 策略5：监控Token使用
    def track_cost(response, model="qwen-plus"):
        # qwen-plus: 输入0.5元/百万tokens, 输出1.5元/百万tokens
        input_cost = response.usage.prompt_tokens * 0.5 / 1000000
        output_cost = response.usage.completion_tokens * 1.5 / 1000000
        total_cost = input_cost + output_cost
        return total_cost
```

#### **3. 定价参考（2025年）**

```
通义千问 API 定价参考：
├─ qwen-max (最强)
│  ├─ 输入：¥0.002/1K tokens
│  └─ 输出：¥0.006/1K tokens
├─ qwen-plus (推荐)
│  ├─ 输入：¥0.0005/1K tokens
│  └─ 输出：¥0.0015/1K tokens
├─ qwen-flash (轻量)
│  ├─ 输入：¥0.00008/1K tokens
│  └─ 输出：¥0.0002/1K tokens
├─ qwen-turbo
│  ├─ 输入：¥0.0002/1K tokens
│  └─ 输出：¥0.0006/1K tokens
└─ qwen-coder-plus (编程)
   ├─ 输入：¥0.001/1K tokens
   └─ 输出：¥0.003/1K tokens

特殊模型：
├─ qwen-vl-plus (视觉): ¥0.02-0.1/张
├─ qwen-math (数学): ¥0.001/1K tokens
└─ qwq (推理): ¥0.002/1K tokens

注：具体价格以官方为准
```

### 4.4 最佳实践总结

#### **安全性**

```python
# 1. 不要在代码中硬编码API Key
# ❌ api_key = "sk-xxxxxx"

# ✅ 使用环境变量
import os
api_key = os.getenv("DASHSCOPE_API_KEY")

# 2. 验证用户输入
def validate_input(user_input, max_length=10000):
    """验证用户输入"""
    if not user_input or len(user_input) > max_length:
        raise ValueError("输入过长或为空")
    return user_input.strip()

# 3. 不要传递敏感信息
# ❌ 包含个人隐私的数据
# ✅ 脱敏或匿名化处理
```

#### **可靠性**

```python
# 1. 添加日志记录
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 2. 实现重试机制
import time
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def call_api(messages):
    return client.chat.completions.create(
        model="qwen-plus",
        messages=messages
    )

# 3. 超时控制
response = client.chat.completions.create(
    model="qwen-plus",
    messages=messages,
    timeout=60  # 60秒超时
)
```

#### **用户体验**

```python
# 1. 提供实时反馈
print("正在处理您的请求...", end="", flush=True)

# 2. 优雅的错误提示
try:
    response = client.chat.completions.create(...)
except Exception as e:
    print(f"请求失败，请稍后重试。错误详情：{str(e)}")

# 3. 显示处理进度
for i, chunk in enumerate(stream):
    print(chunk.choices[0].delta.content or "", end="", flush=True)
    if i % 10 == 0:
        logger.info(f"已处理 {i} 个chunks")
```

---

## 五、常见问题解答

### Q1: 如何选择合适的模型？

**A:** 根据以下维度选择：
- **性能需求**：简单问答用flash，复杂任务用plus/max
- **成本限制**：预算有限用flash，追求质量用plus/max
- **延迟要求**：需要实时用flash，可接受延迟用max
- **特殊需求**：代码用coder，数学用math，视觉用vl

### Q2: 为什么API调用失败？

**A:** 常见原因：
1. **401错误**：API Key无效或过期
2. **429错误**：触发限流，建议实施重试机制
3. **500错误**：服务器错误，稍后重试
4. **超时**：网络问题或请求过大，减少max_tokens

### Q3: 如何降低成本？

**A:** 主要方案：
1. 使用qwen-flash替代qwen-plus
2. 减少不必要的历史消息
3. 使用缓存避免重复请求
4. 优化提示词长度
5. 监控Token消耗

### Q4: 流式输出和非流式的区别？

**A:**
- **流式**：实时返回，用户体验好，适合UI展示
- **非流式**：一次返回完整结果，便于处理统计数据

### Q5: Function Calling会额外收费吗？

**A:** 不会单独收费，但工具描述会计入Token成本，建议精简描述。

---

## 六、快速参考

### 环境变量设置

```bash
export DASHSCOPE_API_KEY="sk-xxxxx"
export QWEN_MODEL="qwen-plus"
```

### 常用命令

```bash
# 安装SDK
pip install openai

# 验证API Key
python -c "from openai import OpenAI; print('OpenAI SDK安装成功')"
```

### 官方资源链接

- **百炼平台**：https://bailian.console.aliyun.com
- **官方文档**：https://help.aliyun.com/zh/model-studio
- **API参考**：https://help.aliyun.com/zh/model-studio/use-qwen-by-calling-api
- **GitHub**：https://github.com/QwenLM

---

## 七、总结

Qwen API是一套强大而灵活的大模型接口系统：

✅ **优势：**
- 兼容OpenAI协议，迁移成本低
- 模型丰富，支持多种专业场景
- 价格有竞争力，特别是轻量模型
- 支持Function Calling等高级功能
- 文档完善，社区活跃

📌 **关键点：**
- 选择合适的模型很重要
- 优化提示词能提升效果
- 实施重试机制提升可靠性
- 监控成本避免超出预算

🚀 **建议行动：**
1. 注册百炼平台获取API Key
2. 从qwen-plus开始体验
3. 根据场景优化提示词
4. 监控使用情况和成本

