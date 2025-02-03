<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <a href="#" class="logo">로고</a>
      <button @click="toggleMenu" class="menu-toggle" aria-label="Toggle menu">
        <span v-if="!isMenuOpen">☰</span>
        <span v-else>✖</span>
      </button>
    </div>
    <ul :class="{ 'is-active': isMenuOpen }" class="navbar-menu">
      <li class="navbar-item"><a href="#home">홈</a></li>
      <li class="navbar-item"><a href="#about">소개</a></li>
      <li class="navbar-item"><a href="#services">서비스</a></li>
      <li class="navbar-item"><a href="#contact">연락처</a></li>
    </ul>
  </nav>
</template>

<script>
import { ref } from "vue";

export default {
  setup() {
    const isMenuOpen = ref(false);

    const toggleMenu = () => {
      isMenuOpen.value = !isMenuOpen.value;
    };

    return { isMenuOpen, toggleMenu };
  },
};
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #333;
  color: white;
}

.navbar-brand {
  display: flex;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  color: white;
  text-decoration: none;
}

.menu-toggle {
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  margin-left: 1rem;
}

.navbar-menu {
  display: flex;
  list-style: none;
  padding: 0;
  margin: 0;
}

.navbar-item {
  margin: 0 1rem;
}

.navbar-item a {
  color: white;
  text-decoration: none;
}

.navbar-menu.is-active {
  display: block; /* 메뉴가 열렸을 때 */
}

@media (max-width: 768px) {
  .navbar-menu {
    display: none; /* 기본적으로 숨김 */
    flex-direction: column;
    position: absolute;
    top: 100%;
    left: 0;
    background-color: #333;
    width: 100%;
  }

  .navbar-menu.is-active {
    display: flex; /* 메뉴가 열렸을 때 표시 */
  }

  .navbar-item {
    margin: 0.5rem 0;
  }
}
</style>
