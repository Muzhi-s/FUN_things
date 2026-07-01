# 这是一个自动关机的小工具

一个轻量的命令行工具，用于在 Windows 上定时或倒计时执行关机（或重启）。适合专注学习/下载任务结束后自动关机等场景。

## 功能
- 定时关机（设置具体时间）
- 倒计时关机（设置间隔时长）
- 可选重启
- 取消已设置的关机计划
- 友好提示与错误处理

具体支持的命令行参数请以程序内帮助为准。

## 环境要求
- Windows 10/11
- Python 3.8+（用于直接运行源码）

## 快速开始
1. 安装/准备 Python 环境。
2. 在项目根目录执行：
	 - 交互式运行：`python shutdown_tool.py`
	 - 查看帮助与全部参数：`python shutdown_tool.py --help`

提示：在部分场景下（例如强制关闭应用）可能需要以管理员权限打开终端运行。

## 常见用法示例
- 直接运行并按提示设置关机：  
	`python shutdown_tool.py`
- 查看可用参数与示例：  
	`python shutdown_tool.py --help`
- 遇到紧急情况需要取消系统层面的关机：  
	在命令行执行 `shutdown -a`（Windows 原生命令，取消已排程的关机）。

由于命令行参数可能随版本变化，请以 `--help` 输出为准。

## 打包为可执行文件
项目已包含 PyInstaller 规格文件：
- 使用现有配置打包：`pyinstaller AutoShutdownTool.spec`
- 或者自行打包：`pyinstaller -F -n AutoShutdownTool shutdown_tool.py`

打包完成后，输出位于 PyInstaller 的默认目录（build/ 与 dist/）。可将生成的可执行文件放入任意位置使用。

## 注意事项
- 设定的关机计划会影响当前系统，请在保存工作后使用。
- 若需要在计划时间前取消，可运行工具中的取消命令，或在终端使用 `shutdown -a`。
- 某些安全策略可能要求以管理员权限运行。

## 目录结构（简要）
- shutdown_tool.py：工具主程序
- AutoShutdownTool.spec：PyInstaller 打包配置
- build/：构建中间产物

## 免责声明
本工具按“现状”提供，使用风险自负。请在确保不影响他人及关键业务的情况下使用本工具。
