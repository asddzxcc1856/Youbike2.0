<template>
  <transition name="fade" appear>
  <div class="container mt-5">
    <h1 class="text-center mb-4">網站地圖</h1>
    <div class="row justify-content-center">
      <div class="col-md-4 col-lg-3 mb-4" v-for="(item, index) in items" :key="index">
        <div class="card animate__animated animate__fadeIn">
          <div class="card-body">
            <h5 class="card-title">{{ item.title }}</h5>
            <router-link :to="item.link" class="btn btn-primary">{{ item.buttonText }}</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
 </transition>
</template>

<script>
export default {
  name: 'SiteMap',
  data() {
    return {
      items: [
        { title: '首頁', link: '/', buttonText: '前往首頁' },
        { title: '使用說明', link: '/instructions', buttonText: '查看使用說明' },
        { title: '關於團隊', link: '/about', buttonText: '了解我們的團隊' },
        { title: '聯絡我們', link: '/contact', buttonText: '聯絡我們' }
      ]
    }
  }
}
</script>

<style scoped>
/* Scoped styles for sitemap */
.card {
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  align-items: center;
  margin-bottom: 600px;
}

.card-title {
  font-size: 1.25rem;
  font-weight: bold;
  margin-bottom: 1rem;
  text-align: center;
}

.btn-primary {
  font-size: 1em;
  font-weight: bold;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}
</style>