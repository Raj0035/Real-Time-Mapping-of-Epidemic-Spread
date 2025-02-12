import logo from './logo.svg';
import React from 'react';
import DiseaseHeatmap from './map.js'
import './App.css';

function App() {
  return(
    <div id="map1" style={{ height: '10vh', width: '100%' ,alignContent:'center'}}>
      <DiseaseHeatmap/>
    </div>
  );
}

export default App;
