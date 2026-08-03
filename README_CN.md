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

<h1>FAST — GNSS 数据下载与信号处理工具包</h1>

<p>
  <a href="https://github.com/ChangChuntao/FAST/releases/tag/v3.01.0">
    <img src="https://img.shields.io/badge/Release-v3.01.00-2ea44f?style=flat-square&logo=github" alt="Release">
  </a>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/Python-3-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
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

<p><em>Flexible And Swift Toolkit for GNSS Data — 中国科学院空天信息创新研究院开发</em></p>

<p>
  <b><a href="#-简介">🎯 简介</a></b> •
  <b><a href="#-功能特性">✨ 功能特性</a></b> •
  <b><a href="#-快速开始">🚀 快速开始</a></b> •
  <b><a href="#-安装">🔧 安装</a></b> •
  <b><a href="#-项目结构">📁 项目结构</a></b> •
  <b><a href="#-版本历史">📝 版本历史</a></b>
</p>

</div>


## 🎯 简介

FAST（**F**lexible **A**nd **S**wift **T**oolkit for GNSS Data）是一套开源的 GNSS 数据处理工具包，覆盖 **数据下载、质量分析、单点定位、站点选择** 四大功能，提供图形界面（GUI）与命令行（CLI）两种使用方式。

![FAST Banner](manual/fig/intro.png)

<div align="center">

| 版本 | 开发单位 | 语言 | 界面 |
|:---:|:---|:---:|:---:|
| **v3.01.00** | 中国科学院空天信息创新研究院 | Python 3 | GUI + CLI |

</div>


---

## ✨ 功能特性

### 📥 数据下载 `src/fast/download/`

- **多线程并发下载**：自动队列管理，断点续传
- **智能检测**：本地重复文件检测与下载完整性校验
- **自动后处理**：下载后自动完成解压、格式转换、数据拼接与重命名
- **数据类型**：BRDC 广播星历 · SP3 精密星历 · CLK 钟差 · OBS 观测数据 · ERP 地球自转参数 · DCB/OSB 偏差产品 · ION/TRO 大气产品 · SINEX 解算结果
- **数据源**：覆盖 IGS 及 WHU、COD、GRG、GFZ、IAC、JAX、SHA 等主要分析中心

### 🔍 质量分析 `src/fast/qc/`

| 模块 | 功能 |
|:---:|:---|
| `satNum` | 卫星观测计数与可用性统计 |
| `noise` | 伪距/载波相位噪声分析（GF 组合三阶差分） |
| `CNR` | 载噪比（Carrier-to-Noise Ratio）分析 |
| `cycleSlip` | 周跳检测与统计 |
| `IOD` | 电离层延迟变化率分析 |
| `multipath` | Turboedit 多路径效应计算 |
| `CMC` | 码减载波（Code minus Phase）计算 |
| `highOrderDiff` | 高次差分分析 |
| `obsFreq` | 观测频率统计 |

### 📍 单点定位 `src/fast/spp/`

- 双频无电离层组合伪距定位
- 支持 GPS、BDS、Galileo 系统
- 流程完整：观测值初始化 → 卫星位置计算 → 大气改正 → 最小二乘求解
- 多种结果输出格式

### 🗺️ 站点选择 `src/fast/site/`

- 全球测站网（IGS）站点筛选与抽稀（`thinning.py`）
- 交互式地图可视化（`plotSite.py`）

### 🖥️ 图形界面 `src/fast/qt/`

基于 PyQt5 的图形界面，集成下载、质量分析、单点定位、站点选择与时间转换等完整操作入口，支持暗色主题与自定义字体。

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

无需配置 `.pth` 等环境变量，从仓库根目录直接运行即可。

<details>
<summary><b>🐧 Linux / 🍎 macOS</b></summary>

```bash
# 1. 克隆仓库
git clone https://github.com/ChangChuntao/FAST.git && cd FAST

# 2. 配置环境
python -m venv venv
source venv/bin/activate
pip install PyQt5 qdarkstyle qbstyles numpy matplotlib cartopy psutil

# 3. 运行
python src/_fast.py      # CLI
python src/_fastQt.py    # GUI
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
pip install PyQt5 qdarkstyle qbstyles numpy matplotlib cartopy psutil

:: 3. 运行
python src\_fast.py      :: CLI
python src\_fastQt.py    :: GUI
```
</details>

---

## 🔧 安装

### 依赖

<div align="center">

| 包 | 用途 |
|:---:|:---|
| PyQt5 | GUI 框架 |
| numpy | 数值计算 |
| matplotlib | 绘图 |
| cartopy | 地图可视化 |
| qdarkstyle | 暗色主题 |
| qbstyles | 绘图样式 |
| psutil | 系统进程监控 |

</div>

```bash
pip install PyQt5 qdarkstyle qbstyles numpy matplotlib cartopy psutil
```

---

## 📁 项目结构

```
FAST/
├── src/                       # 源代码
│   ├── _fast.py               # CLI 入口
│   ├── _fastQt.py             # GUI 入口
│   │
│   ├── fast/                  # 核心包
│   │   ├── com/               # 公共模块（时间/坐标/文件读写/版本）
│   │   ├── download/          # 数据下载模块
│   │   ├── qc/                # 质量分析模块
│   │   ├── spp/               # 单点定位模块
│   │   ├── site/              # 站点选择模块
│   │   ├── qt/                # PyQt5 图形界面
│   │   ├── plot/              # 绘图模块
│   │   └── bin/               # 第三方工具（crx2rnx/teqc/gzip 等）
│   │
│   └── win_bin/               # 界面资源（字体/图标/配置文件）
│
├── 📖 manual/                  # 用户手册（PDF）
├── 📂 sample_data/             # 示例数据
└── 📦 winVenv/                 # Windows 虚拟环境
```

