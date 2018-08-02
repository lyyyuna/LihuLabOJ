<template>
    <div>
        <el-row :gutter="20">
            <el-col :span="18" :offset="3" >
                <el-card shadow="hover">
                    <div class="lyyfont lyycentre" >{{title}}</div>
                    <pre>{{content}}</pre>
                    <p class="lyysamplesection">输入示例</p>
                    <el-row class="lyyresultbox" :gutter="20">
                        <el-col :span="16" :offset="3">
                            <pre class="lyysample">{{input1}}</pre>
                        </el-col>
                    </el-row>
                    <p class="lyysamplesection">输出示例</p>
                    <el-row class="lyyresultbox" :gutter="20">
                        <el-col :span="16" :offset="3">
                            <pre class="lyysample">{{output1}}</pre>
                        </el-col>
                    </el-row>
                    <el-row class="lyyresultbox" :gutter="20">
                        <el-col :span="20" :offset="2">
                            <el-input
                            v-show="login"
                            type="textarea"
                            :autosize="{ minRows: 10}"
                            placeholder="请输入答案（目前只支持 Python 3.5）"
                            v-model="sourceCode">
                            </el-input>
                        </el-col>
                    </el-row>
                    <el-row class="lyyresultbox" :gutter="20">
                        <el-col :span="20" :offset="2">
                            <el-button 
                                v-show="login"
                                class="lyyinput"
                                type="danger" 
                                @click="trySubmitAnswer()">提交答案
                            </el-button>
                        </el-col>
                    </el-row>

                    <el-collapse>
                    <el-collapse-item title="点击查看本题全站排名" name="2">
                        <el-table
                        stripe
                        class="lyybox"
                        :data="answerRankData"
                        border
                        style="width: 100%">
                        <el-table-column
                        prop="username"
                        label="用户名">
                        </el-table-column>
                        <el-table-column
                        prop="cpu"
                        label="CPU">
                            <template slot-scope="scope">
                                <el-tag
                                :type="'info'"
                                disable-transitions>{{mapCPUToString(scope.row.cpu)}}</el-tag>
                            </template>
                        </el-table-column>
                        <el-table-column
                        prop="memory"
                        label="占用内存">
                            <template slot-scope="scope">
                                <el-tag
                                :type="'info'"
                                disable-transitions>{{mapMemoryToString(scope.row.memory)}}</el-tag>
                            </template>
                        </el-table-column>
                    </el-table>
                    </el-collapse-item>

                    <el-collapse-item title="点击查看本人本题答题情况" name="1" v-show="login">
                    <el-table
                        stripe
                        class="lyybox"
                        :data="answerForThisData"
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
                    </el-collapse-item>
                    </el-collapse>
               </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>
import Cookies from 'js-cookie';

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
            title : '',
            content : '',
            input1 : '',
            output1 : '',
            sourceCode : '',
            answerRankData : [],
            answerForThisData : [],
            totalItem: 1,
            currentPrev: '',
            currentNext: ''
        }
    },
    created() {
        this.getProblemDetail()
        this.getProblemRank()
        this.getMyRecentAnswers()
    },
    methods : {
        trySubmitAnswer() {
            // cannot be blank
            if (this.sourceCode == '') {
                this.$message({
                showClose: true,
                message: '答案不能为空',
                type: 'warning',
                duration:2000
                }); 
                return;
            }
            if (this.sourceCode.length > 2048) {
                this.$message({
                showClose: true,
                message: '源码长度不能超过2048',
                type: 'warning',
                duration:2000
                }); 
                return;
            }
            var problemId = this.$route.params.id
            var csrftoken = Cookies.get('csrftoken');
            this.$http.post(this.baseUrl + '/api/ojproblem/'+problemId+'/submit', 
                {source_code : this.sourceCode}, 
                {headers: {"X-CSRFToken":csrftoken }}
            ).then(response => {
                console.log(response)
                var rejs = response.body
                var code = rejs['code']
                var data = rejs['data']
                if (code == 0) {
                    this.$message({
                    showClose: true,
                    message: '提交成功，刷新后在下方查看本人本题答题情况',
                    type: 'success',
                    duration:2000
                    });
                    return
                }
                if (code == 1) {
                    if (data == 'submit too fast') {
                        this.$message({
                        showClose: true,
                        message: '提交过于频繁，请过10s再提交',
                        type: 'warning',
                        duration:2000
                        });    
                        return   
                    }
                    if (data == 'input invalid') {
                        this.$message({
                        showClose: true,
                        message: '输入不符合要求',
                        type: 'warning',
                        duration:2000
                        });    
                        return   
                    }
                }
            }, response => {
                console.log(response)
            })
        },
        getProblemDetail() {
            var problemId = this.$route.params.id
            this.$http.get(this.baseUrl + '/api/ojproblem/'+problemId+'/detail').then(response => {
                console.log(response)
                var rejs  = response.body
                this.title = rejs['data']['title']
                this.content = rejs['data']['content']
                this.input1 = rejs['data']['input1']
                this.output1 = rejs['data']['output1']
            },response => {
                console.log(response)
            })
        },
        getProblemRank() {
            var problemId = this.$route.params.id
            this.$http.get(this.baseUrl + '/api/ojproblem/'+problemId+'/ranks').then(response => {
                console.log(response)
                var rejs  = response.body
                this.answerRankData = rejs['results']
                console.log(this.answerRankData)
            }, response => {
                console.log(response)
            })
        },
        mapCPUToString(cpu) {
            return cpu + ' ms'
        },
        mapMemoryToString(memory) {
            return memory/1024 + ' kB'
        },

        getMyRecentAnswers() {
            var problemId = this.$route.params.id

            this.$http.get(this.baseUrl + '/api/ojproblem/'+problemId+'/myanswers').then(response => {
                console.log(response)
                var rejs = response.body
                this.answerForThisData = rejs['results']
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
            var problemId = this.$route.params.id

            this.$http.get(this.baseUrl + '/api/ojproblem/'+problemId+'/myanswers'+'?page='+current).then(response => {
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
.lyysamplesection {
    color : #409EFF;
}
.lyysample {
    border-left-width: 5px;
    border-left-style: solid;
    border-left-color: #409EFF;
}
</style>