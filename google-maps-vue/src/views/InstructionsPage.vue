<template>
  <div class="instructions-page">
    <h2>使用說明</h2>
    <section class="instructions-content">
      <p>歡迎使用我們的網站！以下是一些基本的使用說明：</p>
      <ul>
        <li>
          <h3>如何查詢推薦的租借站</h3>
          <p>首先，在地圖上可以透過點擊特定位置設定借還站點(第一下是借站，第二下是還站，第三下之後重複)，然後在搜尋框中輸入預定使用的日期和時間，點擊送出按鈕之後，Google地圖上會顯示推薦的借還站點。</p>
        </li>
        <li>
          <h3>如何使用近期查詢過的地點</h3>
          <p>提供查詢紀錄查看近期查詢過的紀錄，包含過去的查詢時間以及查詢預定使用的借還時間和推薦的借還站點，可以讓您不必再次進行重複的查詢。</p>
        </li>
        <li>
          <h3>如何聯絡我們</h3>
          <p>有任何問題，可以透過點擊「聯絡我們」頁面，填寫聯絡表單，我們會盡快回覆您，並且處理問題。</p>
        </li>
        <li>
          <h3>如何了解我們的團隊</h3>
          <p>點擊「關於團隊」頁面，您可以了解我們的團隊成員在這個 Youbike2.0 推薦及預測系統的製作項目。</p>
        </li>
      </ul>
    </section>
  </div>
</template>

<script>
export default {
  name: 'InstructionsPage'
}
</script>

<style scoped>
.instructions-page {
  padding: 20px;
  max-width: 800px;
  margin: auto;
  
}

.instructions-content {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  color: rgb(31, 31, 31);
}


.instructions-content ul {
  list-style-type: none;
  padding: 0;
}

.instructions-content li {
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  transition: background-color 0.3s ease;
}

.instructions-content li:hover {
  background-color: #f9f9f9;
}

.instructions-content h3 {
  margin-top: 0;
  font-size: 1.2em;
  font-weight: bolder;
}
</style>
