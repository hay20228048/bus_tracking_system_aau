/* ========= Entity Classes ========= */

class Bus {
  constructor(id, position, map) {
    this.id = id;
    this.position = position;
    this.map = map;

    this.marker = new google.maps.Marker({
      position: this.position,
      map: this.map,
      icon: {
        url: "https://maps.google.com/mapfiles/ms/icons/bus.png",
        scaledSize: new google.maps.Size(40, 40)
      }
    });

    this.infoWindow = new google.maps.InfoWindow({
      content: `<strong>Bus ${this.id}</strong>`
    });

    this.marker.addListener("click", () => {
      this.infoWindow.open(this.map, this.marker);
    });
  }

  updatePosition(newPosition) {
    this.position = newPosition;
    this.marker.setPosition(newPosition);
  }
}

class Stop {
  constructor(name, position, map) {
    this.name = name;
    this.position = position;
    this.map = map;

    this.marker = new google.maps.Marker({
      position: this.position,
      map: this.map,
      icon: {
        url: "https://maps.google.com/mapfiles/ms/icons/blue-dot.png"
      }
    });

    this.infoWindow = new google.maps.InfoWindow({
      content: `<strong>Stop:</strong> ${this.name}`
    });

    this.marker.addListener("click", () => {
      this.infoWindow.open(this.map, this.marker);
    });
  }
}

class Route {
  constructor(path, map) {
    this.map = map;
    this.polyline = new google.maps.Polyline({
      path: path,
      map: this.map,
      geodesic: true,
      strokeOpacity: 0.8,
      strokeWeight: 4
    });
  }
}

/* ========= Main Map App ========= */

class MapApp {
  constructor() {
    this.defaultLocation = { lat: 31.9450, lng: 35.9287 }; // AAU
    this.map = null;
    this.infowindow = null;

    this.buses = [];
    this.stops = [];
    this.routes = [];
  }

  async init() {
    await customElements.whenDefined("gmp-map");

    const gmpMap = document.querySelector("gmp-map");
    this.map = gmpMap.innerMap;
    this.infowindow = new google.maps.InfoWindow();

    this.map.setCenter(this.defaultLocation);
    this.map.setZoom(15);

    this.renderRoute();
    this.renderStops();
    this.renderBuses();
  }

  /* ===== Routes ===== */
  renderRoute() {
    const routePath = [
      { lat: 31.9450, lng: 35.9287 },
      { lat: 31.9485, lng: 35.9350 },
      { lat: 31.9520, lng: 35.9400 }
    ];

    const route = new Route(routePath, this.map);
    this.routes.push(route);
  }

  /* ===== Stops ===== */
  renderStops() {
    const stopData = [
      { name: "AAU Main Gate", lat: 31.9450, lng: 35.9287 },
      { name: "Sports Complex", lat: 31.9485, lng: 35.9350 },
      { name: "City Center Stop", lat: 31.9520, lng: 35.9400 }
    ];

    stopData.forEach(stop => {
      const stopMarker = new Stop(
        stop.name,
        { lat: stop.lat, lng: stop.lng },
        this.map
      );
      this.stops.push(stopMarker);
    });
  }

  /* ===== Buses ===== */
  renderBuses() {
    const busData = [
      { id: 1, lat: 31.9465, lng: 35.9310 },
      { id: 2, lat: 31.9500, lng: 35.9370 }
    ];

    busData.forEach(bus => {
      const busMarker = new Bus(
        bus.id,
        { lat: bus.lat, lng: bus.lng },
        this.map
      );
      this.buses.push(busMarker);
    });
  }
}

/* ========= Run App ========= */

document.addEventListener("DOMContentLoaded", () => {
  const app = new MapApp();
  app.init();
});
