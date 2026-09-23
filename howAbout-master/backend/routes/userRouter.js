const express = require('express');
const router = express.Router();
const db = require('../config/db');

// 유저 목록 가져오기 (예제)
router.get('/', (req, res) => {
  res.json({ message: '유저 목록 가져오기' });
});

// 유저 등록 (예제)
router.post('/register', (req, res) => {
  const { username, email, password } = req.body;
  res.json({ message: `유저 등록: ${username}, ${email}` });
});

module.exports = router;
