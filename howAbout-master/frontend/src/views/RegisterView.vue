<template>
  <div class="register-container">
    <h2>회원가입</h2>

    <form @submit.prevent="register">
      <div class="form-group">
        <label for="username">이름</label>
        <input
          type="text"
          id="username"
          v-model="username"
          placeholder="이름을 입력하세요"
        />
      </div>

      <div class="form-group">
        <label for="id">아이디</label>
        <input
          type="text"
          id="userid"
          v-model="userid"
          placeholder="아이디를 입력하세요"
        />
      </div>

      <div class="form-group">
        <label for="password">비밀번호</label>
        <input
          type="password"
          id="password"
          v-model="password"
          placeholder="비밀번호를 입력하세요"
        />
      </div>

      <p class="error-message" v-if="errorMessage">{{ errorMessage }}</p>

      <button type="submit" class="register-btn">회원가입</button>
      <button type="button" class="back-btn" @click="goBack">뒤로 가기</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();
const username = ref("");
const userid = ref("");
const password = ref("");
const errorMessage = ref("");
const apiUrl = process.env.VUE_APP_API_URL;

const register = async () => {
  if (!username.value || !userid.value || !password.value) {
    errorMessage.value = "모든 필드를 입력하세요!";
    return;
  }

  try {
    console.log("회원가입 요청:", {
      userid: userid.value,
      username: username.value,
      password: password.value,
    });

    const response = await axios.post(`${apiUrl}/auth/register`, {
      userid: userid.value,
      username: username.value,
      password: password.value,
    });

    if (response.data.result === "ok") {
      alert("회원가입 성공! 🎉");
      router.push("/"); // ✅ 회원가입 성공 시 로그인 페이지로 이동
    } else {
      errorMessage.value = response.data.message || "회원가입 실패!";
    }
  } catch (error) {
    console.error("회원가입 오류:", error);
    errorMessage.value =
      error.response?.data?.message || "회원가입 중 오류 발생!";
  }
};

const goBack = () => {
  router.push("/");
};
</script>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 30px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h2 {
  color: black;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
  text-align: left;
}

label {
  display: block;
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  outline: none;
  transition: 0.3s;
}

input:focus {
  border-color: #dd3333;
  box-shadow: 0 0 5px rgba(221, 51, 51, 0.3);
}

.error-message {
  color: red;
  font-size: 14px;
  margin-bottom: 10px;
}

.register-btn {
  width: 100%;
  padding: 12px;
  background-color: #dd3333;
  color: white;
  border: none;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  border-radius: 5px;
  transition: 0.3s;
  margin-top: 10px;
}

.register-btn:hover {
  background-color: #bb2222;
}

.back-btn {
  width: 100%;
  padding: 12px;
  background-color: gray;
  color: white;
  border: none;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  border-radius: 5px;
  transition: 0.3s;
  margin-top: 10px;
}

.back-btn:hover {
  background-color: darkgray;
}
</style>
