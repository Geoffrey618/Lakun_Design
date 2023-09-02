<template>
  <div id="app">
    <mainHeader v-if="$route.meta.mainNavShow"/>
    <div class="content"> <!-- 将内容包裹在一个容器中 -->
      <router-view />
    </div>
  </div>
</template>

<script>
import mainHeader from "./components/NavBar.vue";
export default {
  name: 'App',
  components: {
    mainHeader,
  },
  data() {
    return {
      globalData: {
        // 定义全局变量
        username_global: '',
        token_global: '',
      }
    }
  }
}
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-color: rgb(241, 241, 241);
}

.content {
    background-color: white;
}
</style>