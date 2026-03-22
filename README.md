# 🚀 LeetCode Daily Auto-Fetch (力扣每日一题自动归档)

本项目是一个基于 Python 和 GitHub Actions 构建的全自动 LeetCode（力扣中国区）每日一题抓取与归档工具。
它每天定时在云端运行，自动获取当天的题目，保存为 PDF 和长截图，并为你准备好专属的 Markdown 刷题笔记模板。

💡 **极客设计：阅后即焚**
当你在当前仓库成功开启自动化脚本后，本说明文档将自动完成它的历史使命并被覆盖，当前页面将蜕变为一个纯净、专业的专属刷题目录！(从你启动的这一天开始记录)

---

## 🛠️ 如何启动你的专属刷题机？ (Fork 本项目)

如果你想在自己的 GitHub 上使用这套自动化工作流，请务必按照以下步骤操作：

### 1. Fork 本仓库
点击本页面右上角的 **Fork** 按钮，将项目复制到你自己的 GitHub 账号下。

### 2. 开启 GitHub Actions 读写权限 (⚠️ 核心步骤)
由于脚本需要向你的仓库自动提交生成的笔记文件，你必须赋予 GitHub Actions 写入权限：
1. 进入你 Fork 后的仓库，点击顶部的 **Settings**。
2. 在左侧边栏找到 **Actions** -> **General**。
3. 滚动到底部找到 **Workflow permissions**，选中 **Read and write permissions**。
4. 点击 **Save** 保存。

### 3. 配置启动开关 (🚀 点火)
为了防止误触发，本项目默认处于静止休眠状态。你需要手动配置变量来唤醒它：
1. 在你的仓库顶部点击 **Settings**。
2. 在左侧边栏找到 **Secrets and variables** -> **Actions**。
3. 切换到 **Variables** 标签页（注意不是 Secrets）。
4. 点击 **New repository variable**。
5. Name 填入：`ENABLE_AUTO_FETCH`
6. Value 填入：`true`
7. 点击 **Add variable**。

### 4. 见证奇迹 (手动触发首次运行)
完成配置后，你可以等待今晚 00:00 的自动执行，或者现在立刻手动测试：
1. 点击仓库顶部的 **Actions** 标签页。
2. 如果提示 "I understand my workflows, go ahead and enable them"，请点击确认。
3. 在左侧点击 **LeetCode Daily Auto-Fetch**。
4. 点击右侧的 **Run workflow** 下拉菜单，然后点击绿色的 **Run workflow** 按钮。
5. 运行成功后，回到仓库首页刷新，你会发现这篇长长的介绍已经消失，取而代之的是你今天的专属题目！

---

## 📅 每日打卡流程
1. 每天将仓库 `git pull` 到本地。
2. 在当天生成的文件夹内的 `.md` 文件中编写你的代码。
3. 将你的题解 `git push` 到云端，完成打卡！