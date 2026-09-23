require("dotenv").config();
const express = require("express");
const mysql = require("./src/database/index"); // MySQL 연결
const mongoose = require("./src/database/mongodb"); // MongoDB 연결
const cors = require("cors");
const app = express();
const { spawn } = require("child_process");
const path = require("path");
const port = 3000; // 백엔드 실행 포트
const router = require("./src/router");
const bodyParser = require("body-parser");
const mongoRoutes = require("./routes/mongoRoute"); // MongoDB 라우트
const authRoutes = require("./routes/authRoutes.js");
const fs = require("fs");
const rankingRoutes = require("./routes/rankingRoute");
const axios = require('axios');
const { MongoClient } = require("mongodb");


const OpenAI = require("openai");

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// GPT 응답 파싱 함수
function parseGPTResult(text) {
  const titleMatch = text.match(/1\.\s*Title:\s*(.+)/i);
  const scriptMatch = text.match(/2\.\s*Script\s*\(.*?\):\s*([\s\S]*)/i);

  return {
    title: titleMatch ? titleMatch[1].trim() : "",
    script: scriptMatch ? scriptMatch[1].trim() : "",
  };
}

app.use("/auth", authRoutes); // 이게 있어야 /auth/login 가능함

app.use(
  cors({
    origin: "*", // 모든 출처 허용 (보안이 필요하면 도메인 지정)
    methods: ["GET", "POST", "PUT", "DELETE"],
    credentials: true,
  })
);

app.use("/api", rankingRoutes);
// JSON 형식의 데이터 처리
app.use(bodyParser.json());
// URL 인코딩 된 데이터 처리
app.use(bodyParser.urlencoded({ extended: true }));

// 라우터를 애플리케이션에 등록
app.use("/", router);
app.use("/api", mongoRoutes);

// 테스트 API: MySQL 연결 확인
app.get("/mysql-test", async (req, res) => {
  try {
    const [rows] = await mysql.query("SELECT 1 + 1 AS result");
    res.json({ message: "✅ MySQL 연결 성공", data: rows });
  } catch (err) {
    res.status(500).json({ message: "❌ MySQL 연결 실패", error: err });
  }
});

// ✅ MongoDB 랭킹 데이터 가져오기 API
app.get("/api/mongo-rank", async (req, res) => {
  try {
    const rankings = await mongoose.connection.db
      .collection("rankings")
      .find()
      .toArray();
    res.json({ message: "✅ 랭킹 데이터 불러오기 성공", data: rankings });
  } catch (error) {
    res.status(500).json({ message: "❌ 랭킹 데이터 불러오기 실패", error });
  }
});

// ✅ MongoDB 연결 테스트 API
app.get("/mongo-test", async (req, res) => {
  try {
    const collections = await mongoose.connection.db
      .listCollections()
      .toArray();
    res.json({ message: "✅ MongoDB 연결 성공", collections });
  } catch (err) {
    res.status(500).json({ message: "❌ MongoDB 연결 실패", error: err });
  }
});

//연관 동영상 가져오기 수정
app.get("/api/keywords-popular-videos", (req, res) => {
  const keyword = req.query.keyword;
  if (!keyword) {
    return res
      .status(400)
      .json({ error: "❌ 키워드가 필요합니다 (keyword=...)" });
  }

  const pythonPath = "../youtube/.venv/Scripts/python.exe"; // ✅ 윈도우용 파이썬 경로
  const scriptPath = path.join(__dirname, "related_video_runner.py");

  const py = spawn(pythonPath, [scriptPath, keyword]);
  py.stdout.setEncoding("utf8"); // ✅ 이 줄 추가!

  let output = "";
  let error = "";

  py.stdout.on("data", (data) => {
    output += data.toString();
  });

  py.stderr.on("data", (data) => {
    error += data.toString();
  });

  py.on("close", (code) => {
    if (code !== 0) {
      console.error("🐍 Python 오류:", error);
      return res
        .status(500)
        .json({ error: "❌ Python 실행 실패", detail: error });
    }

    try {
      const parsed = JSON.parse(output);
      res.json({ data: parsed });
    } catch (e) {
      res.status(500).json({ error: "❌ JSON 파싱 실패", raw: output });
    }
  });
});

// app.get("/api/keywords-popular-videos", async (req, res) => {
//   try {
//     const videos = await mongoose.connection.db
//       .collection("keywords_popular_videos")
//       .find()
//       .toArray();
//     res.json({
//       message: "✅ 키워드 인기 영상 데이터 불러오기 성공",
//       data: videos,
//     });
//   } catch (error) {
//     res
//       .status(500)
//       .json({ message: "❌ 키워드 인기 영상 데이터 불러오기 실패", error });
//   }
// });

// app.get("/api/related-keywords", async (req, res) => {
//   try {
//     const relatedKeywords = await mongoose.connection.db
//       .collection("related_keywords")
//       .find()
//       .toArray();
//     res.json({
//       message: "✅ 관련 키워드 데이터 불러오기 성공",
//       data: relatedKeywords,
//     });
//   } catch (error) {
//     res
//       .status(500)
//       .json({ message: "❌ 관련 키워드 데이터 불러오기 실패", error });
//   }
// });

