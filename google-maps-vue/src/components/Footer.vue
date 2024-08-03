<template>
  <!-- Footer -->
  <footer>
    <div class="container">
      <div class="row">
        <!-- 快速鏈接 -->
        <div class="col-md">
          <h5>Youbike2.0推薦及預測系統</h5>
          <ul class="list-unstyled">
            <li><router-link to="/sitemap">網站地圖</router-link></li>
          </ul>
        </div>
        <!-- 快速鏈接 -->
        <div class="col-md">
          <h5>相關資訊與連結</h5>
          <ul class="list-unstyled">
            <li><router-link to="/">首頁</router-link></li>
            <li><router-link to="/contact">聯絡我們</router-link></li>
            <li><router-link to="/about">關於團隊</router-link></li>
            <li><router-link to="/instructions">使用說明</router-link></li>
          </ul>
        </div>
        <!-- 社交媒體 -->
        <div class="col-md">
          <h5>關注我們</h5>
          <div class="social-icons">
            <a href="#"><i class="fab fa-facebook-f"></i></a>
            <a href="#"><i class="fab fa-instagram"></i></a>
            <a href="#"><i class="fab fa-line"></i></a>
          </div>
        </div>
      </div>
      <hr>
      <p>&copy; 2024 YouBike 2.0 Recommendation System. All rights reserved.</p>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'FooterSection',
};
</script>

<style scoped>
/* Scoped styles for footer */
footer {
  background-color: #cbccce;
  color: #474747;
  width: 100%;
  padding: 20px 0;
  text-align: center;
  z-index: 2;
}

footer h5 {
  margin-bottom: 15px;
  color: #333;
}

footer p,
footer ul {
  margin: 0;
  color: #666;
}

footer ul {
  list-style-type: none;
  padding: 0;
}

footer a {
  color: #666;
  text-decoration: none;
}

footer a:hover {
  color: #333;
}

footer .social-icons a {
  color: #666;
  margin: 0 10px;
  font-size: 1.2em;
}

footer .social-icons a:hover {
  color: #333;
}

hr {
  border-top: 1px solid #ccc;
}
</style>
