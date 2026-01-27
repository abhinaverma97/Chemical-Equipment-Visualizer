import React, { useRef, useState } from 'react';
import { UploadCloud } from 'lucide-react';

const UploadZone = ({ onUpload, isUploading }) => {
    const fileInputRef = useRef(null);
    const [dragActive, setDragActive] = useState(false);

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            onUpload(e.dataTransfer.files[0]);
        }
    };

    const handleChange = (e) => {
        e.preventDefault();
        if (e.target.files && e.target.files[0]) {
            onUpload(e.target.files[0]);
        }
    };

    return (
        <div
            className="card"
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            style={{
                border: `2px dashed ${dragActive ? 'var(--accent)' : 'var(--border)'}`,
                backgroundColor: dragActive ? 'rgba(37, 99, 235, 0.1)' : 'var(--bg-card)',
                textAlign: 'center',
                padding: '3rem',
                cursor: 'pointer',
                transition: 'all 0.2s'
            }}
            onClick={() => fileInputRef.current.click()}
        >
            <input
                ref={fileInputRef}
                type="file"
                accept=".csv"
                onChange={handleChange}
                style={{ display: 'none' }}
            />
            <UploadCloud size={48} style={{ color: 'var(--accent)', marginBottom: '1rem' }} />
            <h3 style={{ fontSize: '1.125rem', marginBottom: '0.5rem' }}>
                {isUploading ? "Uploading..." : "Click to upload or drag and drop"}
            </h3>
            <p style={{ color: 'var(--text-secondary)' }}>CSV files only (Max 10MB)</p>
        </div>
    );
};

export default UploadZone;
