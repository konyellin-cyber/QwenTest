"""
QWen API 调用完整示例集合

包含以下示例：
1. 基本对话
2. 流式对话
3. 函数调用
4. 错误处理和重试
5. 多轮对话
6. 并发调用
"""

import os
import json
import time
from typing import Optional, List, Dict
from dotenv import load_dotenv

# 导入OpenAI SDK（兼容QWen API）
try:
    from openai import OpenAI, RateLimitError, APIConnectionError
except ImportError:
    print("请先安装openai库: pip install openai")
    exit(1)

# 加载环境变量
load_dotenv()

# 初始化客户端
API_KEY = os.getenv('DASHSCOPE_API_KEY')
if not API_KEY:
    raise ValueError("请设置DASHSCOPE_API_KEY环境变量")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://dashscope.aliyun.com/compatible-mode/v1"
)


# ============================================================================
# 示例1: 基本对话
# ============================================================================

def example_basic_chat():
    """最简单的文本生成示例"""
    print("\n" + "="*60)
    print("示例1: 基本对话")
    print("="*60)
    
    messages = [
        {"role": "user", "content": "用一句话介绍QWen大模型"}
    ]
    
    response = client.chat.completions.create(
        model="qwen-plus",
        messages=messages,
        temperature=0.7
    )
    
    print(f"问题: {messages[0]['content']}")
    print(f"\n回答: {response.choices[0].message.content}")
    print(f"Token使用: 输入{response.usage.input_tokens}, 输出{response.usage.output_tokens}")


# ============================================================================
# 示例2: 流式对话
# ============================================================================

def example_streaming_chat():
    """流式输出示例，实时显示生成的内容"""
    print("\n" + "="*60)
    print("示例2: 流式对话")
    print("="*60)
    
    messages = [
        {"role": "user", "content": "请写一个Python计算斐波那契数列的函数"}
    ]
    
    print(f"问题: {messages[0]['content']}\n")
    print("回答: ", end="", flush=True)
    
    token_count = 0
    stream = client.chat.completions.create(
        model="qwen-plus",
        messages=messages,
        stream=True
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            token_count += len(content)
    
    print(f"\n\n生成内容约{token_count}个字符")


# ============================================================================
# 示例3: 函数调用 (Function Calling)
# ============================================================================

def example_function_calling():
    """演示如何使用Function Calling与外部工具集成"""
    print("\n" + "="*60)
    print("示例3: 函数调用 (Function Calling)")
    print("="*60)
    
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
                            "description": "温度单位"
                        }
                    },
                    "required": ["city"]
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
                            "description": "数学表达式，如'2+3*4'"
                        }
                    },
                    "required": ["expression"]
                }
            }
        }
    ]
    
    # 模拟工具执行
    def execute_tool(tool_name: str, tool_input: dict) -> str:
        if tool_name == "get_weather":
            return f"{tool_input['city']}的天气: 晴朗，温度25{tool_input.get('unit', 'celsius')[0].upper()}"
        elif tool_name == "calculate":
            try:
                result = eval(tool_input['expression'])
                return f"计算结果: {result}"
            except Exception as e:
                return f"计算错误: {str(e)}"
        return "未知工具"
    
    # 第一轮：让模型决定要调用的工具
    messages = [
        {"role": "user", "content": "北京今天天气怎么样？另外帮我算一下 123 + 456 的结果"}
    ]
    
    print(f"用户: {messages[0]['content']}\n")
    
    response = client.chat.completions.create(
        model="qwen-plus",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    # 检查是否有工具调用
    if response.choices[0].message.tool_calls:
        print("模型决定调用以下工具:")
        
        # 添加助手响应到消息历史
        messages.append({
            "role": "assistant",
            "content": response.choices[0].message.content or "",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in response.choices[0].message.tool_calls
            ]
        })
        
        # 执行工具调用
        for tool_call in response.choices[0].message.tool_calls:
            tool_name = tool_call.function.name
            tool_input = json.loads(tool_call.function.arguments)
            
            print(f"  - {tool_name}: {tool_input}")
            
            # 执行工具
            result = execute_tool(tool_name, tool_input)
            print(f"    结果: {result}")
            
            # 添加工具结果到消息
            messages.append({
                "role": "tool",
                "content": result,
                "tool_call_id": tool_call.id
            })
        
        # 第二轮：让模型生成最终回答
        print("\n模型最终回答:")
        final_response = client.chat.completions.create(
            model="qwen-plus",
            messages=messages,
            tools=tools
        )
        print(final_response.choices[0].message.content)
    else:
        print("模型直接回答:")
        print(response.choices[0].message.content)


