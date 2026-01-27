from django.urls import path
from .views import UploadCSVView, DatasetListView, DatasetDetailView, SummaryView, ReportView

urlpatterns = [
    path('upload/', UploadCSVView.as_view(), name='upload_csv'),
    path('datasets/', DatasetListView.as_view(), name='dataset_list'),
    path('datasets/<int:id>/', DatasetDetailView.as_view(), name='dataset_detail'),
    path('summary/<int:id>/', SummaryView.as_view(), name='dataset_summary'),
    path('report/<int:id>/', ReportView.as_view(), name='generate_report'),
]
