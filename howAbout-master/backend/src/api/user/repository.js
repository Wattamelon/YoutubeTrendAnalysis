const { pool } = require('../../database');

// 사용자 등록
exports.register = async (userid, username, password) => {
  const query = `INSERT INTO users (userid, username, password) VALUES (?, ?, ?)`;
  return await pool.query(query, [userid, username, password]);
};

// 로그인
exports.login = async (userid, password) => {
  const query = `SELECT * FROM users WHERE userid = ? AND password = ?`;
  let result = await pool.query(query, [userid, password]);
  return (result.length === 0) ? null : result[0];
};

// ID 존재 여부 확인
exports.checkId = async (userid) => {
  const query = `SELECT COUNT(*) as count FROM users WHERE userid = ?`;
  let result = await pool.query(query, [userid]);
  return result[0]; // 결과의 첫 번째 행을 반환합니다.
};