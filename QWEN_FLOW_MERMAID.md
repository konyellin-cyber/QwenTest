# QWen API 流程图 - Mermaid 格式（GitHub原生支持）

> ⭐ **GitHub支持直接渲染Mermaid图表！** 在GitHub网页中打开本文件可以直接看到流程图。

## 1. 完整的端到端调用流程

```mermaid
graph TD
    A["🔷 开始"] --> B["1️⃣ 获取API Key<br/>dashscope.aliyun.com"]
    B --> C["2️⃣ 初始化OpenAI客户端<br/>设置api_key和base_url"]
    C --> D["3️⃣ 构建消息<br/>role: user/assistant<br/>content: 文本内容"]
    D --> E["4️⃣ 发送请求<br/>client.chat.completions.create"]
    E --> F{{"5️⃣ 服务器验证"}}
    
    F -->|❌ 验证失败| G["返回错误<br/>401/429/500"]
    F -->|✅ 验证通过| H["6️⃣ 处理请求<br/>模型推理"]
    
    G --> I["8️⃣ 错误处理<br/>重试或报错"]
    H --> J["7️⃣ 返回响应<br/>JSON格式"]
    
    I --> K{{"是否重试?"}}
    K -->|是| E
    K -->|否| L["❌ 返回错误"]
    
    J --> M["9️⃣ 解析响应<br/>提取content<br/>统计tokens"]
    M --> N["✅ 返回给用户"]
    
    L --> O["🔷 结束"]
    N --> O
    
    style A fill:#90EE90
    style O fill:#FFB6C6
    style G fill:#FFB6C6
    style L fill:#FFB6C6
    style N fill:#90EE90
```

---

## 2. 鉴权流程图

```mermaid
graph LR
    A["🔐 API Key"] --> B["存储方式"]
    B --> B1["环境变量<br/>export DASHSCOPE_API_KEY"]
    B --> B2[".env文件<br/>DASHSCOPE_API_KEY=sk-xxx"]
    B --> B3["直接传入<br/>api_key='sk-xxx'"]
    
    B1 --> C["初始化客户端<br/>client = OpenAI"]
    B2 --> C
    B3 --> C
    
    C --> D["客户端内部保存API Key"]
    D --> E["发送请求时<br/>自动添加Authorization头"]
    E --> F["Authorization: Bearer sk-xxx"]
    
    F --> G["POST 请求到服务器"]
    G --> H{{"服务器验证"}}
    
    H --> H1["1. 解析Authorization头"]
    H1 --> H2["2. 查询API Key有效性"]
    H2 --> H3["3. 检查账户配额"]
    H3 --> H4["4. 检查速率限制"]
    
    H4 --> I{{"所有验证<br/>都通过?"}}
    
    I -->|❌ 验证失败| J["返回401错误<br/>认证失败"]
    I -->|❌ 超出配额| K["返回403错误<br/>禁止访问"]
    I -->|❌ 触发限流| L["返回429错误<br/>限流"]
    I -->|✅ 全部通过| M["处理请求<br/>返回200 OK"]
    
    style A fill:#87CEEB
    style M fill:#90EE90
    style J fill:#FFB6C6
    style K fill:#FFB6C6
    style L fill:#FFD700
```

---

## 3. 错误处理决策树

