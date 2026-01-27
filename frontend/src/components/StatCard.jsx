import React from 'react';

const StatCard = ({ title, value, icon: Icon, color }) => {
    return (
        <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <div style={{
                width: '48px',
                height: '48px',
                borderRadius: '50%',
                backgroundColor: 'var(--bg-secondary)', // Neutral background
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'var(--text-primary)' // Neutral icon color
            }}>
                {Icon && <Icon size={24} />}
            </div>
            <div>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>{title}</p>
                <h3 style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{value}</h3>
            </div>
        </div>
    );
};

export default StatCard;
