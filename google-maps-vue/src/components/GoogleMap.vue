<template>
  <div id="map" ref="mapContainer" class="map"></div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import { Loader } from '@googlemaps/js-api-loader';
import MarkerClusterer from '@googlemaps/markerclustererplus';

export default {
  name: 'GoogleMap',
  props: {
    userLocation: Object,
    recommendedLocation: Object
  },
  setup(props,{emit}) {
    const mapContainer = ref(null);
    let currentInfoWindow = null;
    let markerCluster = null;
    let markers = [];
    let userMarker = null;
    let recommendedMarker = null;
    let map;
    const roundTo = function( num, decimal ) { return Math.round( ( num + Number.EPSILON ) * Math.pow( 10, decimal ) ) / Math.pow( 10, decimal ); }

    const updateUserMarker = (location) => {
      if (userMarker) {
        userMarker.setMap(null);
      }
      userMarker = new google.maps.Marker({
        position: location,
        map,
        title: 'Selected Location',
        icon: {
          url: './user_location.ico',
          scaledSize: new google.maps.Size(40, 40)
        }
      });
      map.setCenter(location);
    };

    const updateRecommendedMarker = (location) => {
      if (recommendedMarker) {
        recommendedMarker.setMap(null);
      }
      recommendedMarker = new google.maps.Marker({
        zIndex: 10,
        position: location,
        map,
        title: 'Recommended Location',
        icon: {
          url: './Recommendation_location.ico',
          scaledSize: new google.maps.Size(40, 40)
        }
      });

      const infoWindow = new google.maps.InfoWindow({
        content: `
        <div>
          <p>推薦站點: ${location.station}</p>
          <p>可借車輛: ${location.predicted_available_bikes}</p>
          <p>距離: ${roundTo(location.distance,3) * 1000} (公尺)(m)</p>
        </div>
                  `
      });

      recommendedMarker.addListener('click', () => {
        if (currentInfoWindow) {
          currentInfoWindow.close();
        }
        infoWindow.open(map, recommendedMarker);
        currentInfoWindow = infoWindow;
      });
      infoWindow.open(map, recommendedMarker);
      currentInfoWindow = infoWindow;
      map.setZoom(18);  // 設置放大級別，可以根據需要調整
      map.setCenter(location);

    };

    onMounted(() => {
      const loader = new Loader({
        apiKey: process.env.VUE_APP_GOOGLE_MAPS_API_KEY,
        version: 'weekly'
      });

      loader.load().then(() => {
        map = new google.maps.Map(mapContainer.value, {
          center: { lat: 25.0330, lng: 121.5654 },
          zoom: 12
        });
        
        if (props.userLocation) {
          updateUserMarker(props.userLocation);
        }

        // 監聽地圖點擊事件
        map.addListener('click', (event) => {
          const lat = event.latLng.lat();
          const lng = event.latLng.lng();
          const location = { lat, lng };
          updateUserMarker(location);
          emit('locationUpdated', location);
        });

        fetch('https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json')
        .then(response => response.json())
        .then(data => {
          data.forEach(station => {
            const sna = station.sna;
            const lat = station.latitude;
            const lng = station.longitude;
            const availableBikes = station.available_rent_bikes;
            const total = station.total;
            const act = station.act;
            const infoTime = station.infoTime;

              let icon = './normal.ico';

              if (availableBikes === 0) {
                icon = './no_bike.ico';
              } else if (availableBikes === total) {
                icon = './full.ico';
              } else if (act === 0) {
                icon = './closed.ico';
              }

              const marker = new google.maps.Marker({
                zIndex: 1,
                position: { lat, lng },
                map,
                title: sna,
                icon: {
                  url: `/${icon}`,
                  scaledSize: new google.maps.Size(40, 40)
                }
              });

              const content = `
                <div>
                  <p>租賃站點查詢: ${sna}</p>
                  <p>站點位置: ${station.ar}</p>
                  <p>可借車輛: ${availableBikes}</p>
                  <p>可停空位: ${station.available_return_bikes}</p>
                  <p>時間: ${infoTime}</p>
                </div>
              `;
              const infoWindow = new google.maps.InfoWindow({
                content: content
              });

              marker.addListener('click', () => {
                if (currentInfoWindow) {
                  currentInfoWindow.close();
                }
                infoWindow.open(map, marker);
                currentInfoWindow = infoWindow;
              });

              markers.push(marker);
            });

            markerCluster = new MarkerClusterer(map, markers, {
              minimumClusterSize: 8,
              imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'
            });

            map.addListener('zoom_changed', () => {
              const currentZoom = map.getZoom();
              if (currentZoom <= 12) {
                markerCluster.setMaxZoom(12);
              } else {
                markerCluster.setMaxZoom(null);
              }
            });
          })
          .catch(error => {
            console.error('Error fetching CSV:', error);
          });
      });
    });

    watch(() => props.userLocation, (newLocation) => {
      if (newLocation) {
        updateUserMarker(newLocation);
      }
    });

    watch(() => props.recommendedLocation, (newLocation) => {
      if (newLocation) {
        updateRecommendedMarker(newLocation);
      }
    });

    return {
      mapContainer
    };
  }
};
</script>

<style scoped>
.map {
  height: 80vh;
  width: 80vw;
  margin: auto;
}
</style>
