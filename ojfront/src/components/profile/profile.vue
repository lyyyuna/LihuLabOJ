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
                        stripe
                        class="lyybox"
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
                                :type="mapResultToColor(scope.row.result, scope.row.runtime)"
                                disable-transitions>{{mapResultToString(scope.row.result, scope.row.runtime)}}</el-tag>
                            </template>
                        </el-table-column>
                        <el-table-column
                        label="操作">
                            <template slot-scope="scope">
                                <el-button @click="handleClick(scope.row)" type="text" size="medium">查看</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                    <el-pagination
                        class="lyycentre"
                        :page-size=20
                        :page-count=4
                        layout="prev, pager, next"
                        :total="totalItem"
                        @current-change="handleIndexChange"
                        @prev-click="handlePrev"
                        @next-click="handleNext"
                        >
                    </el-pagination>
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
            totalItem: 1,
            currentPrev: '',
            currentNext: ''
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
                this.totalItem = rejs['count']
                this.currentPrev = rejs['previous']
                this.currentNext = rejs['next']
            }, response => {
                console.log(response)
            })
        },
        handlePrev(current) {
            this.$http.get(this.currentPrev).then(response => {
                console.log(response)
                var rejs = response.body
                this.tableData = rejs['results']
                this.totalItem = rejs['count']
                this.currentPrev = rejs['previous']
                this.currentNext = rejs['next']
            }, response => {
                console.log(response)
            })
        },
        handleNext(current) {
            this.$http.get(this.currentNext).then(response => {
                console.log(response)
                var rejs = response.body
                this.tableData = rejs['results']
                this.totalItem = rejs['count']
                this.currentPrev = rejs['previous']
                this.currentNext = rejs['next']
            }, response => {
                console.log(response)
            })
        },
        handleIndexChange(current) {
            this.$http.get(this.baseUrl + '/api/ojproblem/myanswers'+'?page='+current).then(response => {
                console.log(response)
                var rejs = response.body
                this.tableData = rejs['results']
                this.totalItem = rejs['count']
                this.currentPrev = rejs['previous']
                this.currentNext = rejs['next']
            }, response => {
                console.log(response)
            })
        },
        handleClick(row) {
            this.$router.push({
                name : 'answerdetail', 
                params : 
                    {id : row.id}
            })
        },
        mapResultToString(result, runtime) {
            switch(result) {
                case 1:
                    return '答案错误'
                case 0:
                    return '答案正确'
            }
            switch(runtime) {
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
        mapResultToColor(result, runtime) {
            switch(result) {
                case 1:
                    return 'danger'
                case 0:
                    return 'success'
            }
            switch(runtime) {
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