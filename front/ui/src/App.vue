<template>
  <AppHeader></AppHeader>
  <router-view> </router-view>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link
    href="https://fonts.googleapis.com/css2?family=42dot+Sans:wght@300..800&display=swap"
    rel="stylesheet"
  />
</template>

<script>
import AppHeader from "./components/common/AppHeader.vue";
export default {
  name: "App",
  components: { AppHeader },
};
</script>

<style>
#app {
  font-family: "42dot Sans", serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #000000;
  margin-top: 60px;
}
</style>
