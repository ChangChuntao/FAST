<!-- 
  ╔═══════════════════════════════════════════════════════════════════════════╗
  ║                         FAST GNSS 工具包                                  ║
  ║              文件下载与信号处理工具包                                      ║
  ╚═══════════════════════════════════════════════════════════════════════════╝
-->

<p align="right">
  <a href="README.md">English</a> | <b>简体中文</b>
</p>

<div align="center">

<h1>GNSS 数据下载与信号处理工具包</h1>

<p>
  <a href="https://github.com/ChangChuntao/FAST/releases/tag/v3.01.0">
    <img src="https://img.shields.io/badge/Release-v3.01.00-2ea44f?style=flat-square&logo=github" alt="Release">
  </a>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" alt="License">
  </a>
</p>

<p>
  <img src="https://img.shields.io/badge/Platform-Windows-blue?style=flat-square&logo=windows" alt="Windows">
  <img src="https://img.shields.io/badge/macOS-Intel-black?style=flat-square&logo=apple" alt="macOS">
  <img src="https://img.shields.io/badge/Linux-Ubuntu|CentOS-orange?style=flat-square&logo=linux" alt="Linux">
</p>

<p><em>武汉大学卫星导航定位技术研究中心开发</em></p>

<p>
  <b><a href="#-快速开始">🚀 快速开始</a></b> •
  <b><a href="#-功能特性">✨ 功能特性</a></b> •
  <b><a href="#-下载">📥 下载</a></b> •
  <b><a href="#-文档">📖 文档</a></b>
</p>

</div>


## 🎯 概述

![FAST Banner](manual/fig/intro.png)

<div align="center">

| 📌 版本 | 🏢 开发单位 | 🐍 语言 | 🖥️ 界面 |
|:------:|:-----------:|:------:|:------:|
| **v3.01.00** | 武汉大学卫星导航定位技术研究中心 | Python 3.12+ | GUI + CLI |

</div>


---

## 🚀 快速开始

### 📥 下载预编译程序

<div align="center">

<table>
<thead>
<tr>
<th>平台</th>
<th>GUI 版本 📦</th>
<th>CLI 版本 🖥️</th>
</tr>
</thead>
<tbody>
<tr>
<td><b>Windows</b></td>
<td><a href="https://github.com/ChangChuntao/FAST/releases/download/v3.01.0/FastQt_Win.zip">FastQt_Win.zip</a></td>
<td><a href="https://github.com/ChangChuntao/FAST/releases/download/v3.01.0/FAST_Win.zip">FAST_Win.zip</a></td>
</tr>
<tr>
<td><b>macOS (Intel)</b></td>
<td><a href="https://github.com/ChangChuntao/FAST/releases/download/v3.01.0/FastQt_Mac.zip">FastQt_Mac.zip</a></td>
<td><a href="https://github.com/ChangChuntao/FAST/releases/download/v3.01.0/FAST_Mac.zip">FAST_Mac.zip</a></td>
</tr>
<tr>
<td><b>Ubuntu</b></td>
<td>—</td>
<td><a href="https://github.com/ChangChuntao/FAST/releases/download/v3.01.0/FAST_Ubuntu.zip">FAST_Ubuntu.zip</a></td>
</tr>
<tr>
<td><b>CentOS</b></td>
<td>—</td>
<td><a href="https://github.com/ChangChuntao/FAST/releases/download/v3.01.0/FAST_CentOS.zip">FAST_CentOS.zip</a></td>
</tr>
</tbody>
</table>

</div>

### 🐍 从源码运行

<details>
<summary><b>🐧 Linux / 🍎 macOS</b></summary>

```bash
# 1. 克隆仓库
git clone https://github.com/ChangChuntao/FAST.git && cd FAST

# 2. 配置环境
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. 运行
python fast/_fast.py      # CLI
python fast/_fastQt.py    # GUI
```
</details>

<details>
<summary><b>🪟 Windows</b></summary>

```batch
:: 1. 克隆仓库
git clone https://github.com/ChangChuntao/FAST.git && cd FAST

:: 2. 配置环境
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

:: 3. 运行
python fast\_fast.py      :: CLI
python fast\_fastQt.py    :: GUI
```
</details>

---

## ✨ 功能特性

### 📥 数据下载 `fast/download/`

| 功能 | 说明 |
|:----:|:----:|
|  **多线程下载** | 并发下载，自动队列管理 |
|  **智能检测** | 智能本地重复检测和文件验证 |
|  **自动后处理** | 自动解压、转换、拼接、重命名 |
|  **数据类型** | BRDC · SP3 · CLK · OBS · ERP · DCB/OSB · ION/TRO 产品 · SINEX |

### 🔍 质量分析 `fast/qc/`

| 模块 | 功能 | 文件 |
|:----:|:----:|:----:|
|  卫星统计 | 观测计数和可用性 | `satNum.py` |
|  噪声分析 | 伪距和载波相位噪声 | `noise.py` / `CNR.py` |
|  周跳检测 | 检测和统计 | `cycleSlip.py` |
|  IOD | 电离层延迟变化率 | `IOD.py` |
|  多路径效应 | Turboedit 多路径计算 | `multipath.py` |
|  CMC | 码减载波计算 | `CMC.py` |
|  高次差 | 差分分析 | `highOrderDiff.py` |

