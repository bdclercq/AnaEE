//
//  ExportPage.tsx
//  
//
//  Created by Beau De Clercq on 09/07/2025.
//

import React, { useState } from 'react';

declare global {
  interface Window {
    electronAPI: {
      saveFileDialog: () => Promise<string | null>;
    };
  }
}

export default function ExportPage() {
  const [filePath, setFilePath] = useState<string | null>(null);

    const handleExportClick = async () => {
      const path = await window.electronAPI.saveFileDialog();
      if (!path) return;

      const data = await window.electronAPI.getData();
      console.log('Will export to', path, data);

      // Write to file (could be implemented in preload or main)
    };

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Export Data</h1>
      <button onClick={handleExportClick}>Select Export Location</button>
      {filePath && <p>Export path: {filePath}</p>}
    </div>
  );
}
