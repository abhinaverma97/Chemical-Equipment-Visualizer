import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import UploadZone from '../components/UploadZone';
import * as api from '../services/api';

const Dashboard = ({ onUploadSuccess }) => {
    const [isUploading, setIsUploading] = useState(false);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleUpload = async (file) => {
        setIsUploading(true);
        setError(null);
        try {
            const response = await api.uploadCSV(file);
            // Response { id: 1, message: "..." }
            await onUploadSuccess(); // Refresh list
            navigate(`/dataset/${response.data.id}`);
        } catch (err) {
            const errorMessage = err.response?.data?.error || "Failed to upload file. Please check format.";
            setError(errorMessage);
        } finally {
            setIsUploading(false);
        }
    };

    return (
        <div>
            <h2 style={{ fontSize: '1.875rem', fontWeight: 'bold', marginBottom: '1rem' }}>Dashboard</h2>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
                Upload a chemical equipment CSV file to generate insights.
            </p>

            {error && (
                <div style={{
                    padding: '1rem',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    color: 'var(--error)',
                    borderRadius: '6px',
                    marginBottom: '1rem'
                }}>
                    {error}
                </div>
            )}

            <UploadZone onUpload={handleUpload} isUploading={isUploading} />

            <div style={{ marginTop: '3rem' }}>
                <h3 style={{ fontSize: '1.25rem', marginBottom: '1rem' }}>Supported Columns</h3>
                <ul style={{ color: 'var(--text-secondary)', lineHeight: '1.8', listStylePosition: 'inside' }}>
                    <li>Equipment Name (String)</li>
                    <li>Type (String)</li>
                    <li>Flowrate (Number)</li>
                    <li>Pressure (Number)</li>
                    <li>Temperature (Number)</li>
                </ul>
            </div>
        </div>
    );
};

export default Dashboard;
