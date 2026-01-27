
DARK_THEME_QSS = """
/* Global */
QWidget {
    background-color: #0a0a0a;
    color: #ffffff;
    font-family: 'Inter', 'Segoe UI', sans-serif;
    font-size: 14px;
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: #171717;
    width: 6px;
    margin: 0px 0px 0px 0px;
}
QScrollBar::handle:vertical {
    background: #3f3f46;
    min-height: 20px;
    border-radius: 3px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Sidebar */
QListWidget {
    background-color: #171717;
    border-right: 1px solid #2e2e2e;
    outline: none;
    padding-top: 10px;
}
QListWidget::item {
    padding: 12px 16px;
    margin: 4px 12px;
    border-radius: 6px;
    color: #a3a3a3;
    border: 1px solid transparent;
}
QListWidget::item:selected {
    background-color: #2563eb;
    color: #ffffff;
    border: none;
}
QListWidget::item:hover {
    background-color: #1f1f1f;
    color: #ffffff;
}

/* Cards & Frames */
QFrame#Card {
    background-color: #09090b;
    border: 1px solid #27272a;
    border-radius: 12px;
}

/* Buttons */
QPushButton {
    background-color: #ffffff;
    color: #000000;
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    font-weight: 600;
    font-size: 13px;
}
QPushButton:hover {
    background-color: #e4e4e7;
}
QPushButton:pressed {
    background-color: #d4d4d8;
}
QPushButton#UploadButton {
    background-color: rgba(255, 255, 255, 0.03);
    color: #a1a1aa;
    border: 1px dashed #3f3f46;
    border-radius: 12px;
    text-align: center;
    padding: 40px;
    font-size: 16px;
}
QPushButton#UploadButton:hover {
    border-color: #71717a;
    background-color: rgba(255, 255, 255, 0.05);
    color: #ffffff;
}

/* Tables */
QTableWidget {
    background-color: #0a0a0a;
    gridline-color: #27272a;
    border: 1px solid #27272a;
    border-radius: 12px;
    selection-background-color: #18181b;
}
QHeaderView::section {
    background-color: #09090b;
    padding: 12px;
    border: none;
    border-bottom: 1px solid #27272a;
    color: #71717a;
    font-weight: 600;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
QTableWidget::item {
    padding: 8px;
    border-bottom: 1px solid #27272a;
}
QTableWidget::item:selected {
     background-color: #18181b;
}

/* Labels */
QLabel#Title {
    font-size: 24px;
    font-weight: 700;
    color: #ffffff;
    padding-bottom: 4px;
}
QLabel#Subtitle {
    font-size: 13px;
    color: #a3a3a3;
}

/* Custom Title Bar */
QWidget#CustomTitleBar {
    background-color: #0a0a0a;
    border-bottom: 1px solid #2e2e2e;
}

QPushButton.TitleBtn {
    background-color: transparent;
    border: none;
    border-radius: 0px;
    color: #a3a3a3;
    font-size: 12px;
    padding: 8px 12px;
}

QPushButton.TitleBtn:hover {
    background-color: #1f1f1f;
    color: #ffffff;
}

QPushButton#CloseBtn:hover {
    background-color: #ef4444;
    color: #ffffff;
}

/* Tabs */
QTabWidget::pane {
    border: 1px solid #2e2e2e;
    background-color: #0a0a0a;
    border-radius: 8px;
}
QTabWidget::tab-bar {
    left: 5px;
}
QTabBar::tab {
    background: #171717;
    color: #a3a3a3;
    padding: 8px 16px;
    margin-right: 2px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    border: 1px solid #2e2e2e;
    border-bottom: none;
}
QTabBar::tab:selected {
    background: #0a0a0a;
    color: #ffffff;
    border-bottom: 1px solid #0a0a0a; /* Merge with pane */
}
QTabBar::tab:hover {
    background: #1f1f1f;
    color: #e4e4e7;
}
"""