# ============================================================================
# 示例4: 错误处理和重试
# ============================================================================

def example_error_handling():
    """展示如何处理API错误和实施重试机制"""
    print("\n" + "="*60)
    print("示例4: 错误处理和重试机制")
    print("="*60)
    
    def call_with_retry(
        messages: List[Dict],
        max_retries: int = 3,
        retry_delay: float = 1.0
    ) -> Optional[str]:
        """
        带重试机制的API调用
        
        参数:
            messages: 消息列表
            max_retries: 最大重试次数
            retry_delay: 初始重试延迟(秒)
        
        返回:
            响应文本或None
        """
        current_delay = retry_delay
        last_error = None
        
        for attempt in range(max_retries):
            try:
                print(f"[尝试 {attempt + 1}/{max_retries}] 发送请求...")
                
                response = client.chat.completions.create(
                    model="qwen-plus",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1024
                )
                
                print("✓ 请求成功")
                return response.choices[0].message.content
                
            except RateLimitError as e:
                last_error = e
                print(f"⚠ 触发限流错误")
                
                if attempt < max_retries - 1:
                    print(f"  等待 {current_delay:.1f} 秒后重试...")
                    time.sleep(current_delay)
                    current_delay *= 2
                else:
                    print(f"✗ 已达最大重试次数")
            
            except APIConnectionError as e:
                last_error = e
                print(f"⚠ 网络连接错误")
                
                if attempt < max_retries - 1:
                    print(f"  等待 {current_delay:.1f} 秒后重试...")
                    time.sleep(current_delay)
                    current_delay *= 2
            
            except Exception as e:
                print(f"✗ 无法恢复的错误: {type(e).__name__}")
                raise
        
        raise last_error or Exception("重试失败")
    
    # 测试
    try:
        result = call_with_retry(
            messages=[
                {"role": "user", "content": "介绍一下Python编程语言"}
            ]
        )
        print(f"\n最终结果: {result[:100]}...")
    except Exception as e:
        print(f"\n最终失败: {str(e)}")


# ============================================================================
# 示例5: 多轮对话
# ============================================================================

def example_multi_turn_conversation():
    """演示多轮对话的完整流程"""
    print("\n" + "="*60)
    print("示例5: 多轮对话")
    print("="*60)
    
    # 初始化对话历史，包括系统提示
    messages = [
        {
            "role": "system",
            "content": "你是一个编程专家，擅长解答Python相关问题。回答要清晰、简洁、准确。"
        }
    ]
    
    # 多轮对话内容
    conversations = [
        "Python和Java有什么主要区别？",
        "那如何在Python中定义类？",
        "能给我一个实际的例子吗？"
    ]
    
    for user_input in conversations:
        print(f"\n用户: {user_input}")
        
        # 添加用户消息
        messages.append({"role": "user", "content": user_input})
        
        # 获取模型回答
        response = client.chat.completions.create(
            model="qwen-plus",
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )
        
        assistant_message = response.choices[0].message.content
        
        # 添加助手消息到历史
        messages.append({"role": "assistant", "content": assistant_message})
        
        print(f"助手: {assistant_message}")
        print(f"(Token使用: 输入{response.usage.input_tokens}, 输出{response.usage.output_tokens})")
    
    print(f"\n本次对话共使用 {len(messages)} 条消息")


# ============================================================================
# 示例6: 并发调用
# ============================================================================

def example_concurrent_calls():
    """演示如何并发调用API以提高效率"""
    print("\n" + "="*60)
    print("示例6: 并发调用")
    print("="*60)
    
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    prompts = [
        "介绍一下Python",
        "介绍一下JavaScript",
        "介绍一下Go语言",
        "介绍一下Rust语言"
    ]
    
    def process_prompt(prompt: str) -> Dict:
        """处理单个提示词"""
        try:
            response = client.chat.completions.create(
                model="qwen-turbo",  # 使用更便宜的模型
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100
            )
            return {
                "prompt": prompt,
                "status": "success",
                "response": response.choices[0].message.content[:100]
            }
        except Exception as e:
            return {
                "prompt": prompt,
                "status": "error",
                "error": str(e)
            }
    
    print(f"准备并发处理 {len(prompts)} 个提示词...\n")
    
    # 使用线程池并发处理
    results = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        # 提交所有任务
        futures = {executor.submit(process_prompt, p): p for p in prompts}
        
        # 处理完成的任务
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            
            if result["status"] == "success":
                print(f"✓ {result['prompt'][:20]}...")
                print(f"  {result['response']}\n")
            else:
                print(f"✗ {result['prompt'][:20]}... - 错误: {result['error']}\n")
    
    print(f"\n完成 {len(results)} 个请求")


