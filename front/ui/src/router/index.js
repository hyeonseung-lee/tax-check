import { createRouter, createWebHistory } from "vue-router";
import Login from "@/components/Login.vue";
import Main from "@/components/Main.vue";
import List from "@/components/List.vue";
const routes = [
  {
    path: "/",
    name: "Login",
    component: Login,
  },
  {
    path: "/main",
    name: "Main",
    component: Main,
  },
  {
    path: "/list",
    name: "List",
    component: List,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
