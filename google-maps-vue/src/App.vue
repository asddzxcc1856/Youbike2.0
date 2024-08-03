<template>
  <div id="container">
    <transition name="fade" appear>
      <div v-if="!appLoaded" class="loading-container">
        <img src="@/assets/loading-bike.gif" alt="Loading..." class="loading-bike" />
      </div>
    </transition>
    <transition name="fade" appear>
      <Header v-if="appLoaded" />
    </transition>
    <router-view v-if="appLoaded" style="z-index: 2;"/>
    <transition name="fade" appear>
      <Footer v-if="appLoaded" />
    </transition>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'animate.css/animate.min.css';


export default {
  name: 'App',
  components: {
    Header,
    Footer
  },
  setup() {
    const appLoaded = ref(false);

    onMounted(() => {
      setTimeout(() => {
        appLoaded.value = true;
      }, 2000); // 模擬應用加載延遲
    });


    return {
      appLoaded
    };
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

#container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  min-height: 100vh;
  background: url('@/assets/Taipei-101-building-Taiwan.webp') no-repeat center center fixed;
  background-size: cover;
  font-family: 'Roboto', sans-serif;
  color: #f5f5f5;
  position: relative;
  z-index: 3; /* 背景層在主要內容後面 */
}

#container::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5); /* 半透明黑色遮罩 */
  z-index: -1; /* 背景層在主要內容後面 */
}

.loading-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  width: 100vw;
  background: rgba(255, 255, 255, 0.8); /* 半透明白色背景 */
  z-index: -1; /* 確保loading容器在最前面 */
}

.loading-bike {
  width: 100px;
  height: 100px;
}

@media (max-width: 768px) {
  #app {
    padding: 10px;
  }
}
</style>