### 📍 单点定位 `fast/spp/`

| 功能 | 详情 |
|:----:|:----:|
|  算法 | 双频无电离层伪距定位 |
|  GNSS 系统 | GPS + BDS + Galileo |
|  导出 | 多种输出格式 |

### 🗺️ 站点选择 `fast/site/`

| 功能 | 说明 |
|:----:|:----:|
|  过滤器 | GNSS 系统 · 天线/接收机 · 地理边界 · 采样率 |
|  可视化 | 交互式地图界面 |
|  抽稀 | 大数据集精简 (`thinning.py`) |

---

## 📁 项目结构

```
FAST/
├── fast/                    # 源代码
│   ├── _fast.py           # CLI 入口
│   ├── _fastQt.py         # GUI 入口
│   │
│   ├── com/               # 公共模块
│   │   ├── pub.py            # 公共函数
│   │   ├── gnssParameter.py  # GNSS 参数
│   │   ├── gnssTime.py       # 时间转换
│   │   ├── readNav.py        # 导航文件读取
│   │   ├── readObs.py        # 观测文件读取
│   │   └── xyz2blh.py        # 坐标转换
│   │
│   ├── download/           # 下载模块
│   │   ├── mode.py           # 主控制器
│   │   ├── download.py       # 核心逻辑
│   │   ├── ftpSrc.py         # FTP 源配置
│   │   └── arg.py            # CLI 参数
│   │
│   ├── qc/                 # 质量分析模块
│   ├── spp/                # 单点定位模块
│   ├── site/               # 站点选择模块
│   ├── qt/                 # PyQt5 GUI
│   ├── plot/               # 图工具
│   └── build/              # 构建输出
│
├── 📖 manual/                  # 文档
├── 📂 sample_data/             # 示例数据
└── 📦 release/                 # 发布版本
```

---

## 🔧 安装

### 依赖

<div align="center">

| 包 | 用途 | 版本 |
|:--:|:----:|:----:|
| Python | 核心运行环境 | 3.12+ |
| PyQt5 | GUI 框架 | — |
| numpy | 数值计算 | — |
| matplotlib | 图库 | — |
| cartopy | 地图可视化 | — |
| qdarkstyle | 暗色主题 | — |
| qbstyles | 图样式 | — |

</div>

```bash
pip install -r requirements.txt
```

---

## 📦 核心模块

### CLI 控制器 (`fast/download/mode.py`)

```python
runApplication()         # 交互模式
runApplicationWithArgs() # 命令行模式
```

### 单点定位 (`fast/spp/sppbybrdc.py`)

```python
spp()           # 广播星历定位
sppLsq()        # 最小二乘求解
writePosData()  # 导出结果
```

### 公共函数 (`fast/com/pub.py`)

```python
printFast()     # 格式化输出
printPanda()    # 带时间戳日志
mkdir()         # 创建目录
rms()           # 均方根计算
```


## 📝 版本历史

<div align="center">

| 版本 | 日期 | 状态 | 说明 |
|:----:|:----:|:----:|:----:|
| **3.01.00** | 2026-03-17 | 🟢 当前 | Bug 修复 |
| **3.00.03** | 2025-08-02 | 🟢 稳定 | 稳定版本 |
| **3.00.02** | 2024-05-22 | 🟡 旧版 | Bug 修复 |
| **3.00.01** | 2024-01-09 | 🟡 旧版 | v3 大版本更新 |
| **2.11** | 2023-09-20 | 🔴 旧版 | 上一稳定版 |

</div>

> 完整历史见 [`fast/com/pub.py`](fast/com/pub.py)。

---

## 👥 开发团队

<div align="center">

| 角色 | 贡献者 | 单位 | 贡献 |
|:----:|:------:|:----:|:----:|
| **项目负责人** | 常春涛 博士 | 武汉大学卫星导航定位技术研究中心 | 架构设计、核心开发、文档编写 |
| **算法专家** | 蒋科材 博士 | 武汉大学卫星导航定位技术研究中心 | 并行计算优化 |
| **核心开发者** | 慕仁海 博士 | 武汉大学卫星导航定位技术研究中心 | 模块开发、测试 |
| **质量保证** | 李博 博士 | 辽宁工程技术大学 | 测试、用户文档 |
| **技术支持** | 魏恒达 博士 | 武汉大学卫星导航定位技术研究中心 | 验证、教程材料 |

</div>

---

## 📖 文档

- 📄 [完整手册](./manual/FAST_manual-V3.00.pdf)
- 🐛 [问题追踪](https://github.com/ChangChuntao/FAST/issues)

---

## 📧 联系方式

<div align="center">

**常春涛 博士** — chuntaochang@whu.edu.cn

武汉大学卫星导航定位技术研究中心

</div>

---

<div align="center">

<p>
  <a href="https://github.com/ChangChuntao/FAST">🐙 GitHub</a> •
  <a href="https://gitee.com/changchuntao/FAST">🔗 Gitee</a>
</p>

<p>
  <img src="https://img.shields.io/github/stars/ChangChuntao/FAST?style=social" alt="Stars">
  <img src="https://img.shields.io/github/forks/ChangChuntao/FAST?style=social" alt="Forks">
</p>

<br>
<sub>© 2022-2026 FAST 开发团队</sub>

</div>
