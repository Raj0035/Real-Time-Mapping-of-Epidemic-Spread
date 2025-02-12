import React, { useEffect } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import fetchData from './datacollect'; // Ensure fetchData fetches data from your Flask server

const DiseaseHeatmap = () => {
  useEffect(() => {
    // Initialize the map
    const map = L.map('map').setView([20, 77], 2); // Centered roughly on the world map

    // Add a Tile Layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map);

    const severityColors = {
      1: 'yellow',
      2: 'orange',
      3: 'darkorange',
      4: 'red',
      5: 'darkred',
    };

    const circles = []; // Store references to all circles

    // Fetch data and populate the map
    const getData = async () => {
      try {
        const data = await fetchData(); // Fetch data from your Flask backend

        data.forEach((item) => {
          const [latitude, longitude] = item.location.split(',').map(Number);
          const severity = parseInt(item.severity, 10);
          const color = severityColors[severity] || 'gray';

          // Create a circle with an initial radius
          const circle = L.circle([latitude, longitude], {
            color,
            fillColor: color,
            fillOpacity: 0.5,
            radius: calculateRadius(map.getZoom()), // Initial radius based on zoom level
          }).addTo(map);

          // Store the circle for later updates
          circles.push(circle);

          // Tooltip content
          const popupContent = `<strong>Date:</strong> ${item.date}<strong>&nbsp&nbsp${item.summary}</strong>`;
          circle.bindTooltip(popupContent, {
            permanent: false,
            direction: 'top',
            offset: [0, -20],
            className: 'custom-tooltip',
          });
        });
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    const calculateRadius = (zoomLevel) => {
      // Adjust the base radius based on zoom level
      const baseRadius = 50000; // Radius at zoom level 2
      const minRadius = 5000; // Minimum threshold for radius
      const radius = baseRadius / Math.pow(2, zoomLevel - 2);

      return Math.max(radius, minRadius); // Ensure the radius doesn't go below the threshold
    };

    // Update circle radii on map zoom
    const updateCircleSizes = () => {
      const zoomLevel = map.getZoom();
      circles.forEach((circle) => {
        circle.setRadius(calculateRadius(zoomLevel));
      });
    };

    // Attach zoom event listener
    map.on('zoomend', updateCircleSizes);

    getData();
    // Add a legend (color bar) to the map
const legend = L.control({ position: 'bottomright' });

legend.onAdd = () => {
  const div = L.DomUtil.create('div', 'legend');
  div.innerHTML = `
    <h4>Severity Levels</h4>
    <div style="display: flex; flex-direction: column; gap: 5px;">
      <div><i style="background: yellow; width: 20px; height: 20px; display: inline-block; margin-right: 8px;"></i>1 (Low)</div>
      <div><i style="background: orange; width: 20px; height: 20px; display: inline-block; margin-right: 8px;"></i>2</div>
      <div><i style="background: darkorange; width: 20px; height: 20px; display: inline-block; margin-right: 8px;"></i>3</div>
      <div><i style="background: red; width: 20px; height: 20px; display: inline-block; margin-right: 8px;"></i>4</div>
      <div><i style="background: darkred; width: 20px; height: 20px; display: inline-block; margin-right: 8px;"></i>5 (High)</div>
    </div>`;
  div.style.padding = '10px';
  div.style.background = 'white';
  div.style.boxShadow = '0 0 15px rgba(0,0,0,0.2)';
  div.style.borderRadius = '5px';
  return div;
};

legend.addTo(map);

    // Cleanup on unmount
    return () => {
      map.off('zoomend', updateCircleSizes);
      map.remove();
    };
  }, []);

  return <div id="map" style={{ height: '100vh', width: '100%' }}></div>;
};

export default DiseaseHeatmap;





