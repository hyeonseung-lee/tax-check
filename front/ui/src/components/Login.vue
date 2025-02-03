<template>
  <div class="login">
    <h1>로그인 화면</h1>
    <button @click="goToMain">메인 화면으로 이동</button>
  </div>
</template>

<script>
export default {
  name: "LoginPage",
  methods: {
    goToMain() {
      this.$router.push({ name: "Main" }); // 메인 화면으로 이동
    },
  },
};
</script>

<style scoped>
.login {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* 전체 화면 높이 */
  background-color: #f5f5f5; /* 배경색 */
}
button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}
</style>
