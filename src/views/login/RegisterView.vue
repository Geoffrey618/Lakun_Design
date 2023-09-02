<template>
  <div class="Register">
    <form @submit.prevent="submitForm">
      <img src="@/assets/images/logo1.jpg" height=100 width=100 style="display: block; margin: 0 auto;">
        <img src="@/assets/images/headline1.jpg" height=40 width=180 style="display: block; margin: 0 auto;">
      <h2>注册</h2>
      <label>
        <input v-model="username" placeholder="账号" type="text" required>
      </label>
      <label>
        <input v-model="email" placeholder="邮箱" type="text" required>
      </label>
      <label>
        <input v-model="password" placeholder="密码" type="password" required>
      </label>
      <label>
        <input v-model="passwordRepeat" placeholder="确认密码" type="password" required>
      </label>
      <label>
          <input v-model="verificationCode" placeholder="验证码" type="text" required>
      </label>
        <label>
          <button type="button" :disabled="isButtonDisabled" @click="sendVerificationCode">获取验证码</button>
      </label>
      <button type="submit" :disabled="isButtonDisabled" @click="RegisterSend">注册</button>
      <div style="display: flex; justify-content: flex-end;">
        <router-link to="/">点此登录</router-link> 
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      passwordRepeat:'',
      remember: false,
      verificationCode: '',
      validPhoneNumber: false,
      isButtonDisabled: false,
      remainingSeconds: 0,
    }
  },

    methods: {
        async RegisterSend() {
            try {
                const response = await axios.post('http://8.130.38.119:12000/user/register/', {
                    username: this.username,
                    email: this.email,
                    password: this.password,
                    repassword: this.passwordRepeat,
                    sms_num: this.verificationCode,
                });

                console.log('Registration response:', response.data);

                // 根据后端的响应进行相应的处理
                if (response.data.code === 200) {
                    alert("恭喜您，注册成功！")
                    // 注册成功的处理逻辑
                } else {
                    alert("注册失败，请您稍后重试！")
                    // 注册失败的处理逻辑
                }
            } catch (error) {
                console.error('Error during registration:', error);
                // 处理错误情况
            }
        },
        async sendVerificationCode() {
            console.log(this.email);
            try {
                const response = await axios.post('http://8.130.38.119:12000/user/sms/', {
                    email: this.email,
                });

                console.log('Verification code sent:', response.data);

                // 根据后端的响应进行相应的处理
                if (response.data.code === 200) {
                    alert("已发送验证码至您的邮箱，请查收！")
                    // 发送成功的处理逻辑

                } else {
                    alert("验证码发送失败，请稍后重试！")
                    // 发送失败的处理逻辑
                }
            } catch (error) {
                console.error('Error sending verification code:', error);
                // 处理错误情况
            }
        },
        // ...其他方法
    },
};
</script>

<style scoped>
.input-button-wrapper {
    display: flex;
    justify-content: space-between;
    flex-direction: row;
}

.input-field {
    flex: 3;
    flex-direction: row;
}

.button-field {
    flex: 1;
    flex-direction: row;
}
.Register {
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

h2 {
  text-align: center;
  color: #333;
}

/* 修改链接的颜色为蓝色 */
a {
  color: black;
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

.button1 {
  padding: 3px;
  font-size: 18px;
  background-color: #239cd8;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  opacity: 1.0;
}
button {
    height: 40px;
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