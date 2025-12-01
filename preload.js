//
//  preload.js
//  
//
//  Created by Beau De Clercq on 09/07/2025.
//

const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  openFileDialog: () => ipcRenderer.invoke('dialog:openFile'),
  saveFileDialog: () => ipcRenderer.invoke('dialog:saveFile'),
  setData: (data) => ipcRenderer.invoke('data:set', data),
  getData: () => ipcRenderer.invoke('data:get'),
});