```mermaid
graph TD
    A["收到响应"] --> B{{"HTTP状态码<br/>是多少?"}}
    
    B -->|200| C["✅ 成功<br/>解析响应"]
    B -->|400| D["❌ 请求格式错误<br/>Bad Request"]
    B -->|401| E["❌ API Key无效<br/>Unauthorized"]
    B -->|403| F["❌ 账户被禁用<br/>Forbidden"]
    B -->|429| G["⚠️ 触发限流<br/>Too Many Requests"]
    B -->|500| H["⚠️ 服务器错误<br/>Internal Server Error"]
    B -->|503| I["⚠️ 服务不可用<br/>Service Unavailable"]
    
    C --> C1["解析JSON<br/>提取数据"]
    C1 --> C2["返回结果给用户"]
    
    D --> D1["检查请求格式"]
    D1 --> D2["验证参数"]
    D2 --> D3["❌ 不重试<br/>修改代码"]
    
    E --> E1["检查API Key"]
    E1 --> E2["访问官方网站"]
    E2 --> E3["❌ 不重试<br/>更新Key"]
    
    F --> F1["检查账户状态"]
    F1 --> F2["处理账户问题"]
    F2 --> F3["❌ 不重试<br/>联系支持"]
    
    G --> G1["等待 1秒"]
    G1 --> G2{{"第 <br/>几次<br/>重试?"}}
    G2 -->|1| G3["✅ 重试<br/>第1次"]
    G2 -->|2| G4["✅ 重试<br/>第2次"]
    G2 -->|3+| G5["❌ 停止<br/>已达限制"]
    G3 --> G1
    G4 --> G1
    
    H --> H1["等待 1秒"]
    H1 --> H2{{"第<br/>几次<br/>重试?"}}
    H2 -->|1| H3["✅ 重试<br/>第1次"]
    H2 -->|2| H4["✅ 重试<br/>第2次"]
    H2 -->|3+| H5["❌ 停止<br/>已达限制"]
    H3 --> H1
    H4 --> H1
    
    I --> I1["等待 2秒"]
    I1 --> I2{{"第<br/>几次<br/>重试?"}}
    I2 -->|1| I3["✅ 重试<br/>第1次"]
    I2 -->|2| I4["✅ 重试<br/>第2次"]
    I2 -->|3+| I5["❌ 停止<br/>已达限制"]
    I3 --> I1
    I4 --> I1
    
    C2 --> J["🎉 完成"]
    D3 --> J
    E3 --> J
    F3 --> J
    G5 --> J
    H5 --> J
    I5 --> J
    
    style C fill:#90EE90
    style J fill:#90EE90
    style D fill:#FFB6C6
    style E fill:#FFB6C6
    style F fill:#FFB6C6
    style D3 fill:#FFB6C6
    style E3 fill:#FFB6C6
    style F3 fill:#FFB6C6
    style G fill:#FFD700
    style H fill:#FFD700
    style I fill:#FFD700
```

---

## 4. 流式调用 vs 传统调用

```mermaid
graph LR
    A["📤 发送请求"] 
    
    A --> B{{"stream参数<br/>是什么?"}}
    
    B -->|stream=False| C["传统调用<br/>等待完整响应"]
    B -->|stream=True| D["流式调用<br/>实时接收数据"]
    
    C --> C1["⏳ 等待..."]
    C1 --> C2["服务器处理..."]
    C2 --> C3["📦 返回完整响应<br/>JSON格式<br/>200 OK"]
    C3 --> C4["解析JSON<br/>提取所有内容"]
    C4 --> C5["显示完整回复"]
    
    D --> D1["🔌 建立连接"]
    D1 --> D2["📡 实时流式传输"]
    D2 --> D3["data: chunk1"]
    D3 --> D4["data: chunk2"]
    D4 --> D5["data: chunk3"]
    D5 --> D6["..."]
    D6 --> D7["data: [DONE]"]
    D7 --> D8["⏱️ 实时显示<br/>逐字出现"]
    
    C5 --> E["✅ 流程完成"]
    D8 --> E
    
    style C fill:#87CEEB
    style D fill:#90EE90
    style E fill:#FFD700
```

---

## 5. 两种API调用方式对比

