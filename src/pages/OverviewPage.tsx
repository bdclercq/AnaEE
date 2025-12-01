import React, { useEffect, useState } from 'react';
import { ValveConfiguration } from '../types/ValveConfiguration';

export default function OverviewPage() {
  const [data, setData] = useState<ValveConfiguration[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      const result = await window.electronAPI.getData();
      setData(result || []);
    };
    fetchData();
  }, []);

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Data Overview</h1>
      <ul>
        {data.map((item, index) => (
          <li key={index}>
            {item.timestamp} | {item.status} | {item.configtype ?? '—'}
          </li>
        ))}
      </ul>
    </div>
  );
}
