# Chemical Equipment Visualizer

A hybrid analytics platform (Web + Desktop) for visualizing chemical equipment parameters.

## User Login
 - **Id** - admin
 - **Password** - admin27

## Deployment
http://140.245.19.236/

## Quick Setup

### 1. Backend (Django)
*Required for both Web and Desktop apps.*
```powershell
pip install -r backend/requirements.txt
cd backend
python manage.py migrate
python manage.py runserver
```
> Server runs at `http://127.0.0.1:8000/`

### 2. Frontend Web (React)
```powershell
cd frontend
npm install
npm run dev
```
> Web App runs at `http://localhost:5173/`

### 3. Frontend Desktop (PyQt5)
requires backend running

```powershell
pip install -r desktop/requirements.txt
python desktop/main.py
```

## Overview

The **Chemical Equipment Visualizer** is a full-stack analytics platform designed to process, store, and visualize sensor data from industrial chemical equipment. The system follows a client-server architecture where a robust Django backend serves as the single source of truth for both a web-based management dashboard and a high-performance desktop analytics workstation.

### System Architecture

#### 1. Backend (`/backend`)
The data backbone built with **Django REST Framework**.
-   **Data Ingestion**: Parses uploaded CSV datasets containing equipment definitions and sensor readings (Flowrate, Pressure, Temperature).
-   **Storage**: Relational mapping (SQLite) of `Datasets` and their associated `Equipment` records.
-   **API Layer**: Exposes RESTful endpoints for:
    -   Summary statistics (averages, counts).
    -   Detailed equipment lists.
    -   PDF Report generation using `ReportLab`.

#### 2. Frontend Web (`/frontend`)
A modern **React** application built with **Vite** for data management and quick insights.
-   **Data Management**: Drag-and-drop CSV upload zone with real-time progress feedback.
-   **Interactive Dashboard**: Filterable and sortable data grids to browse equipment records efficiently.
-   **Visualization**: Lightweight charts (Chart.js) for quick distribution analysis.
-   **State Management**: Synced history and "Trash" restoration features.

#### 3. Frontend Desktop (`/desktop`)
A dedicated engineering tool built with **Python**, **PyQt5**, and **Matplotlib** for deep-dive analytics.
-   **Native Experience**: Custom frameless UI with a dark engineering aesthetic (`#0a0a0a`) and window controls.
-   **Advanced Analytics**:
    -   **Distribution Analysis**: Pie charts showing equipment type breakdown.
    -   **Parameter Profiling**: Dedicated tabs for Flowrate, Pressure, and Temperature analysis.
    -   **Top 10 Rankings**: Bar charts highlighting critical equipment based on sensor values.
-   **Reporting**: Direct PDF generation and download integration with the backend.
