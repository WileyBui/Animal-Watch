// THE FOLLOWING GEOFINDME FUNCTION IS COPIED STRAIGHT FROM
// https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API

function geoFindMe() {
  const status = document.querySelector('#status');
  const id_latitude = $('#location-latitude');
  const id_longitude = $('#location-longitude');

  function success(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;

    id_latitude.val(latitude);
    id_longitude.val(longitude);

    status.textContent = '';
  }

  function error() {
    status.textContent = 'Unable to retrieve your location';
  }

  if (!navigator.geolocation) {
    status.textContent = 'Geolocation is not supported by your browser';
  } else {
    status.textContent = 'Locating…';
    navigator.geolocation.getCurrentPosition(success, error);
  }
}

document.querySelector('#find-me').addEventListener('click', geoFindMe);