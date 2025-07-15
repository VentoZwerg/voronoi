# Voronoi Diagram Generator

This project generates an interactive 2D Voronoi diagram with random points, using Python. The diagram supports customizable numbers of points (2–100) and colors (2–20, capped at the number of points), with regions colored to match their corresponding points. The interface includes toggles for point and boundary visibility, sliders for adjusting the number of points and colors, and a button to regenerate the diagram. Evenly distributes colors (black, white, and random unique colors) with randomized remainder assignment are guaranteed.

## Prerequisites
- Tested on Linux, Windows and MacOS.
- Python 3.8 or higher (assumed to be installed).
- A system with a graphical interface to support the Qt5Agg backend.

## Installation
1. **Clone the Repository**:
   ```bash / cmd
   git clone https://github.com/VentoZwerg/voronoi.git
   cd voronoi
   cd python
   ```

2. **Create and activate venv**
   ```bash / cmd
   python -m venv venv
   ```
   Then activete the venv:

   On Windows:
   ```cmd
   .\venv\Scripts\activate
   ```

   Otherwise:
   ```bash / cmd
   venv/bin/activate
   ```

3. **Install Dependencies**:
   Install the required Python packages using `pip`:
   ```bash / cmd
   pip install -r requirements.txt
   ```
   This installs:
   - `numpy>=1.26.4`: For numerical operations and random point generation.
   - `matplotlib>=3.8.4`: For plotting and interactive GUI.
   - `PyQt5>=5.15.9`: For the Qt5Agg backend used by Matplotlib.

   On some systems, you may need to use `pip3` instead of `pip`.
   
   On Linux, you may also need to install system-level Qt libraries (e.g., `libqt5-dev` on Ubuntu) before installing `PyQt5`:
   ```bash
   sudo apt-get install libqt5-dev
   ```

4. **Verify Installation**:
   Ensure dependencies are installed:
   ```bash / cmd
   python -c "import numpy, matplotlib, PyQt5; print(numpy.__version__, matplotlib.__version__, PyQt5.__version__)"
   ```

5. **Create standalone .exe on Windows if desired**:
   ```cmd
   .\build.bat
   ```
   Builds a standalone .exe into the `dist` directory.

## Usage
1. **Run the Script**:
   ```bash / cmd
   python voronoi_diagram.py
   ```
   This opens a window displaying the Voronoi diagram with:
   - 20 random points (default).
   - 2 colors (default: black and white, evenly distributed).
   - Points with red outlines and colored fills.
   - Interactive controls on the right.

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

## Acknowledgments
- Inspired by computational geometry, art, and interactive visualization techniques.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

Copyright (c) 2025 Vento Christian Huerlimann <box12@openspace.ch>

