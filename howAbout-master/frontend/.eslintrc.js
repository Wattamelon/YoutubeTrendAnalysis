module.exports = {
  root: true,
  env: {
    node: true,
  },
  parser: "vue-eslint-parser",
  parserOptions: {
    parser: "@babel/eslint-parser",
    ecmaVersion: 2020,
    sourceType: "module",
    requireConfigFile: false,
  },
  extends: ["eslint:recommended", "plugin:vue/vue3-recommended"],
  rules: {
    // 필요하다면 여기 규칙을 추가할 수 있음
    // 예: "no-console": "off"
  },
};
