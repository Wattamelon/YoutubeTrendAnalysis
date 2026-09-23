<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const props = defineProps({
  isLoggedIn: Boolean,
  username: String,
});
const emit = defineEmits(["login-success"]);

const router = useRouter();
const isModalOpen = ref(false);
const userid = ref("");
const password = ref("");
const errorMessage = ref("");
const isMenuOpen = ref(false);
const menuRef = ref(null);

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};

const hamburgerRef = ref(null);

// 외부 클릭 감지
const handleClickOutside = (e) => {
  if (
    menuRef.value &&
    !menuRef.value.contains(e.target) &&
    hamburgerRef.value &&
    !hamburgerRef.value.contains(e.target)
  ) {
    isMenuOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener("click", handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener("click", handleClickOutside);
});

// 로그인 요청
const login = async () => {
  if (!userid.value || !password.value) {
    errorMessage.value = "아이디와 비밀번호를 입력하세요!";
    return;
  }

  try {
    const response = await axios.post("/auth/login", {
      userid: userid.value,
      password: password.value,
    });

    if (response.data.access_token) {
      localStorage.setItem("token", response.data.access_token);
      localStorage.setItem("username", response.data.username);
      emit("login-success", response.data.username);
      alert("로그인 성공!");
      closeModal();
      router.push("/");
    } else {
      errorMessage.value = "로그인 실패!";
    }
  } catch (err) {
    errorMessage.value = err.response?.data?.message || "오류 발생";
  }
};

// 로그아웃
const logout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("username");
  location.reload();
};

// 모달 제어
const openModal = () => {
  isModalOpen.value = true;
  window.addEventListener("keydown", escClose);
};
const closeModal = () => {
  isModalOpen.value = false;
  userid.value = "";
  password.value = "";
  errorMessage.value = "";
  window.removeEventListener("keydown", escClose);
};
const escClose = (e) => {
  if (e.key === "Escape") closeModal();
};

const goToRegister = () => {
  router.push("/register");
  closeModal();
};
</script>

<template>
  <nav class="navbar">
    <div class="hamburger" ref="hamburgerRef" @click="toggleMenu">
      <span></span>
      <span></span>
      <span></span>
    </div>

    <transition name="slide-fade">
      <div v-if="isMenuOpen" class="dropdown-menu" ref="menuRef">
        <router-link to="/">홈</router-link>
        <router-link to="/Ranking">키워드 랭킹</router-link>
        <router-link to="/about">영상요약</router-link>
        <router-link to="/planner">동영상 플래너</router-link>
      </div>
    </transition>

    <!-- 🔥 텍스트 로고 -->
    <router-link to="/" class="text-logo"> 이거어때 </router-link>

    <div>
      <template v-if="props.isLoggedIn">
        <span class="welcome-message">환영합니다, {{ props.username }}님!</span>
        <button class="logout-btn" @click="logout">로그아웃</button>
      </template>
      <button v-else class="login-btn" @click="openModal">로그인</button>
    </div>
  </nav>

  <div v-if="isModalOpen" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <h2>로그인</h2>
      <div class="form-group">
        <label>아이디</label>
        <input type="text" v-model="userid" placeholder="아이디를 입력하세요" />
      </div>
      <div class="form-group">
        <label>비밀번호</label>
        <input
          type="password"
          v-model="password"
          placeholder="비밀번호를 입력하세요"
        />
      </div>
      <p class="error" v-if="errorMessage">{{ errorMessage }}</p>
      <button class="modal-btn" @click="login">로그인</button>
      <button class="register-btn" @click="goToRegister">회원가입</button>
      <button class="close-btn" @click="closeModal">닫기</button>
    </div>
  </div>
</template>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #dd3333;
  padding: 5px 20px;
  position: relative;
}

.text-logo {
  font-size: 22px;
  font-weight: bold;
  color: white;
  text-decoration: none;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

.hamburger {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  cursor: pointer;
  margin-left: 10px;
}

.hamburger span {
  width: 25px;
  height: 3px;
  background-color: white;
  border-radius: 2px;
}

.dropdown-menu {
  position: absolute;
  top: 60px;
  left: 10px;
  background: white;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  z-index: 999;
}

.dropdown-menu a {
  text-decoration: none;
  padding: 8px 12px;
  color: #333;
  font-weight: bold;
  border-radius: 5px;
}

.dropdown-menu a:hover {
  background: #f0f0f0;
  transition: 0.2s;
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

.welcome-message {
  color: white;
  margin-right: 10px;
}

.login-btn,
.logout-btn {
  background-color: white;
  color: #dd3333;
  border: none;
  padding: 10px 15px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  border-radius: 10px;
}

.logout-btn {
  background-color: #444;
  color: white;
}

.login-btn:hover {
  background-color: #fff3f3;
  color: #c40000;
  transition: 0.2s;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width: 350px;
  text-align: center;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3);
}

.form-group {
  margin: 15px 0;
  text-align: left;
}

input {
  width: 93%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  outline: none;
}

.modal-btn {
  padding: 10px;
  width: 100%;
  background-color: red;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  margin-top: 15px;
}

.register-btn {
  padding: 10px;
  width: 100%;
  background-color: rgb(232, 66, 20);
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  margin-top: 15px;
}

.close-btn {
  padding: 10px;
  width: 100%;
  background-color: gray;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  margin-top: 15px;
}
</style>
