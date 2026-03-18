# FAST - File Download and Signal Processing Toolkit for GNSS

**FAST** (File Download and Signal Processing Toolkit for GNSS) is a comprehensive GNSS data processing solution developed by the GNSS Research Center of Wuhan University. Built on Python 3.12 with PyQt5 for GUI, it offers both GUI and CLI interfaces with modular architecture design.

**Current Version**: V3.01.00  
**Development Team**: GNSS Research Center, Wuhan University

The software consists of four core modules: (1) data download, (2) quality analysis, (3) Single Point Positioning, and (4) station selection, providing seamless integration with scientific computing workflows.

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

### Running from Source Code

#### CLI Version
```bash
# Interactive mode
python fast/_fast.py

# Command-line argument mode
python fast/_fast.py [options]
```

#### GUI Version
```bash
python fast/_fastQt.py
```

Or run the packaged executable directly.

### Using Pre-built Binaries

#### For CLI versions
```bash
$ ./FAST
$ ./FAST [options]
```

#### For GUI versions
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

## 📁 Project Structure

```
FAST
├── fast/                    # Main source code directory
│   ├── _fast.py            # CLI entry point
│   ├── _fastQt.py          # GUI entry point
│   ├── com/                # Common modules
│   │   ├── pub.py          # Common functions (printing, file operations)
│   │   ├── gnssParameter.py # GNSS parameter definitions
│   │   ├── gnssTime.py     # Time conversion utilities
│   │   ├── readNav.py      # Navigation file reading
│   │   ├── readObs.py      # Observation file reading
│   │   └── xyz2blh.py      # Coordinate conversion
│   ├── download/           # Data download module
│   │   ├── mode.py         # Download mode main control
│   │   ├── download.py     # Core download logic
│   │   ├── ftpSrc.py       # FTP source configuration
│   │   └── arg.py          # Command-line argument parsing
│   ├── qc/                 # Quality analysis module
│   ├── spp/                # Single Point Positioning module
│   ├── site/               # Station selection module
│   ├── qt/                 # PyQt5 GUI interface
│   ├── plot/               # Plotting module
│   └── build/              # Build directory
├── manual/                  # User manual
├── sample_data/            # Sample data
```

## 📦 Dependencies

- Python 3.12
- PyQt5 - GUI framework
- numpy - Numerical computing
- matplotlib - Plotting library
- cartopy - Map plotting
- qdarkstyle - Dark theme for PyQt5
- qbstyles - Matplotlib styles

## 📝 Coding Standards

1. **File Header Comments**: Each file contains module name, author, copyright, creation date, and version history.
2. **Function Documentation**: Use docstrings to describe parameters and return values.
3. **Naming Conventions**:
   - Function names use lowercase letters and underscores
   - Class names use CamelCase
   - Constants use uppercase letters
4. **Print Functions**: Use `printFast()` and `printPanda()` for formatted output.

## 🔑 Key Classes & Functions

### CLI Controller (`fast/download/mode.py`)
- `runApplication()` - Main function for interactive mode
- `runApplicationWithArgs()` - Main function for command-line argument mode

### SPP Positioning (`fast/spp/sppbybrdc.py`)
- `spp()` - Main function for broadcast ephemeris pseudorange single-point positioning
- `sppLsq()` - Least squares solution
- `writePosData()` - Output positioning results

### Multipath Analysis (`fast/qc/multipath.py`)
- `multipath()` - Multipath effect calculation (Turboedit method)
- `writeMp()` - Output multipath results

### Common Functions (`fast/com/pub.py`)
- `printFast()` - Formatted screen printing
- `printPanda()` - Timestamped printing
- `mkdir()` - Create directory
- `exeCmd()` - Execute command line
- `rms()` - Root mean square calculation

## 📊 Data Type Indexing

The system uses the following indexing methods to distinguish data download types:
- `yd_type` - Year + day of year
- `yds_type` - Year + day of year + station
- `ym_type` - Year + month
- `s_type` - Station
- `no_type` - No time index
- `ydh_type` - Year + day of year + hour
- `ydsh_type` - Year + day of year + station + hour

## 📜 Version History

Latest version updates are recorded in `fast/com/pub.py`. Recent versions:

| Version   | Date       | Notes |
|-----------|------------|-------|
| 3.01.00   | 2026-03-17 | Latest development version |
| 3.00.03   | 2025-08-02 | Stable release |
| 3.00.02   | 2024-05-22 | Bug fixes |
| 3.00.01   | 2024-01-09 | Major update to version 3 |
| 2.11      | 2023-09-20 | Previous stable version |

For complete version history, see `fast/com/pub.py`.

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

## 📞 Contact Information

- **Project Lead**: Dr. Chang Chuntao
- **Email**: chuntaochang@whu.edu.cn
- **Affiliation**: GNSS Research Center, Wuhan University

## 🌐 Repository & Stats  

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-181717?logo=github)](https://github.com/ChangChuntao/FAST)  
[![Gitee Mirror](https://img.shields.io/badge/Gitee-Mirror-C71D23?logo=gitee)](https://gitee.com/changchuntao/FAST)  

<!-- [![Page Views Count](https://badges.toozhao.com/badges/01GK8CXX2CKT5SVRRE7VY71E49/green.svg)](https://badges.toozhao.com/stats/01GK8CXX2CKT5SVRRE7VY71E49 "Get your own page views count badge on badges.toozhao.com") -->