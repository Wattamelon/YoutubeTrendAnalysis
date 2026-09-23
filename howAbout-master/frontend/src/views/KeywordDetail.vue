<template>
  <div>
    <!-- 키워드 제목 -->
    <div class="keyword-title">키워드: {{ keyword }}</div>

    <!-- 연관 키워드 + 키워드 통계 -->
    <div class="related-keywords-and-detail">
      <div class="related-keywords">
        <h3>🔗 연관 키워드</h3>
        <v-data-table
          :headers="keywordHeaders"
          :items="relatedKeywordsTable"
          :items-per-page="30"
          class="elevation-1"
          dense
          hide-default-footer
        >
          <template v-slot:[`item.keyword`]="{ item }">
            <span @click="goToKeyword(item.keyword)" class="clickable-keyword">
              #{{ item.keyword }}
            </span>
          </template>
        </v-data-table>
      </div>

      <!-- 키워드 트렌드 그래프 -->
      <div class="trend-chart">
        <h3>📊 키워드 트렌드</h3>
        <canvas ref="trendChart"></canvas>
      </div>

      <!-- ✅ 추가: 성장 점수 -->
      <div class="growth-chart">
        <h3>📈 키워드 성장 점수</h3>
        <canvas ref="growthChart"></canvas>
      </div>
    </div>

    <!-- 콘텐츠 -->
    <div class="content">
      <div v-if="keywordDetail" class="keyword-metrics">
        <h3>📌 키워드 성공 요인</h3>
        <div class="metrics-grid">
          <div class="metric-card">
            <div class="icon">👍</div>
            <div class="value">
              {{ displayNumber(keywordDetail.like_count) }}
            </div>
            <div class="percentage">
              {{
                displayPercent(
                  keywordDetail.like_count,
                  keywordDetail.view_count
                )
              }}
            </div>
            <div>
              등급: <strong>{{ keywordDetail.preference_grade }}</strong>
            </div>
            <div class="label">조회수 대비 좋아요 (선호도)</div>
          </div>
          <div class="metric-card">
            <div class="icon">💬</div>
            <div class="value">
              {{ displayNumber(keywordDetail.comment_count) }}
            </div>
            <div class="percentage">
              {{
                displayPercent(
                  keywordDetail.comment_count,
                  keywordDetail.view_count
                )
              }}
            </div>
            <div>
              등급: <strong>{{ keywordDetail.engagement_grade }}</strong>
            </div>
            <div class="label">조회수 대비 댓글 수 (참여도)</div>
          </div>
          <div class="metric-card">
            <div class="icon">👥</div>
            <div class="value">
              {{ displayNumber(keywordDetail.view_count) }}
            </div>
            <div class="percentage">
              {{
                displayPercent(
                  keywordDetail.view_count,
                  keywordDetail.subscriber_count
                )
              }}
            </div>
            <div class="label">구독자 수 대비 조회수 (성장 가능성)</div>
          </div>
        </div>
      </div>

      <div class="related-videos">
        <h3>📺 연관 동영상</h3>
        <div
          v-for="video in paginatedVideos"
          :key="video.video_id"
          class="video-item"
        >
          <img
            :src="getThumbnailUrl(video.video_id)"
            :alt="video.title"
            class="video-thumbnail"
          />
          <div class="video-info">
            <a
              :href="getVideoUrl(video.video_id)"
              target="_blank"
              class="video-title"
            >
              {{ video.title }}
            </a>
          </div>
        </div>
        <div class="pagination-controls">
          <button @click="prevPage" :disabled="currentPage === 1">
            ⬅ 이전
          </button>
          <button
            @click="nextPage"
            :disabled="currentPage >= Math.ceil(videos.length / itemsPerPage)"
          >
            다음 ➡
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import Chart from "chart.js/auto";
import "chartjs-adapter-date-fns";

