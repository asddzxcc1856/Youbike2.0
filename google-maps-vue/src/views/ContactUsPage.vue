<template>
  <div class="contact-us-page">
    <h2>聯絡我們</h2>
    <section class="contact-form">
      <p>如果您有任何問題或建議，請填寫以下表單與我們聯絡：</p>
      <form @submit.prevent="submitForm">
        <label for="name">姓名</label>
        <input type="text" id="name" v-model="form.name" required />

        <label for="email">電子郵件</label>
        <input type="email" id="email" v-model="form.email" required />

        <label for="message">訊息</label>
        <textarea id="message" v-model="form.message" rows="4" required></textarea>

        <button type="submit" class="submit-button">送出</button>
      </form>
    </section>
  </div>
</template>

<script>
export default {
  name: 'ContactUsPage',
  data() {
    return {
      form: {
        name: '',
        email: '',
        message: ''
      }
    };
  },
  methods: {
    async submitForm() {
      try {
        const response = await fetch('http://localhost/api/contact', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.form)
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        alert('表單已送出！');
        this.form.name = '';
        this.form.email = '';
        this.form.message = '';
      } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
        alert('表單提交失敗，請稍後再試。');
      }
    }
  }
}
</script>

<style scoped>
.contact-us-page {
  padding: 20px;
  max-width: 600px;
  margin: auto;
}

.contact-form {
  background-color: #f5f5f5;
  padding: 20px;
  border-radius: 8px;
  color: rgb(31, 31, 31);
}

.contact-form label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
}

.contact-form input,
.contact-form textarea {
  width: 100%;
  padding: 10px;
  margin-bottom: 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.contact-form .submit-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.contact-form .submit-button:hover {
  background-color: #0056b3;
}
</style>
