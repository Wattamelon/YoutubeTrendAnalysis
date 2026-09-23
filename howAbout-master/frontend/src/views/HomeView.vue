<!-- src/views/HomeView.vue -->
<template>
  <div class="home-wrapper">
    <!-- 아래로 스크롤 시 등장하는 설명 영역 -->
    <div class="scroll-section">
      <section class="info-block">
        <h2>🔍 이거어때란?</h2>
        <p>
          유튜브에서 지금 어떤 키워드가 뜨는지 알려주는 트렌드 분석
          플랫폼입니다.
        </p>
      </section>

      <section class="info-block">
        <h2>📊 어떻게 작동하나요?</h2>
        <ul>
          <li>유튜브 인기 동영상과 댓글 데이터를 분석</li>
          <li>자연어 처리 기반으로 연관 키워드 추천</li>
          <li>트렌드 그래프, 연관 영상, 조회수/좋아요 예측 제공</li>
        </ul>
      </section>

      <section class="info-block">
        <h2>🙋 자주 묻는 질문</h2>
        <p>
          Q. 데이터는 얼마나 자주 갱신되나요?<br />A. 매일 업데이트되며 주간,
          월간 트렌드도 제공합니다.
        </p>
      </section>
    </div>
  </div>
</template>

<style scoped>
.home-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 상단 검색 영역 */
.top-section {
  margin-top: 40px;
  width: 100%;
}

/* 스크롤 가능한 아래 영역 */
.scroll-section {
  margin-top: 100px;
  padding: 60px 20px;
  width: 100%;
  max-width: 900px;
}

.info-block {
  background: #f9f9f9;
  border-radius: 12px;
  padding: 30px;
  margin-bottom: 40px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

.info-block h2 {
  margin-bottom: 16px;
}

.info-block ul {
  padding-left: 20px;
  line-height: 1.8;
}
</style>
