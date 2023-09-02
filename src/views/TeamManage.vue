<template>
<div class="out">
    <el-row type="flex">
        <el-col  :span="3" :offset="18">
            <el-input v-model="team.teamname" placeholder="输入团队名"></el-input>
        </el-col>
        <el-col  :span="1" >
            <el-button type="success" @click="createteam">创建团队</el-button>
        </el-col>
    </el-row>
    <el-form :inline="true" :model="filters">
        <el-form-item>
            <el-select v-model="value" placeholder="请选择团队">
                <el-option
                  v-for="item in options"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
        </el-form-item>
        <el-form-item>
            <el-input v-model="filters.name" placeholder="姓名"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" v-on:click="getUsers">查询</el-button>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="handleAdd">新增</el-button>
        </el-form-item>
    </el-form>
</div>
    
    <el-table :data="users" border style="width: 100%;">
        <el-table-column type="selection"  align="center">
        </el-table-column>
        
        <el-table-column prop="name" label="姓名"  sortable align="center">
        </el-table-column>
        <el-table-column prop="username" label="用户名"  :formatter="formatSex" sortable align="center">
        </el-table-column>
        <el-table-column prop="mail" label="邮箱"  sortable align="center">
        </el-table-column>
        <el-table-column prop="role" label="身份"  sortable align="center">
        </el-table-column>
        <el-table-column label="操作" >
            <el-button type="danger" size="small" @click="handleDel">删除</el-button>
            <el-button type="success" size="small" @click="handle2">设为管理员</el-button>
            <el-button type="warning" size="small" @click="handle3">设为普通人</el-button>
        </el-table-column>
    </el-table>
</template>

<script>
export default{
    data() {
        return {
            filters: {
					name: ''
				},
                users:[{name:'a',username:'111',mail:'sss',role:"b"}
            ],
            options: [{
          value: '团队1',
          label: '团队1'
        }, {
          value: '团队2',
          label: '团队2'
        }],
        value: '',
        dialogFormVisible: false,
        team:{
            teamname:"",
            username:""
        }
        }
        
    },
    methods:{
        getUsers(){

        },
        handleAdd(){

        },
        handleDel(){

        },
        createteam(){

        },
        handle2(){},
        handle3(){}
    }
}

</script>

<style scoped>
.out{
    padding-left: 40%;
}
</style>