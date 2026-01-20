# QWen API 流程图 - PlantUML 格式

> 📌 **PlantUML格式说明**
> 
> PlantUML是一个开源项目，允许用户用简单直观的语言定义图表。
> GitHub不原生支持，但可以通过以下方式查看：
> 1. 使用PlantUML在线编辑器
> 2. 使用VS Code插件
> 3. 转换为SVG或PNG后提交

## 1. 完整调用流程（状态图）

```plantuml
@startuml
skinparam backgroundColor #FEFEFE
skinparam state {
    BackgroundColor #E1F5FE
    BorderColor #0277BD
    FontColor #01579B
}

[*] --> GetAPIKey: 1. 获取API Key
GetAPIKey --> InitClient: 2. 初始化客户端
InitClient --> BuildMessage: 3. 构建消息
BuildMessage --> SendRequest: 4. 发送请求
SendRequest --> Authenticate: 5. 服务器验证

Authenticate --> Success: ✅ 验证通过
Authenticate --> Failed: ❌ 验证失败

Failed --> ErrorResponse: 返回错误\n(401/429/500)
Success --> ProcessRequest: 6. 处理请求
ProcessRequest --> ReturnResponse: 7. 返回响应

ErrorResponse --> ErrorHandling: 8. 错误处理
ErrorHandling --> Retry: 9. 决策：重试?
Retry --> SendRequest: 是 → 重新发送
Retry --> EndWithError: 否 → 返回错误

ReturnResponse --> ParseResponse: 9. 解析响应
ParseResponse --> ReturnToUser: 10. 返回给用户
EndWithError --> [*]
ReturnToUser --> [*]

note right of Authenticate
    检查项：
    1. API Key有效性
    2. 账户配额
    3. 速率限制
end note
@enduml
```

---

## 2. 鉴权流程（活动图）

```plantuml
@startuml
skinparam activityFontSize 16
skinparam backgroundColor #FEFEFE

start
:获取API Key;
:┌─────────────────────┐
|  存储方式选择        |
├─────────────────────┤
| • 环境变量          |
| • .env文件          |
| • 直接传入          |
└─────────────────────┘;
:初始化OpenAI客户端;
:internal: 客户端保存API Key;
:发送请求;
:SDK自动添加鉴权头;
:Authorization: Bearer sk-xxx;
:发送POST到服务器;

split
    :1️⃣ 解析Authorization头;
split again
    :2️⃣ 查询API Key有效性;
split again
    :3️⃣ 检查账户配额;
split again
    :4️⃣ 检查速率限制;
end split

:综合验证结果;

if (所有验证通过?) then (是)
    :处理请求;
    :返回200 OK;
    :success: 鉴权成功;
else (否)
    if (问题是什么?) then (Key无效)
        :返回401错误;
    elseif (账户禁用) then (是)
        :返回403错误;
    else (请求过于频繁)
        :返回429错误;
    endif
endif

stop
@enduml
```

---

## 3. 错误处理决策树

```plantuml
@startuml
skinparam backgroundColor #FEFEFE
skinparam classBackgroundColor #E1F5FE
skinparam classBorderColor #0277BD

class ErrorHandling {
    错误处理策略
    --
    1. 判断状态码
    2. 决定是否重试
    3. 执行相应操作
}

class StatusCode400 {
    Bad Request
    --
    • 请求格式错误
    • JSON无效
    • 参数错误
    ❌ 不重试
    ✅ 修改代码
}

class StatusCode401 {
    Unauthorized
    --
    • API Key无效
    • Key过期
    • Key被删除
    ❌ 不重试
    ✅ 更新Key
}

class StatusCode429 {
    Too Many Requests
    --
    • 请求过于频繁
    • 并发超限
    • 配额用尽
    ✅ 重试（指数退避）
    ⏳ 等待 1s → 2s → 4s
}

class StatusCode500 {
    Internal Server Error
    --
    • 服务器故障
    • 数据库错误
    • 推理错误
    ✅ 重试（指数退避）
    ⏳ 等待 1s → 2s → 4s
}

ErrorHandling --> StatusCode400
ErrorHandling --> StatusCode401
ErrorHandling --> StatusCode429
ErrorHandling --> StatusCode500

note right of StatusCode400
    客户端错误
    需要修复代码
end note

note right of StatusCode401
    认证错误
    需要更新凭据
end note

note right of StatusCode429
    限流错误
    可以重试
end note

note right of StatusCode500
    服务端错误
    可以重试
end note
@enduml
```

---

## 4. 时序图：流式vs非流式

