const express = require("express");
const router = express.Router();
const mongoose = require("../src/database/mongodb"); // MongoDB 연결 파일

// ✅ users 컬렉션
const UserSchema = new mongoose.Schema({
  _id: mongoose.Schema.Types.ObjectId,
  name: String,
  age: Number,
});
const User = mongoose.model("User", UserSchema, "users");

// ✅ category_keywords 컬렉션
const CategoryKeywordSchema = new mongoose.Schema({
  category: String,
  ranked_keywords: [
    {
      순위: Number,
      키워드: String,
    },
  ],
});
const CategoryKeyword = mongoose.model(
  "CategoryKeyword",
  CategoryKeywordSchema,
  "category_keywords"
);

// ✅ keyword_videos 컬렉션
const KeywordVideoSchema = new mongoose.Schema({
  category: String,
  keywords: [
    {
      keyword: String,
      videos: [
        {
          video_id: String,
          score: Number,
          title: String,
        },
      ],
    },
  ],
});
const KeywordVideo = mongoose.model(
  "KeywordVideo",
  KeywordVideoSchema,
  "keyword_videos"
);

// ✅ related_keywords 컬렉션 (스키마 수정됨!)
const RelatedKeywordSchema = new mongoose.Schema({
  keyword: String,
  related: [String],
});
const RelatedKeyword = mongoose.model(
  "RelatedKeyword",
  RelatedKeywordSchema,
  "related_keywords"
);

// ✅ users 조회
router.get("/mongo-users", async (req, res) => {
  try {
    const users = await User.find();
    res.json({ message: "✅ MongoDB 데이터 조회 성공", data: users });
  } catch (error) {
    res.status(500).json({ message: "❌ MongoDB 데이터 조회 실패", error });
  }
});

// ✅ category_keywords 전체 조회
router.get("/mongo-category-keywords", async (req, res) => {
  try {
    const categories = await CategoryKeyword.find();
    res.json({
      message: "✅ category_keywords 데이터 조회 성공",
      data: categories,
    });
  } catch (error) {
    res
      .status(500)
      .json({ message: "❌ category_keywords 데이터 조회 실패", error });
  }
});

// ✅ keyword_videos 전체 조회
router.get("/mongo-keyword-videos", async (req, res) => {
  try {
    const videos = await KeywordVideo.find();
    res.json({ message: "✅ keyword_videos 데이터 조회 성공", data: videos });
  } catch (error) {
    res
      .status(500)
      .json({ message: "❌ keyword_videos 데이터 조회 실패", error });
  }
});

// ✅ 특정 카테고리의 keyword_videos 조회
router.get("/mongo-keyword-videos/:category", async (req, res) => {
  try {
    const category = req.params.category;
    const videos = await KeywordVideo.findOne({ category });

    if (!videos) {
      return res
        .status(404)
        .json({ message: `❌ '${category}' 카테고리의 데이터가 없습니다.` });
    }

    res.json({ message: "✅ keyword_videos 데이터 조회 성공", data: videos });
  } catch (error) {
    res
      .status(500)
      .json({ message: "❌ keyword_videos 데이터 조회 실패", error });
  }
});

// ✅ related_keywords 전체 조회
router.get("/mongo-related-keywords", async (req, res) => {
  try {
    const keywords = await RelatedKeyword.find();
    res.json({
      message: "✅ related_keywords 데이터 조회 성공",
      data: keywords,
    });
  } catch (error) {
    res
      .status(500)
      .json({ message: "❌ related_keywords 데이터 조회 실패", error });
  }
});

// ✅ keyword 자동완성 (예: "윤" → "윤석열")
router.get("/keyword-suggest", async (req, res) => {
  const query = req.query.q;

  if (!query) {
    return res.status(400).json({ message: "❌ 검색어(q)가 필요합니다." });
  }

  try {
    const results = await RelatedKeyword.find({
      keyword: { $regex: query, $options: "i" },
    });

    const keywords = results.map((doc) => doc.keyword); // ✅ 구조 일치!
    res.json(keywords);
  } catch (err) {
    console.error("❌ keyword-suggest 오류:", err);
    res.status(500).json({ message: "서버 오류", error: err });
  }
});

// ✅ 연관 키워드 자동완성 (예: "윤석열" → ["윤석열 > 대통령", ...])
router.get("/mongo-related-suggest", async (req, res) => {
  const query = req.query.q;

  if (!query) {
    return res.status(400).json({ message: "❌ 검색어(query)가 필요합니다." });
  }

  try {
    const results = await RelatedKeyword.find({
      keyword: { $regex: query, $options: "i" },
    });

    const suggestions = [];

    results.forEach((doc) => {
      doc.related.forEach((related) => {
        suggestions.push(`${doc.keyword} > ${related}`);
      });
    });

    res.json(suggestions);
  } catch (error) {
    console.error("❌ mongo-related-suggest 오류:", error);
    res
      .status(500)
      .json({ message: "❌ related_keywords 자동완성 실패", error });
  }
});

module.exports = router;