// 연관 키워드 수정

//연관 키워드
app.get("/api/related-keywords", (req, res) => {
  const keyword = req.query.keyword;
  if (!keyword) {
    return res
      .status(400)
      .json({ error: "❌ 키워드가 필요합니다 (keyword=...)" });
  }

  // ✅ 윈도우용 Python 가상환경 실행 경로
  const pythonPath = "../youtube/.venv/Scripts/python.exe";
  const scriptPath = path.join(__dirname, "related_ngram_runner.py");

  const py = spawn(pythonPath, [scriptPath, keyword]);
  py.stdout.setEncoding("utf8"); // ✅ 이 줄 추가!

  let output = "";
  let error = "";

  py.stdout.on("data", (data) => {
    output += data.toString();
  });

  py.stderr.on("data", (data) => {
    error += data.toString();
  });

  py.on("close", (code) => {
    if (code !== 0) {
      console.error("🐍 Python 오류:", error);
      return res
        .status(500)
        .json({ error: "❌ Python 실행 실패", detail: error });
    }

    try {
      const parsed = JSON.parse(output);
      res.json({ related: parsed });
    } catch (e) {
      res.status(500).json({ error: "❌ JSON 파싱 실패", raw: output });
    }
  });
});

// 동영상 요약
app.get("/run-audio", (req, res) => {
  const youtubeUrl = req.query.url;

  if (!youtubeUrl) {
    return res
      .status(400)
      .json({ error: "❌ 유튜브 URL이 필요합니다. (url=...)" });
  }

  const scriptPath = path.join(__dirname, "audio.py");
  const python = spawn("../youtube/.venv/Scripts/python.exe", [
    scriptPath,
    youtubeUrl,
  ]);

  let result = "";
  let error = "";

  python.stdout.on("data", (data) => {
    result += data.toString();
    console.log("✅ PYTHON STDOUT (raw):", result);
  });

  python.stderr.on("data", (data) => {
    error += data.toString();
    console.error("🐍 PYTHON STDERR:", data.toString());
  });

  python.on("close", (code) => {
    if (code === 0) {
      try {
        res.json(JSON.parse(result));
      } catch (e) {
        res.status(500).json({
          error: "❌ JSON 파싱 실패",
          raw: result,
        });
      }
    } else {
      res.status(500).json({
        error: "❌ Python 실행 중 오류 발생",
        detail: error,
      });
    }
  });
});

// app.get("/api/keyword-detail/:keyword", (req, res) => {
//   const keyword = decodeURIComponent(req.params.keyword);
//   const jsonPath = path.join(__dirname, "../youtube/test/graded_keywords.json");

//   fs.readFile(jsonPath, "utf-8", (err, data) => {
//     if (err) {
//       console.error("❌ JSON 파일 읽기 실패:", err);
//       return res.status(500).json({ error: "서버 내부 오류" });
//     }

//     try {
//       const parsed = JSON.parse(data);

//       let found = null;
//       for (const category in parsed) {
//         if (parsed[category][keyword]) {
//           found = parsed[category][keyword];
//           break;
//         }
//       }

//       if (found) {
//         res.json(found);
//       } else {
//         res
//           .status(404)
//           .json({ error: "해당 키워드 분석 결과를 찾을 수 없습니다." });
//       }
//     } catch (e) {
//       console.error("❌ JSON 파싱 실패:", e);
//       res.status(500).json({ error: "JSON 파싱 오류" });
//     }
//   });
// });

//키워드 그래프
app.get("/api/keyword-trend", (req, res) => {
  const keyword = req.query.keyword;
  if (!keyword) return res.status(400).json({ error: "❌ keyword 필요" });

  const scriptPath = path.join(__dirname, "graph.py");
  const pythonPath = "../youtube/.venv/Scripts/python.exe";

  const py = spawn(pythonPath, [scriptPath, keyword]);

  let output = "";
  py.stdout.on("data", (data) => {
    output += data.toString();
    console.log("📦 PYTHON STDOUT:", data.toString()); // 여기에 찍히는지 확인
  });

  py.stderr.on("data", (data) => {
    console.error("🐍 PYTHON ERROR:", data.toString());
  });

  py.on("close", (code) => {
    if (code !== 0) {
      return res.status(500).json({ error: "Python 실행 실패" });
    }

    try {
      const parsed = JSON.parse(output);
      res.json({ data: parsed });
    } catch (e) {
      res.status(500).json({ error: "JSON 파싱 실패", raw: output });
    }
  });
});

