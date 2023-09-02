<template>
  <div class="Login">
    <form @submit.prevent="submitForm">
      <!--<img src="../../assets/images/logo.jpg" height=80 width=80 style="display: block; margin: 0 auto;">-->
      <img src="@/assets/images/logo1.jpg" height=100 width=100 style="display: block; margin: 0 auto;">
        <img src="@/assets/images/headline1.jpg" height=40 width=180 style="display: block; margin: 0 auto;">
      <h1>登录</h1>
      <label>
        <input v-model="username" placeholder="账号" type="text" required>
      </label>
      <label>
        <input v-model="password" placeholder="密码" type="password" required>
      </label>
      <div class="remember-me">
        <input type="checkbox" id="remember" v-model="remember">
        <p style="font-size: 12px;" for="remember">记住用户名</p>
      </div>
      <button type="submit">登录</button>
      <div style="display: flex; justify-content: flex-end">
        <router-link to="/register">注册账号</router-link> 
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
import { mapState, mapMutations } from 'vuex'
export default {
  computed: {
      ...mapState([
        'username_glo',
        'url_glo',
        'team_glo',
        'show'
      ])
  },
  data() {
    return {
      username: '',
      password: '',
      // remember: false
    }
  },
    methods: {
      submitForm() {
          const userData = {
              username: this.username,
              password: this.password,
          };
          console.log('userData:', userData);
          const backendURL = 'http://8.130.38.119:12000/user/login/';
          axios.post(backendURL, userData).then(response => {
              console.log("login success");
              console.log(this.$store.state.username_glo);
              this.$store.state.show=1;
              this.$store.state.username_glo=userData.username
              console.log(this.$store.state.username_glo);
              this.$router.push('/profile'); // Replace '/' with your main page route
          })
      }
    }
  }

</script>

<style scoped>

.input-wrapper {
  position: relative;
}

.input-img {
  position: absolute;
  top: 50%;
  right: 20px;
  transform: translateY(-50%);
}
.Login {
  width: 100%;
  height: 100%;
  background: url("@/assets/images/background3.jpg") no-repeat;
  background-size: cover;
  overflow: hidden;
  position: fixed;
  justify-content: center;
  align-items: center;
  display: flex;
  height: 100vh;
  opacity: 0.9; /* 设置透明度，可以在 0 到 1 之间调整 */
}

form {
  display: flex;
  flex-direction: column;
  width: 300px;
  gap: 10px;
  padding: 20px;
  border-radius: 20px;
  background-color: white;
  box-shadow: 0px 0px 10px 0px rgba(0,0,0,0.1);
  opacity: 0.8;
}

a {
  color: black;
}


h2 {
  text-align: center;
  color: #333;
}

label {
  text-align: left;
  display: flex;
  flex-direction: column;
  font-size: 18px;
  color: #555;
}
input {
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 10px;
}

button {
  padding: 10px;
  font-size: 18px;
  background-color: #239cd8;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  opacity: 1.0;
}

input[type="checkbox"] {
  margin-right: 5px;
}

button:hover {
  background-color: #0056b3;
}
.remember-me {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  font-size: 16px;
  color: #555;
}
.remember-me label {
  margin-left: 5px;
}
</style>