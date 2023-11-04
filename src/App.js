
import React from 'react';
import Header from './hisHeader';
import Paragraph from './hisParg';
import Photo from './hisPhoto'
import Buttoms from './hisButtom'; //
import DataFetcher from './DataFetcher'; // Import the DataFetcher component
import './App.css';



const App = () => {
  return (
    <div className="App">
      <Header />
      <div className="content">
        <Paragraph /> 
        <DataFetcher /> 
        <Photo />
      </div>
    </div>
  );
};

export default App;

/* import React, { useState, useEffect } from "react";
//import data from './data.json';
import eventsData from './data.json';


import Timeline from "./Timeline";

const App = () => {
  console.log(eventsData);
  //const [data, setData] = useState([]);
  const [data, setData] = useState(eventsData);

  useEffect(() => {
    const fetchData = async () => {
      
        const response = await fetch("./data.json");
        const jsonData = await response.json();
        setData(jsonData);
      
    };

    fetchData();
  }, []); // Empty dependency array ensures useEffect runs once after initial render

  return (
    <div className="App">
      <h1>Historical Events</h1>
      <Timeline data={data} />
    </div>
  );
};

export default App;
  */