const route = useRoute();
const router = useRouter();
const keyword = ref(route.params.keyword || "알 수 없음");
const apiUrl = process.env.VUE_APP_API_URL;
const relatedKeywordsTable = ref([]);
const videos = ref([]);
const keywordDetail = ref(null);
const trendChart = ref(null);
let chartInstance = null;
const currentPage = ref(1);
const itemsPerPage = 5;

const keywordHeaders = [
  { text: "순위", value: "rank" },
  { text: "연관 키워드", value: "keyword" },
  { text: "검색량", value: "search_volume" },
  { text: "관련성 점수", value: "relevance" },
];

const fetchKeywordDetails = async () => {
  try {
    // const relatedResponse = await axios.get(
    //   `${apiUrl}/api/related-keywords`,
    //   {
    //     params: { keyword: keyword.value },
    //   }
    // );
    // const keywordData = relatedResponse.data.data.find(
    //   (item) => item.keyword === keyword.value
    // );
    // relatedKeywordsTable.value = (keywordData?.related || []).map(
    //   (item, index) => ({
    //     rank: index + 1,
    //     keyword: item,
    //   })
    // );

    // 연관 키워드 수정
    const relatedResponse = await axios.get(`${apiUrl}/api/related-keywords`, {
      params: { keyword: keyword.value },
    });
    relatedKeywordsTable.value = relatedResponse.data.related.map(
      (item, index) => ({
        rank: index + 1,
        keyword: item,
      })
    );

    // const videoResponse = await axios.get(
    //   `${apiUrl}/api/mongo-keyword-videos`,
    //   {
    //     params: { keyword: keyword.value },
    //   }
    // );
    // videos.value = videoResponse.data.data
    //   .filter((item) => item.keyword === keyword.value)
    //   .flatMap((item) =>
    //     item.videos.map((video) => ({
    //       video_id: video.video_id,
    //       title: video.title,
    //       score: video.score,
    //     }))
    //   );

    // ✅ 연관 인기 동영상 가져오기 (related_video_runner.py 실행 결과)
    const videoResponse = await axios.get(
      `${apiUrl}/api/keywords-popular-videos`,
      {
        params: { keyword: keyword.value },
      }
    );
    videos.value = videoResponse.data.data.map((video) => ({
      video_id: video.video_id,
      title: video.title,
      score: video.score,
    }));

    const detailResponse = await axios.get(
      `${apiUrl}/api/keyword-details?keyword=${encodeURIComponent(
        keyword.value
      )}`
    );
    keywordDetail.value = detailResponse.data;

    //generateMockChartData();
    generateTrendChartData();
    generateGrowthChartData();
  } catch (error) {
    console.error("❌ 데이터 불러오기 실패:", error);
  }
};

const getThumbnailUrl = (videoId) =>
  `https://img.youtube.com/vi/${videoId}/hqdefault.jpg`;
const getVideoUrl = (videoId) => `https://www.youtube.com/watch?v=${videoId}`;

const goToKeyword = (newKeyword) => {
  if (newKeyword !== keyword.value) {
    router.push(`/keyword/${encodeURIComponent(newKeyword)}`);
  }
};

// const generateMockChartData = async () => {
//   await nextTick();
//   if (chartInstance) chartInstance.destroy();

//   const ctx = trendChart.value.getContext("2d");
//   const mockDates = [
//     "1월",
//     "2월",
//     "3월",
//     "4월",
//     "5월",
//     "6월",
//     "7월",
//     "8월",
//     "9월",
//     "10월",
//   ];
//   const mockValues = Array.from({ length: mockDates.length }, () =>
//     Math.floor(Math.random() * 100)
//   );

