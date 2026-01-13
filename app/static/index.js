class Bus {
  constructor(bus, map) {
    this.id = bus.id;
    this.position = bus.location;
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

  update(location) {
    this.position = location;
    this.marker.setPosition(location);
  }
}

class Stop {
  constructor(stop, map) {
    this.name = stop.name;
    this.position = stop.location;
    this.map = map;

    this.marker = new google.maps.Marker({
      position: this.position,
      map: this.map,
      icon: "https://maps.google.com/mapfiles/ms/icons/blue-dot.png"
    });

    this.infoWindow = new google.maps.InfoWindow({
      content: `<strong>${this.name}</strong>`
    });

    this.marker.addListener("click", () => {
      this.infoWindow.open(this.map, this.marker);
    });
  }
}

class Route {
  constructor(route, map) {
    this.polyline = new google.maps.Polyline({
      path: route.path,
      map: map,
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

    this.buses = new Map();   // id → Bus
    this.stops = [];
    this.routes = [];
  }

  async init() {
    await customElements.whenDefined("gmp-map");

    const gmpMap = document.querySelector("gmp-map");
    this.map = gmpMap.innerMap;

    this.map.setCenter(this.defaultLocation);
    this.map.setZoom(15);

    await this.loadRoutes();
    await this.loadStops();
    await this.loadBuses();

    // 🔄 refresh buses every 5 seconds (ready for real-time)
    setInterval(() => this.loadBuses(), 5000);
  }

  /* ===== API CALLS ===== */

  async loadBuses() {
    const response = await fetch("/api/buses");
    const data = await response.json();

    data.forEach(bus => {
      if (this.buses.has(bus.id)) {
        // Update existing bus
        this.buses.get(bus.id).update(bus.location);
      } else {
        // Create new bus
        this.buses.set(bus.id, new Bus(bus, this.map));
      }
    });
  }

  async loadStops() {
    const response = await fetch("/api/stops");
    const data = await response.json();

    data.forEach(stop => {
      this.stops.push(new Stop(stop, this.map));
    });
  }

  async loadRoutes() {
    const response = await fetch("/api/routes");
    const data = await response.json();

    data.forEach(route => {
      this.routes.push(new Route(route, this.map));
    });
  }
}


/* ========= Run App ========= */

document.addEventListener("DOMContentLoaded", () => {
  const app = new MapApp();
  app.init();
});
