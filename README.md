# FAST - File Download and Signal Processing Toolkit for GNSS

**FAST** is a comprehensive GNSS data processing solution developed in Python 3.12, offering both GUI and CLI interfaces for users of all levels. Built on PyQt5 with modular architecture, it provides seamless integration with scientific computing workflows.The software adopts a modular architecture, consisting of 4 modules: (1) data download, (2) quality analysis, (3) Single Point Positioning, and (4) station selection. 

![FAST Banner](manual/fig/intro.png)


## 📦 Latest Release
[![Latest Release](https://img.shields.io/badge/Download-FAST_V3.00.03-blue)](https://github.com/ChangChuntao/FAST/releases/tag/FAST_V3)

## 🚀 Available Binaries

| Platform       | 🖥️ GUI Version | ⌨️ CLI Version |
|----------------|----------------|----------------|
| **Windows**    | [FastQt_Win_V3.00.03.zip](https://github.com/ChangChuntao/FAST/releases/download/FAST_V3/FastQt_Win_V3.00.03.zip) | [FAST_Win_V3.00.03.zip](https://github.com/ChangChuntao/FAST/releases/download/FAST_V3/FAST_Win_V3.00.03.zip) |
| **macOS (Intel)** | [FastQt_Mac_V3.00.03.zip](https://github.com/ChangChuntao/FAST/releases/download/FAST_V3/FastQt_Mac_V3.00.03.zip) | [FAST_Mac_V3.00.03.zip](https://github.com/ChangChuntao/FAST/releases/download/FAST_V3/FAST_Mac_V3.00.03.zip) |
| **Ubuntu**     | - | [FAST_Ubuntu_V3.00.03.zip](https://github.com/ChangChuntao/FAST/releases/download/FAST_V3/FAST_Ubuntu_V3.00.03.zip) |
| **CentOS**     | - | [FAST_CentOS_V3.00.03.zip](https://github.com/ChangChuntao/FAST/releases/download/FAST_V3/FAST_CentOS_V3.00.03.zip) |

## 🛠️ Installation & Usage

### For CLI versions
```bash
$ ./FAST
$ ./FAST [options]
```

### For GUI versions
Simply double-click the application

## ✨ Key Features

### 📥 **Data Download Module**
- Multi-threaded GNSS data downloading with automatic queue management  
- Intelligent local duplicate detection and file validation  
- Automated post-processing:  
  • Decompression  
  • Format conversion  
  • File concatenation  
  • Standardized renaming  

### 🔍 **Quality Analysis Module**
- Comprehensive RINEX file diagnostics:  
  • Satellite observation counts and availability  
  • Pseudorange & carrier phase noise analysis  
  • Cycle slip detection and statistics  
  • Ionospheric delay variation rates  
- Interactive visualization of quality metrics  

### 📡 **Single Point Positioning Module**
- Dual-frequency ionosphere-free pseudorange positioning  
- Multi-GNSS constellation support:  
  • GPS  
  • BDS  
  • Galileo  
- Beginner-friendly interface with one-click processing  
- Exportable results in multiple formats  

### 📍 **Station Selection Module**
- Flexible filtering options:  
  • By satellite system  
  • By antenna/receiver type  
  • Geographic bounding box  
  • Temporal sampling rate  
- Visual map interface for spatial selection  
- Downsampling capability for large datasets  

## 📚 Documentation  
**Complete user manual**:  `./manual/FAST_manual-V3.00.docx`  

## 👥 Development Team  

| Role                | Contributor         | Affiliation                          | Contributions                     |
|---------------------|---------------------|--------------------------------------|-----------------------------------|
| **Project Lead**    | Dr. Chang Chuntao   | GNSS Research Center, Wuhan University | Architecture, Core Development, Documentation |
| **Algorithm Expert**| Pd. Jiang Kecai     | GNSS Research Center, Wuhan University | Parallel Computing Optimization |
| **Core Developer**  | Dr. Mu Renhai       | GNSS Research Center, Wuhan University | Module Development, Testing |
| **Quality Assurance**| Pd. Li Bo          | Liaoning Technical University        | Testing, User Documentation |
| **Technical Support**| Dr. Wei Hengda     | GNSS Research Center, Wuhan University | Validation, Tutorial Materials |

## 🌐 Repository & Stats  

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-181717?logo=github)](https://github.com/ChangChuntao/FAST)  
[![Gitee Mirror](https://img.shields.io/badge/Gitee-Mirror-C71D23?logo=gitee)](https://gitee.com/changchuntao/FAST)  

[![Page Views Count](https://badges.toozhao.com/badges/01GK8CXX2CKT5SVRRE7VY71E49/green.svg)](https://badges.toozhao.com/stats/01GK8CXX2CKT5SVRRE7VY71E49 "Get your own page views count badge on badges.toozhao.com")