---

## 📦 模块详解

### 公共模块 `src/fast/com/`

| 文件 | 功能 |
|:---|:---|
| `pub.py` | 公共函数（格式化输出/日志/目录管理）与版本历史 |
| `gnssParameter.py` | GNSS 系统参数 |
| `gnssTime.py` | 时间系统转换 |
| `readNav.py` / `readObs.py` | 导航文件 / 观测文件读取 |
| `writeClk.py` / `writeObs.py` / `writeSiteInf.py` | 钟差 / 观测值 / 站点信息输出 |
| `xyz2blh.py` / `xyz2neu.py` / `xy2azi.py` | 坐标转换 |
| `nav2posclk.py` | 广播星历反算卫星位置与钟差 |
| `sat2siteAngle.py` | 卫星与测站几何关系（高度角/方位角） |
| `mgexInf.py` / `mgexSite.py` | MGEX 产品信息 / 站点信息 |
| `readSiteinfo.py` | 站点信息文件读取 |

### 下载模块 `src/fast/download/`

| 文件 | 功能 |
|:---|:---|
| `mode.py` | 主控制器（交互模式 / 命令行模式） |
| `download.py` | 下载核心逻辑 |
| `ftpSrc.py` / `loadFtpSrc.py` | FTP 数据源配置与加载 |
| `menu.py` | 交互式菜单 |
| `arg.py` | 命令行参数解析 |
| `dataInf.py` / `inf.py` | 数据信息管理 |
| `fileOperation.py` | 文件后处理（解压/转换/拼接） |

### 质量分析 `src/fast/qc/`

见上方功能特性表，各模块独立成文件（`satNum.py` / `noise.py` / `CNR.py` / `cycleSlip.py` / `IOD.py` / `multipath.py` / `CMC.py` / `highOrderDiff.py` / `obsFreq.py`）。

### 单点定位 `src/fast/spp/`

| 文件 | 功能 |
|:---|:---|
| `sppbybrdc.py` | 广播星历定位主程序（`spp()` / `sppLsq()` / `writePosData()`） |
| `initObs.py` | 观测值初始化 |
| `satPos.py` | 卫星位置计算 |
| `corr.py` | 误差改正（相对论/潮汐等） |
| `trop.py` | 对流层延迟改正 |

### 站点选择 `src/fast/site/`

| 文件 | 功能 |
|:---|:---|
| `thinning.py` | 测站抽稀（按格网密度采样） |

### 图形界面 `src/fast/qt/`

| 文件 | 功能 |
|:---|:---|
| `qtFrame.py` | 无边框主窗口（标题栏/窗口控制） |
| `qtInitUI.py` | 界面初始化入口 |
| `qtDownload.py` / `qtQc.py` / `qtSpp.py` / `qtSite.py` | 各模块操作界面 |
| `timeTran.py` | 时间转换界面 |
| `qtStyle.py` | 界面样式 |

### 绘图模块 `src/fast/plot/`

`plotSatNum` / `plotCnr` / `plotCMC` / `plotCycleSlip` / `plotFreq` / `plotHighOrderDiff` / `plotIOD` / `plotLnoise` / `plotMultipath` / `plotSite` —— 各质量分析结果的图形输出。

---

## 📝 版本历史

<div align="center">

| 版本 | 日期 | 版本 | 日期 | 版本 | 日期 |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 1.00 | 2022-03-27 | 1.15 | 2022-07-03 | 2.05 | 2022-12-04 |
| 1.10 | 2022-04-12 | 1.16 | 2022-07-13 | 2.06 | 2023-01-14 |
| 1.11 | 2022-04-22 | 1.17 | 2022-07-22 | 2.07 | 2023-02-10 |
| 1.12 | 2022-04-30 | 1.18 | 2022-07-28 | 2.08 | 2023-03-17 |
| 1.13 | 2022-05-24 | 1.19 | 2022-08-04 | 2.09 | 2023-06-30 |
| 1.14 | 2022-05-31 | 1.20 | 2022-09-11 | 2.10 | 2023-08-11 |
| 1.21 | 2022-09-16 | 1.22 | 2022-09-20 | 2.11 | 2023-09-20 |
| 1.23 | 2022-09-28 | 1.24 | 2022-10-10 | 1.25 | 2022-11-02 |
| 2.01 | 2022-11-09 | 2.02 | 2022-11-10 | 2.03 | 2022-11-15 |
| 2.04 | 2022-12-02 | 3.00.01 | 2024-01-09 | 3.00.02 | 2024-05-22 |
| 3.00.03 | 2025-08-02 | **3.01.00** | 2026-03-17 | | |

</div>

---

## 👥 开发团队

<div align="center">

| 角色 | 贡献者 | 单位 | 贡献 |
|:----:|:------:|:----:|:----:|
| **项目负责人** | 常春涛 博士 | 中国科学院空天信息创新研究院 | 架构设计、核心开发、文档编写 |
| **算法专家** | 蒋科材 博士 | 武汉大学卫星导航定位技术研究中心 | 并行计算优化 |
| **核心开发者** | 慕仁海 博士 | 武汉大学卫星导航定位技术研究中心 | 测试、用户文档 |
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

**常春涛 博士** — changchuntao@aircas.ac.cn

中国科学院空天信息创新研究院

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
