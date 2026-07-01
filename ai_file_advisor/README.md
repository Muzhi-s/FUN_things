# AI File Advisor

## Introduction

AI File Advisor is a local-first Windows file analysis tool designed to help users understand unfamiliar program files before deleting or archiving them.

Instead of showing only file names and sizes, the tool explains:

* What the file is
* What it is used for
* Whether it is safe to delete
* Potential risks of deletion
* Confidence level of the analysis

The first version focuses on executable and system-related files commonly found on Windows.

Supported file types:

* .exe
* .dll
* .msi
* .sys
* .bat
* .ps1

---

## Features

### File Metadata Analysis

Extract information from executable files:

* Product Name
* Company Name
* File Description
* Version Information

### AI-Powered Explanation

Generate human-readable explanations using a local LLM.

Example:

Input:

Qt5Core.dll

Output:

Qt framework core library used by many desktop applications. Deleting it may cause dependent software to stop working.

### Risk Assessment

Built-in rule engine evaluates:

* System directories
* Program Files directories
* Downloads folders
* Temporary folders

### Confidence Scoring

Analysis results include a confidence score to indicate reliability.

### Local-First Design

* No file uploads
* No cloud dependency
* All analysis runs locally
* User files remain on the device

---

## Tech Stack

Backend:

* Python 3.11+
* pefile
* pywin32
* SQLite

AI:

* Ollama
* Qwen3:4B

Frontend:

* Streamlit

---

## Architecture

Directory Scan

↓

Metadata Extraction

↓

Rule Engine

↓

LLM Analysis

↓

SQLite Cache

↓

UI Display

---

## Future Roadmap

### V0.2

* Folder-level analysis
* Duplicate installer detection
* Installed software mapping

### V0.3

* Local knowledge base
* File hash identification
* Optional online lookup

### V1.0

* PySide6 desktop application
* Windows Explorer integration
* System tray assistant
* One-click file explanation

---

## Disclaimer

This tool provides recommendations only.

Users should verify important system files before deletion. When confidence is low, the tool will explicitly indicate that identification is uncertain.
