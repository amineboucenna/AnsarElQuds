import React from "react";

const Timeline = ({ data }) => {
  return (
    <div>
      {data.map((event) => (
        <div key={event.id}>
          <h2>{event.title.en}</h2>
          <p>{event.description.en}</p>
        </div>
      ))}
    </div>
  );
};

export default Timeline;
