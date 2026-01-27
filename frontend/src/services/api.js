import axios from 'axios';

const API_BASE_URL = window.location.origin + '/api';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const uploadCSV = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/upload/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
};

export const fetchDatasets = async () => {
    return api.get('/datasets/');
};

export const fetchDatasetDetails = async (id) => {
    return api.get(`/datasets/${id}/`);
};

export const fetchSummary = async (id) => {
    return api.get(`/summary/${id}/`);
};

export const getReportUrl = (id) => {
    return `${API_BASE_URL}/report/${id}/`;
};

export const deleteDataset = async (id) => {
    return api.delete(`/datasets/${id}/`);
};

export default api;
