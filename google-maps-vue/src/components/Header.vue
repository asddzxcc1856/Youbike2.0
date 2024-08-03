<template>
  <header>
    <div class="container">
      <div class="branding">
        <img src="@/assets/youbike2.0.png" alt="Youbike2.0" class="icon-image">
        <h1>YouBike 2.0 推薦及預測系統</h1>
      </div>
      <nav class="nav-links">
        <router-link to="/" @click="closeMenu">首頁</router-link>
        <router-link to="/instructions" @click="closeMenu">使用說明</router-link>
        <router-link to="/about" @click="closeMenu">關於團隊</router-link>
        <router-link to="/contact" @click="closeMenu">聯絡我們</router-link>
      </nav>
      <div class="mobile-menu-icon" @click="toggleMenu">
        <i class="fas fa-bars"></i>
      </div>
    </div>
    <div class="status-types">
      <div class="status">
        <img src="normal.ico" alt="Normal">正常租借
      </div>
      <div class="status">
        <img src="no_bike.ico" alt="No Bikes"> 無車可借
      </div>
      <div class="status">
        <img src="full.ico" alt="Full"> 車位滿載
      </div>
      <div class="status">
        <img src="closed.ico" alt="Closed"> 暫停營運
      </div>
      <div class="status">
        <img src="borrow_location.ico" alt="Borrow_Location"> 預定借站
      </div>
      <div class="status">
        <img src="return_location.ico" alt="Return_Location"> 預定還站
      </div>
    </div>

    <!-- Mobile Menu Modal -->
    <div class="modal" id="mobileMenuModal" tabindex="-1" role="dialog" aria-labelledby="mobileMenuModalLabel" aria-hidden="true">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="mobileMenuModalLabel">選單</h5>
            <button type="button" class="close" @click="closeMenu" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <router-link to="/" @click="closeMenu">首頁</router-link>
            <router-link to="/instructions" @click="closeMenu">使用說明</router-link>
            <router-link to="/about" @click="closeMenu">關於團隊</router-link>
            <router-link to="/contact" @click="closeMenu">聯絡我們</router-link>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'HeaderSection',
  data() {
    return {
      isMenuOpen: false
    };
  },
  methods: {
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen;
      const modal = document.getElementById('mobileMenuModal');
      if (this.isMenuOpen) {
        modal.classList.add('show');
        modal.style.display = 'block';
        modal.setAttribute('aria-modal', 'true');
        modal.removeAttribute('aria-hidden');
      } else {
        this.closeMenu();
      }
    },
    closeMenu() {
      const modal = document.getElementById('mobileMenuModal');
      modal.classList.remove('show');
      modal.style.display = 'none';
      modal.removeAttribute('aria-modal');
      modal.setAttribute('aria-hidden', 'true');
      this.isMenuOpen = false;
    }
  }
}
</script>

<style scoped>
header {
  background: rgba(136, 177, 201, 0.9);
  color: #fff;
  font-weight: bolder;
  padding-top: 20px;
  width: 100%;
}

.container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin: auto;
  padding: 0 20px;
}

.branding {
  display: flex;
  align-items: center;
  white-space: nowrap;
  padding-bottom: 5px;
}

.icon-image {
  width: 50px;
  height: 50px;
  margin-right: 10px;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-links a {
  color: #fff;
  text-decoration: none;
  font-size: 24px;
  transition: color 0.3s ease;
}

.nav-links a:hover {
  color: #ddd;
}

.mobile-menu-icon {
  display: none;
  cursor: pointer;
  font-size: 24px;
  color: #fff;
}

.status-types {
  display: flex;
  justify-content: space-around;
  align-items: center;
  background: rgba(103, 154, 185, 0.9);
  height: 100px;
  white-space: nowrap;
}

.status {
  text-align: center;
}

.status img {
  width: 40px;
  height: 40px;
  margin-bottom: 5px;
}

/* Media Queries for Responsive Design */
@media (max-width: 1200px) {
  .nav-links {
    display: none;
  }

  .mobile-menu-icon {
    display: block;
  }

  .status-types {
    flex-wrap: wrap;
    height: auto;
    padding-top: 20px;
  }

  .status {
    width: 50%;
    margin-bottom: 10px;
  }
  h1 {
    font-size: medium;
  }
}

@media (max-width: 600px) {
  h1 {
    font-size: small;
  }
}

/* Modal Styles */
.modal {
  display: none;
  position: fixed;
  z-index: 1050;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  outline: 0;
  transition: opacity 0.3s ease, transform 0.3s ease;
  background: rgba(0, 0, 0, 0.5);
}

.modal.show {
  display: block;
  opacity: 1;
  transform: scale(1);
}

.modal-dialog {
  position: relative;
  width: auto;
  margin: 10% auto;
  max-width: 500px;
}

.modal-content {
  position: relative;
  display: flex;
  flex-direction: column;
  background-color: #fff;
  background-clip: padding-box;
  border: 1px solid rgba(0, 0, 0, 0.2);
  border-radius: 0.3rem;
  outline: 0;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #dee2e6;
  border-top-left-radius: 0.3rem;
  border-top-right-radius: 0.3rem;
  padding: 0px;
}

.modal-body {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
}

.modal-body a {
  color: #0c0c0c;
  text-decoration: none;
  font-size: 16px;
  transition: color 0.3s ease;
}

.modal-body a:hover {
  color: #494848;
}

.modal-title {
  margin-bottom: 0;
  line-height: 1.5;
}

.close {
  padding: 0.75rem 1.25rem;
  color: #000;
  background: none;
  border: 0;
  cursor: pointer;
}

.close span {
  font-size: 1.5rem;
}
</style>
