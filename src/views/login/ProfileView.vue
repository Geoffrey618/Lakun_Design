<template>
  <div class="app-content">
    <sidebar></sidebar>
    <div class="main-content">
      <div class="profile">
        <div class="avatar">
          <img src="@/assets/images/defaultAvatar.jpeg">
        </div>
        <div class="info">
          <h1>{{ yik }}</h1>
          <p>您的昵称: {{ this.$store.state.username_glo }}</p>
          <p>个性签名：Ta很懒，还没有设置个性签名</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex'
export default {
  name: 'App',
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
      user: {},
      username: 'zk3',
      phonenumber: '15832369597',
      currentTab: '基本信息',
      password: 'encryptedpassword',
      email: 'user@email.com',
      nickname: 'Nickname',
      experience: 30,
      level: 5,
      avatar: '@/assets/images/logo.jpg',
      signature: 'This is my signature.',
    }
  },
}
</script>

<style scoped>
.app-content {
  display: flex;
  padding-top: 50px;
  padding-left: 20%;
}

.demo-progress .el-progress--line {
  margin-bottom: 15px;
  width: 250px;
}

.main-content {
  flex-grow: 1;
  padding-left: 20px;
}

.profile {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 50px;
  margin-right: 20px;
  background: linear-gradient(to bottom right, #ffffff, #f2f2f2);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  padding-bottom: 20px;
}

.avatar img {
  width: 70px;
  height: 70px;
  border-radius: 50%;
}

.info {
  margin-left: 50px;
  margin-bottom: 20px;
  text-align: left;
}

.info h1 {
  margin: 0;
  padding: 0;
  font-size: 2em;
  color: #000;
}

.info p {
  margin: 5px 0;
  color: #666;
  line-height: 1.5;
}

.info .role {
  font-size: 1.2em;
  font-weight: bold;
  color: #333;
}

  /* 底部内容样式 */
  .bottom-content {
    margin-top: 50px;
    padding: 20px;
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    margin-bottom: 300px;
  }

  .bottom-content h2 {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
  }

  .bottom-content p {
    font-size: 16px;
    line-height: 1.5;
    margin-bottom: 10px;
    
  }
</style>