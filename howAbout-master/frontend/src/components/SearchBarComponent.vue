<template>
  <div class="search-bar" ref="searchBarRef">
    <input
      type="text"
      :value="searchQuery"
      placeholder="키워드를 검색하세요..."
      @input="handleInput"
      @compositionstart="handleCompositionStart"
      @compositionend="handleCompositionEnd"
      @keyup.enter="emitSearch"
    />

    <ul v-if="suggestions.length" class="suggestions">
      <li
        v-for="(s, i) in suggestions"
        :key="i"
        @click="selectSuggestion(s)"
        :class="{ active: selectedIndex === i }"
      >
        🔍 {{ s }}
      </li>
    </ul>

    <button @click="emitSearch">검색</button>

    <!-- 최근 검색어 태그 스타일 -->
    <div v-if="recentKeywords.length" class="recent-keywords">
      <div class="recent-label">최근 검색어:</div>
      <div class="chip-list">
        <span
          class="chip"
          v-for="(keyword, i) in recentKeywords"
          :key="'recent-' + i"
          @click="useRecentKeyword(keyword)"
        >
          #{{ keyword }}
        </span>
      </div>
    </div>
  </div>

  <!-- 키워드 추천 모달 -->
  <div v-if="showModal" class="modal-overlay">
    <div class="modal-content">
      <h3>‘{{ searchQuery }}’에 대한 결과가 없습니다</h3>

      <div v-if="altKeywords.length">
        <p>대신 이런 키워드는 어떤가요?</p>
        <ul class="alt-list">
          <li
            v-for="(alt, i) in altKeywords"
            :key="i"
            @click="selectAlternative(alt)"
          >
            🔍 {{ alt }}
          </li>
        </ul>
      </div>
      <div v-else>
        <p>관련 키워드도 없습니다.</p>
      </div>

      <button @click="showModal = false">닫기</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import debounce from "lodash/debounce"; // lodash 사용 시

const searchQuery = ref("");
const suggestions = ref([]);
const selectedIndex = ref(-1); // 🔥 키보드 선택용
const router = useRouter();
const searchBarRef = ref(null);
//const apiUrl = process.env.VUE_APP_API_URL;
const recentKeywords = ref([]);
const showModal = ref(false);
const altKeywords = ref([]);

//대안 검색어
const selectAlternative = (keyword) => {
  searchQuery.value = keyword;
  showModal.value = false;
  emitSearch();
};
// mount 시 로컬에서 불러오기
onMounted(() => {
  const stored = sessionStorage.getItem("recentKeywords"); // ✅ 변경
  if (stored) {
    recentKeywords.value = JSON.parse(stored);
  }
});

// 검색어 저장 함수
const saveRecentKeyword = (keyword) => {
  const trimmed = keyword.trim();
  if (!trimmed) return;

  const newList = [
    trimmed,
    ...recentKeywords.value.filter((k) => k !== trimmed),
  ].slice(0, 5);
  recentKeywords.value = newList;
  sessionStorage.setItem("recentKeywords", JSON.stringify(newList)); // ✅ 변경
};

// 클릭 시 검색 실행
const useRecentKeyword = (keyword) => {
  searchQuery.value = keyword;
  emitSearch();
};

const isComposing = ref(false);

const handleInput = (e) => {
  const value = e.target.value;
  searchQuery.value = value; // 직접 업데이트!
  if (!isComposing.value) {
    fetchSuggestions(value); // 바로 전달
  }
};

const handleCompositionEnd = (e) => {
  isComposing.value = false;
  searchQuery.value = e.target.value; // 조합 완료된 값 반영
  getSuggestions(e.target.value); // 즉시 실행
};

// // 🔹 자동완성 함수
// const getSuggestions = async (value) => {
//   const query = value ?? searchQuery.value;
//   if (!query) {
//     suggestions.value = [];
//     return;
//   }

//   const words = query.split(" ");

//   try {
//     if (words.length === 1) {
//       const res = await axios.get(`${apiUrl}/api/keyword-suggest`, {
//         params: { q: words[0] },
//       });
//       suggestions.value = res.data.slice(0, 14);
//     } else if (words.length >= 2) {
//       const res = await axios.get(`${apiUrl}/api/mongo-related-suggest`, {
//         params: { q: words[0] },
//       });
//       const mapped = res.data.map((r) => `${words[0]} > ${r.split(" > ")[1]}`);
//       suggestions.value = mapped.slice(0, 14);
//     }
//     selectedIndex.value = -1;
//   } catch (e) {
//     console.error("❌ 자동완성 에러:", e);
//     suggestions.value = [];
//   }
// };

const getSuggestions = async (value) => {
  const query = value ?? searchQuery.value;
  if (!query) {
    suggestions.value = [];
    return;
  }

  try {
    const res = await axios.get('/api/suggest-db', { params: { q: query } });
    suggestions.value = res.data.slice(0, 14);
    selectedIndex.value = -1;
  } catch (e) {
    console.error("❌ 자동완성 에러:", e);
    suggestions.value = [];
  }
};


const fetchSuggestions = debounce(getSuggestions, 200);

const selectSuggestion = (s) => {
  const selected = s.includes(">") ? s.split(" > ")[1] : s;
  const words = searchQuery.value.split(" ");
  searchQuery.value = words.length > 1 ? `${words[0]} ${selected}` : selected;

  emitSearch();
};

