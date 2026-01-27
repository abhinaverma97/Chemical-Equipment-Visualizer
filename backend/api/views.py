import pandas as pd
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

from .models import Dataset, Equipment
from .serializers import DatasetSerializer, EquipmentSerializer

class UploadCSVView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        if 'file' not in request.FILES:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)
            
        file = request.FILES['file']
        try:
            df = pd.read_csv(file)
        except Exception as e:
            return Response({"error": f"Failed to parse CSV: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate columns
        required_cols = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
        if not all(col in df.columns for col in required_cols):
            return Response({"error": f"Invalid columns. Required: {required_cols}"}, status=status.HTTP_400_BAD_REQUEST)

        # Create Dataset
        dataset = Dataset.objects.create(filename=file.name)
        
        # Bulk Create Equipment
        equipment_list = [
            Equipment(
                dataset=dataset,
                name=row['Equipment Name'],
                type=row['Type'],
                flowrate=row['Flowrate'],
                pressure=row['Pressure'],
                temperature=row['Temperature']
            )
            for _, row in df.iterrows()
        ]
        Equipment.objects.bulk_create(equipment_list)

        # Cleanup old datasets (Keep last 5)
        ids_to_keep = list(Dataset.objects.order_by('-uploaded_at')[:5].values_list('id', flat=True))
        if ids_to_keep:
            Dataset.objects.exclude(id__in=ids_to_keep).delete()

        return Response({"id": dataset.id, "message": "Upload Successful"}, status=status.HTTP_201_CREATED)

class DatasetListView(APIView):
    def get(self, request):
        datasets = Dataset.objects.order_by('-uploaded_at')
        serializer = DatasetSerializer(datasets, many=True)
        return Response(serializer.data)

class DatasetDetailView(APIView):
    def delete(self, request, id):
        try:
            dataset = Dataset.objects.get(id=id)
            dataset.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Dataset.DoesNotExist:
            return Response({"error": "Dataset not found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        try:
            dataset = Dataset.objects.get(id=id)
        except Dataset.DoesNotExist:
            return Response({"error": "Dataset not found"}, status=status.HTTP_404_NOT_FOUND)
        
        equipment = dataset.equipment.all()
        serializer = EquipmentSerializer(equipment, many=True)
        return Response(serializer.data)

class SummaryView(APIView):
    def get(self, request, id):
        try:
            dataset = Dataset.objects.get(id=id)
        except Dataset.DoesNotExist:
            return Response({"error": "Dataset not found"}, status=status.HTTP_404_NOT_FOUND)
            
        df = pd.DataFrame(list(dataset.equipment.values('type', 'flowrate', 'pressure', 'temperature')))
        
        if df.empty:
             return Response({
                "count": 0,
                "averages": {},
                "distribution": {}
            })

        summary = {
            "count": len(df),
            "averages": {
                "flowrate": df['flowrate'].mean(),
                "pressure": df['pressure'].mean(),
                "temperature": df['temperature'].mean()
            },
            "distribution": df['type'].value_counts().to_dict()
        }
        return Response(summary)

class ReportView(APIView):
    def get(self, request, id):
        try:
            dataset = Dataset.objects.get(id=id)
        except Dataset.DoesNotExist:
            return Response({"error": "Dataset not found"}, status=status.HTTP_404_NOT_FOUND)
            
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_{dataset.id}.pdf"'

        p = canvas.Canvas(response, pagesize=letter)
        p.drawString(100, 750, f"Report for Dataset: {dataset.filename}")
        p.drawString(100, 730, f"Uploaded at: {dataset.uploaded_at}")

        df = pd.DataFrame(list(dataset.equipment.values('type', 'flowrate', 'pressure', 'temperature')))
        
        if not df.empty:
            avg_flow = df['flowrate'].mean()
            avg_press = df['pressure'].mean()
            avg_temp = df['temperature'].mean()
            
            p.drawString(100, 700, "Summary Statistics:")
            p.drawString(120, 680, f"Average Flowrate: {avg_flow:.2f}")
            p.drawString(120, 665, f"Average Pressure: {avg_press:.2f}")
            p.drawString(120, 650, f"Average Temperature: {avg_temp:.2f}")
            
            p.drawString(100, 620, "Equipment Type Distribution:")
            y = 600
            for eq_type, count in df['type'].value_counts().items():
                p.drawString(120, y, f"{eq_type}: {count}")
                y -= 15

        p.showPage()
        p.save()
        return response
