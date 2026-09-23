const express = require('express');
const router = express.Router();

const authenticateToken = require('./middlewares/authMiddleware');

//controller
const apiUserController = require('./api/user/controller');

//router
// router.get('/', webController.home);

router.post('/auth/register', apiUserController.register);
router.post('/auth/login', apiUserController.login);



module.exports = router;

