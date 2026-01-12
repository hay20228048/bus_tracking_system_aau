class MapApp {
  constructor() {
    this.map = null;
    this.marker = null;
    this.placePicker = null;
    this.infowindow = null;
    this.defaultLocation = { lat: 31.9450, lng: 35.9287 }; // AAU
  }

async init() {
  await customElements.whenDefined('gmp-map');

  this.map = document.querySelector('gmp-map');
  this.marker = document.querySelector('gmp-advanced-marker');
  this.placePicker = document.querySelector('gmpx-place-picker');
  this.infowindow = new google.maps.InfoWindow();

  // Set default center if map has no center yet
  this.map.center = this.map.center || this.defaultLocation;

  // Restrict map to Jordan
  this.map.innerMap.setOptions({
    mapTypeControl: false,
    restriction: {
      latLngBounds: {
        north: 33.378,
        south: 29.183,
        west: 34.956,
        east: 39.301
      },
      strictBounds: false // true will prevent users from going outside completely
    }
  });

  this.placePicker.addEventListener('gmpx-placechange', () => this.onPlaceChange());
}


  onPlaceChange() {
    const place = this.placePicker.value;

    if (!place.location) {
      alert(`No details available for input: '${place.name}'`);
      this.infowindow.close();
      this.marker.position = null;
      return;
    }

    if (place.viewport) {
      this.map.innerMap.fitBounds(place.viewport);
    } else {
      this.map.center = place.location;
      this.map.zoom = 17;
    }

    this.marker.position = place.location;
    this.infowindow.setContent(`
      <strong>${place.displayName}</strong><br>
      <span>${place.formattedAddress}</span>
    `);
    this.infowindow.open(this.map.innerMap, this.marker);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const app = new MapApp();
  app.init();
});
