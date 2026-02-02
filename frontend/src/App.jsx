import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate, useParams } from 'react-router-dom';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import Dashboard from './pages/Dashboard';
import Analytics from './pages/Analytics';
import Login from './pages/Login';
import * as api from './services/api';

const AppContent = () => {
  const [datasets, setDatasets] = useState([]);
  const navigate = useNavigate();

  const fetchDatasets = async () => {
    try {
      const response = await api.fetchDatasets();
      setDatasets(response.data);
    } catch (error) {
      console.error("Failed to fetch history:", error);
    }
  };

  useEffect(() => {
    fetchDatasets();
  }, []);

  const handleSelectDataset = (id) => {
    navigate(`/dataset/${id}`);
  };

  const handleDeleteDataset = async (id) => {
    try {
      await api.deleteDataset(id);
      await fetchDatasets();
      navigate('/');
    } catch (error) {
      console.error("Failed to delete dataset", error);
    }
  };

  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Layout datasets={datasets} onSelectDataset={handleSelectDataset} onDeleteDataset={handleDeleteDataset}>
              <Dashboard onUploadSuccess={fetchDatasets} />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/dataset/:id"
        element={
          <ProtectedRoute>
            <Layout datasets={datasets} onSelectDataset={handleSelectDataset} onDeleteDataset={handleDeleteDataset}>
              <Analytics />
            </Layout>
          </ProtectedRoute>
        }
      />
    </Routes>
  );
};

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;
