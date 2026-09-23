<template>
  <div>
    <!-- ✅ 고정 헤더 -->
    <div class="floating-header" v-if="showFloatingHeader">
      <table>
        <thead>
          <tr>
            <th class="rank-col">순위</th>
            <th>키워드</th>
            <th>등락</th>
            <th>이전 순위</th>
          </tr>
        </thead>
      </table>
    </div>

    <div class="centered-content">
      <h2 class="title">🔥 유튜브 인기 키워드 랭킹 🔥</h2>

      <div class="filter-container">
        <label for="category-filter">카테고리 : </label>
        <select id="category-filter" v-model="selectedCategory">
          <option value="News & Politics">뉴스 및 정치</option>
          <option value="Music">음악</option>
          <option value="Sports">스포츠</option>
          <option value="Gaming">게임</option>
          <option value="Science & Technology">과학 및 기술</option>
        </select>

        <label for="period-filter" style="margin-left: 20px">기간 : </label>
        <select id="period-filter" v-model="selectedPeriod">
          <option value="today">오늘</option>
          <option value="week">이번 주</option>
          <option value="month">이번 달</option>
        </select>
      </div>

      <div v-if="loading" class="loading">데이터 불러오는 중...</div>

      <div v-else class="table-wrapper" ref="tableRef">
        <table>
          <thead>
            <tr>
              <th class="rank-col">순위</th>
              <th>키워드</th>
              <th>등락</th>
              <th>이전 순위</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(keyword, index) in filteredKeywords" :key="index">
              <td class="rank-col">{{ index < 30 ? index + 1 : "–" }}</td>
              <td>
                <router-link
                  :to="`/keyword/${encodeURIComponent(keyword.keyword)}`"
                >
                  {{ keyword.keyword }}
                </router-link>
              </td>
              <td>
                <span
                  v-if="keyword.previous_rank === null"
                  style="color: green; font-weight: bold"
                  >NEW</span
                >
                <span
                  v-else-if="keyword.rank_change > 0"
                  style="color: red; font-weight: bold"
                  >▲ {{ keyword.rank_change }}</span
                >
                <span
                  v-else-if="keyword.rank_change < 0"
                  style="color: blue; font-weight: bold"
                  >▼ {{ -keyword.rank_change }}</span
                >
                <span
                  v-else-if="keyword.rank_change === 0"
                  style="color: gray; font-weight: bold"
                  >–</span
                >
                <span
                  v-else-if="keyword.rank_change === null"
                  style="color: gray; font-weight: bold"
                  >out</span
                >
              </td>
              <td>{{ keyword.previous_rank ?? "—" }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from "vue";
import axios from "axios";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

const selectedCategory = ref(route.query.category || "News & Politics");
const selectedPeriod = ref(route.query.period || "today");
const allKeywords = ref({});
const loading = ref(true);
const apiUrl = process.env.VUE_APP_API_URL;

const tableRef = ref(null);
const showFloatingHeader = ref(false);

const handleScroll = () => {
  const tableTop = tableRef.value?.getBoundingClientRect().top || 0;
  showFloatingHeader.value = tableTop < 0;
};

const categoryMap = {
  25: "News & Politics",
  10: "Music",
  17: "Sports",
  20: "Gaming",
  28: "Science & Technology",
};

const fetchKeywords = async () => {
  loading.value = true;
  try {
    const response = await axios.get(
      `${apiUrl}/api/ranking/${selectedPeriod.value}`
    );
    const result = response.data || {};

    const mapped = {};
    for (const id in result) {
      const categoryName = categoryMap[id] || id;
      mapped[categoryName] = result[id];
    }
    allKeywords.value = mapped;
  } catch (error) {
    console.error("❌ 데이터 불러오기 실패:", error);
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  const savedCategory = localStorage.getItem("selectedCategory");
  const savedPeriod = localStorage.getItem("selectedPeriod");
  const savedScroll = localStorage.getItem("rankingScrollY");

  if (savedCategory) selectedCategory.value = savedCategory;
  if (savedPeriod) selectedPeriod.value = savedPeriod;

  await fetchKeywords();

  if (savedScroll) window.scrollTo(0, parseInt(savedScroll));

  window.addEventListener("scroll", handleScroll);
});

onBeforeUnmount(() => {
  localStorage.setItem("rankingScrollY", window.scrollY);
  window.removeEventListener("scroll", handleScroll);
});

watch([selectedCategory, selectedPeriod], async () => {
  localStorage.setItem("selectedCategory", selectedCategory.value);
  localStorage.setItem("selectedPeriod", selectedPeriod.value);

  router.replace({
    query: {
      category: selectedCategory.value,
      period: selectedPeriod.value,
    },
  });

  await fetchKeywords();
});

const filteredKeywords = computed(() => {
  return allKeywords.value[selectedCategory.value] || [];
});
</script>

<style scoped>
.centered-content {
  text-align: center;
  margin-top: 60px;
  padding: 20px;
}

.title {
  color: #e60023;
  font-size: 28px;
  margin-bottom: 30px;
}

.filter-container {
  margin-bottom: 20px;
}

.filter-container select {
  padding: 8px 12px;
  font-size: 16px;
  border-radius: 8px;
  border: 1px solid #ccc;
}

.loading {
  font-size: 18px;
  color: gray;
  margin-top: 20px;
}

.table-wrapper {
  width: 100%;
  padding-top: 60px;
}

table {
  width: 70%;
  margin: 0 auto;
  table-layout: fixed;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 16px;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

thead th {
  position: sticky;
  background-color: #e60023;
  color: white;
  font-weight: 600;
  padding: 12px 15px;
  text-align: center;
  border-bottom: 1px solid #eee;
}
th,
td {
  padding: 12px 15px;
  border-bottom: 1px solid #eee;
  text-align: center;
}
th.rank-col,
td.rank-col {
  width: 80px;
  border-right: 1px solid #ddd;
}

th:nth-child(2),
td:nth-child(2) {
  width: 250px; /* 키워드 열 */
}

th:nth-child(3),
td:nth-child(3) {
  width: 120px; /* 등락 열 */
}

th:nth-child(4),
td:nth-child(4) {
  width: 120px; /* 이전 순위 열 */
}

tr:hover {
  background-color: #f9f9f9;
}

.floating-header {
  position: fixed;
  top: 0;
  left: 50%;
  table-layout: fixed;
  transform: translateX(-50%);
  width: 68%; /* ✅ table과 동일하게 */
  background-color: #e60023;
  color: white;
  z-index: 1000;
  border-top-left-radius: 12px;
  border-top-right-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}

.floating-header table {
  border-collapse: collapse;
  width: 100%;
}

.floating-header th {
  background-color: #e60023;
  color: white;
  font-weight: 600;
  padding: 12px 15px;
  text-align: center;
  border-bottom: 1px solid #eee;
}
</style>