```plantuml
@startuml
skinparam backgroundColor #FEFEFE
skinparam sequenceActorBorderColor #0277BD
skinparam sequenceActorBackgroundColor #E1F5FE

== 传统调用 (stream=False) ==

Client -> SDK: 1. 调用 create()
SDK -> SDK: 2. 构建请求
SDK -> Network: 3. 发送请求
Network -> Server: 4. 传输
Server -> Server: 5. ⏳ 等待完整处理...
Server -> Server: 6. 生成完整响应
Server -> Network: 7. 返回JSON
Network -> SDK: 8. 接收完整数据
SDK -> SDK: 9. 解析JSON
SDK -> Client: 10. 返回Response

Client -> Client: 11. 提取内容\n12. 显示给用户

== 流式调用 (stream=True) ==

Client -> SDK: 1. 调用 create(stream=True)
SDK -> SDK: 2. 构建请求
SDK -> Network: 3. 发送请求
Network -> Server: 4. 传输
Server -> Server: 5. 建立连接
Server -> Network: 6. data: chunk1
Network -> SDK: 7. 接收chunk1
SDK -> Client: 8. 处理chunk1
Client -> Client: 9. 实时显示chunk1

Server -> Network: 10. data: chunk2
Network -> SDK: 11. 接收chunk2
SDK -> Client: 12. 处理chunk2
Client -> Client: 13. 实时显示chunk2

note over Server
    持续传输数据块
    客户端实时处理
end note

Server -> Network: ... data: [DONE]
Network -> SDK: 接收完成标记
SDK -> Client: 流式完成

Client -> Client: 用户看到完整内容
@enduml
```

---

## 5. 类图：API调用组件

```plantuml
@startuml
skinparam backgroundColor #FEFEFE
skinparam classBackgroundColor #E1F5FE
skinparam classBorderColor #0277BD

package "QWen API" {
    class OpenAIClient {
        - api_key: str
        - base_url: str
        - timeout: int
        --
        + create_completion()
        + create_chat_completion()
        + handle_response()
    }

    class Request {
        - model: str
        - messages: list
        - temperature: float
        - max_tokens: int
        - stream: bool
        --
        + to_json()
        + add_auth_header()
    }

    class Response {
        - status_code: int
        - data: dict
        - error: Exception
        --
        + parse()
        + get_content()
        + get_tokens()
    }

    class AuthHandler {
        - api_key: str
        --
        + verify_key()
        + create_bearer_token()
        + validate_response()
    }

    class ErrorHandler {
        - error_code: int
        - error_message: str
        --
        + should_retry()
        + get_wait_time()
        + handle_error()
    }

    OpenAIClient --> Request: 创建
    OpenAIClient --> Response: 接收
    OpenAIClient --> AuthHandler: 使用
    OpenAIClient --> ErrorHandler: 使用
    Request --> AuthHandler: 需要认证
    Response --> ErrorHandler: 检查错误
}

package "Models" {
    class Model {
        - name: str
        - input_price: float
        - output_price: float
        --
        + get_cost()
    }

    class QwenTurbo {
        - name: "qwen-turbo"
        - input_price: 0.0003
        - output_price: 0.0006
    }

    class QwenPlus {
        - name: "qwen-plus"
        - input_price: 0.0008
        - output_price: 0.002
    }

    class QwenMax {
        - name: "qwen-max"
        - input_price: 0.02
        - output_price: 0.06
    }

    Model <|-- QwenTurbo
    Model <|-- QwenPlus
    Model <|-- QwenMax
}

OpenAIClient --> Model: 选择

@enduml
```

---

## 6. 组件图：系统架构

```plantuml
@startuml
skinparam backgroundColor #FEFEFE
skinparam componentStyle uml2

package "客户端" {
    [Python应用]
    [OpenAI SDK]
}

package "传输层" {
    [HTTP/HTTPS]
    [TLS加密]
}

package "阿里云服务器" {
    [API网关]
    [鉴权服务]
    [限流服务]
    [路由引擎]
    [QWen推理引擎]
    [响应构建]
}

package "存储层" {
    [API Key数据库]
    [用户配额数据库]
    [请求日志]
}

[Python应用] --> [OpenAI SDK]: 调用API
[OpenAI SDK] --> [HTTP/HTTPS]: 发送请求
[HTTP/HTTPS] --> [TLS加密]: 加密传输
[TLS加密] --> [API网关]: 接收请求

[API网关] --> [鉴权服务]: 1. 验证
[鉴权服务] --> [API Key数据库]: 查询
[API Key数据库] --> [鉴权服务]: 返回
[鉴权服务] --> [限流服务]: 2. 检查限流

[限流服务] --> [用户配额数据库]: 查询
[用户配额数据库] --> [限流服务]: 返回
[限流服务] --> [路由引擎]: 3. 路由

[路由引擎] --> [QWen推理引擎]: 4. 执行推理
[QWen推理引擎] --> [响应构建]: 5. 构建响应
[响应构建] --> [请求日志]: 记录
[响应构建] --> [TLS加密]: 返回响应

[TLS加密] --> [HTTP/HTTPS]: 解密
[HTTP/HTTPS] --> [OpenAI SDK]: 接收
[OpenAI SDK] --> [Python应用]: 返回结果
@enduml
```

