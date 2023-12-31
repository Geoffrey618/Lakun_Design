import { createStore } from 'vuex'
import createPersistedState from 'vuex-persistedstate'

const store = createStore({
  state() {
    return {
      count: 0,//测试用的
      username_glo: 'TestUser1',
      token_glo:'',
      exp_glo:'',
      url_glo:'http://127.0.0.1:12000/',
      team_glo:'TestTeam1',
      pagename_glo:'TestProgram',
      project_glo:'TestProgram',
      show:'0',//0表示不显示s
    }
  },
  mutations: {
    increment(state) {
      state.count++
    },
    decrement(state) {
      state.count--
    },
    updateUsername_glo(state,un){
        state.username_glo = un;
    },
    updateToken_glo(state,tok){
      state.token_glo = tok;
    },
    updateExp_glo(state,exp){
      state.exp_glo = exp;
    }
  },
  //全局变量保存在浏览器里（感觉也合理，并且方便测试:可以直接输入对应url，不会丢失全局变量）
  plugins: [createPersistedState()]
})

export default store