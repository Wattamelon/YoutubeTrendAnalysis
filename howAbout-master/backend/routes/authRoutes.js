const express = require("express");
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const db = require("../src/database");
const dotenv = require("dotenv");

dotenv.config();
const router = express.Router();

// ✅ 인증 미들웨어
function authenticateToken(req, res, next) {
  const authHeader = req.headers["authorization"];
  const token = authHeader && authHeader.split(" ")[1];
  if (!token) return res.sendStatus(401);

  jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
    if (err) return res.sendStatus(403);
    req.user = user;
    next();
  });
}

// ✅ 로그인 상태 확인 API
router.get("/auth/me", authenticateToken, (req, res) => {
  res.json({ id: req.user.id, username: req.user.username });
});

// ✅ 회원가입 API
router.post("/register", async (req, res) => {
  const { id, username, password } = req.body;

  if (!id || !username || !password) {
    return res.status(400).json({ message: "모든 필드를 입력하세요." });
  }

  const hashedPassword = await bcrypt.hash(password, 10);
  const newUser = await db.query(
    "INSERT INTO users (id, username, password) VALUES ($1, $2, $3) RETURNING *",
    [id, username, hashedPassword]
  );

  const user = newUser.rows[0];
  const token = jwt.sign(
    { id: user.id, username: user.username },
    process.env.JWT_SECRET,
    {
      expiresIn: "1h",
    }
  );
  res.status(201).json({ access_token: token, username: user.username }); // username도 같이 반환
});

// ✅ 로그인 API
router.post("/auth/login", async (req, res) => {
  const { userid, password } = req.body;

  if (!userid || !password) {
    return res
      .status(400)
      .json({ message: "아이디와 비밀번호를 모두 입력하세요." });
  }

  // 사용자 조회
  const result = await db.query("SELECT * FROM users WHERE id = $1", [userid]);
  const user = result.rows[0];
  if (!user) {
    return res.status(401).json({ message: "존재하지 않는 사용자입니다." });
  }

  // 비밀번호 검증
  const isValid = await bcrypt.compare(password, user.password);
  if (!isValid) {
    return res.status(401).json({ message: "비밀번호가 틀렸습니다." });
  }

  // 토큰 발급
  const token = jwt.sign(
    { id: user.id, username: user.username },
    process.env.JWT_SECRET,
    { expiresIn: "1h" }
  );

  res.json({ access_token: token, username: user.username });
});

module.exports = router;
