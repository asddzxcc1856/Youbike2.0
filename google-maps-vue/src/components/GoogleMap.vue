<template>
  <div id="map" ref="mapContainer" class="map"></div>
  <div v-if="props.borrowRecommendedLocation !== null || props.returnRecommendedLocation !== null" class="card border-primary shadow-lg animate__animated animate__fadeInUp my-4" style="border-radius: 15px; overflow: hidden;">
    <div class="card-body" style="background: linear-gradient(135deg, #e0f7fa 30%, #ffffff 100%);">
      <div v-if="props.borrowRecommendedLocation !== null && props.borrowRecommendedLocation.station != '無'">
        <h5 class="card-title text-primary mb-3" style="font-weight: bold;">
          借車時間： {{ props.formData.borrow_date }} {{ props.formData.borrow_time }}
        </h5>
        <p class="card-text mb-3" style="font-size: 1.1rem; color: #007bff;">
          推薦借車地點：<strong>{{ props.borrowRecommendedLocation.station }}</strong>
        </p>
        <button 
          class="btn btn-outline-primary btn-sm mb-4" 
          style="border-radius: 20px; padding: 0.5rem 1.5rem; font-size: 0.9rem;" 
          @click="showBorrowLocation">
          顯示借車位置
        </button>
      </div>
      <hr 
        v-if="props.borrowRecommendedLocation !== null && props.returnRecommendedLocation !== null" 
        style="border-top: 1px solid rgba(0, 123, 255, 0.5);">
      <div v-if="props.returnRecommendedLocation !== null && props.returnRecommendedLocation.station != '無'">
        <h5 class="card-title text-success mb-3" style="font-weight: bold;">
          還車時間： {{ props.formData.return_date }} {{ props.formData.return_time }}
        </h5>
        <p class="card-text mb-3" style="font-size: 1.1rem; color: #28a745;">
          推薦還車地點：<strong>{{ props.returnRecommendedLocation.station }}</strong>
        </p>
        <button 
          class="btn btn-outline-success btn-sm" 
          style="border-radius: 20px; padding: 0.5rem 1.5rem; font-size: 0.9rem;" 
          @click="showReturnLocation">
          顯示還車位置
        </button>
      </div>
    </div>
  </div>
  <div class="form-container container mt-5">
    <div v-if="formDataMap === '1' || formDataMap === '2'" class="form-group mb-3">
      <label for="borrow_block" class="form-label">借車區域:</label>
      <select id="borrow_block" class="form-select animate__animated animate__fadeIn"
        v-model="searchFormData.borrowBlock" @change="handleBorrowBlockChange">
        <option value="大安區">大安區</option>
        <option value="大同區">大同區</option>
        <option value="士林區">士林區</option>
        <option value="文山區">文山區</option>
        <option value="中正區">中正區</option>
        <option value="中山區">中山區</option>
        <option value="內湖區">內湖區</option>
        <option value="北投區">北投區</option>
        <option value="松山區">松山區</option>
        <option value="南港區">南港區</option>
        <option value="信義區">信義區</option>
        <option value="萬華區">萬華區</option>
        <option value="臺大公館校區">臺大公館校區</option>
      </select>
    </div>
    <div v-if="formDataMap === '1' || formDataMap === '2'" class="form-group mb-3">
      <label for="borrow_station" class="form-label">借車站點:</label>
      <select v-if="borrowStations.length == 1438" id="borrow_station"
        class="form-select animate__animated animate__fadeIn" v-model="searchFormData.borrowStation"
        @change="handleBorrowSatationChange">
        <template v-for="(station, index) in borrowStations">
          <option v-if="searchFormData.borrowBlock === station.block" :key="index" :value="station.value">
            {{ station.text }}
          </option>
        </template>
      </select>
    </div>
    <div v-if="formDataMap === '1' || formDataMap === '3'" class="form-group mb-3">
      <label for="return_block" class="form-label">還車區域:</label>
      <select id="return_block" class="form-select animate__animated animate__fadeIn"
        v-model="searchFormData.returnBlock" @change="handleReturnBlockChange">
        <option value="大安區">大安區</option>
        <option value="大同區">大同區</option>
        <option value="士林區">士林區</option>
        <option value="文山區">文山區</option>
        <option value="中正區">中正區</option>
        <option value="中山區">中山區</option>
        <option value="內湖區">內湖區</option>
        <option value="北投區">北投區</option>
        <option value="松山區">松山區</option>
        <option value="南港區">南港區</option>
        <option value="信義區">信義區</option>
        <option value="萬華區">萬華區</option>
        <option value="臺大公館校區">臺大公館校區</option>
      </select>
    </div>
    <div v-if="formDataMap === '1' || formDataMap === '3'" class="form-group mb-3">
      <label for="return_station" class="form-label">還車站點:</label>
      <select v-if="returnStations.length == 1438" id="return_station"
        class="form-select animate__animated animate__fadeIn" v-model="searchFormData.returnStation"
        @change="handleReturnSatationChange">
        <template v-for="(station, index) in returnStations">
          <option v-if="searchFormData.returnBlock === station.block" :key="index" :value="station.value">
            {{ station.text }}
          </option>
        </template>
      </select>
    </div>
  </div>
