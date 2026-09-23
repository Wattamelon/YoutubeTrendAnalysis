// backend/routes/rankingRoute.js
const express = require("express");
const router = express.Router();
const { spawn } = require("child_process");
const path = require("path");

// 캐시 저장용 객체
const rankingCache = {
  today: { data: null, lastUpdated: null },
  week: { data: null, lastUpdated: null },
  month: { data: null, lastUpdated: null },
};

const CACHE_TTL_MS = 60 * 60 * 1000; // 1시간

function isExpired(timestamp) {
  if (!timestamp) return true;
  return new Date() - timestamp > CACHE_TTL_MS;
}

function runPythonScript(scriptName) {
  return new Promise((resolve, reject) => {
    const pythonPath = "../youtube/.venv/Scripts/python.exe";
    const scriptPath = path.join(__dirname, "../", scriptName);

    const py = spawn(pythonPath, [scriptPath]);
    let result = "";
    let error = "";

    py.stdout.setEncoding("utf-8");
    py.stdout.on("data", (data) => {
      result += data.toString();
    });

    py.stderr.on("data", (data) => {
      error += data.toString();
    });

    py.on("close", (code) => {
      if (code === 0) {
        try {
          const parsed = JSON.parse(result);
          resolve(parsed);
        } catch (e) {
          reject({ message: "❌ JSON 파싱 실패", raw: result });
        }
      } else {
        reject({ message: "❌ Python 실행 실패", raw: error });
      }
    });
  });
}

//api
router.get("/ranking/:period", async (req, res) => {
  const period = req.params.period;
  const cache = rankingCache[period];


  let script;
  if (period === "today") script = "ranking_today.py";
  else if (period === "week") script = "ranking_week.py";
  else if (period === "month") script = "ranking_month.py";
  else return res.status(400).json({ error: "❌ 잘못된 기간" });

  // 캐시 확인
  if (cache.data && !isExpired(cache.lastUpdated)) {
    console.log(`✅ [캐시 사용] ${period} 랭킹`);
    return res.json(cache.data);
  }

    // 캐시 없거나 만료 → Python 실행
    console.log(`🔄 [파이썬 실행] ${period} 랭킹`);
    try {
      const data = await runPythonScript(script);
      rankingCache[period].data = data;
      rankingCache[period].lastUpdated = new Date();
      res.json(data);
    } catch (err) {
      res.status(500).json(err);
    }
  });


//   const pythonPath = "../youtube/.venv/Scripts/python.exe";
//   const scriptPath = path.join(__dirname, "../", script);

//   const py = spawn(pythonPath, [scriptPath]);
//   let result = "";

//   py.stdout.setEncoding("utf-8");
//   py.stdout.on("data", (data) => {
//     result += data.toString();
//     console.log("📥 PYTHON STDOUT:", data.toString());
//   });

//   py.stderr.on("data", (data) => {
//     console.error("🐍 PYTHON STDERR:", data.toString());
//   });

//   py.on("close", (code) => {
//     console.log("PYTHON 종료 코드:", code);
//     if (code === 0) {
//       try {
//         const parsed = JSON.parse(result);
//         res.json(parsed);
//       } catch (e) {
//         console.error("❌ JSON 파싱 실패:", e);
//         res.status(500).json({ error: "❌ JSON 파싱 실패", raw: result });
//       }
//     } else {
//       console.error("❌ Python 실행 실패, 종료 코드:", code);
//       res.status(500).json({ error: "❌ Python 실행 실패", raw: result });
//     }
//   });
// });

module.exports = router; // ✅ 꼭 router 객체를 export 해야 함
