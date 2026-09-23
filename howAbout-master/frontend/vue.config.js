const { defineConfig } = require("@vue/cli-service");
const apiUrl = process.env.VUE_APP_API_URL;
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    host: "0.0.0.0", // 모바일에서도 접근 가능하게 설정
    port: 8080, // 프론트엔드 실행 포트 (고정)
    allowedHosts: "all", // 모든 네트워크에서 접근 허용
    hot: true, // 핫 모듈 리로딩 활성화
    historyApiFallback: true, // Vue Router의 히스토리 모드 지원
    client: {
      overlay: false, // 컴파일 에러 발생 시 화면을 덮지 않도록 설정
    },
    proxy: {
      "/api": {
        target: `${apiUrl}`, // ✅ 여기에 PC의 로컬 IP 입력
        changeOrigin: true,
        secure: false,
        pathRewrite: { "^/api": "" }, // "/api"를 백엔드로 전달
      },
      "/auth": {
        target: "http://localhost:3000",
        changeOrigin: true,
      },
    },
  },
});
