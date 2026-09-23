import { createRouter, createWebHistory } from "vue-router";
import RegisterView from "@/views/RegisterView.vue";
import RankingView from "@/views/RankingView.vue";
import KeywordDetail from "@/views/KeywordDetail.vue";
import YoutubeSummaryPage from "@/views/YoutubeSummaryPage.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/register",
      name: "Register",
      component: RegisterView,
    },
    

    {
      path: "/ranking",
      name: "Ranking",
      component: RankingView,
    },

    {
      path: "/keyword/:keyword",
      component: KeywordDetail,
      props: true,
    },
    {
      path: "/about",
      name: "About",
      component: YoutubeSummaryPage,
    },
    {
      path: "/ranking",
      name: "Ranking",
      component: () => import("@/views/RankingView.vue"),
    },
    {
      path: "/",
      name: "Home",
      component: () => import("@/views/HomeView.vue"),
    },

    {
      path: "/planner",
      name: "Planner",
      component: () => import("@/views/VideoPlanner.vue")
    }
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition; // ✅ 뒤로가기 시 스크롤 복원
    } else {
      return { top: 0 }; // 새 페이지는 최상단
    }
  },
});

export default router;
