# QWen 大模型 API 完整调研指南

## 目录
1. [官方API接口文档](#官方api接口文档)
2. [主要接口类型](#主要接口类型)
3. [Python调用示例](#python调用示例)
4. [最佳实践和建议](#最佳实践和建议)
5. [常见问题解决](#常见问题解决)

---

## 官方API接口文档

### 1.1 基础信息

**官方网址**: https://dashscope.aliyun.com/

Qwen是由阿里巴巴集团推出的大型语言模型，提供通过DashScope平台的API服务。

### 1.2 API调用方式

Qwen支持两种主流API调用方式：

#### 方式一：OpenAI兼容接口（推荐用于快速迁移）
```
Base URL: https://dashscope.aliyun.com/compatible-mode/v1
```

优点：
- 与OpenAI API兼容
- 可直接使用OpenAI SDK
- 迁移成本低

#### 方式二：DashScope原生接口
```
Base URL: https://dashscope.aliyun.com/api/v1
```

优点：
- 更多高级功能支持
- 更详细的响应信息
- 更灵活的配置选项

### 1.3 鉴权方式

**API Key获取步骤**：
1. 访问 https://dashscope.aliyun.com/
2. 登录阿里云账户
3. 创建API Key
4. 复制保存到环境变量：`DASHSCOPE_API_KEY`

**鉴权头信息**：
```
Authorization: Bearer YOUR_API_KEY
```

### 1.4 支持的模型列表

#### 📱 通用对话模型（推荐）
| 模型名称 | 特点 | 用途 | 输入价格(¥/1K) | 输出价格(¥/1K) |
|---------|------|------|---------------|---------------|
| qwen-turbo | 快速、经济 | 通用对话、简单任务 | **0.0003** | **0.0006** |
| qwen-plus | 平衡性强 | **推荐用于大多数场景** | **0.0008** | **0.002** |
| qwen-max | 性能最强 | 复杂推理、专业任务 | **0.02** | **0.06** |
| qwen-max-latest | 最新版本 | 最新功能支持 | 0.02 | 0.06 |

#### 🚀 超大规模模型
| 模型名称 | 参数量 | 特点 |
|---------|-------|------|
| qwen-ultra | 可变参数 | 性能最强，成本最高 |
| qwen-long | 可变参数 | 支持超长上下文(100K tokens) |

#### 💻 代码和编程模型
| 模型名称 | 特点 | 用途 |
|---------|------|------|
| qwen-coder | 代码优化 | 代码生成、调试、分析 |
| qwen-math | 数学优化 | 数学问题求解 |

#### 🎨 多模态模型
| 模型名称 | 支持类型 | 用途 |
|---------|--------|------|
| qwen-vl-plus | 文本+图像 | 图像理解、OCR |
| qwen-vl-max | 文本+高清图像 | 高精度图像分析 |
| qwen-audio | 文本+语音 | 语音识别、转录 |

### 1.5 地域端点

```
全球地域：https://dashscope.aliyun.com/api/v1
新加坡：   https://dashscope-sg.aliyuncs.com/api/v1
日本：     https://dashscope-jp.aliyuncs.com/api/v1
```

### 1.6 请求/响应格式

#### 请求格式示例
```json
{
  "model": "qwen-plus",
  "messages": [
    {
      "role": "user",
      "content": "你是一个有帮助的助手。请回答问题。"
    }
  ],
  "temperature": 0.7,
  "top_p": 0.8,
  "max_tokens": 2048
}
```

#### 响应格式示例
```json
{
  "status_code": 200,
  "request_id": "uuid-string",
  "code": null,
  "message": null,
  "output": {
    "choices": [
      {
        "finish_reason": "stop",
        "message": {
          "role": "assistant",
          "content": "回复内容"
        }
      }
    ],
    "usage": {
      "input_tokens": 10,
      "output_tokens": 50
    }
  }
}
```

---

## 主要接口类型

### 2.1 文本生成/对话接口

**端点**: `POST /v1/services/aigc/text-generation/generation`

**参数说明**:
- `model`: 模型名称
- `messages`: 对话历史，包含role和content
- `temperature`: 0-2，控制随机性（默认0.7）
- `top_p`: 0-1，核采样参数（默认0.8）
- `max_tokens`: 最大输出token数
- `stream`: 是否使用流式输出

**关键参数详解**：

| 参数 | 范围 | 默认值 | 说明 |
|-----|------|-------|------|
| temperature | 0-2 | 0.7 | 值越小输出越确定性，值越大越随机 |
| top_p | 0-1 | 0.8 | 核采样，选择累积概率最高的token |
| top_k | 1-50 | 无 | 选择概率最高的K个token |
| max_tokens | 1-最大值 | 无限制 | 限制输出长度，节省成本 |
| repetition_penalty | 0-2 | 1.0 | 控制重复内容，>1减少重复 |

### 2.2 流式响应接口

**特点**：
- 实时返回数据，无需等待完整响应
- 改善用户体验
- 适合长文本生成

**流式响应格式**：
```
data: {"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":"第一个字"}}]}}

data: {"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":"第二个字"}}]}}

data: [DONE]
```

### 2.3 函数调用接口 (Function Calling)

**用途**：
- 与外部工具集成
- 构建智能Agent
- 结构化输出

**定义函数schema示例**：
```json
{
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "获取城市天气",
    "parameters": {
      "type": "object",
      "properties": {
        "city": {
          "type": "string",
          "description": "城市名称"
        },
        "unit": {
          "type": "string",
          "enum": ["celsius", "fahrenheit"],
          "description": "温度单位"
        }
      },
      "required": ["city"]
    }
  }
}
```

**调用流程**：
1. 发送包含tools定义的请求
2. 模型返回应该调用的工具和参数
3. 客户端执行工具
4. 将结果作为新消息发回模型
5. 模型生成最终响应

### 2.4 高级功能

#### 2.4.1 联网搜索
```python
{
    "model": "qwen-plus",
    "messages": [...],
    "tools": [
        {
            "type": "web_search",
            "web_search": {}
        }
    ]
}
```

#### 2.4.2 RAG (检索增强生成)
```python
{
    "model": "qwen-plus",
    "messages": [...],
    "documents": [
        {
            "title": "文档标题",
            "content": "文档内容"
        }
    ]
}
```

#### 2.4.3 长上下文处理
```python
# 使用qwen-long模型支持100K token上下文
{
    "model": "qwen-long",
    "messages": [...],
    "max_tokens": 4096
}
```

---

## Python调用示例

### 3.1 环境准备

#### 安装SDK
```bash
# 安装官方SDK
pip install dashscope

# 或使用OpenAI兼容SDK
pip install openai
```

#### 设置API Key
```bash
export DASHSCOPE_API_KEY=your-api-key-here
```

或在Python代码中：
```python
import os
os.environ['DASHSCOPE_API_KEY'] = 'your-api-key-here'
```

### 3.2 基本调用示例

#### 使用OpenAI SDK（推荐快速开始）
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
print(f"总tokens: {response.usage.total_tokens}")
```

#### 使用官方SDK
```python
from dashscope import Generation
import dashscope

dashscope.api_key = 'your-api-key'

response = Generation.call(
    model='qwen-plus',
    messages=[
        {'role': 'user', 'content': '你好，请介绍一下自己'}
    ]
)

if response.status_code == 200:
    print(response.output.choices[0].message.content)
    print(f"输入tokens: {response.usage.input_tokens}")
    print(f"输出tokens: {response.usage.output_tokens}")
else:
    print(f"Error: {response.code} - {response.message}")
```

### 3.3 流式调用示例

#### OpenAI SDK流式调用
```python
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="https://dashscope.aliyun.com/compatible-mode/v1"
)

stream = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "user", "content": "请写一首关于春天的诗"}
    ],
    stream=True
)

# 实时输出
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end='', flush=True)
print()
```

#### 官方SDK流式调用
```python
from dashscope import Generation
import dashscope

