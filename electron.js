const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');

let mainWindow;
let valveConfigurations = [];

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1024,
    height: 768,
      webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
          },
  });

  mainWindow.loadFile(path.join(__dirname, 'dist/index.html'));
    
    mainWindow.webContents.openDevTools();
    
    
    ipcMain.handle('dialog:openFile', async () => {
        const { canceled, filePaths } = await dialog.showOpenDialog(mainWindow, {
          properties: ['openFile'],
          filters: [{ name: 'CSV Files', extensions: ['csv'] }, { name: 'All Files', extensions: ['*'] }],
        });
        if (canceled) return null;
        return filePaths[0];
      });

      ipcMain.handle('dialog:saveFile', async () => {
        const { canceled, filePath } = await dialog.showSaveDialog(mainWindow, {
          filters: [{ name: 'CSV Files', extensions: ['csv'] }, { name: 'All Files', extensions: ['*'] }],
          defaultPath: 'export.csv',
        });
        if (canceled) return null;
        return filePath;
      });
    
    ipcMain.handle('data:set', (event, data) => {
      valveConfigurations = data; // expecting array of ValveConfiguration
      return true;
    });

    ipcMain.handle('data:get', () => {
      return valveConfigurations;
    });
    
  mainWindow.on('closed', () => (mainWindow = null));
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
  if (mainWindow === null) createWindow();
});
