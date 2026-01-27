import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Activity, Gauge, Thermometer, Droplets, Download } from 'lucide-react';
import * as api from '../services/api';
import StatCard from '../components/StatCard';
import DataTable from '../components/DataTable';
import { DistributionChart, ParametersChart } from '../components/Charts';

const Analytics = () => {
    const { id } = useParams();
    const [details, setDetails] = useState([]);
    const [summary, setSummary] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadData = async () => {
            setLoading(true);
            try {
                const [detailsRes, summaryRes] = await Promise.all([
                    api.fetchDatasetDetails(id),
                    api.fetchSummary(id)
                ]);
                setDetails(detailsRes.data);
                setSummary(summaryRes.data);
            } catch (err) {
                console.error("Failed to fetch data", err);
            } finally {
                setLoading(false);
            }
        };

        if (id) loadData();
    }, [id]);

    const handleDownload = () => {
        window.open(api.getReportUrl(id), '_blank');
    };

    if (loading) return <div style={{ color: 'var(--text-secondary)' }}>Loading analytics...</div>;
    if (!summary) return <div style={{ color: 'var(--error)' }}>Failed to load data.</div>;

    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <div>
                    <h2 style={{ fontSize: '1.875rem', fontWeight: 'bold' }}>Analysis Report</h2>
                    <p style={{ color: 'var(--text-secondary)' }}>Dataset ID: {id}</p>
                </div>

                <button className="btn btn-primary" onClick={handleDownload}>
                    <Download size={18} /> Download PDF
                </button>
            </div>

            {/* Stats Grid */}
            <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
                gap: '1.5rem',
                marginBottom: '2rem'
            }}>
                <StatCard title="Total Equipment" value={summary.count} icon={Activity} />
                <StatCard title="Avg Flowrate" value={summary.averages.flowrate?.toFixed(1) || 0} icon={Droplets} />
                <StatCard title="Avg Pressure" value={summary.averages.pressure?.toFixed(2) || 0} icon={Gauge} />
                <StatCard title="Avg Temperature" value={summary.averages.temperature?.toFixed(1) || 0} icon={Thermometer} />
            </div>

            {/* Charts Section */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '1.5rem', marginBottom: '2rem' }}>
                <div className="card">
                    <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem' }}>Equipment Distribution</h3>
                    <div style={{ height: '300px', display: 'flex', justifyContent: 'center' }}>
                        <DistributionChart data={summary.distribution} />
                    </div>
                </div>
                <div className="card">
                    <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem' }}>Parameter Comparison (Top 10)</h3>
                    <div style={{ height: '300px' }}>
                        <ParametersChart equipmentList={details} />
                    </div>
                </div>
            </div>

            {/* Data Table */}
            <div className="card">
                <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem' }}>Raw Data</h3>
                <DataTable data={details} />
            </div>
        </div>
    );
};

export default Analytics;
