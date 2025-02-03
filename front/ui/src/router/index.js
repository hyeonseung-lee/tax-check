import { createRouter, createWebHistory } from "vue-router";
import SplashScreen from "@/components/SplashScreen.vue";
import Login from "@/components/Login.vue";
import Main from "@/components/Main.vue";

const routes = [
  {
    path: "/",
    name: "SplashScreen",
    component: SplashScreen,
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/main",
    name: "Main",
    component: Main,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
