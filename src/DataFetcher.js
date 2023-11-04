//Trying to fetch using Axios
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const DataFetcher = () => {
  const [data, setData] = useState(null);

  const fetchData = async (buttonNumber) => {
    try {
      const response = await axios.get(`./button${buttonNumber}Data.json`);
      setData(response.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  useEffect(() => {
    fetchData(1); // Fetch initial data when the component mounts

    // Cleanup function
    return () => {
      // You can perform cleanup operations here if necessary
    };
  }, []); // Empty dependency array means this effect runs once after the initial render

  return (
    <div>
      <button onClick={() => fetchData(1)}>Before 1900</button>
      <button onClick={() => fetchData(2)}>1900 - 2000</button>
      <button onClick={() => fetchData(3)}>2000 - Now</button>

      {data && (
        <div>
          {/* Render your data here */}
          {data.map((item) => (
            <div key={item.id}>
              <p>{item.title.en}</p>
              <p>{item.description.en}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default DataFetcher;






/*
import React, { useState } from 'react';
const DataFetcher = () => {
  const [data, setData] = useState(null);

  const fetchData = async (buttonNumber) => {
    try {
      const response = await fetch(`./button${buttonNumber}Data.json`);
      console.log(response)
      const jsonData = await response.json();
      setData(jsonData);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div>
      <button onClick={() => fetchData(1)}>Before 1900 </button>
      <button onClick={() => fetchData(2)}>1900 - 2000</button>
      <button onClick={() => fetchData(3)}>2000 - Now</button>

      {data && (
        <div>
          {data.map((item) => (
            <div key={item.id}>
              <p>{item.name}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default DataFetcher;

 
*/

//2
/*
import React, { useState } from 'react';

const DataFetcher = () => {
  const [data, setData] = useState(null);

  const fetchData = async (buttonNumber) => {
    try {
      const response = await fetch(`./button${buttonNumber}Data.json`);
      const jsonData = await response.json();
      setData(jsonData);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div>
      <button onClick={() => fetchData(1)}>Before 1900 </button>
      <button onClick={() => fetchData(2)}>1900 - 2000</button>
      <button onClick={() => fetchData(3)}>2000 - Now</button>

      {data && (
        <div>
          {data.map((item) => (
            <div key={item.id}>
              <p>{item.title.en}</p>
              <p>{item.description.en}</p> 
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default DataFetcher;
*/