dashscope.api_key = 'your-api-key'

responses = Generation.call(
    model='qwen-plus',
    messages=[
        {'role': 'user', 'content': '请写一首关于春天的诗'}
    ],
    stream=True,
    result_format='message'
)

total_tokens = 0
for response in responses:
    if response.status_code == 200:
        for choice in response.output.choices:
            print(choice.message.content, end='', flush=True)
        total_tokens += response.usage.output_tokens
    else:
        print(f"Error: {response.code} - {response.message}")

print(f"\n总输出tokens: {total_tokens}")
```

### 3.4 函数调用完整示例

```python
from openai import OpenAI
import json

client = OpenAI(
    api_key="your-api-key",
    base_url="https://dashscope.aliyun.com/compatible-mode/v1"
)

# 定义工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "温度单位",
                        "default": "celsius"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "获取指定城市的当前时间",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

# 模拟工具执行
def execute_tool(tool_name, tool_input):
    if tool_name == "get_weather":
        return f"{tool_input['city']}的天气: 晴朗,温度 {20} {tool_input.get('unit', 'celsius')}"
    elif tool_name == "get_time":
        return f"{tool_input['city']}的当前时间: 2024-01-20 15:30:00"
    return "未知工具"

# 第一轮对话
messages = [
    {"role": "user", "content": "北京和上海今天天气怎么样？"}
]

