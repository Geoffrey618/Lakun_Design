<template>
  <div class="info-pagination">
    <span>
        <el-p style="text-align: left;">新建项目&emsp;</el-p>
        <el-input v-model="newProjectName" placeholder="项目名称" :style="{ width: '250px' }"></el-input>
        <el-button @click="addInfo">添加</el-button>
    </span>
    <span>
      <el-p style="text-align: left;">搜索项目&emsp;</el-p>
      <el-input v-model="searchName" placeholder="项目名称" :style="{ width: '250px' }"></el-input>
      <el-button @click="search">搜索</el-button>
    </span>
    <span>
      <el-p style="text-align: left;">排序方式&emsp;</el-p>
      <el-select v-model="selectedSort" :style="{ width: '250px' }">
        <el-option label="按时间" value="按时间" @click="sortByTime">
          <span slot="dropdown">按时间排序</span>
        </el-option>
        <el-option label="按名称" value="按名称" @click="sortByName">
          <span slot="dropdown">按名称排序</span>
        </el-option>
        <el-option label="按创建者" value="按创建者" @click="sortBySource">
          <span slot="dropdown">按创建者排序</span>
        </el-option>
      </el-select>
      <el-button style="opacity: 0">搜索</el-button>
    </span>
    <div class="info-list">
      <el-table :data="infoData" style="width: 100%">
        <el-table-column label="项目名称" prop="projectname"  :width="200">
            <template v-slot="{ row }">
                <!-- 给项目名称加粗并标红 -->
                <span class="highlighted-name">{{ row.projectname }}</span>
            </template>
        </el-table-column>
        <el-table-column label="创建者" prop="creatorid"></el-table-column>
        <el-table-column label="创建时间">
          <template v-slot="{ row }">
            {{ formatTimeWithT(row.created_time) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" :width="340">
          <template v-slot="{  $index }">
            <el-button type="primary" @click="showDialog($index)">查看</el-button>
            <el-dialog
              v-model="dialogVisible"
              title="查看项目详细内容"
              :modal="false"
              width="30%"
              @close="closeDialog"
            >
              <!-- 弹框的内容放在这里 -->
              <p>您想要查看哪个内容？</p>
              <!-- 在这里添加显示成绩、显示分数等按钮 -->
              <el-button @click="showCircle(a)">查看原型</el-button>
              <el-button @click="showFile(a)">查看文档</el-button>
            </el-dialog>
            <el-button type="danger" @click="deleteInfo($index)">删除</el-button>
            <el-button type="success" @click="renameInfo($index)">重命名</el-button>
            <el-button type="warning" @click="copyInfo($index)">复制</el-button>
          </template>
        </el-table-column>
      </el-table>
      <p></p>
      <!-- 新增输入框和添加按钮 -->

    </div>
  </div>
</template>

<script>
import router from "@/router";
import { faTemperature1 } from "@fortawesome/free-solid-svg-icons";
import axios from "axios";
import { mapState, mapMutations } from 'vuex'
export default {
  computed: {
      ...mapState([
        'username_glo',
        'url_glo',
        'team_glo'
      ])
    },
  data() {
    return {
      selectedSort: '按时间',
      totalInfoCount: 6,
      currentPage: 1,
      pageSize: 10,
      infoData: [],
      newProjectName: "", // 用于存储用户输入的项目名称
      searchName:'',
      dialogVisible: false,
      a:''
    };
  },
  computed: {
    // 根据当前页和每页数量计算要显示的信息
    displayedInfo() {
      const startIndex = (this.currentPage - 1) * this.pageSize;
      const endIndex = startIndex + this.pageSize;
      return this.infoData.slice(startIndex, endIndex);
    },
  },
  mounted() {
      const data = {
        teamname: this.$store.state.team_glo, // 替换为实际的团队名称
      }
      console.log(this.$store.state.username_glo);
      axios.post('http://8.130.38.119:12000/project/get_project_list/', data)
      .then(response => {
        // 处理成功响应
        const responseData = response.data;
        if (responseData.result === 1) {
          // 请求成功，处理项目列表数据
          const team = responseData.team;
          const projectList = responseData.project_list;
          console.log('获取项目列表成功！');
          console.log('团队名称:', team.teamname);
          console.log('项目列表:', projectList);
          this.infoData=projectList;
          console.log('项目列表:', this.infoData);
        } else {
          // 请求失败，处理错误消息
          console.error('获取项目列表失败:', responseData.message);
        }
      })
      .catch(error => {
        // 处理请求错误
        console.error('获取项目列表请求错误:', error);
      });
    },
  methods: {
    formatTimeWithT(timeWithT) {
      const date = new Date(timeWithT);
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      const seconds = String(date.getSeconds()).padStart(2, '0');
      return `${year}-${month}-${day}  ${hours}:${minutes}:${seconds}`;
    },
    // 处理分页变化
    handlePageChange(newPage) {
      // 更新当前页
      this.currentPage = newPage;
      // 加载当前页的信息
    },
    showDialog(index) {
      this.dialogVisible = true;
      this.a=index;
    },
    showCircle(index){
      console.log(index);
      console.log(this.infoData[index].projectid);
      this.$store.state.project_glo=this.infoData[index].projectid;
      this.$router.push('/design');
    },
    showFile(index){
      console.log(index);
      console.log(this.infoData[index].projectid);
      this.$store.state.project_glo=this.infoData[index].projectid;
      this.$router.push('/editor');
    },
    sortByName() {
      this.infoData.sort((a, b) => {
        const nameA = a.projectname.toUpperCase();
        const nameB = b.projectname.toUpperCase();
        if (nameA < nameB) {
          return -1;
        }
        if (nameA > nameB) {
          return 1;
        }
        return 0;
      });
    },
    sortBySource() {
      this.infoData.sort((a, b) => {
        const nameA = a.creatorid.toUpperCase();
        const nameB = b.creatorid.toUpperCase();
        if (nameA < nameB) {
          return -1;
        }
        if (nameA > nameB) {
          return 1;
        }
        return 0;
      });
    },
    sortByTime() {
      this.infoData.sort((a, b) => {
        const timeA = new Date(a.created_time);
        const timeB = new Date(b.created_time);
        return timeA - timeB;
      });
    },
    search(){
      const data={
        query:this.searchName,
        team_name:this.$store.state.team_glo,
      }
      console.log(data);
      axios.post('http://8.130.38.119:12000/project/search_project/'+this.$store.state.username_glo+'/', data)
        .then(response => {
          // 处理成功响应
          //console.log(data);
          console.log(response.data);
          //window.location.reload();
          this.infoData=response.data.project;
        })
        .catch(error => {
          // 处理请求错误
          console.error('请求错误:', error);
        });
    },
    // 添加新信息
    addInfo() {
      const data={
        teamname:this.$store.state.team_glo,
        projectname:this.newProjectName,
      }
      console.log(data.projectname);
        axios.post('http://8.130.38.119:12000/project/create_project/'+this.$store.state.username_glo+'/', data)
        .then(response => {
          // 处理成功响应
          console.log('成功创建了项目'+data.projectname);
          console.log(response.data);
          window.location.reload();
        })
        .catch(error => {
          // 处理请求错误
          console.error('请求错误:', error);
        }); 
    },
    // 查看信息
    viewInfo(info) {
      this.$router.push('/design')
    },
    // 删除信息
    deleteInfo(index) {
      const confirmDelete = window.confirm('确认删除这个项目吗？');
      if (confirmDelete) {
        var data={
          teamname:this.$store.state.team_glo,
          projectname:this.infoData[index].projectname,
          username:this.$store.state.username_glo,
        }
        console.log('全局变量-用户名：'+this.$store.state.username_glo);
        console.log('mamam',this.infoData[1].projectname);
        console.log('传入的data:',data);
        axios.post('http://8.130.38.119:12000/project/delete_project/', data)
        .then(response => {
          // 处理成功响应
          console.log('成功删除了项目'+data.projectname);
          console.log(response.data);
          window.location.reload();
        })
        .catch(error => {
          console.error('请求错误:', error);
        });
      }
    },
    copyInfo(index){
      const newName = prompt('请输入新的项目名称', this.infoData[index].projectname+'-副本');
      if (newName !== null) {
        //this.infoData[index].projectName = newName;
        var data={
          teamname:this.$store.state.team_glo,
          projectname:this.infoData[index].projectname,
          newprojectname:newName,
        }
        console.log(this.$store.state.username_glo);
        console.log(data);
        axios.post('http://8.130.38.119:12000/project/copy_project/'+this.$store.state.username_glo+'/', data)
        .then(response => {
          // 处理成功响应
          console.log('成功复制了项目'+data.projectname);
          console.log(response.data);
          window.location.reload();
        })
        .catch(error => {
          // 处理请求错误
          console.error('请求错误:', error);
          });
      }
    },
    renameInfo(index) {
      console.log(index);
      const newName = prompt('请输入新的项目名称', this.infoData[index].projectname);
      if (newName !== null) {
        //this.infoData[index].projectName = newName;
        var data={
          teamname:this.$store.state.team_glo,
          projectname:this.infoData[index].projectname,
          newprojectname:newName,
        }
        console.log(this.$store.state.username_glo);
        console.log(data);
        axios.post('http://8.130.38.119:12000/project/rename_project/', data)
        .then(response => {
          // 处理成功响应
          console.log('成功重命名了项目'+data.projectname);
          console.log(response.data);
          window.location.reload();
        })
        .catch(error => {
          // 处理请求错误
          console.error('请求错误:', error);
          });
      }
    },
  },
};
</script>

<style scoped>
.info-pagination {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 2.5%;
  padding-left: 20%;
  background-color: rgb(255, 255, 255);
}

.info-list {
  width: 80%;
  font-weight: 320; /* 设置字体为较细 */
  /*font-family: serif;*/
  /*font-family: 'Helvetica Neue', Arial, sans-serif; 选择字体，按优先级列出多个备选字体 */
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  border-top: 0px solid #00f; /* 1像素宽度的实线边框，颜色为黑色 */
  border-bottom: 2px solid rgb(151, 151, 151); /* 2像素宽度的虚线边框，颜色为蓝色 */
}

.info-content {
  display: flex;
  align-items: center;
}

.info-separator {
  margin: 0 10px; /* 调整分隔符的间距 */
  border-right: 1px solid #ccc; /* 分隔符样式 */
  height: 16px; /* 控制分隔符的高度 */
}

.info-actions {
  display: flex;
  align-items: center;
}

/* 自定义样式来居中页码 */
.el-pagination {
  display: flex;
  justify-content: center;
  margin-top: 16px; /* 可根据需要调整页码与其他内容的间距 */
}
.highlighted-name {
    color: rgb(54, 154, 235);
    font-weight: bold;
    font-family: "Microsoft YaHei", Tahoma, Arial, sans-serif;
}
span {
    display: block; /* 设置<span>元素为块级元素 */
    margin-bottom: 10px; /* 可选：添加底部边距以增加行距 */
}
</style>
