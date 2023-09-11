<template slot-scope="scope">
    <div class="out">
        <el-row type="flex">
            <el-col  :span="3" :offset="18">
                <el-input v-model="team.teamname2" placeholder="输入团队名"></el-input>
            </el-col>
            <el-col  :span="1" >
                <el-button type="success" @click="createteam">创建团队</el-button>
            </el-col>
        </el-row>
        <el-form :inline="true" :model="filters">
            <el-form-item>
                <el-select v-model="value" placeholder="请选择团队" @change="handlechange">
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
            <!-- <el-form-item> -->
                <!-- <el-button type="primary" v-on:click="getUsers">查询</el-button> -->
            <!-- </el-form-item> -->
            <el-form-item>
                <el-button type="primary" @click="handleAdd">新增</el-button>
            </el-form-item>
        </el-form>
    </div>
        
        <el-table :data="users" border style="width: 100%;">
            <el-table-column type="selection"  align="center">
            </el-table-column>
            
            <el-table-column prop="nickname" label="昵称"  sortable align="center">
            </el-table-column>
            <el-table-column prop="username" label="用户名"  :formatter="formatSex" sortable align="center">
            </el-table-column>
            <el-table-column prop="mail" label="邮箱"  sortable align="center">
            </el-table-column>
            <el-table-column prop="role" label="身份"  sortable align="center">
            </el-table-column>
            <el-table-column prop="location" label="所在地"  sortable align="center">
            </el-table-column>
            <el-table-column label="操作" >
                <template v-slot="{row}">
                <el-button type="danger" size="small" @click="handleDel(row)">删除</el-button>
                <el-button type="success" size="small" @click="handle2(row)">设为管理员</el-button>
                <el-button type="warning" size="small" @click="handle3(row)">设为普通人</el-button>
                </template>
            </el-table-column>
        </el-table>
    </template>
    
    <script>
    import axios, { Axios } from 'axios';
    
    export default{
        data() {
            return {
                filters: {
                        name: ''
                    },
                    users:[],
                options: [
                    {
                        value:'zk1',
                        label:'zk1'
                    },
                    {
                        value:'zk2',
                        label:'zk2'
                    }

                ],
            value: '',
            dialogFormVisible: false,
            team:{
                teamname:"",
                username:localStorage.getItem('username'),
                //username:'aaaa',
                teamid:0,
                teamname2:''
            }
            }
            
        },
        methods:{
            getUsers(){
                var params1={
                    //teamid:0
                    teamname:this.team.teamname
                }
                //params1.teamid=this.team.teamid
                axios({
                    method:'post',
                    url:'http://8.130.38.119:12000/team/get_user_list/'+this.team.teamname+'/',
                    //url:'http://8.130.38.119:12000/team/get_user_list/SyhTeam/'
                    //params:params1
                }).then((res)=>{
                    this.users=res.data.like_list
                    console.log(res)
                })
            },
            handleAdd(){
                var params1={
                    username:'zk',
                    //username:localStorage.getItem('username')

                }
                //params.username=this.team.username
                axios({
                    method:'post',
                    url:'http://8.130.38.119:12000/team/add_team_member/'+this.$store.state.username_glo+'/',
                    //params:params1,
                    data:{
                        
                    username:this.filters.name,
                    //username:'zk',
                      // teamname:'abc'
                    teamname:this.value
                        
                        
                    }
                }).then((res)=>{console.log(res)})
            },
            handleDel(row){
                var params1={
                    username:'zk'
                    //username:localStorage.getItem('username')
                }
                //params.username=this.team.username
                axios({
                    method:'post',
                    url:'http://8.130.38.119:12000/team/delete_team_member/'+this.$store.state.username_glo+'/',
                    //params:params1,
                    data:{
                        teamname:this.value,
                        deletename:row.username,
                        //deletename:'zk',
                        //teamname:'abc'
                        
                    }
                }).then((res)=>{console.log(res)})
                this.getUsers
            },
            createteam(){
                var params1={
                    username:'zk'
                    //username:localStorage.getItem('username')
                }
                //params.teamname=this.team.teamname
                /*axios({
                    method:'post',
                    url:'http://8.130.38.119:12000/user/form_team/'+this.$store.state.username_glo+'/',
                    //params:params1,
                   data:{
                    //teamname:this.team.teamname,
                    teamname:'SyhTeam',
                    members:['zk']
                   } 

                }).then((res)=>{console.log(res)})*/
                const data={
                teamname:this.team.teamname2,
                
                //teamname:'syhhhh',
                members:['zk']
                }
                axios.post('http://8.130.38.119:12000/user/form_team/testuser10'+'/', data).then(
                    (res)=>{
                        console.log(res)
                    }
                )
            },
            handle2(row){
                var params1={
                    username:localStorage.getItem('username')
                }
                //params.teamname=this.team.teamname
                //params.username=this.team.username
                axios({
                    method:'post',
                    url:'http://8.130.38.119:12000/team/add_admin/'+this.$store.state.username_glo+'/',
                    //params:params1,
                    data:{
                        teamname:this.value,
                        username:row.username,
                        //username:'zk',
                        //teamname:'abc'
                    }
                }).then((res)=>{console.log(res)})
            },
            handle3(row){
                var params1={
                    username:localStorage.getItem('username')
                }
                //params.teamname=this.team.teamname
                //params.username=this.team.username
                axios({
                    method:'post',
                    url:'http://8.130.38.119:12000/team/delete_admin/'+this.$store.state.username_glo+'/',
                    //params:params1,
                    data:{
                        teamname:this.value,
                        deletename:row.username,
                        //username:'bbb'
                    }
                }).then((res)=>{console.log(res)})
            },
            getTeam(){
                var params1={
                    username:'zk'
                    //username:localStorage.getItem('username')
                }
                axios({
                    method:'post',
                    url:'http://8.130.38.119:12000/team/get_team_list/'+this.$store.state.username_glo+'/',
                    //params:params1
                }).then((res)=>{
                    console.log(this.$store.state.username_glo)
                    console.log(res)
                    //if(res.data.like_list.length>0)
                    console.log(res.data.like_list[0])
                    for(var a=0;a<res.data.like_list.length;a++){
                        var x={
                            value: res.data.like_list[a].teamname,
                            label: res.data.like_list[a].teamname,
                    }
                    this.options.push(x)
                    }
                    console.log(res)
                })
            },
            handlechange(){
                //this.team.teamid=this.value
                //this.getTeam()
                this.team.teamname=this.value
                this.getUsers()
            }
        },
        created() {
             this.getTeam()
            //var a=0
            //this.handleDel(a)
            //this.handle2()
            //this.getUsers()
        },
        watch(){}
    }
    
    </script>
    
    <style scoped>
    .out{
        padding-left: 40%;
    }
    </style>