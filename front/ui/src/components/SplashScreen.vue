<template>
  <div class="splash-screen">
    <img src="@/assets/logo.png" alt="로고" class="logo" />
  </div>
</template>

<script>
export default {
  mounted() {
    setTimeout(() => {
      this.$router.replace({ name: "Login" }); // 로그인 화면으로 이동
    }, 3000); // 3초
  },
};
</script>

<style scoped>
.splash-screen {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* 전체 화면 높이 */
  background-color: #fff; /* 배경색 */
}
.logo {
  width: 200px; /* 로고의 너비 */
  height: auto; /* 자동 높이 */
}
</style>
