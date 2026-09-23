<template>
  <div class="video-planner">
    <h1>🎬 AI 유튜브 영상 기획 도우미</h1>

    <form @submit.prevent="generateVideoIdea">
      <!-- 타겟층 선택 -->
      <div class="form-group">
        <label>타겟층</label>
        <select v-model="form.target_audience" required>
          <option disabled value="">-- 선택하세요 --</option>
          <option>10대</option>
          <option>20대</option>
          <option>30대</option>
          <option>40대</option>
          <option>50대</option>
          <option>60대 이상</option>

        </select>
      </div>

      <!-- 영상 길이 선택 -->
      <div class="form-group">
        <label>영상 길이</label>
        <select v-model="form.video_length" required>
          <option disabled value="">-- 선택하세요 --</option>
          <option>1분</option>
          <option>3분</option>
          <option>5분</option>
          <option>5분 이상</option>
        </select>
      </div>

      <!-- 주요 키워드 -->
      <div class="form-group">
        <label>📌 주요 키워드</label>
        <input v-model="form.main_keyword" placeholder="예: 미국" required />
      </div>

      <!-- 연관 키워드 -->
      <div class="form-group">
        <label>🔗 연관 키워드 (쉼표로 구분)</label>
        <input v-model="form.related_keywords" placeholder="예: 관세, 트럼프, 한국" />
      </div>

      <!-- 스타일 선택 -->
      <div class="form-group">
        <label>🎨 스타일</label>
        <select v-model="form.style" required>
          <option disabled value="">-- 선택하세요 --</option>
          <option>사실 소개 중심</option>
          <option>개그 스타일</option>
          <option>유행하는 밈 기반 스타일</option>
        </select>
      </div>

      <button type="submit" :disabled="loading">
        {{ loading ? '생성 중...' : '생성하기' }}
      </button>
    </form>

    <!-- 결과 출력 -->
    <div v-if="result" class="result-box">
      <h2>✅ 제목</h2>
      <p class="title">{{ result.title }}</p>

      <h2>📝 스크립트</h2>
      <pre class="script">{{ result.script }}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
const apiUrl = process.env.VUE_APP_API_URL;

const form = ref({
  target_audience: '',
  video_length: '',
  main_keyword: '',
  related_keywords: '',
  style: ''
})

const result = ref(null)
const loading = ref(false)

const generateVideoIdea = async () => {
  loading.value = true
  result.value = null

  try {
    const res = await axios.post(`${apiUrl}/planner`, {
      target_audience: form.value.target_audience,
      video_length: form.value.video_length,
      main_keyword: form.value.main_keyword,
      related_keywords: form.value.related_keywords.split(',').map(k => k.trim()),
      style: form.value.style
    })
    result.value = res.data.result
  } catch (err) {
    alert("에러 발생: " + err.message)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.video-planner {
  max-width: 800px;
  margin: 0 auto;
  padding: 24px;
  font-family: 'Pretendard', sans-serif;
}
form {
  background: #f7f7f7;
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 30px;
}
.form-group {
  margin-bottom: 16px;
}
input, select {
  width: 100%;
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid #ccc;
}
button {
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
button:disabled {
  background: gray;
}
.result-box {
  background: #ffffff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.title {
  font-size: 1.2rem;
  font-weight: bold;
}
.script {
  background: #f1f1f1;
  padding: 12px;
  border-radius: 8px;
  white-space: pre-wrap;
}
</style>
