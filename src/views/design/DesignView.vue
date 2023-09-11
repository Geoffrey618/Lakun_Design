<template>
    <div class="page-container">
      <div class="canvas-container">
        <div class="canvas-wrapper"> 
          <canvas ref="canvas"></canvas>
        </div>
        <div class="controls">
          <br>
          <h2 style="margin: 2px">正在编辑：{{ project_glo }}</h2>
          <el-color-picker v-model="selectedColor"></el-color-picker>
          <div>
            <el-button type="primary" @click="addRectangle">矩形</el-button>
            <el-button type="primary" @click="addCircle">圆形</el-button>
          </div>
          <div class="file-upload">
            <input id="file-input" type="file" @change="handleFileUpload" accept="image/*" style="padding-left: 80px">
          </div>
          <el-input v-model="textToAdd" placeholder="输入文本"></el-input>
          <div>
            <el-button type="primary" @click="addText">添加文本</el-button>
            <el-button type="primary" @click="deleteObject">删除对象</el-button>
          </div>
          <div>
            <el-button type="primary" @click="rotateObject1">顺时针旋转</el-button>
            <el-button type="primary" @click="rotateObject2">逆时针旋转</el-button>
          </div>
          <div>
            <el-button type="primary" @click="scaleObject1">放大该对象</el-button>
            <el-button type="primary" @click="scaleObject2">缩小该对象</el-button>
          </div>
          <div>
            <label>画布宽度:
              <el-slider v-model="canvasWidth" :min="400" :max="800"></el-slider>
              <span>{{ canvasWidth }}</span>
            </label>
          </div>
          <div>
            <label>画布高度:
              <el-slider v-model="canvasHeight" :min="200" :max="600"></el-slider>
              <span>{{ canvasHeight }}</span>
            </label>
          </div>
          <div>
            <div>
                <el-button type="primary" @click="exportImage">导出图片</el-button>
                <el-button type="primary" @click="exportHTML">导出当前设计</el-button>
            </div>
            <br>
            <div>
                <el-button type="primary" @click="downloadDesign">加载设计</el-button>
                <el-button type="primary" @click="saveDesign">保存当前设计</el-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { fabric } from 'fabric';
  import { mapState, mapMutations } from 'vuex';
  import axios from 'axios';
  
  export default {
    computed: {
      ...mapState([
        'username_glo',
        'url_glo',
        'team_glo',
        'project_glo',
        'pagename_glo',
      ])
    },
    data() {
      return {
        canvas: null,
        canvasWidth: 800,
        canvasHeight: 600,
        selectedColor: '#000000', // Default color is red
        textToAdd: '',
      };
    },
    methods: {
        addRectangle() {
            const rect = new fabric.Rect({
                left: 10,
                top: 10,
                fill: this.selectedColor,
                width: 100,
                height: 100,
            });
            this.canvas.add(rect);
        },
        addCircle() {
            const circle = new fabric.Circle({
                left: 50,
                top: 50,
                fill: this.selectedColor,
                radius: 50,
            });
            this.canvas.add(circle);
        },
        exportImage() {
            const dataURL = this.canvas.toDataURL({ format: 'png' });
            const link = document.createElement('a');
            link.href = dataURL;
            link.download = 'Lakun-Design.png';
            link.click();
        },
        handleFileUpload(event) {
            const file = event.target.files[0];
            const reader = new FileReader();
            reader.onload = () => {
                const img = new fabric.Image();
                img.setSrc(reader.result, () => {
                    img.set({
                        left: 10,
                        top: 10,
                        scaleX: 0.5,
                        scaleY: 0.5,
                    });
                    this.canvas.add(img);
                });
            };
            reader.readAsDataURL(file);
        },
        deleteObject() {
            const activeObject = this.canvas.getActiveObject();
            if (activeObject) {
                this.canvas.remove(activeObject);
            }
        },

        rotateObject1() {
            const activeObject = this.canvas.getActiveObject();
            if (activeObject) {
                activeObject.rotate(activeObject.angle + 15); // 旋转角度可以根据需要调整
                this.canvas.renderAll();
            }
        },

        rotateObject2() {
            const activeObject = this.canvas.getActiveObject();
            if (activeObject) {
                activeObject.rotate(activeObject.angle - 15); // 旋转角度可以根据需要调整
                this.canvas.renderAll();
            }
        },

        scaleObject1() {
            const activeObject = this.canvas.getActiveObject();
            if (activeObject) {
                activeObject.scaleX *= 1.2; // 缩放因子可以根据需要调整
                activeObject.scaleY *= 1.2;
                this.canvas.renderAll();
            }
        },

        scaleObject2() {
            const activeObject = this.canvas.getActiveObject();
            if (activeObject) {
                activeObject.scaleX *= 0.8; // 缩放因子可以根据需要调整
                activeObject.scaleY *= 0.8;
                this.canvas.renderAll();
            }
        },

        addText() {
            const text = new fabric.Textbox(this.textToAdd, {
                left: 10,
                top: 10,
                fill: this.selectedColor,
            });
            this.canvas.add(text);
        },
      // ... 其他方法没有变化 ...
      downloadDesign() {
  // 创建要发送给后端的数据对象
  const requestData = {
    pagename: this.$store.state.pagename_glo,
    projectid: this.$store.state.project_glo,
  };

  // 向后端发送请求，指定响应类型为文本
  axios.post('http://8.130.38.119:12000/PrototypePage/get_page_content/', requestData, {
    responseType: 'text', // 指定响应类型为文本
  })
    .then(response => {
      // 处理成功响应，response.data 包含后端返回的文本数据
      try {
        let canvasData = response.data.replace(/"None"/g, "null");
        canvasData = JSON.parse(canvasData);
        if (canvasData.success) {
          let parsedContent = canvasData.pagecontent.replace(/None/g, 'null').replace(/True/g, 'true').replace(/False/g, 'false');
          this.canvas.loadFromJSON(JSON.parse(parsedContent), () => {
        this.canvas.renderAll();
        this.$message.success('设计加载成功');
        });
        }
      } catch (error) {
        // 处理 JSON 解析错误
        this.$message.error('JSON 解析失败');
        console.error('JSON 解析失败', error);
      }
    })
    .catch(error => {
      // 处理请求失败的情况
      this.$message.error('加载失败');
      console.error('加载失败', error);
    });
},

      saveDesign() {
        const canvasData = this.canvas.toJSON(); // 将Canvas数据转换为JSON格式
        const data = {
            canvasData,
            projectid: this.$store.state.project_glo,
            pagesize:this.canvasWidth*this.canvasHeight,
            pagename:this.$store.state.pagename_glo,
        }
        // 发送Canvas数据到后端接口
        axios.post('http://8.130.38.119:12000/PrototypePage/create_page/', data)
          .then(response => {
            // 处理成功保存的响应
            this.$message.success('设计已保存');
          })
          .catch(error => {
            // 处理保存失败的错误
            this.$message.error('保存失败');
            console.error('保存失败', error);
          });
      },
  
      exportHTML() {
        const canvasData = this.canvas.toDataURL({ format: 'png' }); // 将Canvas内容导出为Base64图片数据
  
        // 创建一个新的HTML文档字符串
        const htmlContent = `
            <!DOCTYPE html>
            <html>
            <head>
                <title>Canvas导出</title>
            </head>
            <body>
                <img src="${canvasData}" alt="Canvas导出">
            </body>
            </html>
        `;
  
        // 创建Blob对象并保存为HTML文件
        const blob = new Blob([htmlContent], { type: 'text/html' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'Lakun-Design.html';
        link.click();
      },
    },
    mounted() {
      this.canvas = new fabric.Canvas(this.$refs.canvas, {
        backgroundColor: 'white',
        borderColor: 'black',
        cornerColor: 'black',
        cornerSize: 8,
        controlsAboveOverlay: true,
      });
      this.canvas.setWidth(this.canvasWidth);
      this.canvas.setHeight(this.canvasHeight);
    },
    watch: {
      canvasWidth(newWidth) {
        this.canvas.setWidth(newWidth);
      },
      canvasHeight(newHeight) {
        this.canvas.setHeight(newHeight);
      },
    },
  };
  </script>
  
  <style scoped>
  
  .styled-button {
    background-color: #ffffff;
    color: rgba(0, 0, 0, 0.77);
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .styled-button:hover {
    background-color: #0a89e7;
  }
  
  .page-container {
    display: flex;
  }
  
  .canvas-container {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    left: 80px;
    transform: translateY(3%);
  }
  
  .controls {
    height: 650px;
    width: 260px;
    background-color: #ffffff;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 0;
    box-sizing: border-box;
    gap: 10px;
    position: fixed;
    top: -30px; /* 你想要的初始位置 */
    right: 0; /* 你想要的初始位置 */
  }
  
  .canvas-wrapper {
    border: 2px solid black;
    margin-right: 20px;
  }
  
  .button-group {
  display: flex; /* 将按钮水平排列 */
  gap: 10px; /* 按钮之间的间距 */
}

/* 设置按钮背景颜色为浅灰色 */
.button-group .el-button {
  background-color: #f0f0f0;
  color: rgba(0, 0, 0, 0.77);
}

.button-group .el-button:hover {
  background-color: #d0d0d0; /* 鼠标悬停时的背景颜色 */
}

  .controls {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  </style>