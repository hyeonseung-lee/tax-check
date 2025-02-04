import { createRouter, createWebHistory } from "vue-router";
import Login from "@/components/Login.vue";
import Main from "@/components/Main.vue";
import List from "@/components/List.vue";
import Report from "@/components/Report.vue";
import ReportHistory from "@/components/ReportHistory.vue";

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
  {
    path: "/report-history",
    name: "ReportHistory",
    component: ReportHistory,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