---

## 7. 对象图：请求示例

```plantuml
@startuml
skinparam backgroundColor #FEFEFE

object Request {
    model = "qwen-plus"
    messages = [
        {role: "user", content: "你好"}
    ]
    temperature = 0.7
    max_tokens = 1024
    stream = false
    timestamp = "2026-01-20T10:00:00Z"
}

object Headers {
    Authorization = "Bearer sk-xxxxxxxxxx"
    Content-Type = "application/json"
    User-Agent = "OpenAI/Python 1.0.0"
    Accept-Encoding = "gzip, deflate"
}

object Response {
    status_code = 200
    status_text = "OK"
    choices = [
        {
            finish_reason: "stop"
            message: {role: "assistant", content: "..."}
        }
    ]
    usage = {
        input_tokens: 10
        output_tokens: 50
        total_tokens: 60
    }
    request_id = "uuid-1234-5678"
}

object TokenUsage {
    input_tokens = 10
    output_tokens = 50
    total_tokens = 60
    cost = 0.0014
}

Request --> Headers: 包含
Response --> TokenUsage: 统计

@enduml
```

---

## 8. 部署图：DashScope架构

```plantuml
@startuml
skinparam backgroundColor #FEFEFE
skinpanel rectangle {
    BackgroundColor #E1F5FE
    BorderColor #0277BD
}

rectangle "用户端" {
    artifact "Python应用" as PyApp
    artifact "OpenAI SDK" as OpenAISDK
    artifact ".env文件\n(API Key)" as Env
}

rectangle "互联网" {
    artifact "HTTPS请求" as HTTPS
}

rectangle "阿里云 DashScope" {
    rectangle "全球地域" {
        node "中国" as CN {
            card "API服务\nqwen-plus\nqwen-max" as CNAPI
        }
        
        node "新加坡" as SG {
            card "API服务\nqwen-plus\nqwen-max" as SGAPI
        }
        
        node "日本" as JP {
            card "API服务\nqwen-plus\nqwen-max" as JPAPI
        }
    }
    
    rectangle "核心服务" {
        card "鉴权\n验证Key" as Auth
        card "限流\n检查配额" as RateLimit
        card "推理引擎\nQWen模型" as Inference
    }
    
    rectangle "存储" {
        database "Key存储" as KeyDB
        database "配额存储" as QuotaDB
        database "日志存储" as LogDB
    }
}

PyApp --> Env: 读取
PyApp --> OpenAISDK: 调用
OpenAISDK --> HTTPS: 加密传输
HTTPS --> CNAPI: 路由

CNAPI --> Auth: 1验证
Auth --> KeyDB: 查询
CNAPI --> RateLimit: 2限流
RateLimit --> QuotaDB: 查询
CNAPI --> Inference: 3推理
Inference --> LogDB: 记录

note right of CNAPI
    选择最近的服务器
    减少延迟
end note

@enduml
```

---

## 在线查看方式

### 方式1：PlantUML在线编辑器
访问 http://www.plantuml.com/plantuml/uml/

1. 复制上面的代码
2. 粘贴到编辑器
3. 自动生成图表
4. 可导出为PNG/SVG/PDF

### 方式2：VS Code插件
1. 安装 "PlantUML" 插件
2. 打开此markdown文件
3. 预览时自动渲染

### 方式3：转换为SVG
```bash
# 需要安装 plantuml
plantuml -Tsvg QWEN_FLOW_PLANTUML.md

# 或使用在线服务
```

---

## PlantUML 的优点

✨ **相比其他格式的优势：**

- ✅ 支持多种图表类型
- ✅ 代码简洁易读
- ✅ 自动布局，无需手工调整
- ✅ 易于版本控制
- ✅ 支持导出多种格式
- ✅ 生态工具丰富

## PlantUML 图表类型

本文档使用了：

- 📊 **stateDiagram** - 状态图
- 📈 **activity** - 活动图
- 🔄 **sequence** - 时序图
- 📦 **class** - 类图
- 🏗️ **component** - 组件图
- 🗂️ **object** - 对象图
- 🌐 **deployment** - 部署图

