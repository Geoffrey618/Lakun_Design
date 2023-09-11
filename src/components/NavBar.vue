<template>
  <div class="page">
    <nav class="sidebar">
      <img src="@/assets/images/logo1.jpg" height="120" width="120" style="display: block; margin: 0 auto;">
      <img src="@/assets/images/headline1.jpg" height="50" width="220" style="display: block; margin: 0 auto;">
      <br>
      <br>
      <div class="menu-item" id="one">
          <div class="myel">
              <el-icon :size="'26px'"><User /></el-icon>
          </div>
          <router-link to="/profile">个人中心</router-link>
      </div>
      <div class="menu-item" id="two">
          <div class="myel">
              <el-icon :size="'26px'"><HomeFilled /></el-icon>
          </div>
          <router-link to="/team">我的团队</router-link>
      </div>
      <div class="menu-item" id="three">
          <div class="myel">
            <div class="notification-icon">

                <el-icon :size="'26px'"><ChatDotRound /></el-icon>
              <div v-if="unreadMessages > 0" class="notification-badge">
                {{ unreadMessages }}
              </div>
            </div>
          </div>

          <div style="display: flex; align-items: center">
            <el-popover placement="right" :width="800" trigger="click">
              <template #reference>
                <a style="margin-right: 16px">&nbsp;&nbsp;消息中心</a>
              </template>
              <div class="popover-content"> <!-- 添加一个容器元素 -->
                <el-button type="success" @click="readAll">一键已读</el-button>
                <el-button type="danger" @click="deleteRead">删除已读消息</el-button>
                <div class="scrollable-content"> <!-- 添加一个容器元素，用于滚动 -->
                  <el-table :data="gridData">
                    <el-table-column width="110" prop="timestamp" label="date">
                      <template v-slot="{ row }">
                        {{ row.timestamp }}
                        <div class="notification-badge1" v-if=!row.read></div>
                      </template>
                    </el-table-column>
                    <el-table-column width="100" prop="sender" label="Source" />
                    <el-table-column width="300" prop="content" label="Content" />
                    <el-table-column width="100">
                      <template v-slot="scope">
                        <el-button type="danger" @click="handleDelete(scope.row)" style="vertical-align: middle;">
                          删除
                        </el-button>
                      </template>
                    </el-table-column>
                    <el-table-column width="100">
                      <template v-slot="scope">
                        <el-button type="primary" @click="handleRead(scope.row)" :disabled=scope.row.read style="vertical-align: middle;">
                          已读
                        </el-button>
                      </template>
                    </el-table-column>
                  </el-table>
                </div>
              </div>
            </el-popover>
          </div>
      </div>
      <div class="menu-item" id="four">
          <div class="myel">
              <el-icon :size="'26px'"><DocumentCopy /></el-icon>
          </div>
          <router-link to="/projectmanage">项目管理</router-link>
      </div>
      <div class="menu-item" id="five">
          <div class="myel">
            <el-icon :size="'26px'"><ChatLineRound /></el-icon>
          </div>
          <a href="http://8.130.13.60/">聊天中心</a>
      </div>
      <div class="menu-item" id="six">
              <div class="myel">
                  <el-icon :size="'26px'"><share /></el-icon>
              </div>
              <a href="https://github.com/Geoffrey618/Lakun_Design.git">关于LaKun</a>
          </div>
        <div class="container">

  </div>
  <div id="finally"></div>
    </nav>
  </div>
</template>
<script>
import axios from "axios";
import { mapState, mapMutations, useStore } from 'vuex';
import IntroJs from 'intro.js' // introjs库
import 'intro.js/introjs.css' // introjs默认css样式
// introjs还提供了多种主题，可以通过以下方式引入
import 'intro.js/themes/introjs-modern.css'
import { nextTick, onMounted } from "vue";

