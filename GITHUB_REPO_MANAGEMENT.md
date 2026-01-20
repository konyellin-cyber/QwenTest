# GitHub 仓库管理快速参考

> 快速查询GitHub仓库的常见操作

## 🎯 快速导航

### 我想...

| 操作 | 步骤 | 可逆性 | 文档 |
|------|------|--------|------|
| 📌 删除仓库 | Settings > Danger zone > Delete | ❌ 不可逆 | [详见](#删除仓库) |
| 📦 归档仓库 | Settings > Archive this repository | ✅ 可逆 | [详见](#归档仓库) |
| 🔄 转移仓库 | Settings > Transfer ownership | ✅ 可逆 | [详见](#转移仓库) |
| 🔒 设为私有 | Settings > Visibility > Private | ✅ 可逆 | [详见](#改变仓库可见性) |
| 🌐 设为公开 | Settings > Visibility > Public | ✅ 可逆 | [详见](#改变仓库可见性) |
| 💾 备份仓库 | git clone --mirror | ✅ 可逆 | [详见](#备份仓库) |
| 📋 导出Issues | GitHub API / export | ✅ 可逆 | [详见](#导出数据) |

---

## 删除仓库

### 🖥️ 网页方式（最简单）

1. **打开仓库** → 点击 **Settings**
2. **向下滚动** → 找到 **Danger zone**
3. **点击** `Delete this repository` (红色按钮)
4. **输入** 仓库名称确认 (格式: `username/repo-name`)
5. **点击** 确认删除

```
⏱️  耗时: 1-2分钟
⚠️  风险: 极高 (不可逆)
```

### 💻 命令行方式

```bash
# 使用GitHub CLI
gh auth login
gh repo delete username/repository-name --confirm
```

### ⚠️ 删除前检查

```
☐ 仓库名称正确
☐ 已备份所有数据
☐ 没有其他人依赖
☐ 没有活跃的PR/Issues
☐ 等待24小时再确认一次
```

---

## 归档仓库

### 🖥️ 步骤

1. **Settings** → 向下滚动
2. 找到 **"Archive this repository"**
3. 点击 **Archive**
4. 确认

### ✅ 优点

- ✅ 保留所有代码和历史
- ✅ 变为只读
- ✅ 随时可以取消归档
- ✅ 其他人仍可fork
- ✅ 完全可逆

### 📌 适用场景

- 不再维护的项目
- 已完成的项目
- 实验性项目

---

## 转移仓库

### 🖥️ 步骤

1. **Settings** → **Transfer ownership**
2. 输入接收者的用户名或组织名
3. 确认转移

### ✅ 优点

- ✅ 保留所有代码
- ✅ 交给新维护者
- ✅ 完全可逆
- ✅ 接收方可以再转移回来

### 📌 适用场景

- 开源项目交接
- 团队协作管理
- 组织接管

---

## 改变仓库可见性

### 🖥️ 设置为私有

1. **Settings** → **Visibility**
2. 选择 **Private**
3. 点击 **Change visibility**

### 🖥️ 设置为公开

1. **Settings** → **Visibility**
2. 选择 **Public**
3. 点击 **Change visibility**

### ⚠️ 注意

- ✅ 完全可逆
- ✅ 可以随时切换
- ❌ 私有仓库会限制fork功能
- ❌ GitHub账户级别的配额可能受限

---

## 备份仓库

### 💾 创建完整备份

```bash
# 方式1: 使用 mirror clone
git clone --mirror https://github.com/username/repo.git
cd repo.git
git push --mirror https://github.com/newusername/backup-repo.git

# 方式2: 使用 GitHub CLI
gh repo clone username/repo --mirror

# 方式3: 简单的clone
git clone https://github.com/username/repo.git
cd repo
git push --mirror https://github.com/newusername/backup-repo.git
```

### 📦 备份完整的仓库数据

```bash
# 导出所有信息
git clone --bare https://github.com/username/repo.git repo-backup

# 压缩备份
tar -czf repo-backup.tar.gz repo-backup/

# 保存到安全位置
cp repo-backup.tar.gz /backup/location/
```

---

## 导出数据

### 📋 导出Issues

```bash
# 使用GitHub CLI
gh issue list --limit 1000 > issues.csv

# 导出为JSON
gh issue list --limit 1000 --json title,body,state,created,closed > issues.json
```

### 📝 导出Releases

```bash
# 使用GitHub CLI
gh release list > releases.txt

# 或手动下载
# 访问: https://github.com/username/repo/releases
```

### 📊 导出完整数据

```bash
# 使用GitHub API
curl -H "Authorization: token YOUR_TOKEN" \
     https://api.github.com/repos/username/repo \
     > repo-info.json
```

---

## 操作对比表

| 操作 | 保留数据 | 可逆 | 他人可见 | 推荐度 |
|------|--------|------|--------|--------|
| 🗑️ 删除 | ❌ | ❌ | ❌ | ⚠️⚠️⚠️ |
| 📦 归档 | ✅ | ✅ | ✅ | ✅✅✅ |
| 🔄 转移 | ✅ | ✅ | ✅ | ✅✅✅ |
| 🔒 私有化 | ✅ | ✅ | ❌ | ✅✅ |
| 💾 备份 | ✅ | ✅ | ❌ | ✅✅✅ |

---

## 危险操作清单

### 🚨 不可逆的操作

```
❌ 删除仓库
   → 无法恢复
   → 所有数据永久消失
   → 其他人无法访问

❌ 强制删除分支
   → 可能丢失提交
   → 需要谨慎操作

❌ 重写历史 (force push)
   → 其他协作者的本地版本会冲突
   → 需要团队协调
```

### ✅ 相对安全的操作

```
✅ 归档仓库
   → 可以随时取消
   → 数据完全保留

✅ 转移所有权
   → 新所有者可以转移回
   → 数据完全保留

✅ 改变可见性
   → 可以随时切换
   → 数据完全保留
```

---

## 常见错误

### ❌ 错误1: 不意中删除了仓库

**症状**: 
- 仓库突然消失了
- 无法访问之前的代码

**解决方案**:
- 如果你有本地clone，可以重新创建仓库并push
- 如果有fork，fork仍然存在
- 立即联系GitHub支持（虽然恢复机会很小）

### ❌ 错误2: 转移后无法访问

**症状**:
- 找不到转移后的仓库
- 本地clone的remote失效

**解决方案**:
```bash
# 更新本地remote URL
git remote set-url origin https://github.com/newowner/repo.git
```

### ❌ 错误3: 私有化后无法共享

**症状**:
- 将公开仓库改为私有
- 其他人无法访问

**解决方案**:
```
Settings → Manage access → Add collaborators
或将仓库改回公开
```

---

## 最佳实践

### ✅ 操作前

```
□ 备份重要数据
□ 检查是否有依赖
□ 通知相关人员
□ 等待24小时确认
```

### ✅ 操作时

```
□ 仔细核对仓库名称
□ 逐字输入确认信息
□ 检查最后一次是否正确
```

### ✅ 操作后

```
□ 确认操作已生效
□ 更新相关文档
□ 如需要，更新DNS或转发
```

---

## 获取帮助

### 📚 GitHub官方文档

- 删除仓库: https://docs.github.com/repositories/creating-and-managing-repositories/deleting-a-repository
- 管理仓库: https://docs.github.com/repositories
- API文档: https://docs.github.com/en/rest

### 💬 获得支持

- GitHub Support: https://github.com/support
- GitHub Discussions: https://github.com/orgs/community/discussions
- Stack Overflow: 标签 `github`

---

## 速记表

```
🎯 我想删除仓库
  Settings → Danger zone → Delete → 输入名称 → 确认

🎯 我想备份仓库
  git clone --mirror → 上传到新位置

🎯 我想保留但停用
  Settings → Archive this repository

🎯 我想给别人
  Settings → Transfer ownership

🎯 我想改变公开/私有
  Settings → Visibility
```