# ============================================================================
# 示例7: 成本监控
# ============================================================================

class CostTracker:
    """用于追踪API调用成本"""
    
    def __init__(self):
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.calls_by_model = {}
        
        # 定价信息（¥/1K tokens）
        self.model_costs = {
            "qwen-turbo": {"input": 0.00008, "output": 0.00016},
            "qwen-plus": {"input": 0.0005, "output": 0.0015},
            "qwen-max": {"input": 0.002, "output": 0.006},
        }
    
    def track(self, model: str, input_tokens: int, output_tokens: int):
        """记录一次API调用"""
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        
        if model not in self.calls_by_model:
            self.calls_by_model[model] = {
                "input": 0,
                "output": 0,
                "calls": 0
            }
        
        self.calls_by_model[model]["input"] += input_tokens
        self.calls_by_model[model]["output"] += output_tokens
        self.calls_by_model[model]["calls"] += 1
    
    def get_total_cost(self, model: str) -> float:
        """计算特定模型的总成本"""
        costs = self.model_costs.get(model, {})
        
        calls_info = self.calls_by_model.get(model, {})
        input_cost = calls_info.get("input", 0) * costs.get("input", 0) / 1000
        output_cost = calls_info.get("output", 0) * costs.get("output", 0) / 1000
        
        return input_cost + output_cost
    
    def print_report(self):
        """打印成本报告"""
        print("\n" + "="*60)
        print("成本分析报告")
        print("="*60)
        
        total_cost = 0
        
        for model, calls_info in self.calls_by_model.items():
            cost = self.get_total_cost(model)
            total_cost += cost
            
            print(f"\n模型: {model}")
            print(f"  调用次数: {calls_info['calls']}")
            print(f"  输入tokens: {calls_info['input']:,}")
            print(f"  输出tokens: {calls_info['output']:,}")
            print(f"  预估成本: ¥{cost:.6f}")
        
        print(f"\n{'─'*60}")
        print(f"总计成本: ¥{total_cost:.6f}")
        print(f"平均单价: ¥{total_cost / max(1, sum(info['calls'] for info in self.calls_by_model.values())):.6f}/调用")


def example_cost_tracking():
    """演示成本追踪"""
    print("\n" + "="*60)
    print("示例7: 成本监控")
    print("="*60)
    
    tracker = CostTracker()
    
    # 进行一些API调用并追踪成本
    test_queries = [
        ("qwen-turbo", "什么是Python？"),
        ("qwen-plus", "解释一下深度学习的基本概念"),
        ("qwen-turbo", "Git是什么？"),
    ]
    
    for model, query in test_queries:
        try:
            print(f"\n调用 {model}...")
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": query}],
                max_tokens=200
            )
            
            # 追踪成本
            tracker.track(
                model,
                response.usage.input_tokens,
                response.usage.output_tokens
            )
            
            print(f"✓ 成功 (输入:{response.usage.input_tokens} 输出:{response.usage.output_tokens})")
        except Exception as e:
            print(f"✗ 失败: {str(e)}")
    
    # 打印报告
    tracker.print_report()


# ============================================================================
# 主函数
# ============================================================================

def main():
    """运行所有示例"""
    print("\n" + "="*60)
    print("QWen API Python 示例集合")
    print("="*60)
    
    examples = [
        ("1", "基本对话", example_basic_chat),
        ("2", "流式对话", example_streaming_chat),
        ("3", "函数调用", example_function_calling),
        ("4", "错误处理", example_error_handling),
        ("5", "多轮对话", example_multi_turn_conversation),
        ("6", "并发调用", example_concurrent_calls),
        ("7", "成本监控", example_cost_tracking),
    ]
    
    print("\n请选择要运行的示例:")
    for num, name, _ in examples:
        print(f"  {num}. {name}")
    print("  8. 运行全部示例")
    print("  0. 退出")
    
    choice = input("\n请输入选项 (0-8): ").strip()
    
    if choice == "0":
        print("退出程序")
        return
    elif choice == "8":
        for _, _, example_func in examples:
            try:
                example_func()
                print("\n" + "─"*60)
            except Exception as e:
                print(f"\n✗ 示例失败: {str(e)}")
                print("─"*60)
    else:
        for num, _, example_func in examples:
            if choice == num:
                try:
                    example_func()
                except Exception as e:
                    print(f"\n✗ 示例失败: {str(e)}")
                return
        
        print("无效的选项")


if __name__ == "__main__":
    main()
