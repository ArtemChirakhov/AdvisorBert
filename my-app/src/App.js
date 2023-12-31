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
    <div class="wrap">
      <div class="search">
        <input onChange={updateText} placeholder="What are you interested in?" class="searchTerm"/>
        <button onClick={updateResultWithQuery} class="searchButton"> search </button>
      </div>
    </div>
  )
}

function GoogleMapMarks({marks, isOpen, setIsOpen, setTitles}) {
  const [mapRef, setMapRef] = useState();

  const [infoWindowData, setInfoWindowData] = useState();

  const onMapLoad = (map) => {

    setMapRef(map);

    const bounds = new google.maps.LatLngBounds();

    marks?.forEach(({ lat, lng }) => bounds.extend({ lat, lng }));

    map.fitBounds(bounds);

  };

  const handleMarkerClick = (id, coord, info, publications) => {

    mapRef?.panTo(coord);

    setInfoWindowData({ id, info});

    setIsOpen(true);

    setTitles(publications)
  };

  return (<GoogleMap

          mapContainerClassName="map-container"

          onLoad={onMapLoad}

          onClick={() => setIsOpen(false)}
          
          initialCenter={{
            lat: 47.5162, lng: 14.5501
          }}

          zoom={5}
        >
          
          {marks.map(({ info, coord, publications, color }, ind) => (
            
            <MarkerF

              key={ind}

              position={coord}

              onClick={() => {

                handleMarkerClick(ind, coord, info, publications);

              }}
              // blue
              // yellow
              // orange
              // red
              icon={'http://maps.google.com/mapfiles/ms/icons/' + color + '-dot.png'}
            >

              {isOpen && infoWindowData?.id === ind && (

                <InfoWindowF

                  onCloseClick={() => {

                    setIsOpen(false);

                  }}

                >
                  <div>
                    <h3>{infoWindowData.info.name}</h3>
                    <h5>University: {infoWindowData.info.insitution}</h5>
                    <p><a href={infoWindowData.info.link}>Link</a></p>
                  </div>

                </InfoWindowF>

              )}

            </MarkerF>

          ))}

  </GoogleMap>)
}

function PublicationList({titles}) {
  return (
    <div class="pub-list">
      <p>Publication list</p>
      <ul class="box">
        {titles.map(t => <li class="pub-el">{t}</li>)}
      </ul>
    </div> 
  )
}

function App() {
  const [marks, setMarks]  = useState([]);
  const [isOpen, setIsOpen] = useState(false);
  const [titles, setTitles] = useState([])
  
  function GetNewResult(searchQuery) {

    let Path = "/search/"
    Path = Path +searchQuery
      fetch(Path).then(res => res.json()).then(data => {

      let pubLengths = data.map(mark => mark.publications.length)
      let minCitation = Math.min(...pubLengths)
      let maxCitation = Math.max(...pubLengths)

      for (let i = 0; i < data.length; i++) { 
        let score = (data[i].publications.length - minCitation) / (maxCitation - minCitation);
        if (score <= 0.25) {
          data[i].color = 'blue'
        } else if (score <= 0.5) {
          data[i].color = 'yellow'
        } else if (score <= 0.75) {
          data[i].color = 'orange'
        } else {
          data[i].color = 'red'
        }
      }

      setMarks(data);
    });
    setIsOpen(false);
  }
  const { isLoaded } = useLoadScript({
    googleMapsApiKey: "AIzaSyD2LhLsaPLxdu52uAXd3EKJXdNyr3oFwOg",
  });

  return (
    <div class="parent-flex">
      <SearchField GetNewResult={GetNewResult}/>
      {!isLoaded ? (
        <h1>Loading...</h1>
      ) : (
        <GoogleMapMarks marks={marks} isOpen={isOpen} setIsOpen={setIsOpen} setTitles={setTitles} />
      )}
      <PublicationList titles={titles}/>
    </div>
  );
};

export default App;