// emitSearch 함수 내에 저장 호출
const emitSearch = async () => {
  const keyword = searchQuery.value.trim();
  if (!keyword) return;

  try {
    const res = await axios.get("/api/resolve-keyword", {
      params: { query: keyword }
    });

    const { exists, alternatives } = res.data;

    if (exists) {
      saveRecentKeyword(keyword);
      router.push(`/keyword/${encodeURIComponent(keyword)}`);
    } else if (alternatives.length > 0) {
      altKeywords.value = alternatives;
      showModal.value = true;
    } else {
      altKeywords.value = []; // 빈 경우도 모달로
      showModal.value = true;
    }

    suggestions.value = [];
  } catch (e) {
    console.error("❌ 검색 오류:", e);
  }
};

// 🔹 키보드 이벤트 핸들링
const handleKeyDown = (e) => {
  if (!suggestions.value.length) return;

  if (e.key === "ArrowDown") {
    e.preventDefault(); // 🔹 기본 커서 이동 방지
    selectedIndex.value = (selectedIndex.value + 1) % suggestions.value.length;
  } else if (e.key === "ArrowUp") {
    e.preventDefault();
    selectedIndex.value =
      (selectedIndex.value - 1 + suggestions.value.length) %
      suggestions.value.length;
  } else if (e.key === "Enter" && selectedIndex.value !== -1) {
    e.preventDefault();
    selectSuggestion(suggestions.value[selectedIndex.value]);
  } else if (e.key === "Tab" && selectedIndex.value !== -1) {
    e.preventDefault(); // 🔥 기본 탭 동작 막기 (포커스 이동 방지)
    const selected = suggestions.value[selectedIndex.value];
    const keywordOnly = selected.includes(">")
      ? selected.split(" > ")[1]
      : selected;

    const words = searchQuery.value.split(" ");
    searchQuery.value =
      words.length > 1 ? `${words[0]} ${keywordOnly}` : keywordOnly;

    suggestions.value = []; // 리스트 닫기
    selectedIndex.value = -1; // 인덱스 초기화
  } else if (e.key === "Escape") {
    suggestions.value = [];
    selectedIndex.value = -1;
  }
};

// 🔹 외부 클릭 감지 함수
const handleClickOutside = (e) => {
  if (searchBarRef.value && !searchBarRef.value.contains(e.target)) {
    suggestions.value = []; // 외부 클릭 시 자동완성 닫기
    selectedIndex.value = -1;
  }
};

// 🔹 mount 시 등록
onMounted(() => {
  window.addEventListener("keydown", handleKeyDown);
  document.addEventListener("click", handleClickOutside); // 🔥 클릭 감지 등록
});

// 🔹 해제
onUnmounted(() => {
  window.removeEventListener("keydown", handleKeyDown);
  document.removeEventListener("click", handleClickOutside);
});

// 🔹 mount 시 이벤트 등록
onMounted(() => {
  window.addEventListener("keydown", handleKeyDown);
});
onUnmounted(() => {
  window.removeEventListener("keydown", handleKeyDown);
});
</script>

<style scoped>
.recent-keywords {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-top: 10px;
  padding-left: 4px;
  width: 100%;
  max-width: 500px;
}

.recent-label {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 4px;
  color: #555;
}

.chip-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.chip {
  background-color: #f1f1f1;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 13px;
  cursor: pointer;
  transition: background 0.2s;
}

.chip:hover {
  background-color: #e0e0e0;
}

.search-bar {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap; /* 화면이 좁을 때 버튼이 자동으로 아래로 내려감 */
  gap: 10px;
  margin: 1px auto;
  width: 100%;
  max-width: 600px;
}

.search-bar input {
  flex: 1; /* 남는 공간을 채움 */
  min-width: 250px; /* 최소 크기 설정 */
  max-width: 500px; /* 최대 크기 제한 */
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 5px;
  outline: none;
}

.suggestions {
  position: absolute;
  top: 50px;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #ccc;
  border-radius: 4px;
  list-style: none;
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
  padding: 0;
  z-index: 1000;
}

.suggestions li {
  text-align: left;
  padding: 10px 12px;
  cursor: pointer;
  transition: background 0.2s;
  display: flex; /* 🔥 아이콘과 텍스트 나란히 */
  align-items: center;
  gap: 8px; /* 아이콘과 글자 사이 간격 */
  padding-left: 20px; /* 전체적으로 살짝 더 왼쪽 */
}

.suggestions li:hover,
.suggestions li.active {
  background-color: #e5e5e5;
  font-weight: bold;
}

.search-bar button {
  padding: 12px 15px;
  background: #ff0000;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  font-size: 16px;
  transition: background 0.3s;
}

.search-bar button:hover {
  background: #cc0000;
}

/* 🔹 모바일 환경에서 최적화 */
@media screen and (max-width: 768px) {
  .search-bar {
    flex-direction: column;
    width: 100%;
  }

  .search-bar input {
    width: 90%;
  }

  .search-bar button {
    width: 90%;
  }
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}
.modal-content {
  background: white;
  padding: 24px;
  border-radius: 12px;
  max-width: 400px;
  width: 90%;
  text-align: center;
}
.alt-list {
  list-style: none;
  padding: 0;
  margin-top: 10px;
}
.alt-list li {
  cursor: pointer;
  padding: 8px;
  border-bottom: 1px solid #eee;
}
.alt-list li:hover {
  background-color: #f0f0f0;
  font-weight: bold;
}
</style>
