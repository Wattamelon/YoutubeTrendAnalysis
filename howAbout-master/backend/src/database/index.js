const mysql = require("mysql2/promise");
require("dotenv").config();

exports.pool = mysql.createPool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  port: process.env.DB_PORT,
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
});

exports.pool.query = async (queryString, params) => {
  // 디버깅: 매개변수 출력
  console.log("queryString:", queryString);
  console.log("params:", params);

  const [results] = await this.pool.execute(queryString, params);
  return results;
};

