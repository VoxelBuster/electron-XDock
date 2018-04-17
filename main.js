const electron = require('electron');
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
const url = require('url');
const path = require('path');
const ps = require('./scripts/protonService.js');
const api = require('./scripts/protonAPI.js');

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let win;

function chron() {
  setInterval(function () {
    if (ps.isConnected()) {
      ps.updateBattery();
    }
  }, 500);
}

const appSettings = require('./appSettings.js');

if (!appSettings.hwAccel) {
  app.disableHardwareAcceleration();
}

function createWindow () {
  // Create the browser window.
  win = new BrowserWindow({
    width: 1920,
    height: 1080,
    transparent: true,
    frame: false,
    toolbar: false,
    icon: "assets/ico/appicon.png",
    webPreferences:  {
      webSecurity: false
    }});

  // and load the index.html of the app.
  win.loadURL(url.format({
    pathname: path.join(__dirname, 'index.html'),
    protocol: 'file:',
    slashes: true
  }));

  // Open the DevTools.
  // win.webContents.openDevTools()

  // Emitted when the window is closed.
  win.on('closed', () => {
    // Dereference the window object, usually you would store windows
    // in an array if your app supports multi windows, this is the time
    // when you should delete the corresponding element.
    win = null
  });

  ps.init();
  chron();
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow);

// Quit when all windows are closed.
app.on('window-all-closed', () => {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  ps.disconnect();
  if (process.platform !== 'darwin') {
    app.quit()
  }
});

app.on('activate', () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (win === null) {
    createWindow()
  }
});
