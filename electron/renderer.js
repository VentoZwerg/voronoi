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

const sketch = (p) => {
  let points = [];
  let colors = [];
  let colorPool = ['#000000', '#FFFFFF'];
  let colorGrid = [];
  let indexGrid = [];
  let showPoints = true;
  let showBoundaries = false;
  let numPoints = 2;
  let numColors = 2;
  const gridSize = 600;
  const canvasSize = 600; // 10x10 area scaled to 600x600 pixels

  p.setup = () => {
    p.createCanvas(canvasSize, canvasSize);
    p.pixelDensity(1); // Ensure consistent pixel rendering
    p.noLoop(); // Draw only when needed
    generateVoronoi();
    updateUI();
  };

  function generateUniqueColor(existingColors) {
    const threshold = 0.1;
    const maxAttempts = 100;
    for (let i = 0; i < maxAttempts; i++) {
      const rgb = [p.random(1), p.random(1), p.random(1)];
      const hex = '#' + rgb.map(v => Math.floor(v * 255).toString(16).padStart(2, '0')).join('');
      let tooClose = false;
      for (let existing of existingColors) {
        const eRgb = p.color(existing);
        const dist = p.sqrt(
          p.sq(rgb[0] - p.red(eRgb) / 255) +
          p.sq(rgb[1] - p.green(eRgb) / 255) +
          p.sq(rgb[2] - p.blue(eRgb) / 255)
        );
        if (dist < threshold) {
          tooClose = true;
          break;
        }
      }
      if (!tooClose) return hex;
    }
    return '#808080'; // Fallback gray
  }

  function generateVoronoi() {
    // Generate random points
    points = Array.from({ length: numPoints }, () => [p.random(10), p.random(10)]);

    // Cap numColors at numPoints
    numColors = Math.min(numColors, numPoints);

    // Generate color pool
    colorPool = ['#000000', '#FFFFFF'];
    for (let i = colorPool.length; i < numColors; i++) {
      colorPool.push(generateUniqueColor(colorPool));
    }

    // Assign colors evenly with random remainder
    const colorsPerPoint = Math.floor(numPoints / numColors);
    const remainder = numPoints % numColors;
    colors = [];
    for (let i = 0; i < numColors; i++) {
      for (let j = 0; j < colorsPerPoint; j++) {
        colors.push(colorPool[i]);
      }
    }
    if (remainder > 0) {
      const extraIndices = p.shuffle([...Array(numColors).keys()]).slice(0, remainder);
      for (let i of extraIndices) {
        colors.push(colorPool[i]);
      }
    }
    colors = p.shuffle(colors);

    // Debug color assignments
    console.log(`Num colors: ${numColors}, Color pool: ${colorPool.slice(0, numColors)}`);
    console.log(`Point colors: ${colors.map((c, i) => `(${i}, ${c})`)}`);
    const colorCounts = {};
    colors.forEach(c => colorCounts[c] = (colorCounts[c] || 0) + 1);
    console.log(`Color counts: ${JSON.stringify(colorCounts)}`);

    // Create color-to-index mapping
    const colorToIndex = {};
    colorPool.slice(0, numColors).forEach((color, i) => colorToIndex[color] = i);

    // Compute Voronoi grid
    colorGrid = Array(gridSize).fill().map(() => Array(gridSize).fill(0));
    indexGrid = Array(gridSize).fill().map(() => Array(gridSize).fill(0));
    for (let i = 0; i < gridSize; i++) {
      for (let j = 0; j < gridSize; j++) {
        const x = (j / (gridSize - 1)) * 10;
        const y = (i / (gridSize - 1)) * 10;
        let minDist = Infinity;
        let closestIdx = 0;
        points.forEach((pt, idx) => {
          const dist = p.sq(pt[0] - x) + p.sq(pt[1] - y);
          if (dist < minDist) {
            minDist = dist;
            closestIdx = idx;
          }
        });
        indexGrid[i][j] = closestIdx;
        colorGrid[i][j] = colorToIndex[colors[closestIdx]];
      }
    }

    // Debug color grid
    console.log(`Sample colorGrid: ${colorGrid.slice(0, 5).map(row => row.slice(0, 5))}`);
    p.redraw();
  }

  p.draw = () => {
    p.background(255); // Clear canvas
    const scale = canvasSize / 10; // Scale 10x10 to canvasSize
    const cellSize = canvasSize / gridSize; // Size of each grid cell in pixels (2)

    // Draw Voronoi regions as filled rectangles
    p.noStroke();
    for (let i = 0; i < gridSize; i++) {
      for (let j = 0; j < gridSize; j++) {
        p.fill(colorPool[colorGrid[i][j]]);
        // Map grid coordinates to canvas, flip y-axis to match Python orientation
        const x = j * cellSize;
        const y = (gridSize - 1 - i) * cellSize;
        p.rect(x, y, cellSize, cellSize);
      }
    }

    // Draw boundaries
    if (showBoundaries) {
      p.stroke(128); // Grey boundaries
      p.strokeWeight(1);
      const dx = cellSize; // 2 pixels
      for (let i = 0; i < gridSize - 1; i++) {
        for (let j = 0; j < gridSize - 1; j++) {
          // Horizontal boundaries
          if (indexGrid[i][j] !== indexGrid[i][j + 1]) {
            const x1 = j * dx;
            const y1 = (gridSize - 1 - i) * dx;
            const x2 = (j + 1) * dx;
            p.line(x1, y1, x2, y1);
          }
          // Vertical boundaries
          if (indexGrid[i][j] !== indexGrid[i + 1][j]) {
            const x1 = j * dx;
            const y1 = (gridSize - 1 - i) * dx;
            const y2 = (gridSize - 1 - (i + 1)) * dx;
            p.line(x1, y1, x1, y2);
          }
        }
      }
    }

    // Draw points
    if (showPoints) {
      p.stroke(255, 0, 0); // Red outline
      p.strokeWeight(2);
      points.forEach((pt, i) => {
        p.fill(colors[i]);
        p.ellipse(pt[0] * scale, (10 - pt[1]) * scale, 8, 8);
      });
    }
  };

  function updateUI() {
    document.getElementById('pointsValue').textContent = numPoints;
    document.getElementById('colorsValue').textContent = numColors;
  }

  // UI event handlers
  document.getElementById('showPoints').addEventListener('change', (e) => {
    showPoints = e.target.checked;
    p.redraw();
  });

  document.getElementById('showBoundaries').addEventListener('change', (e) => {
    showBoundaries = e.target.checked;
    p.redraw();
  });

  document.getElementById('regenerate').addEventListener('click', () => {
    // Update numPoints and numColors from sliders
    numPoints = parseInt(document.getElementById('numPoints').value);
    numColors = parseInt(document.getElementById('numColors').value);
    updateUI();
    generateVoronoi();
  });

  document.getElementById('numPoints').addEventListener('input', (e) => {
    numPoints = parseInt(e.target.value);
    updateUI();
    // No generateVoronoi() call here
  });

  document.getElementById('numColors').addEventListener('input', (e) => {
    numColors = parseInt(e.target.value);
    updateUI();
    // No generateVoronoi() call here
  });

  // Handle window resize
  window.addEventListener('resize', () => {
    const controls = document.getElementById('controls');
    controls.style.right = '20px';
    controls.style.width = '222px';
  });
};

// Initialize p5.js sketch
new p5(sketch, 'canvas-container');