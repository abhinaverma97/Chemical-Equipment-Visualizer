import React, { useState } from 'react';
import { NavLink, useNavigate, useLocation } from 'react-router-dom';
import { LayoutDashboard, FileText, Trash2 } from 'lucide-react';
import * as api from '../services/api';

const Sidebar = ({ datasets, onSelectDataset, onDeleteDataset }) => {
    return (
        <aside style={{
            width: '260px',
            backgroundColor: 'var(--bg-secondary)',
            borderRight: '1px solid var(--border)',
            display: 'flex',
            flexDirection: 'column',
            height: '100vh',
            position: 'fixed'
        }}>
            <div style={{ padding: '1.5rem', borderBottom: '1px solid var(--border)' }}>
                <h1 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: 'var(--text-primary)' }}>
                    ChemVisualizer
                </h1>
            </div>

            <nav style={{ flex: 1, padding: '1rem' }}>
                <div style={{ marginBottom: '2rem' }}>
                    <NavLink
                        to="/"
                        className={({ isActive }) => `btn ${isActive ? 'btn-primary' : ''}`}
                        style={{
                            width: '100%',
                            justifyContent: 'flex-start',
                            marginBottom: '0.5rem',
                            backgroundColor: ({ isActive }) => isActive ? 'var(--accent)' : 'transparent',
                            color: 'var(--text-primary)'
                        }}
                    >
                        <LayoutDashboard size={18} /> Dashboard
                    </NavLink>
                </div>

                <div>
                    <p style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: 'var(--text-secondary)', marginBottom: '0.5rem', fontWeight: 600 }}>
                        History (Last 5)
                    </p>
                    {datasets.length === 0 ? (
                        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>No history yet.</p>
                    ) : (
                        datasets.map((ds) => (
                            <div
                                key={ds.id}
                                style={{
                                    padding: '0.5rem',
                                    borderRadius: '6px',
                                    fontSize: '0.9rem',
                                    color: 'var(--text-secondary)',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'space-between',
                                    marginBottom: '0.25rem',
                                    transition: 'background 0.2s',
                                    cursor: 'pointer'
                                }}
                                onMouseEnter={(e) => {
                                    e.currentTarget.style.backgroundColor = 'var(--bg-card)';
                                    e.currentTarget.style.color = 'var(--text-primary)';
                                }}
                                onMouseLeave={(e) => {
                                    e.currentTarget.style.backgroundColor = 'transparent';
                                    e.currentTarget.style.color = 'var(--text-secondary)';
                                }}
                            >
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flex: 1 }} onClick={() => onSelectDataset(ds.id)}>
                                    <FileText size={16} /> {ds.filename}
                                </div>
                                <Trash2
                                    size={16}
                                    style={{ color: 'var(--error)', cursor: 'pointer', opacity: 0.7 }}
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        if (window.confirm('Delete this dataset?')) onDeleteDataset(ds.id);
                                    }}
                                    onMouseEnter={(e) => e.target.style.opacity = 1}
                                    onMouseLeave={(e) => e.target.style.opacity = 0.7}
                                />
                            </div>
                        ))
                    )}
                </div>
            </nav>
        </aside>
    );
};

const Layout = ({ children, datasets = [], onSelectDataset, onDeleteDataset }) => {
    return (
        <div style={{ display: 'flex', minHeight: '100vh' }}>
            <Sidebar datasets={datasets} onSelectDataset={onSelectDataset} onDeleteDataset={onDeleteDataset} />
            <main style={{
                flex: 1,
                marginLeft: '260px',
                padding: '2rem',
                backgroundColor: 'var(--bg-primary)'
            }}>
                <div className="container">
                    {children}
                </div>
            </main>
        </div>
    );
};

export default Layout;
