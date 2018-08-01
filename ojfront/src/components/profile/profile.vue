<template>
    <div>
        <el-row :gutter="20">
            <el-col :span="18" :offset="3" >
                <el-card shadow="hover">
                    <div class="lyyfont lyycentre" >{{userName}}</div>
                    <div class="lyycentre">{{signature}}</div>
                    <hr>
                    <div class="lyybox"><el-badge :value="passNum" class="item">
                        <el-button type="success" size="medium">通过题目数</el-button>
                    </el-badge></div>
                    <div class="lyybox"><el-badge :value="totalNum" class="item">
                        <el-button type="danger" size="medium">总提交数</el-button>
                    </el-badge></div>
                    <el-table
                        :data="tableData"
                        border
                        style="width: 100%">
                        <el-table-column
                        prop="id"
                        label="提交编号">
                        </el-table-column>
                        <el-table-column
                        prop="problem"
                        label="对应题目编号">
                        </el-table-column>
                        <el-table-column
                        prop="create_time"
                        label="提交时间">
                        </el-table-column>
                        <el-table-column
                        prop="result"
                        label="结果">
                            <template slot-scope="scope">
                                <el-tag
                                :type="mapResultToColor(scope.row.result)"
                                disable-transitions>{{mapResultToString(scope.row.result)}}</el-tag>
                            </template>
                        </el-table-column>
                        <el-table-column
                        label="操作">
                            <template slot-scope="scope">
                                <el-button @click="handleClick(scope.row)" type="text" size="small">查看</el-button>
                            </template>
                        </el-table-column>
                    </el-table>

                </el-card>

            </el-col>

        </el-row>
    </div>
</template>

<script>
export default {
    computed : {
        baseUrl() {
            return this.$store.state.baseUrl;
        },
        login() {
            return this.$store.state.login;
        },
        userName() {
            return this.$store.state.userName;
        }
    },
    data() {
        return {
            signature : '',
            passNum : 0,
            totalNum : 0,
            tableData:[],
        }
    },
    created : function() {
        this.getMyProfile()
        this.getMyRecentAnswers()
    },
    methods : {
        getMyProfile() {
            this.$http.get(this.baseUrl + '/api/ojuser/profile/my').then(response => {
                var rejs = response.body
                this.signature = rejs['data']['signature']
                this.totalNum = rejs['data']['total_num']
                this.passNum = rejs['data']['pass_num']
                var name = rejs['data']['username']
                this.$store.commit('setUserName', name)

            }, response => {
                console.log(response)
            });
        },
        getMyRecentAnswers() {
            this.$http.get(this.baseUrl + '/api/ojproblem/myanswers').then(response => {
                console.log(response)
                var rejs = response.body
                this.tableData = rejs['results']
            }, response => {
                console.log(response)
            })
        },
        mapResultToString(result) {
            switch(result) {
                case -1:
                    return '答案错误'
                case 0:
                    return '答案正确'
                case 1:
                    return '运行超时'
                case 2:
                    return '运行超时'
                case 3:
                    return '内存溢出'
                case 4:
                    return '运行时错误'
                case 5:
                    return '系统错误'
                default:
                    return 'N/A'
            }
        },
        mapResultToColor(result) {
            switch(result) {
                case -1:
                    return 'danger'
                case 0:
                    return 'success'
                case 1:
                    return 'warning'
                case 2:
                    return 'warning'
                case 3:
                    return 'warning'
                case 4:
                    return 'info'
                case 5:
                    return 'info'
                default:
                    return 'primary'
            }
        }
    }
}
</script>


<style>
.el-input .el-row{
    margin-bottom: 20px;
}
.lyyfont {
    font-size: 40px;
}
.lyycentre {
    text-align: center;
}
.lyybox {
    margin-bottom: 20px;
}
</style>