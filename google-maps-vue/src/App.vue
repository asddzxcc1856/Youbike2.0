<template>
  <div id="app">
    <div v-if="!appLoaded" class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
    <Header v-if="appLoaded" />
    <form v-if="appLoaded" @submit.prevent="handleSubmit" class="form-container">
      <label for="date">選擇日期:</label>
      <input type="date" v-model="formData.date" :min="minDate" required @change="handleDateChange" />
      <label for="time">選擇時間:</label>
      <input type="time" v-model="formData.time" :min="minTime" required />
      <button type="submit" class="btn btn-primary">送出</button>
    </form>
    <GoogleMap
      v-if="appLoaded"
      class="map animated fadeIn"
      @locationUpdated="updateLocation"
      :userLocation="userLocation"
      :recommendedLocation="recommendedLocation"
    />
    <Footer v-if="appLoaded" />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import GoogleMap from './components/GoogleMap.vue';
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'animate.css/animate.min.css';

export default {
  name: 'App',
  components: {
    GoogleMap,
    Header,
    Footer
  },
  setup() {
    const appLoaded = ref(false);
    const formData = ref({ date: '', time: '' });
    const userLocation = ref(null);
    const recommendedLocation = ref(null);
    const minDate = ref(new Date().toISOString().split('T')[0]);
    const minTime = ref(new Date().toLocaleTimeString('it-IT').slice(0, 5));

    onMounted(() => {
      setTimeout(() => {
        appLoaded.value = true;
      }, 2000); // 模擬應用加載延遲

      const now = new Date();
      formData.value.date = now.toISOString().split('T')[0];
      formData.value.time = now.toLocaleTimeString('it-IT').slice(0, 5);

      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          position => {
            userLocation.value = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };
          },
          error => {
            console.error('Error getting user location:', error);
          }
        );
      }
    });

    const handleSubmit = async () => {
      if (!userLocation.value) {
        alert('無法獲取使用者位置');
        return;
      }

      const data = {
        date: formData.value.date,
        time: formData.value.time,
        location: userLocation.value
      };

      try {
        const response = await fetch('http://192.168.1.7:5000/api/recommend', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const result = await response.json();
        
        // 確保經緯度值是有效的數字
        if (result.location.lat && result.location.lng && !isNaN(result.location.lat) && !isNaN(result.location.lng)) {
          recommendedLocation.value = {
            lat: parseFloat(result.location.lat),
            lng: parseFloat(result.location.lng),
            station: result.station,
            distance: result.distance,
            predicted_available_bikes: result.predicted_available_bikes
          };
        } else {
          console.error('Invalid coordinates received from the API');
        }

        console.log('Recommendation:', result);
      } catch (error) {
        console.error('Error submitting data:', error);
      }
    };

    const updateLocation = (location) => {
      userLocation.value = location;
    };

    const handleDateChange = () => {
      const selectedDate = new Date(formData.value.date);
      const today = new Date();
      
      if (selectedDate.toDateString() === today.toDateString()) {
        minTime.value = today.toLocaleTimeString('it-IT', { hour12: false }).slice(0, 5);
      } else {
        minTime.value = '00:00';
      }
    };

    return {
      appLoaded,
      formData,
      minDate,
      minTime,
      handleSubmit,
      userLocation,
      recommendedLocation,
      updateLocation,
      handleDateChange
    };
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

#app {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f0f0, #ffffff);
  font-family: 'Roboto', sans-serif;
}

.spinner-border {
  margin-top: 20%;
}

.map {
  height: 70vh;
  width: 80vw;
  margin: 20px auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  background-color: #c5b1b1;
}

.form-container {
  width: 80vw;
  padding: 20px;
  margin-top: 20px;
  background: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-bottom: 20px;
}

.form-container label {
  margin: 5px 0;
  font-weight: bold;
}

.form-container input {
  margin: 5px 0;
  padding: 8px;
  width: 100%;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.form-container button {
  margin-top: 10px;
  align-self: flex-end;
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
}

.form-container button:hover {
  background-color: #0056b3;
}

@media (max-width: 768px) {
  #app {
    padding: 10px;
  }

  .form-container {
    width: 100%;
  }

  .map {
    width: 100%;
  }
}
</style>
