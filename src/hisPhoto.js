import React from 'react';
import leftPhoto from './leftPhoto.svg';  // Path: ansarelquds/src/leftPhoto.svg
import rightPhoto from './rightPhoto.svg'; 

const Photo = ({ side }) => {
  const imageUrl = side === 'left' ? leftPhoto : rightPhoto;

  return <div className={`photo ${side}`}><img src={imageUrl} alt={`Photo ${side}`} /></div>;
};

export default Photo;
