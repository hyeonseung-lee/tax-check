import { createRouter, createWebHistory } from "vue-router";
import Login from "@/components/Login.vue";
import Main from "@/components/Main.vue";
import List from "@/components/List.vue";
import Report from "@/components/Report.vue";

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
  {
    path: "/report",
    name: "Report",
    component: Report,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
