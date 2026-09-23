const mongoose = require('mongoose');
require('dotenv').config();

const mongoURI = process.env.MONGO_URI;

mongoose.connect(mongoURI, {
  useNewUrlParser: true,
  useUnifiedTopology: true
})
.then(() => console.log('✅ MongoDB 연결 성공!'))
.catch(err => console.error('❌ MongoDB 연결 실패:', err));

module.exports = mongoose;

//1. npm install mysql2 mongoose dotenv
// 몽고DB 설치하고

//몽고 DB 명령어
// use test_database  (test_database 없으면 생성, 있으면 이동)
// db.createCollection("users") 컬렉션 생성
// db.users.insertOne({ name: "Alice", age: 25 }) 데이터 삽입
// show dbs db 모두 확인
// db 현재 사용중인 db 확인

// # MongoDB 연결 정보
// MONGO_URI=mongodb://localhost:27017/몽고db에 db만든거 이름    // .env 파일에 추가됨
// http://localhost:27017/
// url입력하고, It looks like you are trying to access MongoDB over HTTP on the native driver port. 이 문구 뜨면 몽고db 실행중임을 의미. 
// mongosh는 터미널에서 MongoDB 공식 Shell // 터미널에서 몽고db 접속하는 명령어
// 몽고DB compass는 mySQLworkbench처럼 그래픽으로 몽고DB조작 가능하게 하는 프로그램
// database 디렉토리 안에 index.js는 mysql연결파일, mongodb.js는 몽고db연결파일
// 
 




// const mysql = require('./src/database/index');  // MySQL 연결 주소
// const mongoose = require('./src/database/mongodb');  // MongoDB 연결 주소