// 키워드 디테일
app.get("/api/keyword-details", (req, res) => {
  const keyword = req.query.keyword;
  if (!keyword) {
    return res
      .status(400)
      .json({ error: "❌ 키워드가 필요합니다 (keyword=...)" });
  }

  const pythonPath = "../youtube/.venv/Scripts/python.exe";
  const scriptPath = path.join(__dirname, "detail_runner.py"); // runner 파일 이름 넣기

  const py = spawn(pythonPath, [scriptPath, keyword]);
  py.stdout.setEncoding("utf8");

  let output = "";
  let error = "";

  py.stdout.on("data", (data) => {
    output += data.toString();
  });

  py.stderr.on("data", (data) => {
    error += data.toString();
  });

  py.on("close", (code) => {
    if (code !== 0) {
      return res
        .status(500)
        .json({ error: "❌ Python 실행 오류", detail: error });
    }

    try {
      const parsed = JSON.parse(output);
      res.json(parsed);
    } catch (e) {
      res.status(500).json({ error: "❌ JSON 파싱 실패", raw: output });
    }
  });
});

app.get("/api/keyword-growth", (req, res) => {
  const keyword = req.query.keyword;
  if (!keyword) {
    return res
      .status(400)
      .json({ error: "❌ 키워드가 필요합니다 (keyword=...)" });
  }

  const pythonPath = "../youtube/.venv/Scripts/python.exe";
  const scriptPath = path.join(__dirname, "keyword_growth_single.py");

  const py = spawn(pythonPath, [scriptPath, keyword]);
  py.stdout.setEncoding("utf8");

  let output = "";
  let error = "";

  py.stdout.on("data", (data) => {
    output += data.toString();
  });

  py.stderr.on("data", (data) => {
    error += data.toString();
  });

  py.on("close", (code) => {
    if (code !== 0) {
      return res.status(500).json({
        error: "❌ Python 실행 실패",
        detail: error,
      });
    }

    try {
      const parsed = JSON.parse(output);
      res.json({ data: parsed });
    } catch (e) {
      res.status(500).json({
        error: "❌ JSON 파싱 실패",
        raw: output,
      });
    }
  });
});

//gpt api 제목, 스크립트 뽑아주기
// POST /planner
app.post("/planner", async (req, res) => {
  app.use(express.json());

  const {
    target_audience,
    video_length,
    main_keyword,
    related_keywords,
    style,
  } = req.body;

  const prompt = `
너는 유튜브 컨텐츠 어시스트야.
다음 입력값에 따라서, 조회수가 잘 나올만한 제목을 지어주고, 동영상 길이 ${video_length} 만큼의 스크리브를 짜줘

Target Audience: ${target_audience}
Main Keyword: ${main_keyword}
Related Keywords: ${related_keywords.join(", ")}
Style: ${style}

Output format:
1. Title:
2. Script (for a ${video_length} video):
`;
  try {
    const response = await openai.chat.completions.create({
      model: "gpt-4.1",
      messages: [{ role: "user", content: prompt }],
      temperature: 0.8,
    });

    // OpenAI SDK v4에서는 response 자체가 최종 데이터다!
    console.log("GPT 응답 전체:", response);

    const rawText = response.choices[0].message.content;
    const parsedResult = parseGPTResult(rawText);

    res.json({ result: parsedResult });
  } catch (err) {
    console.error("OpenAI API Error:", err.message);
    res.status(500).json({ error: "Failed to generate content." });
  }
});

// //검색어 자동완성

// app.get("/api/yt-suggest", async (req, res) => {
//   const q = req.query.q;
//   if (!q) return res.json([]);

//   const url = `https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&q=${encodeURIComponent(q)}`;
//   try {
//     const { data } = await axios.get(url);
//     res.json(data[1]); // 추천어 배열만 전달
//   } catch (err) {
//     console.error("❌ yt-suggest 서버 내부 에러:", err); // ← 이 줄이 핵심!

//     res.status(500).json([]);
//   }
// });

// 검색어 자동완성_DB
// /api/suggest-db
router.get("/suggest-db", async (req, res) => {
  const q = req.query.q?.trim();
  if (!q) return res.json([]);

  const db = await MongoClient.connect("mongodb://localhost:27017/");
  const keywords = await db
    .db("search_keyword")
    .collection("search_keyword")
    .find({ keyword: { $regex: `^${q}`, $options: "i" } }) // 대소문자 무시
    .limit(10)
    .toArray();

  res.json(keywords.map(k => k.keyword));
});

//검색어 resolve 
app.get("/resolve-keyword", async (req, res) => {
  const { query } = req.query;
  if (!query) return res.json({ exists: false, alternatives: [] });

  const client = await MongoClient.connect("mongodb://localhost:27017/");
  const db = client.db("keyword");
  const collection = db.collection("keyword");

  // 1. 복합 키워드가 그대로 combined_score 안에 있는지 확인
  const exact = await collection.findOne({
    [`combined_score.${query}`]: { $exists: true }
  });

  if (exact) {
    client.close();
    return res.json({ exists: true, alternatives: [] });
  }

  // 2. 공백 기준 분해
  const parts = query.split(" ");
  const foundParts = [];

  for (const word of parts) {
    const result = await collection.findOne({
      [`combined_score.${word}`]: { $exists: true }
    });
    if (result) foundParts.push(word);
  }

  client.close();
  return res.json({ exists: false, alternatives: foundParts });
});




// 서버 실행
app.listen(port, "0.0.0.0", () => {
  console.log(`✅ 서버 실행 중: http://0.0.0.0:${port}`);
});
