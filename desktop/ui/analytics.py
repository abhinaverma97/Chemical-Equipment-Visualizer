from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QPushButton, QTabWidget)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from .widgets import TitleBar, StatCard
import webbrowser

class ChartTab(QWidget):
    def __init__(self, title):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        self.figure = Figure(figsize=(5, 6), dpi=100)
        self.figure.patch.set_facecolor('#0a0a0a')
        
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background-color: #0a0a0a; border-radius: 8px;")
        
        layout.addWidget(self.canvas)
        self.setLayout(layout)

class AnalyticsWidget(QWidget):
    def __init__(self, api_service, worker_class):
        super().__init__()
        self.api = api_service
        self.Worker = worker_class
        self.dataset_id = None
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(20)
        
        # Header
        top_bar = QHBoxLayout()
        self.header = TitleBar("Analysis Report", "Loading...")
        top_bar.addWidget(self.header)
        
        self.download_btn = QPushButton("Download PDF")
        self.download_btn.clicked.connect(self.download_pdf)
        self.download_btn.setVisible(False)
        top_bar.addWidget(self.download_btn)
        
        self.layout.addLayout(top_bar)
        
        # Stats Row
        self.stats_layout = QHBoxLayout()
        self.layout.addLayout(self.stats_layout)
        
        # Content Area (Table Left, Charts Tabs Right)
        self.content_layout = QHBoxLayout()
        
        # Table Column
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Name", "Type", "Flow", "Press", "Temp"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.content_layout.addWidget(self.table, stretch=2)
        
        # Charts Column (Tabs)
        self.tabs = QTabWidget()
        self.tab_dist = ChartTab("Distribution")
        self.tab_flow = ChartTab("FlowRate")
        self.tab_press = ChartTab("Pressure")
        self.tab_temp = ChartTab("Temperature")
        
        self.tabs.addTab(self.tab_dist, "Distribution")
        self.tabs.addTab(self.tab_flow, "FlowRate")
        self.tabs.addTab(self.tab_press, "Pressure")
        self.tabs.addTab(self.tab_temp, "Temperature")
        
        self.content_layout.addWidget(self.tabs, stretch=3)
        
        self.layout.addLayout(self.content_layout)
        self.setLayout(self.layout)

    def load_data(self, dataset_id):
        self.dataset_id = dataset_id
        self.header.sub.setText(f"Dataset ID: {dataset_id}")
        self.table.setRowCount(0)
        
        self.worker_summary = self.Worker(self.api.get_summary, dataset_id)
        self.worker_summary.finished.connect(self.render_summary)
        self.worker_summary.start()
        
        self.worker_details = self.Worker(self.api.get_details, dataset_id)
        self.worker_details.finished.connect(self.render_details)
        self.worker_details.start()

    def render_summary(self, data):
        # Stats
        while self.stats_layout.count():
            item = self.stats_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
            
        stats = [
            ("Total Equipment", data['count'], "#8b5cf6"),
            ("Avg Flowrate", f"{data['averages']['flowrate']:.1f}", "#2563eb"),
            ("Avg Pressure", f"{data['averages']['pressure']:.2f}", "#10b981"),
            ("Avg Temperature", f"{data['averages']['temperature']:.1f}", "#ef4444"),
        ]
        
        for title, val, color in stats:
            self.stats_layout.addWidget(StatCard(title, val, color))
            
        # Distribution Chart
        fig = self.tab_dist.figure
        fig.clear()
        ax = fig.add_subplot(111)
        ax.set_facecolor('#0a0a0a')
        
        dist = data['distribution']
        labels = list(dist.keys())
        values = list(dist.values())
        
        # Expanded Palette to avoid duplicates
        colors = [
            "#2563eb", "#10b981", "#ef4444", "#8b5cf6", "#f59e0b", 
            "#ec4899", "#6366f1", "#14b8a6", "#f97316", "#84cc16"
        ]
                  
        wedges, _ = ax.pie(values, startangle=90, colors=colors)
        centre_circle = plt.Circle((0,0),0.65,fc='#0a0a0a')
        ax.add_artist(centre_circle)
        
        # Legend inside
        ax.legend(wedges, labels, loc="center", frameon=False, labelcolor='#a3a3a3', fontsize=7)
        
        self.tab_dist.canvas.draw()
        self.download_btn.setVisible(True)

    def render_details(self, data):
        self.table.setRowCount(len(data))
        for row, item in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(str(item['name'])))
            self.table.setItem(row, 1, QTableWidgetItem(str(item['type'])))
            self.table.setItem(row, 2, QTableWidgetItem(str(item['flowrate'])))
            self.table.setItem(row, 3, QTableWidgetItem(str(item['pressure'])))
            self.table.setItem(row, 4, QTableWidgetItem(str(item['temperature'])))

        top_10 = data[:10]
        names = [x['name'] for x in top_10]
        
        # Pass 'white' as color for all bars
        self.plot_bar(self.tab_flow, names, [x['flowrate'] for x in top_10], "Flowrate", "white")
        self.plot_bar(self.tab_press, names, [x['pressure'] for x in top_10], "Pressure", "white")
        self.plot_bar(self.tab_temp, names, [x['temperature'] for x in top_10], "Temperature", "white")

    def plot_bar(self, tab, x_data, y_data, title, color):
        fig = tab.figure
        fig.clear()
        ax = fig.add_subplot(111)
        ax.set_facecolor('#0a0a0a')
        
        # Ensure pure RGBA tuple if passing string (Matplotlib can be picky, but hex works usually if no alpha)
        # Using simple hex for solid color
        bars = ax.bar(x_data, y_data, color=color, alpha=0.6, width=0.6)
        
        # Add values on top
        # for bar in bars:
        #    height = bar.get_height()
        #    ax.text(bar.get_x() + bar.get_width()/2., height,
        #            f'{height:.1f}', ha='center', va='bottom', color='#a3a3a3', fontsize=8)

        ax.set_title(f"Top 10 {title}", color='#e4e4e7', pad=10)
        ax.tick_params(axis='x', rotation=45, colors='#a3a3a3', labelsize=8)
        ax.tick_params(axis='y', colors='#a3a3a3', labelsize=8)
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('#2e2e2e')
        ax.spines['left'].set_color('#2e2e2e')
        
        fig.tight_layout()
        tab.canvas.draw()

    def download_pdf(self):
        if self.dataset_id:
            url = self.api.get_report_url(self.dataset_id)
            webbrowser.open(url)
