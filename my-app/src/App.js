/* global google */

import logo from './logo.svg';
import './App.css';
import {InfoWindowF} from "@react-google-maps/api";
import {useState} from 'react';
import { GoogleMap, MarkerF, useLoadScript } from "@react-google-maps/api";
import { useMemo } from "react";
import React, { useEffect } from 'react';
import './App.css';


function SearchField({GetNewResult}) {
  const [searchQuery, setSearchQuery] = useState("");

  function updateText(event) { setSearchQuery(event.target.value)}
  function updateResultWithQuery() { GetNewResult(searchQuery) }

  return (
    <div>
      <input onChange={updateText}/>
      <button onClick={updateResultWithQuery}> search </button>
    </div>
  )
}

function GoogleMapMarks({marks, isOpen, setIsOpen}) {
  const [mapRef, setMapRef] = useState();

  const [infoWindowData, setInfoWindowData] = useState();

  const onMapLoad = (map) => {

    setMapRef(map);

    const bounds = new google.maps.LatLngBounds();

    marks?.forEach(({ lat, lng }) => bounds.extend({ lat, lng }));

    map.fitBounds(bounds);

  };

  const handleMarkerClick = (id, lat, lng, info) => {

    mapRef?.panTo({ lat, lng });

    setInfoWindowData({ id, info});

    setIsOpen(true);

  };

   const center = useMemo(() => ({ lat: 18.52043, lng: 73.856743 }), []);

  return (<GoogleMap

          mapContainerClassName="map-container"

          onLoad={onMapLoad}

          onClick={() => setIsOpen(false)}

        >

          {marks.map(({ info, lat, lng }, ind) => (

            <MarkerF

              key={ind}

              position={{ lat, lng }}

              onClick={() => {

                handleMarkerClick(ind, lat, lng, info);

              }}

              icon={"https://avatars.akamai.steamstatic.com/6f8cee28433a1c3c2ddfaaed7609fdbdb995b5a4_medium.jpg"}

            >

              {isOpen && infoWindowData?.id === ind && (

                <InfoWindowF

                  onCloseClick={() => {

                    setIsOpen(false);

                  }}

                >
                  <div>
                  <h3>{infoWindowData.info.name}</h3>
                  <h5>Rating: {infoWindowData.info.rating}</h5>
                  <p>{infoWindowData.info.description}</p>
                  <p><a href={infoWindowData.info.link}>Link</a></p></div>


                </InfoWindowF>

              )}

            </MarkerF>

          ))}

  </GoogleMap>)
}
function App() {
  const [sentResults, setSentResults] = useState([]);
  const [marks, setMarks]  = useState([]);
  const [isOpen, setIsOpen] = useState(false);
  
  function GetNewResult(searchQuery) {

    let Path = "/search/"
    Path = Path +searchQuery
      fetch(Path).then(res => res.json()).then(data => {
      setMarks(data);
    });
    setIsOpen(false)}
  const { isLoaded } = useLoadScript({
    googleMapsApiKey: "AIzaSyD2LhLsaPLxdu52uAXd3EKJXdNyr3oFwOg",
  });

  return (
    <div className="App">
      <SearchField GetNewResult={GetNewResult}/>
      {!isLoaded ? (
        <h1>Loading...</h1>
      ) : (
        <GoogleMapMarks marks={marks} isOpen={isOpen} setIsOpen={setIsOpen}/>

      )}

    </div>
  );
};

export default App;