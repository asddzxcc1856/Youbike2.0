<template>
  <div class="about-us-page">
    <h2>關於團隊</h2>
    <section class="team-members">
      <p>我們是一群追求新技術的大學生，致力於實作實用的功能來提供給大眾，這次的Youbike2.0預測以及推薦系統的建置，是透過大家的分工合作來完成，每個人負責的項目都是各自的專長和興趣。</p>
      <div class="member-card" v-for="member in team" :key="member.id">
        <img :src="member.photo" alt="Profile Photo" class="member-photo" />
        <h3>{{ member.name }}</h3>
        <p>{{ member.role }}</p>
        <p>{{ member.description }}</p>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'AboutUsPage',
  data() {
    return {
      team: [
        {
          id: 1,
          name: '王智弘',
          role: '學生',
          description: '專注於前端開發和UI設計。',
          photo: 'photo1.jpg'
        },
        {
          id: 2,
          name: '胡冠廷',
          role: '學生',
          description: '專注於系統架構和數據庫設計。',
          photo: 'photo1.jpg'
        },
        {
          id: 3,
          name: '蔡程安',
          role: '學生',
          description: '專注於系統架構和數據庫設計。',
          photo: 'photo1.jpg'
        },
        {
          id: 4,
          name: '賴威廷',
          role: '學生',
          description: '專注於模型訓練以及評估。',
          photo: 'photo1.jpg'
        },
        {
          id: 5,
          name: '賴庭岳',
          role: '學生',
          description: '專注於模型訓練以及評估。',
          photo: 'photo1.jpg'
        },
        // 可以添加更多團隊成員
      ]
    };
  }
}
</script>

<style scoped>
.about-us-page {
  padding: 20px;
  max-width: 800px;
  margin: auto;
}

.team-members {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.member-card {
  background-color: #f5f5f5;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  width: calc(50% - 20px);
  transition: transform 0.3s ease;
  color: rgb(31, 31, 31);
  font-weight: bold;
}

.member-card:hover {
  transform: scale(1.05);
}

.member-photo {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-bottom: 10px;
}

.member-card h3 {
  margin: 10px 0;
  font-size: 1.2em;
  font-weight: bold;
}

.member-card p {
  margin: 5px 0;
}
</style>
