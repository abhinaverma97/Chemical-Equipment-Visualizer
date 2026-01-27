import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate, useParams } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Analytics from './pages/Analytics';
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
    <Layout datasets={datasets} onSelectDataset={handleSelectDataset} onDeleteDataset={handleDeleteDataset}>
      <Routes>
        <Route path="/" element={<Dashboard onUploadSuccess={fetchDatasets} />} />
        <Route path="/dataset/:id" element={<Analytics />} />
      </Routes>
    </Layout>
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
