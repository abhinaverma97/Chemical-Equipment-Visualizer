from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from .widgets import TitleBar

class DashboardWidget(QWidget):
    fileUploaded = pyqtSignal(dict) # Emits upload response

    def __init__(self, api_service, worker_class):
        super().__init__()
        self.api = api_service
        self.Worker = worker_class
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        title = TitleBar("Dashboard", "Upload a chemical equipment CSV file to generate insights.")
        layout.addWidget(title)
        
        self.upload_btn = QPushButton("Click to Upload CSV")
        self.upload_btn.setObjectName("UploadButton")
        self.upload_btn.setFixedSize(400, 200)
        self.upload_btn.clicked.connect(self.browse_file)
        
        self.status_label = QLabel("Supported columns: Equipment Name, Type, Flowrate, Pressure, Temperature")
        self.status_label.setObjectName("Subtitle")
        self.status_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.upload_btn, alignment=Qt.AlignCenter)
        layout.addWidget(self.status_label, alignment=Qt.AlignCenter)
        
        self.setLayout(layout)

    def browse_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open CSV', 'd:\\lumi\\Projects\\fosse', "CSV Files (*.csv)")
        if fname:
            self.status_label.setText("Uploading...")
            self.worker = self.Worker(self.api.upload_csv, fname)
            self.worker.finished.connect(self.handle_success)
            self.worker.error.connect(self.handle_error)
            self.worker.start()

    def handle_success(self, response):
        self.status_label.setText("Upload Successful!")
        self.fileUploaded.emit(response)

    def handle_error(self, error_msg):
        self.status_label.setText(f"Error: {error_msg}")
        self.status_label.setStyleSheet("color: #ef4444;")
