# 如何删除GitHub仓库

> ⚠️ **警告：删除仓库是不可逆的操作！删除后所有代码、Issue、Pull Request等都会永久消失，无法恢复。**

## 📋 目录

1. [图形界面方式（推荐）](#图形界面方式推荐)
2. [命令行方式](#命令行方式)
3. [删除前的检查清单](#删除前的检查清单)
4. [常见问题](#常见问题)
5. [如何避免误删](#如何避免误删)

---

## 图形界面方式（推荐）

### 第一步：打开仓库设置

1. 打开浏览器，访问你的GitHub仓库
   ```
   https://github.com/username/repository-name
   ```

2. 点击顶部菜单栏的 **Settings**（设置）
   ```
   仓库页面
   ├─ Code
   ├─ Issues
   ├─ Pull requests
   ├─ Discussions
   ├─ Actions
   ├─ Projects
   ├─ Wiki
   ├─ Security
   ├─ Insights
   └─ Settings ← 点这里
   ```

### 第二步：找到危险区域

3. 在Settings页面中，向下滚动到页面最底部

4. 找到 **Danger zone**（危险区域）红色区块
   ```
   ⚠️  Danger zone
   ┌─────────────────────────────────┐
   │ Delete this repository           │
   │ 删除此仓库                       │
   │ Once you delete a repository...  │
   │ [Delete this repository] 按钮    │
   └─────────────────────────────────┘
   ```

### 第三步：确认删除

5. 点击红色的 **Delete this repository**（删除此仓库）按钮

6. GitHub会显示一个确认对话框
   ```
   Are you absolutely sure?
   你确定吗?
   
   This action CANNOT be undone. This will permanently delete the 
   username/repository-name repository and remove all of its history.
   
   这个操作无法撤销。这将永久删除 username/repository-name 
   仓库及其所有历史记录。
   
   [输入框] 请输入: username/repository-name
   
   I understand the consequences, delete this repository
   我理解后果，删除此仓库 [Delete this repository]
   ```

### 第四步：输入确认文字

7. 在输入框中输入完整的仓库名称
   ```
   格式: username/repository-name
   
   例如: konyellin-cyber/QwenTest
   ```

8. 点击红色的 **Delete this repository** 按钮

### 第五步：验证

9. 稍等片刻，仓库将被删除

10. 系统会自动重定向到你的GitHub首页

---

## 命令行方式

### ⚠️ 注意事项

```
命令行删除需要使用GitHub CLI工具
需要先安装GitHub CLI (gh)
```

### 安装GitHub CLI

```bash
# macOS (使用Homebrew)
brew install gh

# Ubuntu/Debian
curl -fsSLhttps://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/linux stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# Windows (使用Chocolatey)
choco install gh

# 或从官网下载: https://github.com/cli/cli
```

### 登录GitHub

```bash
gh auth login
# 按照提示操作，选择GitHub.com并使用web浏览器登录
```

### 删除仓库

```bash
# 语法
gh repo delete [repository]

# 例子
gh repo delete konyellin-cyber/QwenTest

# 如果需要确认
gh repo delete konyellin-cyber/QwenTest --confirm

# 如果仓库在你的账户下，可以简化为
gh repo delete QwenTest --confirm
```

### 完整的命令行示例

```bash
# 第一步：验证当前登录用户
gh auth status

# 第二步：列出你的仓库
gh repo list

# 第三步：删除指定仓库
gh repo delete konyellin-cyber/QwenTest --confirm

# 删除后验证
gh repo list
# 仓库应该从列表中消失
```

---

## 删除前的检查清单

### ⚠️ 删除前必读

在删除仓库之前，请检查以下事项：

```
☐ 确认这是你要删除的仓库
  └─ 仓库名称: 
  └─ 所有者: 
  └─ URL: 

☐ 已备份重要数据
  └─ 克隆了本地副本
  └─ 导出了Issues
  └─ 导出了Wiki
  └─ 备份了Releases

☐ 检查协作者
  └─ 仓库中没有其他人的重要工作
  └─ 通知了其他贡献者

☐ 检查依赖关系
  └─ 没有其他项目依赖这个仓库
  └─ 没有从这个仓库fork的其他项目

☐ 检查链接
  └─ 没有外部文档指向这个仓库
  └─ 没有CI/CD管道依赖这个仓库

☐ 检查保护规则
  └─ 仓库没有branch protection rules
  └─ 没有活跃的Pull Requests

☐ 最后确认
  └─ 我真的确定要删除这个仓库
  └─ 我已经做好后果的心理准备
```

---

## 常见问题

### Q1: 删除仓库后能恢复吗？

```
❌ 不能！

GitHub无法恢复已删除的仓库。
如果仓库被删除，所有代码、Issue、PR等都会永久消失。

唯一的方法是：
1. 如果你有本地clone，可以重新push到新仓库
2. 如果你有备份，可以从备份恢复
```

### Q2: 删除仓库会删除fork的副本吗？

```
❌ 不会！

删除原仓库不会影响已fork的副本。
已fork的副本会继续存在。

但是：
• 新的fork会指向已删除的仓库（失效链接）
• 其他人无法再fork这个仓库
```

### Q3: 如果仓库有pending的PR怎么办？

```
⚠️ 警告！

删除仓库会同时删除所有关联的PR。
如果有重要的PR，请先：

1. 检查所有待审PR
2. 合并重要的PR或保存代码
3. 关闭或保存其他PR的内容
4. 再进行删除
```

### Q4: 删除仓库需要什么权限？

```
✅ 你需要：

• 仓库所有者权限，或
• 组织所有者权限（对于组织仓库），或
• 具有"删除仓库"权限的成员

⚠️ 不能删除：
• 不是你所有的仓库（你不是owner）
• 组织仓库（需要组织所有者权限）
• 已fork但不是你的原始仓库
```

### Q5: 删除个人仓库 vs 组织仓库的区别？

```
【删除个人仓库】
1. 打开仓库 Settings
2. 向下滚动到 Danger zone
3. 点击 Delete this repository
4. 输入仓库完整名称确认
5. 删除

【删除组织仓库】
1. 需要组织所有者权限
2. 打开仓库 Settings
3. 向下滚动到 Danger zone
4. 点击 Delete this repository
5. 输入确认信息
6. 删除

⚠️ 注意：
删除组织仓库可能需要额外的确认
取决于组织的安全设置
```

---

## 如何避免误删

### 🛡️ 防护措施

#### 方式1：将仓库归档（Archive）

如果你想保留仓库但不再使用，可以归档而不是删除：

```
Settings → Archive this repository
├─ 仓库变为只读
├─ 其他人可以fork
├─ 代码和历史都保留
├─ 任何时候可以取消归档
└─ 完全可逆！
```

#### 方式2：转移仓库所有权

如果你想放弃仓库但保留代码：

```
Settings → Transfer ownership
├─ 转移给另一个用户
├─ 转移给另一个组织
├─ 代码和历史都保留
└─ 接收方成为新owner
```

#### 方式3：设置提醒

删除前在日历中标记提醒：

```
// 删除前等待
1. 创建备份副本（fork或clone）
2. 等待24-48小时，确认你的决定
3. 再进行删除

理由：
• 给你时间来改变主意
• 确保备份已成功创建
• 降低误删风险
```

#### 方式4：使用GitHub的删除保护功能

对于重要的仓库，考虑使用：

```
1. Branch protection rules
   └─ 防止删除main分支

2. 限制admin权限
   └─ 只有特定人员可以删除

3. 组织级别的policy
   └─ 需要多个人批准才能删除
```

---

## 删除仓库的详细步骤（图文版）

### Step 1: 打开Settings

```
GitHub仓库页面
│
├─ Code ────┐
├─ Issues   │
├─ ...      ├─ 顶部标签栏
├─ Wiki     │
├─ Insights │
└─ Settings ← 点这里 (齿轮图标)
```

### Step 2: 向下滚动到最底部

```
Settings页面
│
├─ General Settings
├─ Repository name
├─ Description
├─ URL
├─ ...其他选项
│
└─ ⚠️ Danger zone (红色区块)
   └─ 这是最后一个区块
```

### Step 3: 找到Delete按钮

```
┌─────────────────────────────────────┐
│ ⚠️  Danger zone                      │
├─────────────────────────────────────┤
│                                      │
│ Delete this repository              │
│ 删除此仓库                           │
│                                      │
│ Once you delete a repository, there  │
│ is no going back. Please be certain. │
│                                      │
│ [Delete this repository] ← 红色按钮  │
│                                      │
└─────────────────────────────────────┘
```

### Step 4: 输入确认信息

```
┌─────────────────────────────────────┐
│ Are you absolutely sure?             │
│ 你确定吗?                            │
├─────────────────────────────────────┤
│                                      │
│ This action CANNOT be undone.       │
│                                      │
│ Please type in the name of the      │
│ repository to confirm.              │
│                                      │
│ [username/repository-name]           │
│ [输入框: 请输入仓库名]               │
│                                      │
│ [Delete this repository] (红色按钮)  │
│                                      │
└─────────────────────────────────────┘
```

### Step 5: 完成

```
✅ 仓库已删除

仓库现已从GitHub移除
所有代码、Issue、PR等都已永久删除
你将被重定向到GitHub首页
```

---

## 删除仓库的替代方案

### 📌 如果你不确定要不要删除，可以考虑：

#### 方案1: 归档仓库（Archive）

```
优点：
✅ 保留所有代码和历史
✅ 可以随时取消归档
✅ 其他人仍然可以fork
✅ 完全可逆

缺点：
❌ 仓库仍然占用空间
❌ 仍然显示在你的列表中

使用场景：
• 不再维护但想保留参考
• 保存历史项目
• 学习用的实验项目
```

#### 方案2: 转移所有权（Transfer）

```
优点：
✅ 保留所有代码和历史
✅ 其他人接管维护
✅ 完全可逆（新owner可以转移回来）

缺点：
❌ 不再是你的仓库
❌ 无法收到通知

使用场景：
• 将项目交给团队
• 将项目交给新维护者
• 将项目捐献给组织
```

#### 方案3: 创建私有副本

```
优点：
✅ 保留所有代码
✅ 新副本是私有的
✅ 原公开仓库仍存在
✅ 可以随时删除

缺点：
❌ 创建新仓库
❌ 历史关系断裂

使用场景：
• 保存重要代码但不公开
• 创建个人备份
• 逐步迁移代码
```

---

## 小结

| 操作 | 描述 | 可逆性 | 推荐度 |
|------|------|--------|--------|
| **删除** | 永久移除仓库 | ❌ 不可逆 | ⚠️ 谨慎 |
| **归档** | 标记为只读 | ✅ 可逆 | ✅ 保留选项 |
| **转移** | 转移给他人 | ✅ 可逆 | ✅ 协作选项 |
| **克隆** | 创建本地副本 | ✅ 可逆 | ✅ 备份选项 |

---

## 最后的建议

```
🎯 删除前的最终检查清单：

□ 确认仓库名称正确
□ 确认已备份所有重要数据
□ 确认没有其他人依赖这个仓库
□ 等待24小时，再次确认你的决定
□ 考虑是否可以使用归档而不是删除
□ 确认我真的要删除这个仓库

如果上述任何一项有疑问，请：
❌ 不要删除
✅ 选择归档或转移

记住：
⚠️  删除仓库是不可逆的！
⚠️  删除后无法恢复！
⚠️  一旦确认，所有数据都会永久消失！
```

