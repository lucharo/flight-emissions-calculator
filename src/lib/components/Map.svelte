<script lang="ts">
  import { onMount } from 'svelte';
  import L from 'leaflet';
  import 'leaflet/dist/leaflet.css';

  let mapElement: HTMLDivElement;
  let map: L.Map;
  let flightPath: L.Polyline;
  let markers: L.Marker[] = [];
  let locationControl: L.Control;

  export let originCoords: [number, number] | null = null;
  export let destCoords: [number, number] | null = null;

  // Esri WorldStreetMap theme
  const esriUrl = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}';
  const attribution = 'Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012';

  function createLocationControl() {
    const LocationControl = L.Control.extend({
      options: {
        position: 'bottomright'
      },

      onAdd: function() {
        const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control');
        const button = L.DomUtil.create('a', 'location-button', container);
        button.innerHTML = `
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4">
            <circle cx="12" cy="12" r="10"/>
            <point cx="12" cy="12"/>
          </svg>
        `;
        button.href = '#';
        button.title = 'Show my location';

        button.onclick = function() {
          if ('geolocation' in navigator) {
            button.classList.add('loading');
            navigator.geolocation.getCurrentPosition(
              (position) => {
                const { latitude, longitude } = position.coords;
                map.setView([latitude, longitude], 6);
                button.classList.remove('loading');
              },
              (error) => {
                console.error('Error getting location:', error);
                button.classList.remove('loading');
              }
            );
          }
          return false;
        };

        return container;
      }
    });

    return new LocationControl();
  }

  onMount(() => {
    map = L.map(mapElement, {
      zoomControl: false,
      minZoom: 2,
      maxZoom: 18,
      maxBounds: [[-90, -180], [90, 180]],
      maxBoundsViscosity: 1.0,
      worldCopyJump: true,
      preferCanvas: true
    }).setView([30, 0], 3);

    // Add zoom control first
    L.control.zoom({
      position: 'bottomright'
    }).addTo(map);

    // Add location control
    locationControl = createLocationControl();
    map.addControl(locationControl);

    // Add the Esri WorldStreetMap theme
    L.tileLayer(esriUrl, {
      attribution,
      maxZoom: 18,
      minZoom: 2,
      className: 'esri-tiles',
      tileSize: 256,
      zoomOffset: 0,
      detectRetina: true,
      crossOrigin: true
    }).addTo(map);
  });

  $: if (map && originCoords && destCoords) {
    // Clear existing markers and flight path
    markers.forEach(marker => marker.remove());
    markers = [];
    if (flightPath) {
      flightPath.remove();
    }

    // Add new markers
    const originMarker = L.marker(originCoords, {
      icon: L.divIcon({
        className: 'custom-marker origin-marker',
        html: '<div class="marker-dot"></div>',
        iconSize: [20, 20]
      })
    });
    const destMarker = L.marker(destCoords, {
      icon: L.divIcon({
        className: 'custom-marker dest-marker',
        html: '<div class="marker-dot"></div>',
        iconSize: [20, 20]
      })
    });

    markers = [originMarker, destMarker];
    markers.forEach(marker => marker.addTo(map));

    // Calculate great circle path
    const latlngs = [];
    const segments = 100;
    for (let i = 0; i <= segments; i++) {
      const fraction = i / segments;
      const lat = originCoords[0] + (destCoords[0] - originCoords[0]) * fraction;
      const lng = originCoords[1] + (destCoords[1] - originCoords[1]) * fraction;
      // Add some curvature
      const curveOffset = Math.sin(fraction * Math.PI) * 5;
      latlngs.push([lat + curveOffset, lng]);
    }

    // Draw curved flight path
    flightPath = L.polyline(latlngs, {
      color: '#2563eb',
      weight: 3,
      opacity: 0.8,
      smoothFactor: 1,
      dashArray: '10, 10',
    }).addTo(map);

    // Fit map to show the entire flight path with padding
    map.fitBounds(flightPath.getBounds(), { 
      padding: [50, 50],
      maxZoom: 12
    });
  }
</script>

<svelte:head>
  <link 
    rel="stylesheet" 
    href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
    integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
    crossorigin="" 
  />
</svelte:head>

<div bind:this={mapElement} class="w-full h-full"></div>

<style>
  :global(.leaflet-control-zoom) {
    margin-bottom: 100px !important;
    border-radius: 8px !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
  }

  :global(.leaflet-control-zoom a) {
    border-radius: 8px !important;
    color: #666 !important;
    transition: background-color 0.2s !important;
  }

  :global(.location-button) {
    width: 30px !important;
    height: 30px !important;
    line-height: 30px !important;
    text-align: center !important;
    background-color: white !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
  }

  :global(.location-button.loading) {
    animation: spin 1s linear infinite;
  }

  :global(.esri-tiles) {
    filter: saturate(1.05) contrast(1.05) !important;
  }

  :global(.custom-marker) {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  :global(.marker-dot) {
    width: 14px;
    height: 14px;
    background-color: #2563eb;
    border: 2px solid white;
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    position: relative;
    z-index: 2;
  }

  :global(.leaflet-control) {
    border-radius: 8px !important;
  }

  :global(.leaflet-container) {
    font-family: "Roboto", Arial, sans-serif !important;
    background-color: #f5f5f5 !important;
  }
</style>
