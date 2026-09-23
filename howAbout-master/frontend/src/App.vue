<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import Navbar from "./components/NavbarComponent.vue";
import SearchBarComponent from "./components/SearchBarComponent.vue";

// 로그인 상태 전역 관리
const isLoggedIn = ref(false);
const username = ref("");
const route = useRoute();

// 로그인 성공 시 상태 반영
const updateLoginState = (name) => {
  isLoggedIn.value = true;
  username.value = name;
};

// 앱 로드시 토큰 기반 로그인 복원
onMounted(async () => {
  const token = localStorage.getItem("token");
  const savedUsername = localStorage.getItem("username");

  if (token && savedUsername) {
    isLoggedIn.value = true;
    username.value = savedUsername;
  } else {
    isLoggedIn.value = false;
    username.value = "";
  }
});
</script>

<template>
  <Navbar
    :isLoggedIn="isLoggedIn"
    :username="username"
    @login-success="updateLoginState"
  />
  <!-- SearchBar는 /register 제외 + 메인에서는 아래로 더 내려오게 -->
  <div
    v-if="route.path !== '/register'"
    :class="['main-container', { 'main-home': route.path === '/' }]"
  >
    <!-- 🔥 로고는 메인에서만 표시 -->
    <router-link v-if="route.path === '/'" to="/">
      <img src="@/assets/logo.png" alt="로고" class="logo" />
    </router-link>

    <SearchBarComponent />
  </div>

  <router-view />
</template>

<style>
html,
body {
  margin: 0;
  padding: 0;
  height: 100%;
}

.main-container {
  display: flex;
  flex-direction: column; /* 수직 정렬 */
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.main-home {
  height: 50vh; /* 메인에서만 살짝 아래로 */
}

@media screen and (max-width: 768px) {
  .main-container {
    flex-direction: column;
    height: auto;
  }
}

.logo {
  width: 250px;
  margin-bottom: 1px;
  margin-top: 20px; /* 필요 시 위쪽 여백 추가 */
}
</style>
