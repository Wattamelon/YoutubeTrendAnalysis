import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import vuetify from "./plugins/vuetify"; // ✅ Vuetify 플러그인 불러오기

const app = createApp(App);
app.use(router);
app.use(vuetify); // ✅ Vuetify 사용 등록
app.mount("#app");