//   chartInstance = new Chart(ctx, {
//     type: "line",
//     data: {
//       labels: mockDates,
//       datasets: [
//         {
//           label: "검색량",
//           data: mockValues,
//           borderColor: "#007bff",
//           backgroundColor: "rgba(0, 123, 255, 0.2)",
//           fill: true,
//           tension: 0.4,
//         },
//       ],
//     },
//     options: {
//       responsive: true,
//       maintainAspectRatio: false,
//       scales: {
//         x: { title: { display: true, text: "월별" } },
//         y: { title: { display: true, text: "검색량" } },
//       },
//     },
//   });
// };

//import dayjs from "dayjs";

const generateTrendChartData = async () => {
  await nextTick();

  if (chartInstance) {
    chartInstance.destroy();
    chartInstance = null;
  }

  const ctx = trendChart.value.getContext("2d");

  // ✅ API 요청
  const response = await axios.get(`${apiUrl}/api/keyword-trend`, {
    params: { keyword: keyword.value },
  });

  const trendData = response.data.data;

  // ✅ Chart.js가 인식할 수 있도록 x, y 포맷으로 재구성
  const formattedData = trendData.map((item) => ({
    x: new Date(item.date),
    y: item.score,
  }));

  chartInstance = new Chart(ctx, {
    type: "line",
    data: {
      datasets: [
        {
          label: "트렌드 점수",
          data: formattedData, // ✅ 여기가 핵심
          borderColor: "#007bff",
          backgroundColor: "rgba(0, 123, 255, 0.2)",
          fill: true,
          tension: 0.4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          type: "time",
          time: {
            unit: "day",
            tooltipFormat: "yyyy-MM-dd",
            displayFormats: {
              day: "MM/dd",
            },
          },
          title: {
            display: true,
            text: "날짜",
          },
        },
        y: {
          min: 0,
          max: 1,
          title: {
            display: true,
            text: "정규화된 점수",
          },
        },
      },
    },
  });
};

const growthChart = ref(null); // 캔버스 참조 추가
let growthChartInstance = null;

const generateGrowthChartData = async () => {
  await nextTick();

  if (growthChartInstance) {
    growthChartInstance.destroy();
    growthChartInstance = null;
  }

  const ctx = growthChart.value.getContext("2d");

  const response = await axios.get(`${apiUrl}/api/keyword-growth`, {
    params: { keyword: keyword.value },
  });

  const trendData = response.data.data;

  const formattedData = trendData.map((item) => ({
    x: new Date(item.date),
    y: item.growth_score,
  }));

  growthChartInstance = new Chart(ctx, {
    type: "line",
    data: {
      datasets: [
        {
          label: "성장 점수",
          data: formattedData,
          borderColor: "#ff5722",
          backgroundColor: "rgba(255, 87, 34, 0.2)",
          fill: true,
          tension: 0.4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          type: "time",
          time: {
            unit: "day",
            tooltipFormat: "yyyy-MM-dd",
            displayFormats: {
              day: "MM/dd",
            },
          },
          title: {
            display: true,
            text: "날짜",
          },
        },
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: "성장 점수",
          },
        },
      },
    },
  });
};

onMounted(fetchKeywordDetails);

watch(
  () => route.params.keyword,
  (newKeyword) => {
    keyword.value = newKeyword;
    fetchKeywordDetails();
  },
  { immediate: true }
);

const paginatedVideos = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return videos.value.slice(start, end);
});