```mermaid
graph TD
    A["选择API调用方式"] --> B{{"熟悉OpenAI API?"}}
    
    B -->|是| C["使用 OpenAI SDK<br/>兼容模式"]
    B -->|否/需要更多特性| D["使用 DashScope SDK<br/>原生模式"]
    
    C --> C1["from openai import OpenAI"]
    C1 --> C2["base_url: .../compatible-mode/v1"]
    C2 --> C3["API调用方式<br/>与OpenAI相同"]
    C3 --> C4["优点:<br/>✓ 学习成本低<br/>✓ 迁移成本低<br/>✓ 生态丰富"]
    C4 --> C5["缺点:<br/>✗ 部分特性可能受限"]
    
    D --> D1["from dashscope import Generation"]
    D1 --> D2["base_url: .../api/v1"]
    D2 --> D3["DashScope特定的<br/>调用方式"]
    D3 --> D4["优点:<br/>✓ 支持全部特性<br/>✓ 更多配置选项"]
    D4 --> D5["缺点:<br/>✗ 需要学习新SDK<br/>✗ 代码不兼容OpenAI"]
    
    C5 --> E["推荐使用场景"]
    D5 --> E
    
    E --> E1["快速开发"]
    E --> E2["原型测试"]
    E --> E3["生产环境"]
    E --> E4["复杂功能"]
    
    E1 -.->|优先| C5
    E2 -.->|优先| C5
    E3 -.->|推荐| C5
    E4 -.->|优先| D5
    
    style C fill:#87CEEB
    style D fill:#90EE90
```

---

## 6. 单个请求的生命周期

```mermaid
sequenceDiagram
    participant Client as 客户端<br/>Python代码
    participant SDK as SDK
    participant Network as 网络
    participant Server as 服务器
    
    Client->>SDK: 1. 调用 create()
    SDK->>SDK: 2. 构建JSON请求体
    SDK->>SDK: 3. 添加Authorization头<br/>Bearer sk-xxx
    SDK->>Network: 4. 发送POST请求
    
    Network->>Server: 5. 传输请求数据
    Server->>Server: 6. 接收请求
    Server->>Server: 7. 验证鉴权
    
    alt 鉴权失败
        Server->>Network: 返回 401 错误
        Network->>SDK: 传输响应
        SDK->>Client: 抛出异常
    else 鉴权通过
        Server->>Server: 8. 路由到推理引擎
        Server->>Server: 9. 生成响应
        Server->>Network: 10. 返回200 OK<br/>JSON响应
        Network->>SDK: 11. 传输响应
        SDK->>SDK: 12. 解析JSON
        SDK->>Client: 13. 返回Response对象
        Client->>Client: 14. 提取content<br/>统计tokens
    end
```

---

## 7. 模型选择决策树

```mermaid
graph TD
    A["选择QWen模型"] --> B{{"你的场景<br/>需求是?"}}
    
    B -->|速度最快<br/>成本最低| C["qwen-turbo<br/>¥0.0003/1K"]
    B -->|平衡方案| D["qwen-plus<br/>¥0.0008/1K<br/>推荐！"]
    B -->|性能最强| E["qwen-max<br/>¥0.02/1K"]
    B -->|处理长文本| F["qwen-long<br/>¥0.0005/1K<br/>100万token"]
    
    C --> C1["适用场景:<br/>• 简单任务<br/>• 高频调用<br/>• 成本敏感"]
    D --> D1["适用场景:<br/>• 通用对话<br/>• 推理任务<br/>• 代码生成<br/>🌟 大多数场景"]
    E --> E1["适用场景:<br/>• 复杂推理<br/>• 深度分析<br/>• 专业任务"]
    F --> F1["适用场景:<br/>• 长文档处理<br/>• 论文分析<br/>• 大规模数据"]
    
    C1 --> G["成本对比<br/>处理100万tokens"]
    D1 --> G
    E1 --> G
    F1 --> G
    
    G --> G1["qwen-turbo: ¥300"]
    G --> G2["qwen-plus: ¥800"]
    G --> G3["qwen-max: ¥20,000"]
    G --> G4["qwen-long: ¥500"]
    
    style D fill:#90EE90
    style G fill:#FFD700
```

---

## 8. 实际应用场景1：简单问答

