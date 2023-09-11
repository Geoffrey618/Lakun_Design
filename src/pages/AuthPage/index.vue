<template>
    <div class="login-page">
      <div class="card">
        <form @submit.prevent="login">
          <h1>LaKun设计聊天室</h1>
          <div class="title">登录</div>
          <input placeholder="Username" type="text" v-model="username" />
          <br />
          <input placeholder="Password" type="password" v-model="password" />
          <br />
          <button type="submit">登录</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import { loginRest, signupRest } from "./api";
  
  export default {
    data() {
      return {
        username: "",
        password: "",
        email: "",
        first_name: "",
        last_name: "",
      };
    },
    methods: {
      login() {
        loginRest(this.username, this.password)
          .then((response) =>
            this.$emit("onAuth", { ...response.data, secret: this.password })
          )
          .catch((error) => console.log("Login error", error));
      },
    },
  };
  </script>