import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QStackedWidget
from PyQt5.QtCore import Qt, QSize
from ui.styles import DARK_THEME_QSS
from ui.dashboard import DashboardWidget
from ui.analytics import AnalyticsWidget
from ui.widgets import CustomTitleBar
from services.api import APIService, Worker

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(1280, 800)
        
        # Central Widget
        central_widget = QWidget()
        central_widget.setObjectName("CentralWidget")
        central_widget.setStyleSheet("#CentralWidget { border: 1px solid #2e2e2e; }") # Scoped Window border
        self.setCentralWidget(central_widget)
        
        # Main Vertical Layout (Title Bar + Content)
        main_v_layout = QVBoxLayout(central_widget)
        main_v_layout.setContentsMargins(0, 0, 0, 0)
        main_v_layout.setSpacing(0)
        
        # Custom Title Bar
        self.title_bar = CustomTitleBar(self)
        main_v_layout.addWidget(self.title_bar)
        
        # Content Area (Horizontal: Sidebar + Stack)
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        main_v_layout.addWidget(content_widget)
        
        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(260)
        self.sidebar.currentRowChanged.connect(self.navigate)
        self.sidebar.addItem("Dashboard")
        self.sidebar.addItem("History (Recent)")
        # Separator hack or just list items
        
        content_layout.addWidget(self.sidebar)
        
        # Content Stack
        self.stack = QStackedWidget()
        content_layout.addWidget(self.stack)
        
        # Pages
        self.api = APIService()
        self.dashboard_page = DashboardWidget(self.api, Worker)
        self.analytics_page = AnalyticsWidget(self.api, Worker)
        
        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.analytics_page)
        
        # Connect Signals
        self.dashboard_page.fileUploaded.connect(self.on_file_uploaded)
        self.sidebar.itemClicked.connect(self.on_sidebar_click)
        
        # Initial Load
        self.load_history()

    def navigate(self, index):
        # Index 0 is Dashboard. 
        # History items start from index 2 (Label 'History' is 1)
        if index == 0:
            self.stack.setCurrentIndex(0)

    def on_sidebar_click(self, item):
        if item.text() == "Dashboard":
            self.stack.setCurrentIndex(0)
        elif item.data(Qt.UserRole): # It's a dataset
            dataset_id = item.data(Qt.UserRole)
            self.analytics_page.load_data(dataset_id)
            self.stack.setCurrentIndex(1)

    def contextMenuEvent(self, event):
        item = self.sidebar.itemAt(self.sidebar.mapFromGlobal(event.globalPos()))
        if item and item.data(Qt.UserRole):
            from PyQt5.QtWidgets import QMenu
            menu = QMenu(self)
            delete_action = menu.addAction("Delete Dataset")
            action = menu.exec_(event.globalPos())
            if action == delete_action:
                self.delete_dataset(item.data(Qt.UserRole))

    def delete_dataset(self, dataset_id):
        self.worker = Worker(self.api.delete_dataset, dataset_id)
        self.worker.finished.connect(lambda: self.load_history()) # Reload after delete
        self.worker.start()

    def on_file_uploaded(self, response):
        dataset_id = response['id']
        self.load_history() # Refresh list
        self.analytics_page.load_data(dataset_id)
        self.stack.setCurrentIndex(1) # Switch to Analytics

    def load_history(self):
        self.sidebar.clear()
        self.sidebar.addItem("Dashboard")
        
        header_item = QListWidget().item(0) # Dummy
        # Just add text "History" non-selectable ideally, but for now simple list item
        
        self.sidebar.addItem("--- History ---")
        
        self.worker = Worker(self.api.get_datasets)
        self.worker.finished.connect(self.update_sidebar_list)
        self.worker.start()

    def update_sidebar_list(self, datasets):
        for ds in datasets:
            from PyQt5.QtWidgets import QListWidgetItem
            item = QListWidgetItem(ds['filename'])
            item.setData(Qt.UserRole, ds['id'])
            self.sidebar.addItem(item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_THEME_QSS)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())
