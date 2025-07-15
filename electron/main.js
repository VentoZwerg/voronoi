/*
Voronoi Diagram Generator

This project generates an interactive 2D Voronoi diagram with random points, using using Javascript and Electron.
The diagram supports customizable numbers of points (2–100) and colors (2–20, capped at the number of points),
with regions colored to match their corresponding points. The interface includes toggles for point and boundary
visibility, sliders for adjusting the number of points and colors, and a button to regenerate the diagram. Evenly
distributes colors (black, white, and random unique colors) with randomized remainder assignment are guaranteed.

License
This project is licensed under the MIT License. See the `LICENSE` file for details.

Copyright (c) 2025 Vento Christian Huerlimann <box12@openspace.ch>

Changelog:
250715 v1.0.0   Initial Commit                                  Vento Christian Huerlimann <box12@openspace.ch>
*/

const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
  const win = new BrowserWindow({
    width: 960,
    height: 720,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  });

  win.loadFile('index.html');
  // win.webContents.openDevTools(); // Uncomment for debugging
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});