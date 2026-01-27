import React, { useState, useMemo } from 'react';
import { ArrowUpDown, ArrowUp, ArrowDown } from 'lucide-react';

const DataTable = ({ data }) => {
    const [sortConfig, setSortConfig] = useState({ key: null, direction: 'ascending' });

    if (!data || data.length === 0) return <p>No data available.</p>;

    const sortedData = useMemo(() => {
        let sortableItems = [...data];
        if (sortConfig.key !== null) {
            sortableItems.sort((a, b) => {
                if (a[sortConfig.key] < b[sortConfig.key]) {
                    return sortConfig.direction === 'ascending' ? -1 : 1;
                }
                if (a[sortConfig.key] > b[sortConfig.key]) {
                    return sortConfig.direction === 'ascending' ? 1 : -1;
                }
                return 0;
            });
        }
        return sortableItems;
    }, [data, sortConfig]);

    const requestSort = (key) => {
        let direction = 'ascending';
        if (sortConfig.key === key && sortConfig.direction === 'ascending') {
            direction = 'descending';
        }
        setSortConfig({ key, direction });
    };

    const getSortIcon = (key) => {
        if (sortConfig.key !== key) return <ArrowUpDown size={14} style={{ opacity: 0.3 }} />;
        return sortConfig.direction === 'ascending' ? <ArrowUp size={14} /> : <ArrowDown size={14} />;
    };

    const columns = [
        { key: 'name', label: 'Equipment Name' },
        { key: 'type', label: 'Type' },
        { key: 'flowrate', label: 'Flowrate' },
        { key: 'pressure', label: 'Pressure' },
        { key: 'temperature', label: 'Temperature' },
    ];

    return (
        <div style={{ overflowX: 'auto', borderRadius: '8px', border: '1px solid var(--border)' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.9rem' }}>
                <thead style={{ backgroundColor: 'var(--bg-secondary)', color: 'var(--text-secondary)' }}>
                    <tr>
                        {columns.map((col) => (
                            <th
                                key={col.key}
                                onClick={() => requestSort(col.key)}
                                style={{
                                    padding: '0.75rem',
                                    cursor: 'pointer',
                                    userSelect: 'none',
                                    transition: 'color 0.2s'
                                }}
                                onMouseEnter={(e) => e.target.style.color = 'var(--text-primary)'}
                                onMouseLeave={(e) => e.target.style.color = 'var(--text-secondary)'}
                            >
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                    {col.label}
                                    {getSortIcon(col.key)}
                                </div>
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {sortedData.map((item, index) => (
                        <tr key={index} style={{ borderTop: '1px solid var(--border)' }}>
                            <td style={{ padding: '0.75rem', fontWeight: 500 }}>{item.name}</td>
                            <td style={{ padding: '0.75rem' }}>
                                <span style={{
                                    padding: '0.25rem 0.5rem',
                                    borderRadius: '4px',
                                    backgroundColor: 'rgba(255, 255, 255, 0.05)',
                                    color: 'var(--text-secondary)',
                                    fontSize: '0.8rem'
                                }}>
                                    {item.type}
                                </span>
                            </td>
                            <td style={{ padding: '0.75rem' }}>{item.flowrate}</td>
                            <td style={{ padding: '0.75rem' }}>{item.pressure}</td>
                            <td style={{ padding: '0.75rem' }}>{item.temperature}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default DataTable;
