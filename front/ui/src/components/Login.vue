<template>
  <div class="login-container">
    <h1>로그인</h1>

    <div class="social-login">
      <button class="social-button google">금융인증서로 로그인</button>
      <button class="social-button apple">Apple로 로그인</button>
      <button class="social-button kakao">Kakao로 로그인</button>
    </div>

    <div class="or-divider">or</div>

    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="email">아이디(이메일)</label>
        <input
          type="email"
          id="email"
          v-model="email"
          placeholder="Enter Email Address"
          required
        />
      </div>
      <div class="form-group">
        <label for="password">비밀번호</label>
        <input
          type="password"
          id="password"
          v-model="password"
          placeholder="Enter Password"
          required
        />
      </div>
      <div class="form-group">
        <label>
          <input type="checkbox" v-model="rememberMe" /> 자동 로그인
        </label>
      </div>
      <button type="submit" class="login-button">로그인</button>
    </form>

    <p class="signup-link">아직 계정이 없으신가요? <a href="#">회원가입</a></p>
  </div>
</template>

<script>
import { ref } from "vue";

export default {
  name: "LoginPage",
  setup() {
    const email = ref("");
    const password = ref("");
    const rememberMe = ref(false);

    const handleSubmit = () => {
      // 로그인 로직 추가
      console.log("로그인 정보:", {
        email: email.value,
        password: password.value,
        rememberMe: rememberMe.value,
      });
    };

    return { email, password, rememberMe, handleSubmit };
  },
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.social-login {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.social-button {
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  color: white;
}

.google {
  background-color: #db4437; /* Google 색상 */
}

.apple {
  background-color: #000; /* Apple 색상 */
}

.kakao {
  background-color: #f7e03b; /* Kakao 색상 */
  color: black;
}

.or-divider {
  text-align: center;
  margin: 10px 0;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input[type="email"],
input[type="password"] {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.login-button {
  width: 100%;
  padding: 10px;
  background-color: #ed6d1e; /* 로그인 버튼 색상 */
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.signup-link {
  text-align: center;
  margin-top: 15px;
}
</style>
