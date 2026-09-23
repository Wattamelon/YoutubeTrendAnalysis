<template>
  <div class="search-container">
    <h2 class="title">🎧 유튜브 요약/키워드 추출</h2>
    <div class="input-section">
      <input
        v-model="youtubeUrl"
        type="text"
        placeholder="유튜브 영상 링크를 입력하세요"
        class="url-input"
      />
      <button
        @click="analyzeYoutube"
        :disabled="loading"
        class="analyze-button"
      >
        {{ loading ? "분석 중..." : "분석하기" }}
      </button>
    </div>

    <div v-if="result" class="result-section">
      <h3>📄 요약 결과</h3>
      <p class="summary">{{ result.summary_text }}</p>

      <!-- <h4>🔑 키워드</h4>
      <ul>
        <li v-for="(kw, i) in extractedKeywords" :key="i">#{{ kw }}</li>
      </ul> -->
    </div>

    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      youtubeUrl: "",
      result: null,
      error: "",
      loading: false,
    };
  },
  computed: {
    extractedKeywords() {
      if (!this.result?.summary_text) return [];
      const match = this.result.summary_text.match(/\n\n?(.*)/);
      if (match) {
        const keywords = match[1]
          .split(/[,\n]/)
          .map((k) => k.trim())
          .filter(Boolean);
        return keywords.slice(0, 5);
      }
      return [];
    },
  },
  methods: {
    async analyzeYoutube() {
      this.loading = true;
      this.result = null;
      this.error = "";
      try {
        const response = await axios.get(`http://localhost:3000/run-audio`, {
          params: { url: this.youtubeUrl },
        });
        this.result = response.data;
        console.log("✅ response:", response);              // 전체 응답 객체
        console.log("✅ response.data:", response.data);    // JSON 결과만
      } catch (err) {
        this.error = err.response?.data?.error || "요청 실패";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.search-container {
  max-width: 700px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

.title {
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
}

.input-section {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-bottom: 1rem;
}

.url-input {
  width: 60%;
  padding: 0.5rem;
  font-size: 1rem;
}

.analyze-button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

.analyze-button:disabled {
  background-color: gray;
}

.result-section {
  margin-top: 2rem;
  text-align: left;
}

.summary {
  white-space: pre-wrap;
  background: #f9f9f9;
  padding: 1rem;
  font-size: 1rem;

  border-radius: 6px;
  margin-bottom: 1rem;
}

ul {
  list-style: none;
  padding-left: 0;
}

li {
  display: inline-block;
  margin-right: 8px;
  background: #e0e0e0;
  padding: 5px 10px;
  border-radius: 4px;
}

.info {
  font-size: 0.9rem;
  color: #666;
}

.error {
  color: red;
  margin-top: 1rem;
}
</style>
