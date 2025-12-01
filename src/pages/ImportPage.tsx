import React, { useState, useEffect } from 'react';
import { ValveConfiguration } from '../types/ValveConfiguration';

export default function ImportPage() {
  const [filePath, setFilePath] = useState<string | null>(null);
  const [entries, setEntries] = useState<ValveConfiguration[]>([]);

  const [timestamp, setTimestamp] = useState('');
  const [status, setStatus] = useState('');
  const [configType, setConfigType] = useState<0 | 1 | ''>('');
  const [editIndex, setEditIndex] = useState<number | null>(null);

  const [errors, setErrors] = useState<{ timestamp?: string; status?: string }>({});

  useEffect(() => {
    const fetchData = async () => {
      const data = await window.electronAPI.getData();
      if (data) setEntries(data);
    };
    fetchData();
  }, []);

  // Validate form
  const validate = () => {
    const newErrors: { timestamp?: string; status?: string } = {};
    if (!timestamp) newErrors.timestamp = 'Timestamp is required';
    if (!status) newErrors.status = 'Status is required';
    else if (!/^[01]+$/.test(status)) newErrors.status = 'Status must contain only 0 and 1';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const isFormValid = () => {
  if (!timestamp) return false;
  if (!status) return false;
  if (!/^[01]+$/.test(status)) return false;
  return true;
};

  const handleAddOrUpdate = async () => {
    if (!validate()) return;

    const newEntry: ValveConfiguration = {
      timestamp,
      status,
      configtype: configType === '' ? undefined : configType,
    };

    let newEntries: ValveConfiguration[];
    if (editIndex !== null) {
      newEntries = [...entries];
      newEntries[editIndex] = newEntry;
      setEditIndex(null);
    } else {
      newEntries = [...entries, newEntry];
    }

    await window.electronAPI.setData(newEntries);
    setEntries(newEntries);

    setTimestamp('');
    setStatus('');
    setConfigType('');
    setErrors({});
  };

  const handleEdit = (index: number) => {
    const entry = entries[index];
    setTimestamp(entry.timestamp);
    setStatus(entry.status);
    setConfigType(entry.configtype ?? '');
    setEditIndex(index);
  };

  const handleDelete = async (index: number) => {
    const newEntries = entries.filter((_, i) => i !== index);
    await window.electronAPI.setData(newEntries);
    setEntries(newEntries);
  };

  const handleImportClick = async () => {
    const path = await window.electronAPI.openFileDialog();
    if (!path) return;
    setFilePath(path);

    // TODO: read CSV via preload.js
    const csvRows = [
      { timestamp: new Date().toISOString(), status: '010101', configtype: '1' },
      { timestamp: new Date().toISOString(), status: '111000', configtype: '' },
    ];

    const parsedData: ValveConfiguration[] = csvRows.map(row => ({
      timestamp: row.timestamp,
      status: row.status,
      configtype: row.configtype === '' ? undefined : Number(row.configtype),
    }));

    await window.electronAPI.setData(parsedData);
    setEntries(parsedData);
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Import / Manage Data</h1>

      <button onClick={handleImportClick}>Select File to Import</button>
      {filePath && <p>Selected file: {filePath}</p>}

      <h2>{editIndex !== null ? 'Edit Entry' : 'Add Entry'}</h2>
      <div style={{ display: 'flex', flexDirection: 'column', maxWidth: '300px' }}>
        <label>
          Timestamp:
          <input
            type="datetime-local"
            value={timestamp}
            onChange={(e) => setTimestamp(e.target.value)}
          />
          {errors.timestamp && <span style={{ color: 'red' }}>{errors.timestamp}</span>}
        </label>

        <label>
          Status:
          <input
            type="text"
            value={status}
            placeholder="Sequence of 0 and 1"
            onChange={(e) => setStatus(e.target.value)}
            style={{ borderColor: errors.status ? 'red' : undefined }}
          />
          {errors.status && <span style={{ color: 'red' }}>{errors.status}</span>}
        </label>

        <label>
          Config Type:
          <select
            value={configType}
            onChange={(e) =>
              setConfigType(e.target.value === '' ? '' : Number(e.target.value) as 0 | 1)
            }
          >
            <option value="">—</option>
            <option value="1">Start</option>
            <option value="0">End</option>
          </select>
        </label>

        <button onClick={handleAddOrUpdate} style={{ marginTop: '1rem' }}>
          {editIndex !== null ? 'Update Entry' : 'Add Entry'}
          disabled={!isFormValid()}
        </button>
      </div>

      <h2>Current Entries</h2>
      <table border={1} cellPadding={4}>
        <thead>
          <tr>
            <th>Timestamp</th>
            <th>Status</th>
            <th>Config Type</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {entries.map((entry, index) => (
            <tr key={index}>
              <td>{entry.timestamp}</td>
              <td>{entry.status}</td>
              <td>{entry.configtype ?? '—'}</td>
              <td>
                <button onClick={() => handleEdit(index)}>Edit</button>
                <button onClick={() => handleDelete(index)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}