# AI File Advisor

一个基于本地大语言模型的 Windows 文件分析助手。

AI File Advisor 致力于解决一个常见问题：

> 当电脑磁盘空间不足时，面对大量陌生的 `.exe`、`.dll`、`.sys` 等程序文件，用户往往不知道这些文件是什么、有什么作用、是否可以删除，因此不敢清理。

本项目通过文件元数据分析、规则引擎和本地大模型能力，为用户提供文件用途解释、风险评估和删除建议，帮助用户更安全地管理电脑文件。

---

# 项目目标

让用户在删除文件之前，快速获得以下信息：

* 这个文件是什么？
* 它属于哪个软件？
* 它的主要作用是什么？
* 删除后可能产生什么影响？
* 是否建议保留？
* 当前分析结果的可信度如何？

例如：

文件：

```text
Qt5Core.dll
```

分析结果：

```text
文件简介：
Qt 框架核心动态链接库。

主要作用：
为许多桌面软件提供图形界面和基础功能支持。

风险等级：
高

可信度：
95%

建议：
保留，删除后可能导致相关软件无法启动。
```

---

# 功能特性

## 文件扫描

扫描指定目录下的程序文件：

支持格式：

* .exe
* .dll
* .msi
* .sys
* .bat
* .ps1

获取：

* 文件名
* 文件路径
* 文件大小
* 修改时间

---

## 元数据提取

自动读取 Windows 可执行文件信息：

* Product Name（产品名称）
* Company Name（公司名称）
* File Description（文件描述）
* Version（版本号）

例如：

```text
Company:
Google LLC

Product:
Google Chrome

Description:
Chrome Browser
```

---

## AI 智能分析

基于本地运行的 Qwen3 模型生成文件解释。

输出内容包括：

* 文件简介
* 文件用途
* 风险等级
* 删除建议
* 可信度评分

对于信息不足的文件，系统会明确提示：

```text
无法可靠识别该文件。

建议查看文件来源或进一步分析。
```

而不会编造不存在的信息。

---

## 风险评估

内置规则引擎对文件所在位置进行初步判断。

示例：

### Windows 系统目录

```text
C:\Windows
```

风险等级：

```text
高
```

---

### Program Files

```text
C:\Program Files
```

风险等级：

```text
中-高
```

---

### Downloads

```text
C:\Users\用户名\Downloads
```

风险等级：

```text
低
```

---

## 本地优先

本项目采用 Local First 设计理念。

特点：

* 不上传用户文件
* 不依赖云服务
* 支持离线运行
* 所有分析均在本地完成

用户数据始终保留在本机。

---

# 技术架构

```text
目录扫描
    ↓
元数据提取
    ↓
规则引擎
    ↓
Qwen3 本地分析
    ↓
SQLite缓存
    ↓
结果展示
```

---

# 技术栈

## 后端

* Python 3.11+
* pathlib
* pefile
* pywin32
* sqlite3

## AI

* Ollama
* Qwen3:4B

## 前端

第一阶段：

* Streamlit

未来版本：

* PySide6

---

# 项目结构

```text
ai-file-advisor/

├── app/
│   ├── scanner.py
│   ├── extractor.py
│   ├── analyzer.py
│   ├── rules.py
│   ├── cache.py
│   └── models.py
│
├── prompts/
│   └── explain_prompt.txt
│
├── ui/
│   └── streamlit_app.py
│
├── database/
│   └── advisor.db
│
├── tests/
│
├── requirements.txt
│
└── README.md
```

---

# 当前版本规划

## V0.1

核心能力验证

实现：

* 文件扫描
* 元数据提取
* AI解释
* 风险评估
* SQLite缓存
* Streamlit界面

---

## V0.2

增强分析能力

新增：

* 文件夹整体分析
* 软件关联识别
* 重复安装包检测
* 大文件风险分析

---

## V0.3

知识库增强

新增：

* 文件 Hash 识别
* 本地知识库
* 可信度优化
* 可选联网查询

---

## V1.0

桌面客户端版本

基于 PySide6 实现。

目标体验类似：

* Everything
* WizTree
* TreeSize

支持：

* 文件右键分析
* 系统托盘助手
* Windows资源管理器集成

---

# 项目原则

本项目遵循以下原则：

### 优先准确

不确定时明确说明“不知道”。

### 禁止幻觉

不编造文件用途。

### 本地运行

保护用户隐私。

### 可解释

所有分析结果都应让普通用户能够理解。

---

# 免责声明

本工具提供的是辅助分析和建议，不保证结果绝对正确。

对于系统文件、驱动文件以及重要软件组件，请在删除前自行确认其用途，并做好备份。

当系统无法可靠识别文件时，会主动降低可信度并提示用户进行人工确认。
