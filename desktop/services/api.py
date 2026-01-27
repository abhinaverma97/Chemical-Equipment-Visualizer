import requests
from PyQt5.QtCore import QObject, pyqtSignal, QThread

BASE_URL = "http://127.0.0.1:8000/api"

class Worker(QThread):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

class APIService:
    @staticmethod
    def upload_csv(file_path):
        with open(file_path, 'rb') as f:
            response = requests.post(f"{BASE_URL}/upload/", files={'file': f})
            response.raise_for_status()
            return response.json()

    @staticmethod
    def get_datasets():
        response = requests.get(f"{BASE_URL}/datasets/")
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_details(dataset_id):
        response = requests.get(f"{BASE_URL}/datasets/{dataset_id}/")
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_summary(dataset_id):
        response = requests.get(f"{BASE_URL}/summary/{dataset_id}/")
        response.raise_for_status()
        return response.json()
    
    @staticmethod
    def delete_dataset(dataset_id):
        response = requests.delete(f"{BASE_URL}/datasets/{dataset_id}/")
        response.raise_for_status()
        return True

    @staticmethod
    def get_report_url(dataset_id):
        return f"{BASE_URL}/report/{dataset_id}/"