const nextPage = () => {
  if (currentPage.value < Math.ceil(videos.value.length / itemsPerPage)) {
    currentPage.value++;
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

const displayNumber = (val) => {
  return Number.isFinite(val) ? val.toLocaleString() : "-";
};

const displayPercent = (numerator, denominator) => {
  if (!denominator || denominator === 0) return "-";
  const percent = (numerator / denominator) * 100;
  return percent.toFixed(2) + "%";
};
</script>

<style scoped>
/* 🔹 페이지 상단 타이틀 */
.keyword-title {
  width: 100%;
  text-align: center;
  background-color: #f0f0f0;
  padding: 15px 0;
  margin-bottom: 20px;
  font-size: 30px;
  font-weight: bold;
}

/* 🔹 연관 키워드 + 트렌드 섹션 */
.related-keywords-and-detail {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  padding: 10px 20px;
  flex-wrap: wrap;
}

/* 🔹 연관 키워드 테이블 */
.related-keywords {
  padding: 8px;
  background-color: #f5f5f5;
  border-radius: 8px;
  flex: 0.3;
  min-width: 300px;
  max-width: 600px;

  /* 🔽 추가되는 스타일 */
  max-height: 350px; /* 원하는 높이로 조정 가능 */
  overflow-y: auto;
  text-align: center;
}

/* 🔹 키워드 클릭 가능 링크 */
.clickable-keyword {
  color: #007bff;
  cursor: pointer;
  font-weight: bold;
  text-decoration: none;
}
.clickable-keyword:hover {
  text-decoration: underline;
}

/* 🔹 트렌드 차트 */
.trend-chart {
  background-color: white;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #ddd;
  height: 350px;
  overflow: hidden;
  position: relative;
  flex: 0.35;
  min-width: 300px;
  max-width: 900px;
  padding-bottom: 40px;
}

.trend-chart canvas {
  display: block;
  width: 100% !important;
  height: 100% !important;
  margin-bottom: 0;
}

.growth-chart {
  background-color: white;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #ddd;
  height: 350px;
  overflow: hidden;
  position: relative;
  flex: 0.35;
  min-width: 300px;
  max-width: 900px;
  padding-bottom: 40px;
}
.growth-chart canvas {
  display: block;
  width: 100% !important;
  height: 100% !important;
}

/* 🔹 콘텐츠 영역: 연관 동영상 + 키워드 성공 요인 */
.content {
  width: 100%;
  display: flex;
  justify-content: space-between;
  gap: 20px;
  padding: 20px;
  box-sizing: border-box;
  flex-wrap: wrap;
}

/* 🔹 연관 동영상 카드 */
.related-videos {
  background-color: #f9f9f9;
  border-radius: 10px;
  padding: 15px;
  flex: 0.3;
  min-width: 300px;
  max-width: 600px;
  text-align: center;
}

/* 동영상 썸네일 + 제목 */
.video-item {
  display: flex;
  align-items: center;
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 5px;
  background-color: #fff;
  margin-bottom: 15px;
  gap: 12px;
}

.video-thumbnail {
  width: 120px;
  height: 90px;
  object-fit: cover;
  border-radius: 5px;
}

.video-info {
  flex: 1;
}

.video-title {
  display: -webkit-box;
  -webkit-line-clamp: 2; /* 최대 줄 수 */
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 14px;
  color: black;
  text-decoration: none;
}
.video-title:hover {
  text-decoration: underline;
}

/* 🔹 페이지네이션 */
.pagination-controls {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

/* 🔹 키워드 성공 요인 (카드 형식) */
.keyword-metrics {
  background: #ffffff;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 30px;
  flex: 0.7;
  min-width: 300px;
  max-width: 1000px;
  max-height: flex;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.metric-card {
  background: #f1f5f9;
  padding: 15px;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.metric-card .icon {
  font-size: 28px;
  margin-bottom: 8px;
}

.metric-card .value {
  font-size: 22px;
  font-weight: bold;
}

.metric-card .percentage {
  font-size: 14px;
  color: green;
  margin-bottom: 5px;
}

.metric-card .label {
  font-size: 13px;
  color: #555;
}

/* ✅ 키워드 평가 카드 디자인 */
.grade-summary {
  margin-top: 25px;
  padding: 20px;
  background: #e9f5ff;
  border: 1px solid #b3d8ff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  font-size: 15px;
  line-height: 1.7;
  color: #222;
  text-align: center;
}
.grade-summary h3 {
  margin-bottom: 12px;
  font-size: 20px;
  color: #0056b3;
}
.grade-summary strong {
  color: #0056b3;
  font-weight: 600;
  font-size: 16px;
}
</style>
