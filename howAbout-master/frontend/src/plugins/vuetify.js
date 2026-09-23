// plugins/vuetify.js
import { createVuetify } from "vuetify";
import "vuetify/styles"; // Vuetify 스타일 불러오기
import { VDataTable } from "vuetify/components"; // ✅ 변경: labs 경로 제거

export default createVuetify({
  components: {
    VDataTable, // ✅ Vuetify 3 테이블 등록
  },
});