export default{
  computed: {
    ...mapState([
      'url_glo',
      'username_glo',
      'show'
    ])
  },
  setup() {
    const store = useStore();
      const initPageIntro = () => {
          // 引导图
          const allSteps = [
              {
                  element: '#one', //这是添加引导的元素id
                  intro: '这里可以查看个人信息并进行修改。', //这是引导提示内容
                  position: 'right' //这是引导位置
              },
              {
                  element: '#two',
                  intro: '这里能直观地看到所属团队的基本信息和成员，假如你是管理员，还可以对团队人员及信息进行管理与修改。',
                  position: 'left'
              },
              {
                  element: '#three',
                  intro: '这里可以看到所有收到的消息，并对于消息进行已读或删除。',
                  position: 'left'
              },
              {
                  element: '#four',
                  intro: '这里可以查看团队的所有项目，并可以进行新建删除项目等操作。',
                  position: 'left'
              },
              {
                  element: '#five',
                  intro: '这里可以创建团队的群聊，也可以与团队成员进行私聊。',
                  position: 'left'
              },
              {
                  element: '#six',
                  intro: '这里可以查看网站的相关介绍。',
                  position: 'top'
              },
              {
                  element: '#finally',
                  intro: '引导结束，现在开始使用lakun吧！',
                  position: 'top'
              }
          ]

          const curIntro = IntroJs()
          curIntro.setOptions({
              prevLabel: `上一步`,
              nextLabel: `下一步`,
              skipLabel: `跳过`,
              doneLabel: `完成`,
              tooltipPosition: `bottom` /* 引导说明框相对高亮说明区域的位置 */,
              hidePrev: `true`, // 隐藏第一步中的上一个按钮
              tooltipClass: `` /* 引导说明文本框的样式 */,
              highlightClass: `` /* 说明高亮区域的样式 */,
              exitOnOverlayClick: false /* 是否允许点击空白处退出 */,
              showStepNumbers: false /* 是否显示说明的数据步骤*/,
              keyboardNavigation: false /* 是否允许键盘来操作 */,
              showButtons: true /* 是否按键来操作 */,
              showBullets: true /* 是否使用点点点显示进度 */,
              showProgress: false /* 是否显示进度条 */,
              scrollToElement: true /* 是否滑动到高亮的区域 */,
              overlayOpacity: 0.6 /* 遮罩层的透明度 */,
              positionPrecedence: [`bottom`, `top`, `right`, `left`] /* 当位置选择自动的时候，位置排列的优先级 */,
              disableInteraction: false, /* 是否禁止与元素的相互关联 */
              hintPosition: 'top-middle',
              steps: allSteps
          })
          curIntro.oncomplete(() => {
              // 点击结束按钮后执行的事件
              console.log(`oncomplete`)
          })
          curIntro.onexit(() => {
              // 点击跳过按钮后执行的事件
              console.log(`onexit`)
          })
          curIntro.onchange(() => {
              // 点击下一步执行的事件
              console.log(`onchange`)
          })
          curIntro.start()
      }
      if(store.state.show==1){
          onMounted(() => {
            nextTick(() => {
                initPageIntro()
            })
        })
      }
      store.state.show=0;
      
  },
  data () {
    return {
      profilePopoverVisible: true, // 控制个人中心弹出框的显示和隐藏
      unreadMessages: 0, // 未读消息数量，根据实际情况动态设置
      gridData: [
        {
          id:1,
          sender:'zyt',
          content:'wwdddg',
          timestamp:'2023-08-31 19:24:46',
          read:false,//false代表未读，true代表已读
        },
      ],
    }
  },
  mounted(){
      this.$store.state.username_glo='TestUser1';
      const data={
        username:this.$store.state.username_glo,
      }
      console.log(data);
      axios.post('http://8.130.38.119:12000/chat/get_message_list/'+this.$store.state.username_glo+'/', data)
      .then(response => {
        console.log('start');
        console.log('data',response.data);
        //this.infoData=response.data.project;
        //console.log(response.data.unread_messages[0].timestamp);
        console.log(response.data.unread_messages);
        this.unreadMessages=response.data.unread_messages.length;
        this.gridData=response.data.read_messages.concat(response.data.unread_messages);
        this.setFirstNItemsAsTrueAndRestAsFalse(this.gridData,response.data.read_messages.length);
        this.gridData.sort((a, b) => {
            return new Date(a.timestamp) - new Date(b.timestamp);
        });
        this.shortenContact(this.gridData);
        console.log('end');
      })
      .catch(error => {
        // 处理请求错误
        console.error('请求错误1:', error);
      });
  },
  methods: {
    getlist(){
      const data={
        username:this.$store.state.username_glo,
      }
      axios.post('http://8.130.38.119:12000/get_message_list/'+this.$store.state.username_glo+'/', data)
      .then(response => {
        console.log('start');
        console.log('data',response.data);
        //this.infoData=response.data.project;
        console.log(response.data.read_messages);
        console.log(response.data.unread_messages);
        console.log('end');
      })
      .catch(error => {
        // 处理请求错误
        console.error('请求错误:', error);
      });
    },
    shortenContact(data) {
        return data.map(item => {
            if (item.content.length > 25) {
                item.content = item.content.substring(0, 25) + '...';
            }
            return item;
        });
    },
    setFirstNItemsAsTrueAndRestAsFalse(gridData, n) {
      for (let i = 0; i < gridData.length; i++) {
        if (i < n) {
          gridData[i].read = true;
        } else {
          gridData[i].read = false;
        }
      }
    },
    showProfilePopover() {
      // 当点击个人中心时触发
      console.log('showProfilePopover called');
      this.profilePopoverVisible = true;
    },
    jump(){
      this.$router.push('/login');
    },
    handleDelete(row){
      axios.post('http://8.130.38.119:12000/chat/delete_message/'+row.id+'/')
      .then(response => {
        //console.log('data',response.data);
      })
      .catch(error => {
        console.error('请求错误:', error);
      });
      const index = this.gridData.indexOf(row); // 获取要删除项的索引
        if (index !== -1) {
          this.gridData.splice(index, 1); // 使用splice方法删除项
      }
    },
    handleRead(row){
      //row.read=true;
      const data={
        messageid:row.id,
      };
      axios.post('http://8.130.38.119:12000/chat/mark_message_as_read/'+row.id+'/',data)
      .then(response => {
        //console.log('data',response.data);
      })
      .catch(error => {
        console.error('请求错误:', error);
      });
      this.unreadMessages--;
      row.read=true;
    },
    readAll(){
      const readMessages = this.gridData;
      readMessages.forEach(message => {
        this.handleRead(message);
      });
    },
    deleteRead(){
      const readMessages = this.gridData.filter(item => item.read === true);
      readMessages.forEach(message => {
        this.handleDelete(message);
      });
    },
  }
}

