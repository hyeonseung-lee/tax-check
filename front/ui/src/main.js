import { createApp } from "vue";
import App from "./App.vue";
import router from "./router"; // 라우터 임포트

const app = createApp(App);
app.use(router); // 라우터 사용
app.mount("#app");
