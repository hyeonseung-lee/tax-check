<template>
  <header class="header">
    <div class="header-content">
      <button class="menu-button" @click="toggleMenu">
        <svg
          data-slot="icon"
          fill="none"
          stroke-width="1.5"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
          aria-hidden="true"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
          ></path>
        </svg>
      </button>
      <button class="menu-logo">
        <img src="@/assets/logo.png" alt="메뉴" class="icon-image" />
      </button>
    </div>

    <!-- side bar open button -->
    <div class="side-menu" :class="{ 'side-menu-open': isMenuOpen }">
      <!-- X button -->
      <div class="close-button-container">
        <button class="close-button" @click="toggleMenu">
          <svg
            fill="none"
            stroke="currentColor"
            stroke-width="1.5"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
            aria-hidden="true"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M6 18L18 6M6 6l12 12"
            ></path>
          </svg>
        </button>
      </div>
      <!-- side bar -->
      <div class="list-container">
        <ul>
          <li>
            <a href="/main">절세전략 확인하기</a>
          </li>
          <li><a href="/list">절세전략 모아보기</a></li>
        </ul>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  data() {
    return {
      isMenuOpen: false,
    };
  },
  methods: {
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen;
    },
  },
};
</script>

<style scoped>
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 56px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  background-color: white;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  margin: 0 auto;
}

.left-section {
  display: flex;
  align-items: center;
  gap: 16px;
}

.icon-image {
  object-fit: contain;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 210px; /* 아이콘 크기 조절 */
}

.menu-button {
  width: 40px;
  padding-left: 10px;
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center; /* 상하 가운데 정렬 */
}

/* css for SIDE-MENU */
.side-menu {
  position: fixed;
  top: 0;
  left: -250px;
  width: 250px;
  height: 100%;
  background-color: #fff;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  transition: left 0.3s ease;
  z-index: 999;
}

.side-menu-open {
  left: 0;
}

.side-menu ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.side-menu li {
  padding: 16px;
  border-bottom: 1px solid #ddd;
}

.side-menu a {
  text-decoration: none;
  color: #333;
}

.close-button-container {
  position: relative;
}
.close-button {
  position: absolute;
  top: 5px;
  right: 0px;
  padding-top: 10px;
  padding-right: 10px;
  padding-bottom: 10px;
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
}
.close-button svg {
  width: 24px;
  height: 24px;
}

.list-container {
  padding-top: 56px;
}
</style>
