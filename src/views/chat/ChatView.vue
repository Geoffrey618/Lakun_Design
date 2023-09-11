<template>
    <div class="chat-app">
      <div class="chat-window">
        <div class="chat-header">
          <h2>在线聊天</h2>
        </div>
        <div class="chat-messages" ref="chatMessages">
          <!-- 聊天消息将在这里显示 -->
          <div
            v-for="(message, index) in messages"
            :key="index"
            :class="['chat-message', { 'sent': message.sentByUser, 'received': !message.sentByUser }]"
            style="display: block;"
          >
            <span class="message-text">{{ message.text }}</span>
          </div>
        </div>
        <div class="chat-input">
          <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="输入消息..." />
          <button @click="sendMessage">发送</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        messages: [], // 存储聊天消息
        newMessage: '', // 输入的新消息
      };
    },
    methods: {
      sendMessage() {
        if (this.newMessage.trim() !== '') {
          this.messages.push({ text: this.newMessage, sentByUser: true });
          this.newMessage = ''; // 清空输入框
          // 此处应该将消息发送到服务器
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* 样式可以自行调整 */
  .chat-app {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }
  
  .chat-window {
    width: 700px; /* 增加宽度 */
    height: 500px; /* 增加高度 */
    border: 1px solid #ccc;
    padding: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: column; /* 垂直方向排列子元素 */
  }
  
  .chat-header {
    text-align: center;
    font-size: 18px;
    margin-bottom: 10px;
    display: block;
  }
  
  .chat-messages {
    max-height: 350px; /* 减小消息显示区域的最大高度 */
    overflow-y: auto;
    display: block;
    flex: 1; /* 占据剩余空间，使得输入框位于底部 */
    overflow-y: auto; /* 添加滚动条以处理消息溢出 */
  }
  
  .chat-message {
    margin-bottom: 15px;
    padding: 10px;
    border-radius: 10px;
    max-width: 70%;
    word-wrap: break-word;
    display: block;
    clear: both; /* 添加这行以确保每个消息独占一行 */
  }
  
  .chat-message.sent {
    background-color: #d1a83a;
    color: white;
    align-self: flex-end;
    float: right;
    display: block;
  }
  
  .chat-message.received {
    background-color: #eee;
    color: #333;
    align-self: flex-start;
  }
  
  .message-text {
    display: block; /* 确保文本内容在新行上 */
    text-align: left; /* 左对齐文本 */
  }
  
  .chat-input {
    display: flex;
    align-items: center;
  }
  
  .chat-input input {
    flex: 1;
    padding: 5px;
    border: 1px solid #ccc;
    border-radius: 3px;
  }
  
  .chat-input button {
    margin-left: 10px;
    padding: 5px 10px;
    background-color: #007BFF;
    color: white;
    border: none;
    border-radius: 3px;
    cursor: pointer;
  }
  </style>
  