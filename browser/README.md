# Voronoi Diagram Generator

This project generates an interactive 2D Voronoi diagram with random points, using only vanilla Javascript and HTML. The diagram supports customizable numbers of points (2–100) and colors (2–20, capped at the number of points), with regions colored to match their corresponding points. The interface includes toggles for point and boundary visibility, sliders for adjusting the number of points and colors, and a button to regenerate the diagram. Evenly distributes colors (black, white, and random unique colors) with randomized remainder assignment are guaranteed.

## Prerequisites / Installation / Running / Deployment
- This should run in any JavaScript capable browser on any platform.
- Can be deployed to any webspace, by copying all the files in the directory to any webserver.
- Tu run it locally, just double-click the `index.html` file to open it in your browser.

This opens a browser window displaying the Voronoi diagram with:
   - 20 random points (default).
   - 2 colors (default: black and white, evenly distributed).
   - Points with red outlines and colored fills.
   - Interactive controls on the right.

**Interact with the Diagram**:
   - Use the "Num Points" slider to set 2–100 points.
   - Use the "Num Colors" slider to set 2–20 colors (capped at the number of points).
   - Click "Show Points" to toggle point visibility.
   - Click "Show Boundaries" to toggle grey boundary lines.
   - Click "Regenerate Image" to create a new diagram with current settings.

**Example Scenarios**:
   - Set 3 points, 2 colors: Expect ~50% chance of 2 black + 1 white or 1 black + 2 white.
   - Set 12 points, 3 colors: Expect ~4 black, 4 white, 4 random color points/regions.
   - Set 2 points, 5 colors: Expect 1 black, 1 white point/region.

## Files
- `index.html`: UI structure and styles.
- `renderer.js`: p5.js logic for Voronoi diagram rendering and UI interactions.
- `p5.min.js`: Local p5.js library (version 1.4.2).

## Acknowledgments
- Inspired by computational geometry, art, and interactive visualization techniques.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

Copyright (c) 2025 Vento Christian Huerlimann <box12@openspace.ch>

