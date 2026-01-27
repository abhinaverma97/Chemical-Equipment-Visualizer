from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class StatCard(QFrame):
    def __init__(self, title, value, color="#ffffff"):
        super().__init__()
        self.setObjectName("Card")
        self.setFixedSize(200, 100)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        self.title_label = QLabel(title)
        self.title_label.setObjectName("Subtitle")
        self.title_label.setAlignment(Qt.AlignCenter)
        
        self.value_label = QLabel(str(value))
        self.value_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        self.value_label.setAlignment(Qt.AlignCenter)
        
        layout.addStretch()
        layout.addWidget(self.value_label)
        layout.addWidget(self.title_label)
        layout.addStretch()
        
        self.setLayout(layout)

class TitleBar(QWidget):
    def __init__(self, title, subtitle=""):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 20)
        
        self.title = QLabel(title)
        self.title.setObjectName("Title")
        
        self.sub = QLabel(subtitle)
        self.sub.setObjectName("Subtitle")
        
        layout.addWidget(self.sub)
        self.setLayout(layout)

from PyQt5.QtWidgets import QPushButton

class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("CustomTitleBar")
        self.setFixedHeight(35)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # App Title/Icon area
        self.title_label = QLabel("CEV - Desktop")
        self.title_label.setStyleSheet("color: #a3a3a3; font-weight: bold; font-size: 12px;")
        self.layout.addWidget(self.title_label)
        
        self.layout.addStretch()
        
        # Window Controls
        self.btn_min = QPushButton("_")
        self.btn_min.setObjectName("MinBtn")
        self.btn_min.setProperty("class", "TitleBtn")
        self.btn_min.clicked.connect(self.window().showMinimized)
        
        self.btn_max = QPushButton("□")
        self.btn_max.setObjectName("MaxBtn")
        self.btn_max.setProperty("class", "TitleBtn")
        self.btn_max.clicked.connect(self.toggle_max)
        
        self.btn_close = QPushButton("✕")
        self.btn_close.setObjectName("CloseBtn")
        self.btn_close.setProperty("class", "TitleBtn")
        self.btn_close.clicked.connect(self.window().close)
        
        for btn in [self.btn_min, self.btn_max, self.btn_close]:
             btn.setFixedSize(45, 35) # Windows style width
             self.layout.addWidget(btn)
             
        self.setLayout(self.layout)
        
        self.start = None

    def toggle_max(self):
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start = event.globalPos()
            self.click_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self.start:
            delta = event.globalPos() - self.start
            self.window().move(self.window().pos() + delta)
            self.start = event.globalPos()
    
    def mouseReleaseEvent(self, event):
        self.start = None