</script>

<style scoped>
.page {
  display: flex;
}

.content {
  flex: 1; /* 主体内容占据剩余空间 */
  padding: 20px;
}

.sidebar {
position: fixed; /* 设置为固定定位 */
top: 0; /* 从顶部开始 */
left: 0; /* 靠左边 */
width: 250px; /* 设置宽度 */
height: 100%; /* 高度充满整个屏幕 */
background-color: #ffffff; /* 背景颜色 */
color: #429eee; /* 文字颜色 */
z-index: 1000; /* 设置 z-index 以确保位于其他内容之上 */
/* 其他样式可以根据需要自定义 */
}
.menu-item {
/*padding: 10px 20px;  设置内边距 */
border-bottom: 1px solid #7cade9ac; /* 下边框线 */
transition: background-color 0.3s ease; /* 添加过渡效果 */
height: 60px;
align-items: center;
justify-content: center; /* 水平居中 */
display: flex; /* 使用 Flexbox 布局 */
}

.menu-item a {
display: block;
color: #0d0d0d;
text-decoration: none;
padding: 0;
height: 60px;
line-height: 60px; /* 将文本垂直居中 */
}


.menu-item:hover {
  background-color: #559dfd; /* 鼠标悬停时的背景颜色 */
}
.myel{
  height: 25px;
  width: 25px;
  margin-right: 10px; /* 为图标和文本之间添加一些间距 */
  color: #0d0d0d;
}
.router-link {
display: flex;
align-items: center; /* 文本垂直居中对齐 */
}
.notification-icon {
  position: relative;
  display: inline-block;
}

.notification-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background-color: red;
  color: white;
  border-radius: 50%;
  padding: 2px 2px;
  font-size: 12px;
  height: 13px;
  width: 13px;
}

.notification-badge1 {
  position: absolute;
  top: 0px;
  right: 5px;
  background-color: red;
  color: white;
  border-radius: 50%;
  padding: 2px 2px;
  font-size: 12px;
  height: 13px;
  width: 13px;
}
</style>