response = client.chat.completions.create(
    model="qwen-plus",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

print(f"模型响应: {response.choices[0].message.content}")

# 处理函数调用
if response.choices[0].message.tool_calls:
    # 添加助手消息到历史
    messages.append({"role": "assistant", "content": response.choices[0].message.content})
    
    # 执行所有工具调用
    tool_results = []
    for tool_call in response.choices[0].message.tool_calls:
        tool_name = tool_call.function.name
        tool_input = json.loads(tool_call.function.arguments)
        
        print(f"执行工具: {tool_name}，参数: {tool_input}")
        result = execute_tool(tool_name, tool_input)
        print(f"工具结果: {result}")
        
        tool_results.append({
            "role": "tool",
            "content": result,
            "tool_call_id": tool_call.id,
            "name": tool_name
        })
    
    # 添加工具结果
    messages.extend(tool_results)
    
    # 第二轮对话 - 让模型生成最终响应
    final_response = client.chat.completions.create(
        model="qwen-plus",
        messages=messages,
        tools=tools
    )
    
    print(f"最终答案: {final_response.choices[0].message.content}")
```

### 3.5 错误处理和重试机制

```python
from openai import OpenAI
import time
from typing import Optional

client = OpenAI(
    api_key="your-api-key",
    base_url="https://dashscope.aliyun.com/compatible-mode/v1"
)

def call_with_retry(
    messages: list,
    max_retries: int = 3,
    retry_delay: float = 1.0,
    backoff_multiplier: float = 2.0
) -> Optional[str]:
    """
    带重试机制的API调用
    
    参数:
        messages: 消息列表
        max_retries: 最大重试次数
        retry_delay: 初始重试延迟(秒)
        backoff_multiplier: 指数退避倍数
    
    返回:
        响应文本或None
    """
    current_delay = retry_delay
    last_error = None
    
    for attempt in range(max_retries):
        try:
            print(f"尝试第 {attempt + 1}/{max_retries}...")
            
            response = client.chat.completions.create(
                model="qwen-plus",
                messages=messages,
                temperature=0.7,
                max_tokens=2048
            )
            
            print("✓ 调用成功")
            return response.choices[0].message.content
            
        except Exception as e:
            last_error = e
            error_name = type(e).__name__
            
            # 判断是否应该重试
            if "RateLimitError" in str(error_name):
                print(f"⚠ 触发限流 ({error_name})")
            elif "Timeout" in str(error_name):
                print(f"⚠ 请求超时 ({error_name})")
            elif "ServiceUnavailable" in str(error_name):
                print(f"⚠ 服务不可用 ({error_name})")
            else:
                # 其他错误可能不可恢复
                print(f"✗ 无法恢复的错误: {error_name} - {str(e)}")
                raise
            
            if attempt < max_retries - 1:
                print(f"等待 {current_delay:.1f} 秒后重试...")
                time.sleep(current_delay)
                current_delay *= backoff_multiplier
            else:
                print(f"✗ 已达最大重试次数")
    
    raise last_error or Exception("未知错误")

# 使用示例
try:
    result = call_with_retry(
        messages=[
            {"role": "user", "content": "写一个Python函数计算fibonacci数列"}
        ]
    )
    print(f"结果:\n{result}")
except Exception as e:
    print(f"最终失败: {e}")
```

### 3.6 多轮对话示例

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="https://dashscope.aliyun.com/compatible-mode/v1"
)

# 初始化对话历史
messages = [
    {
        "role": "system",
        "content": "你是一个擅长Python编程的助手，请用简洁清晰的方式回答问题。"
    }
]

def chat(user_input: str) -> str:
    """添加用户消息并获取响应"""
    messages.append({"role": "user", "content": user_input})
    
    response = client.chat.completions.create(
        model="qwen-plus",
        messages=messages,
        temperature=0.7
    )
    
    assistant_message = response.choices[0].message.content
    messages.append({"role": "assistant", "content": assistant_message})
    
    return assistant_message

# 多轮对话示例
print("=== Python编程助手 ===\n")

response1 = chat("Python中的列表和元组有什么区别？")
print(f"Q: Python中的列表和元组有什么区别？\nA: {response1}\n")

response2 = chat("那如何创建一个元组呢？")
print(f"Q: 那如何创建一个元组呢？\nA: {response2}\n")

response3 = chat("给我一个实际应用例子")
print(f"Q: 给我一个实际应用例子\nA: {response3}\n")

print(f"本次对话使用了 {len(messages)} 条消息")
```

---

## 最佳实践和建议

### 4.1 提示词优化（Prompt Engineering）

#### 原则一：清晰定义角色
```python
# ❌ 不好的例子
"帮我生成一些代码"

# ✅ 好的例子
system_prompt = """
你是一个资深Python开发工程师，具有10年的项目开发经验。
你擅长编写高效、可维护的代码。
当用户要求代码时，请确保：
1. 代码有详细注释
2. 遵循PEP8规范
3. 包含错误处理
4. 提供使用示例
"""
```

#### 原则二：具体化需求
```python
# ❌ 不好的例子
"生成一个排序函数"

# ✅ 好的例子
"请生成一个Python函数，用快速排序算法对整数列表进行降序排列。
要求：
- 函数名为quick_sort_desc
- 传入参数为list，返回排序后的list
- 添加类型注解
- 包含docstring说明
- 提供3个测试用例"
```

#### 原则三：提供上下文
```python
# ❌ 不好的例子
"如何优化这个函数"

# ✅ 好的例子
"""
我有以下函数，用于处理100万条用户数据：

```python
def process_users(users):
    result = []
    for user in users:
        if user['age'] > 18:
            user['category'] = 'adult'
        else:
            user['category'] = 'minor'
        result.append(user)
    return result
```

这个函数在处理大数据时比较慢。请从以下几个方面建议优化方案：
1. 算法优化
2. 内存使用优化
3. 并发处理优化
"""
```

#### 原则四：结构化输出
```python
# ❌ 不好的例子
"分析这个错误"

# ✅ 好的例子
"""
请分析以下错误，并按以下格式返回：

错误原因：[简明扼要的原因]
影响范围：[可能受影响的其他代码]
解决方案：
1. [方案1及其优缺点]
2. [方案2及其优缺点]
推荐方案：[最好的解决方案，及其步骤]

错误信息：
TypeError: 'NoneType' object is not subscriptable
"""
```

### 4.2 性能优化技巧

#### 技巧一：选择合适的模型
```python
# 不同场景选择不同模型
use_cases = {
    "简单问答": "qwen-turbo",          # 最快最便宜
    "通用任务": "qwen-plus",            # 推荐选择
    "复杂推理": "qwen-max",             # 性能最强
    "长文本处理": "qwen-long",          # 100K token上下文
    "代码生成": "qwen-coder",           # 优化编程
    "数学问题": "qwen-math"             # 优化数学
}
```

#### 技巧二：使用流式输出
```python
# 流式输出可以更早展示结果，改善用户体验
response = client.chat.completions.create(
    model="qwen-plus",
    messages=messages,
    stream=True  # 启用流式输出
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end='', flush=True)
```

#### 技巧三：并发请求
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

def make_request(prompt):
    response = client.chat.completions.create(
        model="qwen-plus",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# 并发处理多个请求
prompts = ["问题1", "问题2", "问题3"]
with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(make_request, prompts))
```

#### 技巧四：限制输出长度
```python
# 使用max_tokens限制输出，减少处理时间和成本
response = client.chat.completions.create(
    model="qwen-plus",
    messages=messages,
    max_tokens=500  # 限制输出为500个token
)
```

#### 技巧五：缓存热查询
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_cached_response(prompt):
    response = client.chat.completions.create(
        model="qwen-plus",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# 相同提示词会直接返回缓存
result1 = get_cached_response("Python是什么？")
result2 = get_cached_response("Python是什么？")  # 返回缓存，无需调用API
```

### 4.3 成本控制方案

#### 成本对比表

根据阿里云 2024 年 12 月 31 日最新降价（官方来源：https://www.ithome.com/0/821/422.htm）

```
模型          | 输入价格    | 输出价格    | 上下文长度   | 推荐用途
-----------  | ---------- | ---------- | ---------- | ----------------
qwen-turbo   | ¥0.0003    | ¥0.0006    | 100万      | 简单任务、高频调用
qwen-plus    | ¥0.0008    | ¥0.002     | 131K       | 通用任务（推荐）
qwen-max     | ¥0.02      | ¥0.06      | 32K        | 复杂任务、高精度
qwen-long    | ¥0.0005    | ¥0.002     | 1000万     | 长文档处理
```

**重要说明**：
- 上述价格已于 2024 年 12 月 31 日生效
- qwen-turbo 已从原价 ¥0.002 降至 ¥0.0003（输入价格），降幅 85%
- qwen-plus 已从原价 ¥0.004 降至 ¥0.0008（输入价格），降幅 80%
- qwen-max 已从原价 ¥0.04 降至 ¥0.02（输入价格），降幅 50%

#### 成本优化建议

1. **使用更便宜的模型**
   ```python
   # 优化：用qwen-turbo替代qwen-plus，成本可节省96.25%
   # qwen-turbo 输入价格：¥0.0003/1K
   # qwen-plus 输入价格：¥0.0008/1K
   # 成本比例：0.0003 / 0.0008 = 37.5% （节省62.5%）
   # 最简单的任务优先使用 qwen-turbo
   model = "qwen-turbo"  # 从 qwen-plus 改为 qwen-turbo
   ```

2. **限制输出长度**
   ```python
   # 对于摘要、分类等任务，限制max_tokens
   response = client.chat.completions.create(
       model="qwen-plus",
       messages=messages,
       max_tokens=200  # 限制输出
   )
   ```

3. **批量处理**
   ```python
   # 批量发送请求，减少单次调用数量
   def batch_process(items, batch_size=10):
       for i in range(0, len(items), batch_size):
           batch = items[i:i+batch_size]
           # 将多个项目合并到一个请求中
           combined_prompt = "\n".join(batch)
           # 单次API调用处理多个项目
   ```

4. **缓存策略**
   ```python
   # 构建本地缓存，避免重复调用
   import json
   
   cache_file = "response_cache.json"
   
   def get_response_with_cache(prompt):
       # 检查缓存
       try:
           with open(cache_file, 'r') as f:
               cache = json.load(f)
               if prompt in cache:
                   return cache[prompt]
       except:
           cache = {}
       
       # 调用API
       response = client.chat.completions.create(
           model="qwen-plus",
           messages=[{"role": "user", "content": prompt}]
       )
       result = response.choices[0].message.content
       
       # 保存到缓存
       cache[prompt] = result
       with open(cache_file, 'w') as f:
           json.dump(cache, f)
       
       return result
   ```

5. **成本监控**
   ```python
   class CostTracker:
       def __init__(self):
           self.total_input_tokens = 0
           self.total_output_tokens = 0
           self.model_costs = {
               "qwen-turbo": {"input": 0.00008, "output": 0.00016},
               "qwen-plus": {"input": 0.0005, "output": 0.0015},
               "qwen-max": {"input": 0.002, "output": 0.006},
           }
       
       def track(self, model, input_tokens, output_tokens):
           self.total_input_tokens += input_tokens
           self.total_output_tokens += output_tokens
       
       def get_cost(self, model):
           costs = self.model_costs.get(model, {})
           input_cost = self.total_input_tokens * costs.get("input", 0) / 1000
           output_cost = self.total_output_tokens * costs.get("output", 0) / 1000
           return input_cost + output_cost
       
       def print_report(self, model):
           cost = self.get_cost(model)
           print(f"模型: {model}")
           print(f"输入tokens: {self.total_input_tokens}")
           print(f"输出tokens: {self.total_output_tokens}")
           print(f"预估成本: ¥{cost:.4f}")
   
   # 使用
   tracker = CostTracker()
   # ... 进行API调用 ...
   # tracker.track("qwen-plus", input_tokens, output_tokens)
   # tracker.print_report("qwen-plus")
   ```

### 4.4 安全性和可靠性建议

#### 安全建议
```python
import os
from dotenv import load_dotenv

# 1. 不要在代码中硬编码API Key
# ❌ 不好的做法
api_key = "sk-xxx-xxx-xxx"

# ✅ 好的做法：使用环境变量
load_dotenv()
api_key = os.getenv("DASHSCOPE_API_KEY")

# 2. 对用户输入进行验证和清理
def validate_input(user_input):
    # 检查长度
    if len(user_input) > 10000:
        raise ValueError("输入过长")
    
    # 检查恶意内容
    forbidden_keywords = ["DROP", "DELETE", "EXEC"]
    if any(keyword in user_input.upper() for keyword in forbidden_keywords):
        raise ValueError("输入包含禁止内容")
    
    return user_input.strip()

# 3. 使用请求超时
response = client.chat.completions.create(
    model="qwen-plus",
    messages=messages,
    timeout=30  # 30秒超时
)

# 4. 记录所有API调用日志
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_api_call(messages, response):
    logger.info(f"API Call: {messages}")
    logger.info(f"Response: {response.choices[0].message.content[:100]}")
```

#### 可靠性建议
```python
# 1. 实施健康检查
def health_check():
    try:
        response = client.chat.completions.create(
            model="qwen-plus",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=1
        )
        return True
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return False

# 2. 实施熔断机制
from datetime import datetime, timedelta

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.last_failure_time = None
        self.is_open = False
    
    def call(self, func, *args, **kwargs):
        if self.is_open:
            if datetime.now() - self.last_failure_time > timedelta(seconds=self.timeout):
                self.is_open = False
                self.failure_count = 0
            else:
                raise Exception("Circuit breaker is open")
        
        try:
            result = func(*args, **kwargs)
            self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()
            if self.failure_count >= self.failure_threshold:
                self.is_open = True
            raise
```

### 4.5 用户体验优化

```python
# 1. 进度显示
import sys

def stream_response_with_progress(stream):
    token_count = 0
    for chunk in stream:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            print(content, end='', flush=True)
            token_count += len(content)
            sys.stdout.write(f" [{token_count} 字符]")
            sys.stdout.flush()

# 2. 格式化输出
def format_response(response_text):
    # 对长文本进行格式化
    import textwrap
    lines = response_text.split('\n')
    formatted = '\n'.join(
        textwrap.fill(line, width=80) for line in lines
    )
    return formatted

# 3. 错误提示改进
def friendly_error_message(error):
    error_map = {
        "RateLimitError": "请求过于频繁，请稍后再试",
        "TimeoutError": "请求超时，请检查网络连接",
        "AuthenticationError": "API Key无效，请检查配置",
        "ServiceUnavailableError": "服务暂时不可用，请稍后再试"
    }
    
    error_name = type(error).__name__
    return error_map.get(error_name, f"发生错误: {str(error)}")
```

---

## 常见问题解决

### 5.1 认证问题

**问题**: `AuthenticationError: Invalid API key`

**解决方案**:
```python
# 1. 检查API Key是否正确
import os
api_key = os.getenv('DASHSCOPE_API_KEY')
print(f"API Key: {api_key[:20]}...")  # 只显示前20个字符

# 2. 确保API Key有效期未过期
# 在DashScope控制台检查API Key状态

# 3. 尝试更新client
client = OpenAI(
    api_key=api_key,
    base_url="https://dashscope.aliyun.com/compatible-mode/v1"
)
```

### 5.2 限流问题

**问题**: `RateLimitError: Rate limit exceeded`

**解决方案**:
```python
import time
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def call_api_with_retry(messages):
    return client.chat.completions.create(
        model="qwen-plus",
        messages=messages
    )

# 或手动实现
def call_with_backoff(messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.chat.completions.create(
                model="qwen-plus",
                messages=messages
            )
        except RateLimitError:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"限流，等待 {wait_time} 秒...")
                time.sleep(wait_time)
            else:
                raise
```

### 5.3 超时问题

**问题**: `Timeout: Request timed out`

**解决方案**:
```python
# 1. 增加超时时间
client = OpenAI(
    api_key="your-api-key",
    base_url="https://dashscope.aliyun.com/compatible-mode/v1",
    timeout=60  # 增加到60秒
)

# 2. 减少max_tokens
response = client.chat.completions.create(
    model="qwen-plus",
    messages=messages,
    max_tokens=1024  # 从2048减少到1024
)

# 3. 使用流式输出
for chunk in client.chat.completions.create(
    model="qwen-plus",
    messages=messages,
    stream=True
):
    print(chunk.choices[0].delta.content or "", end="")
```

### 5.4 响应解析问题

**问题**: `JSON decode error`

**解决方案**:
```python
import json

def safe_parse_response(response_text):
    try:
        # 尝试直接解析
        return json.loads(response_text)
    except json.JSONDecodeError:
        # 尝试清理字符串
        cleaned = response_text.strip()
        if cleaned.startswith('```json'):
            cleaned = cleaned[7:-3]
        
        try:
            return json.loads(cleaned)
        except:
            # 返回原始文本
            return {"raw": response_text}

# 使用
response_text = response.choices[0].message.content
parsed = safe_parse_response(response_text)
```

### 5.5 模型错误

**问题**: `Model not found`

**解决方案**:
```python
# 检查可用的模型列表
available_models = [
    "qwen-turbo",
    "qwen-plus",
    "qwen-max",
    "qwen-max-latest",
    "qwen-long",
    "qwen-vl-plus",
    "qwen-vl-max"
]

# 使用时检查
model_name = "qwen-plus"
if model_name not in available_models:
    raise ValueError(f"模型 {model_name} 不可用")
```

---

## 总结

### 快速开始检查清单

- [ ] 已获取API Key并设置环境变量
- [ ] 已安装openai库：`pip install openai`
- [ ] 已测试基本连接
- [ ] 已了解不同模型的差异
- [ ] 已配置错误处理机制
- [ ] 已评估成本和性能需求

### 下一步建议

1. **本地开发**：使用qwen-plus模型进行开发
2. **性能优化**：根据实际情况选择合适的模型
3. **生产部署**：实施完整的错误处理和监控
4. **持续优化**：监控成本和性能指标

### 相关资源

- 官方文档: https://dashscope.aliyun.com/
- API参考: https://help.aliyun.com/zh/dashscope/
- Python SDK: https://github.com/aliyun/dashscope-python-sdk
- OpenAI兼容: https://dashscope.aliyun.com/compatible-mode/v1

---

**文档更新时间**: 2024年1月
**版本**: 1.0
