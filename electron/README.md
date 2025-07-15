# Voronoi Diagram Generator

This project generates an interactive 2D Voronoi diagram with random points, using Javascript / Electron. The diagram supports customizable numbers of points (2–100) and colors (2–20, capped at the number of points), with regions colored to match their corresponding points. The interface includes toggles for point and boundary visibility, sliders for adjusting the number of points and colors, and a button to regenerate the diagram. Evenly distributes colors (black, white, and random unique colors) with randomized remainder assignment are guaranteed.

## Prerequisites
- Tested on Linux, Windows and MacOS.
- **Node.js**: Version 16 or higher (includes npm). Download from [nodejs.org](https://nodejs.org).
- **Wine** (non-Windows platforms): Required for building Windows executables on macOS/Linux. Install via Homebrew (`brew install wine`) on macOS or your package manager on Linux (e.g., `sudo apt install wine` for Ubuntu).


## Installation
1. **Clone the Repository**:
   ```bash / cmd
   git clone https://github.com/VentoZwerg/voronoi.git
   cd voronoi
   cd electron
   ```
2. ** Install dependencies **:
   ```bash / cmd
   npm install
   ```

## Running the Application
1. **Start the Electron app**:
   ```bash / cmd
   npm start
2. **Interact with the Diagram**:
   - Use the "Num Points" slider to set 2–100 points.
   - Use the "Num Colors" slider to set 2–20 colors (capped at the number of points).
   - Click "Show Points" to toggle point visibility.
   - Click "Show Boundaries" to toggle grey boundary lines.
   - Click "Regenerate Image" to create a new diagram with current settings.

3. **Example Scenarios**:
   - Set 3 points, 2 colors: Expect ~50% chance of 2 black + 1 white or 1 black + 2 white.
   - Set 12 points, 3 colors: Expect ~4 black, 4 white, 4 random color points/regions.
   - Set 2 points, 5 colors: Expect 1 black, 1 white point/region.
   ```

## Packaging as a Standalone .exe
To create a single-file `.exe` with no external dependencies (including no internet access requirement), use `electron-builder` with the `portable` target. This bundles all necessary files (Electron, Node.js, p5.js, application code) into one executable that runs offline on Windows.

### Steps
   ```bash / cmd
   npm run dist
   ```
   - On non-Windows platforms, ensure Wine is installed to support Windows builds.
   - This creates a single `Voronoi Diagram.exe` in the `dist` folder.

## Files
- `main.js`: Electron main process (window setup).
- `index.html`: UI structure and styles.
- `renderer.js`: p5.js logic for Voronoi diagram rendering and UI interactions.
- `p5.min.js`: Local p5.js library (version 1.4.2).
- `package.json`: Project configuration and dependencies.

## Acknowledgments
- Inspired by computational geometry, art, and interactive visualization techniques.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

Copyright (c) 2025 Vento Christian Huerlimann <box12@openspace.ch>