```mermaid
graph LR
    A["用户:<br/>你好"] --> B["构建消息"]
    B --> C["发送API请求"]
    C --> D["服务器验证<br/>✅ 通过"]
    D --> E["模型处理<br/>qwen-turbo"]
    E --> F["返回响应<br/>状态码200"]
    F --> G["解析回复"]
    G --> H["显示给用户:<br/>你好！有什么<br/>我可以帮助的吗？"]
    
    style A fill:#87CEEB
    style H fill:#90EE90
    style D fill:#FFD700
```

---

## 9. 实际应用场景2：流式对话

```mermaid
graph LR
    A["用户:<br/>请写一首诗"] --> B["启用stream=True"]
    B --> C["发送API请求"]
    C --> D["服务器验证<br/>✅ 通过"]
    D --> E["建立流连接"]
    E --> F1["传输chunk1:<br/>春天"]
    F1 --> F2["传输chunk2:<br/>来临"]
    F2 --> F3["传输chunk3:<br/>了"]
    F3 --> F4["..."]
    F4 --> F5["传输[DONE]"]
    F5 --> G["用户看到:<br/>逐字显示诗歌"]
    
    style A fill:#87CEEB
    style G fill:#90EE90
    style E fill:#FFD700
```

---

## 10. 实际应用场景3：错误处理和重试

```mermaid
graph TD
    A["发送请求"] --> B["收到429错误<br/>限流"]
    B --> C["等待1秒"]
    C --> D["第一次重试"]
    D --> E["仍然收到429"]
    E --> F["等待2秒"]
    F --> G["第二次重试"]
    G --> H["成功! 200 OK"]
    H --> I["解析响应<br/>返回结果"]
    
    style A fill:#87CEEB
    style H fill:#90EE90
    style B fill:#FFD700
    style E fill:#FFD700
```

---

## 快速参考表

```mermaid
graph TD
    A["QWen API 快速参考"]
    
    A --> B["API端点"]
    B --> B1["OpenAI兼容:<br/>compatible-mode/v1"]
    B --> B2["DashScope原生:<br/>api/v1"]
    
    A --> C["鉴权方式"]
    C --> C1["Authorization: Bearer KEY"]
    C --> C2["dashscope.api_key = KEY"]
    
    A --> D["模型选择"]
    D --> D1["qwen-turbo: 快速"]
    D --> D2["qwen-plus: 推荐"]
    D --> D3["qwen-max: 强大"]
    
    A --> E["常见错误"]
    E --> E1["401: 检查Key"]
    E --> E2["429: 使用重试"]
    E --> E3["500: 等待重试"]
    
    A --> F["配置参数"]
    F --> F1["temperature: 0-2"]
    F --> F2["top_p: 0-1"]
    F --> F3["max_tokens: 限制长度"]
    F --> F4["stream: 流式输出"]
```

---

## 如何在GitHub网页中查看

✨ **GitHub 原生支持 Mermaid 图表！**

在GitHub网页中查看此文件时，所有Mermaid代码块会被自动渲染成漂亮的流程图。

### 优点：
- ✅ GitHub原生支持，无需插件
- ✅ 代码版本控制
- ✅ 易于编辑和维护
- ✅ 支持导出为图片
- ✅ 响应式设计，适配各种屏幕

### 如何使用：
1. 访问 https://github.com/konyellin-cyber/QwenTest/blob/main/QWEN_FLOW_MERMAID.md
2. GitHub会自动渲染所有流程图
3. 可以滚动、放大、查看细节

### 导出图片：
- 在图表右上角有下载按钮
- 可导出为 PNG, SVG, PDF等格式

---

## 更多Mermaid图表类型

本文档使用了以下Mermaid图表类型：

- 📊 **flowchart (graph)** - 流程图、决策树
- 📈 **sequenceDiagram** - 时序图、交互流程
- 🔄 **stateDiagram** - 状态转移图

所有这些在GitHub网页中都能完美渲染！

