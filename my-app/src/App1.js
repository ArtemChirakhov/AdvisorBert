/* global google */

import logo from './logo.svg';
import './App.css';
import {InfoWindowF} from "@react-google-maps/api";
import {useState} from 'react';
import { GoogleMap, MarkerF, useLoadScript } from "@react-google-maps/api";
import { useMemo } from "react";

function SearchField({getNewResult}) {
  const [searchQuery, setSearchQuery] = useState("");

  function updateText(event) { setSearchQuery(event.target.value)}
  function updateResultWithQuery() { getNewResult(searchQuery) }

  return (
    <div>
      <input onChange={updateText}/>
      <button onClick={updateResultWithQuery}> search </button>
    </div>
  )
}

function GoogleMapMarks({marks}) {
  const [mapRef, setMapRef] = useState();

  const [isOpen, setIsOpen] = useState(false);

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

const markers = {doctor: [{info: {name: "Billy Jones", description: "adghdgfgsfgfgaf", rating: 1, link: "ya.ru"}, lat: 18.52043, lng: 73.856743 },
{info: {name: "MD. Popov", description: "Greatest Medical Doctor Ever", rating: 100, link: "ya.ru"}, lat: 0, lng: 0 }],
scientist: [{info: {name: "Albert Einstein", description: "Greatest Scientist Ever", rating: 10, link: "https://ya.ru"}, lat: 23.52043, lng: 34.856743 }]}
function App() {
  const [sentResults, setSentResults] = useState([]);

  const [marks, setMarks]  = useState(markers.doctor);

  function getNewResult(searchQuery) {
    setMarks(markers.doctor.map( position=>
               <MarkerF position={{lat: position.lat, lng: position.lng}} icon={"https://avatars.akamai.steamstatic.com/6f8cee28433a1c3c2ddfaaed7609fdbdb995b5a4_medium.jpg"}/>))
  }
  const { isLoaded } = useLoadScript({
    googleMapsApiKey: "AIzaSyD2LhLsaPLxdu52uAXd3EKJXdNyr3oFwOg",
  });

  return (
    <div className="App">
      <SearchField getNewResult={getNewResult}/>
      {!isLoaded ? (
        <h1>Loading...</h1>
      ) : (
        <GoogleMapMarks marks={marks}/>

      )}

    </div>
  );
};

export default App;