# -*- coding: utf-8 -*-
# FAST           : Qt Style Definitions
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University
# Creation       : 2026.03.17
def get_input_style():
    """输入框样式"""
    return """
        QLineEdit {
            background-color: #313244;
            color: #cdd6f4;
            border: 1px solid #45475a;
            border-radius: 4px;   /* 圆角微调，配合较小的高度 */
            padding: 4px 8px;     /* 上下留白压到极小 */
            min-height: 22px;     /* 完美锁定 22px */
            max-height: 22px;
        }
        QLineEdit:focus {
            border: 2px solid #89b4fa;
            background-color: #3a3d52;
        }
        QLineEdit:disabled {
            background-color: #1e1e2e;
            color: #6c7086;
        }
    """


def get_combo_style():
    """下拉框样式 - 带下三角箭头"""
    return """
        QComboBox {
            background-color: #313244;
            color: #cdd6f4;
            border: 1px solid #45475a;
            border-radius: 4px;
            padding: 4px 24px 4px 8px; /* 右侧留24px给下拉按钮 */
            min-height: 22px;          /* 与输入框完美对齐 */
            max-height: 22px;           
            min-width: 90px;
        }
        QComboBox:hover {
            border: 1px solid #89b4fa;
            background-color: #3a3d52;
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: center right;
            width: 24px;
            background-color: transparent;
            border: none;
            border-left: 1px solid #45475a;
            border-radius: 0 4px 4px 0;
        }
        QComboBox::down-arrow {
            width: 10px;  /* 箭头稍微缩小以适应 22px 高度 */
            height: 10px;
        }
        QComboBox QAbstractItemView {
            background-color: #313244;
            color: #cdd6f4;
            selection-background-color: #585b70; 
            selection-color: #cdd6f4;
            border: 1px solid #45475a;
            border-radius: 4px;
            padding: 4px;
        }
        QComboBox QAbstractItemView::item {
            padding: 4px 8px;
            border-radius: 2px;
            min-height: 20px; 
        }
        QComboBox QAbstractItemView::item:hover {
            background-color: #45475a;
        }
    """

def get_small_btn_style():
    """小按钮样式（如 ... 按钮）"""
    return """
        QPushButton {
            background-color: #45475a;
            color: #cdd6f4;
            border: none;
            border-radius: 6px;
            padding: 8px 14px;
        }
        QPushButton:hover {
            background-color: #585b70;
        }
        QPushButton:pressed {
            background-color: #313244;
        }
    """


def get_primary_btn_style():
    """主按钮样式 - 统一风格"""
    return """
        QPushButton {
            background-color: #45475a;
            color: #cdd6f4;
            border: 1px solid #585b70;
            border-radius: 8px;
            padding: 12px 32px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #585b70;
            border: 1px solid #7f849c;
        }
        QPushButton:pressed {
            background-color: #313244;
            border: 1px solid #45475a;
        }
    """


def get_danger_btn_style():
    """危险按钮样式（终止按钮）- 统一风格"""
    return """
        QPushButton {
            background-color: #45475a;
            color: #cdd6f4;
            border: 1px solid #585b70;
            border-radius: 8px;
            padding: 12px 32px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #585b70;
            border: 1px solid #7f849c;
        }
        QPushButton:pressed {
            background-color: #313244;
            border: 1px solid #45475a;
        }
    """


def get_save_btn_style():
    """保存按钮样式 - 统一风格"""
    return """
        QPushButton {
            background-color: #45475a;
            color: #cdd6f4;
            border: 1px solid #585b70;
            border-radius: 8px;
            padding: 12px 32px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #585b70;
            border: 1px solid #7f849c;
        }
        QPushButton:pressed {
            background-color: #313244;
            border: 1px solid #45475a;
        }
    """


def get_run_btn_style():
    """运行按钮样式 - 统一风格"""
    return """
        QPushButton {
            background-color: #45475a;
            color: #cdd6f4;
            border: 1px solid #585b70;
            border-radius: 8px;
            padding: 12px 32px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #585b70;
            border: 1px solid #7f849c;
        }
        QPushButton:pressed {
            background-color: #313244;
            border: 1px solid #45475a;
        }
    """


def get_log_style():
    # 日志输出框风格
    return """
    QTextEdit {
        background-color: #181825; /* 更深的背景区分层次 */
        color: #A6E3A1; /* 极客绿文字 */
        border: 1px solid #313244;
        border-radius: 8px;
        padding: 10px;
        font-family: "Consolas", "Courier New", monospace;
    }
    """


def get_tab_style():
    """Tab样式"""
    return """
        QTabBar::tab {
            margin: 1;
            padding: 12px 60px;
        }
    """


def get_qc_plot_tab_style(screen_width, screen_height):
    """QC Plot Tab样式"""
    return """
        QTabBar::tab {
            min-height: 10px;
            max-height: 10px;
            padding: 0px 4px;
            font-size: 18px;
            margin: 1;
        }
    """


def apply_download_styles(widget):
    """应用下载模块样式"""
    input_style = get_input_style()
    combo_style = get_combo_style()
    
    widget.year_line.setStyleSheet(input_style)
    widget.month_line.setStyleSheet(input_style)
    widget.begin_doy_line.setStyleSheet(input_style)
    widget.end_doy_line.setStyleSheet(input_style)
    widget.pro_name_line.setStyleSheet(input_style)
    widget.site_file_line.setStyleSheet(input_style)
    widget.out_dir_line.setStyleSheet(input_style)
    
    widget.data_type_combo.setStyleSheet(combo_style)
    widget.name_type_combo.setStyleSheet(combo_style)
    widget.hour_combo.setStyleSheet(combo_style)
    widget.unzip_combo.setStyleSheet(combo_style)
    widget.pool_combo.setStyleSheet(combo_style)


def apply_qc_styles(widget, open_btn):
    """应用QC模块样式"""
    qc_btn_style = get_primary_btn_style()
    qc_save_style = get_save_btn_style()
    open_btn.setStyleSheet(get_small_btn_style())
    return qc_btn_style, qc_save_style


def apply_spp_styles(widget, obs_btn, nav_btn):
    """应用SPP模块样式"""
    spp_run_style = get_run_btn_style()
    spp_save_style = get_save_btn_style()
    obs_btn.setStyleSheet(get_small_btn_style())
    nav_btn.setStyleSheet(get_small_btn_style())
    return spp_run_style, spp_save_style