</template>


<script>
import { ref, onMounted, watch } from 'vue';
import { Loader } from '@googlemaps/js-api-loader';
import MarkerClusterer from '@googlemaps/markerclustererplus';

export default {
  name: 'GoogleMap',
  props: {
    borrowLocation: Object,
    returnLocation: Object,
    borrowRecommendedLocation: Object,
    returnRecommendedLocation: Object,
    formData: Object
  },
  setup(props, { emit }) {
    const mapContainer = ref(null);
    const formDataMap = ref('1');
    const searchFormData = ref({ borrowBlock: "", borrowStation: "", returnBlock: "", returnStation: "" });
    const borrowStations = ref([]);
    const returnStations = ref([]);
    let currentInfoWindow = null;
    let markerCluster = null;
    let markers = [];
    let borrowMarker = null;
    let returnMarker = null;
    let borrowRecommendedMarker = null;
    let returnRecommendedMarker = null;
    let map;
    let clickCount = 0; // 增加 clickCount 來跟踪點擊次數


    const roundTo = function (num, decimal) { return Math.round((num + Number.EPSILON) * Math.pow(10, decimal)) / Math.pow(10, decimal); }


    const updateBorrowMarker = (location) => {
      if (borrowMarker) {
        borrowMarker.setMap(null);
      }
      borrowMarker = new google.maps.Marker({
        position: location,
        map,
        title: 'Borrow Location',
        icon: {
          url: './borrow_location.ico',
          scaledSize: {
            width: 40,
            height: 40
          }
        }
      });
    };

    const updateReturnMarker = (location) => {
      if (returnMarker) {
        returnMarker.setMap(null);
      }
      returnMarker = new google.maps.Marker({
        position: location,
        map,
        title: 'Return Location',
        icon: {
          url: './return_location.ico',
          scaledSize: {
            width: 40,
            height: 40
          }
        }
      });
    };

    const updateBorrowRecommendedMarker = (location) => {
      if (borrowRecommendedMarker) {
        borrowRecommendedMarker.setMap(null);
      }
      borrowRecommendedMarker = new google.maps.Marker({
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
          <p>推薦借車站點: ${location.station}</p>
          <p>可借車輛: ${location.predicted_available_bikes}</p>
          <p>距離: ${roundTo(location.distance, 3) * 1000} (公尺)(m)</p>
        </div>
                  `
      });

      borrowRecommendedMarker.addListener('click', () => {
        if (currentInfoWindow) {
          currentInfoWindow.close();
        }
        infoWindow.open(map, borrowRecommendedMarker);
        currentInfoWindow = infoWindow;
      });
      infoWindow.open(map, borrowRecommendedMarker);
      currentInfoWindow = infoWindow;
      map.setZoom(18);  // 設置放大級別，可以根據需要調整
      map.setCenter(location);

    };

    const updateReturnRecommendedMarker = (location) => {
      if (returnRecommendedMarker) {
        returnRecommendedMarker.setMap(null);
      }
      returnRecommendedMarker = new google.maps.Marker({
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
          <p>推薦還車站點: ${location.station}</p>
          <p>剩餘空位: ${location.predicted_available_bikes}</p>
          <p>距離: ${roundTo(location.distance, 3) * 1000} (公尺)(m)</p>
        </div>
                  `
      });

      returnRecommendedMarker.addListener('click', () => {
        if (currentInfoWindow) {
          currentInfoWindow.close();
        }
        infoWindow.open(map, returnRecommendedMarker);
        currentInfoWindow = infoWindow;
      });
      infoWindow.open(map, returnRecommendedMarker);
      currentInfoWindow = infoWindow;
      map.setZoom(18);  // 設置放大級別，可以根據需要調整
      map.setCenter(location);

    };

    const updateMapCenter = (lat, lng, zoom = 20) => {
      map.setCenter({ lat, lng });
      map.setZoom(zoom); // Adjust zoom level as needed
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
        map.addListener('click', (event) => {
          if (event.placeId) {
            // 阻止 POI 點擊事件的默認行為
            event.stop();
          }
        });
        if (props.borrowLocation) {
          updateBorrowMarker(props.borrowLocation);
        }

        if (props.returnLocation) {
          updateReturnMarker(props.returnLocation);
        }

        // 監聽地圖點擊事件
        map.addListener('click', (event) => {
          const lat = event.latLng.lat();
          const lng = event.latLng.lng();
          const location = { lat, lng };

          if (clickCount === 0) {
            updateBorrowMarker(location);
            emit('borrowLocationUpdated', location);
            clickCount++;
          } else if (clickCount === 1) {
            updateReturnMarker(location);
            emit('returnLocationUpdated', location);
            clickCount = 0;  // 重置計數
          }
        });
        const populateSelectOptions = (stations) => {
          borrowStations.value = stations.map(station => ({
            value: station.title,
            text: station.title,
            block: station.block
          }));
          returnStations.value = stations.map(station => ({
            value: station.title,
            text: station.title,
            block: station.block
          }));
          console.log(borrowStations.value)

        };

        fetch('https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json')
          .then(response => response.json())
          .then(data => {

            const stationsList = [];
            data.forEach(station => {
              const sna = station.sna;
              const lat = station.latitude;
              const lng = station.longitude;
              const availableBikes = station.available_rent_bikes;
              const total = station.total;
              const act = station.act;
              const infoTime = station.infoTime;
              const sarea = station.sarea;

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

              stationsList.push({
                title: sna,
                block: sarea
              });
            });

            populateSelectOptions(stationsList);

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


    watch(() => props.borrowLocation, (newLocation) => {
      if (newLocation) {
        updateBorrowMarker(newLocation);
      }
    });

    watch(() => props.returnLocation, (newLocation) => {
      if (newLocation) {
        updateReturnMarker(newLocation);
      }
    });

    watch(() => props.borrowRecommendedLocation, (newLocation) => {
      if ((formDataMap.value == "1" || formDataMap.value == "2") && newLocation && newLocation.lat && newLocation.lng && !isNaN(newLocation.lat) && !isNaN(newLocation.lng)) {
        updateBorrowRecommendedMarker(newLocation);
      }
      if (formDataMap.value == "2")
      {
        returnRecommendedMarker.setMap(null);
        returnRecommendedMarker = null;
      }
    });

    watch(() => props.returnRecommendedLocation, (newLocation) => {
      if ((formDataMap.value == "1" || formDataMap.value == "3") && newLocation && newLocation.lat && newLocation.lng && !isNaN(newLocation.lat) && !isNaN(newLocation.lng)) {
        updateReturnRecommendedMarker(newLocation);
      }
      if (formDataMap.value == "3")
      {
        borrowRecommendedMarker.setMap(null);
        borrowRecommendedMarker = null;
      }
    });

    watch(() => props.formData.search_type, (search_type) => {
      formDataMap.value = search_type;
    });

    const handleBorrowSatationChange = () => {
      const newValue = searchFormData.value
      if (newValue.borrowStation) {
        const selectedStation = markers.find(marker => marker.title === newValue.borrowStation);
        if (selectedStation) {
          updateMapCenter(selectedStation.getPosition().lat(), selectedStation.getPosition().lng());
        }
      }
    }

    const handleReturnSatationChange = () => {
      const newValue = searchFormData.value
      if (newValue.returnStation) {
        const selectedStation = markers.find(marker => marker.title === newValue.returnStation);
        if (selectedStation) {
          updateMapCenter(selectedStation.getPosition().lat(), selectedStation.getPosition().lng());
        }
      }
    }

    const showBorrowLocation = () => {
      if (props.borrowRecommendedLocation) {
        updateBorrowRecommendedMarker(props.borrowRecommendedLocation);
        map.setZoom(18);
        map.setCenter(props.borrowRecommendedLocation);
      }
    };

    const showReturnLocation = () => {
      if (props.returnRecommendedLocation) {
        updateReturnRecommendedMarker(props.returnRecommendedLocation);
        map.setZoom(18);
        map.setCenter(props.returnRecommendedLocation);
      }
    };

    const handleBorrowBlockChange = () => {
      const newValue = searchFormData.value
      if (newValue.borrowBlock) {
        switch (newValue.borrowBlock) {
          case "大安區":
            updateMapCenter(25.02952, 121.55406, 15);
            break;
          case "大同區":
            updateMapCenter(25.06864, 121.5107, 15);
            break;
          case "士林區":
            updateMapCenter(25.08128, 121.51784, 15);
            break;
          case "文山區":
            updateMapCenter(25.00402, 121.54074, 15);
            break;
          case "中正區":
            updateMapCenter(25.013741, 121.53068, 15);
            break;
          case "中山區":
            updateMapCenter(25.08251, 121.54004, 15);
            break;
          case "內湖區":
            updateMapCenter(25.09122, 121.55961, 15);
            break;
          case "北投區":
            updateMapCenter(25.1168, 121.5048, 15);
            break;
          case "松山區":
            updateMapCenter(25.04987, 121.57785, 15);
            break;
          case "南港區":
            updateMapCenter(25.04591, 121.59226, 15);
            break;
          case "信義區":
            updateMapCenter(25.02035, 121.55769, 15);
            break;
          case "萬華區":
            updateMapCenter(25.02365, 121.49528, 15);
            break;
          case "臺大公館校區":
            updateMapCenter(25.01493, 121.53044, 15);
            break;
        }
      }
    }

    const handleReturnBlockChange = () => {
      const newValue = searchFormData.value
      if (newValue.returnBlock) {
        switch (newValue.returnBlock) {
          case "大安區":
            updateMapCenter(25.02952, 121.55406, 15);
            break;
          case "大同區":
            updateMapCenter(25.06864, 121.5107, 15);
            break;
          case "士林區":
            updateMapCenter(25.08128, 121.51784, 15);
            break;
          case "文山區":
            updateMapCenter(25.00402, 121.54074, 15);
            break;
          case "中正區":
            updateMapCenter(25.013741, 121.53068, 15);
            break;
          case "中山區":
            updateMapCenter(25.08251, 121.54004, 15);
            break;
          case "內湖區":
            updateMapCenter(25.09122, 121.55961, 15);
            break;
          case "北投區":
            updateMapCenter(25.1168, 121.5048, 15);
            break;
          case "松山區":
            updateMapCenter(25.04987, 121.57785, 15);
            break;
          case "南港區":
            updateMapCenter(25.04591, 121.59226, 15);
            break;
          case "信義區":
            updateMapCenter(25.02035, 121.55769, 15);
            break;
          case "萬華區":
            updateMapCenter(25.02365, 121.49528, 15);
            break;
          case "臺大公館校區":
            updateMapCenter(25.01493, 121.53044, 15);
            break;
        }
      }
    }

    return {
      mapContainer,
      borrowStations,
      returnStations,
      searchFormData,
      formDataMap,
      handleBorrowSatationChange,
      handleReturnSatationChange,
      handleBorrowBlockChange,
      handleReturnBlockChange,
      showBorrowLocation,
      showReturnLocation,
      props
    };
  }
};
</script>

<style scoped>
.map {
  height: 80vh;
  width: 80%;
  margin-top: 20px;
  color: black;
}

.form-container {
  max-width: 600px;
  margin: auto;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  color: rgb(31, 31, 31);
  font-size: larger;
}

.form-group {
  margin-bottom: 1rem;
}

.form-label {
  font-weight: 500;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.form-select {
  border-radius: 4px;
  border: 1px solid #ced4da;
}

.form-select:focus {
  box-shadow: none;
  border-color: #80bdff;
}

@media (max-width: 768px) {
  .form-container {

    font-size: medium;
  }

}
</style>
