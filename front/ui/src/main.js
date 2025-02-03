import { createApp } from "vue";
import App from "./App.vue";
import router from "./router"; // 라우터 임포트

// Vuetify
import "vuetify/styles";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";

const vuetify = createVuetify({
  components,
  directives,
});

const app = createApp(App);
app.use(vuetify);
app.use(router); // 라우터 사용
app.mount("#app");
