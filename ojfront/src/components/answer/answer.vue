<template>
    <div>
        <el-row :gutter="20">
            <el-col :span="18" :offset="3" >
                <el-card shadow="hover">
                    <el-steps :active="activeIndex" align-center finish-status="success">
                    <el-step title="等待分析" :description="time1"></el-step>
                    <el-step title="开始分析" :description="time2"></el-step>
                    <el-step title="结束分析" :description="time3"></el-step>
                    </el-steps>
                    <el-row class="lyyresultbox" :gutter="20">
                        <el-col :span="4" :offset="3">结果</el-col>
                        <el-col :span="16">
                            <el-tag
                                :type="mapResultToColor(result, runtime)"
                                disable-transitions>{{mapResultToString(result, runtime)}}
                            </el-tag>
                        </el-col>
                    </el-row>
                    <el-row class="lyyresultbox" :gutter="20">
                        <el-col :span="4" :offset="3">CPU</el-col>
                        <el-col :span="16">
                            <el-tag
                                :type="'info'"
                                disable-transitions>{{cpu}}
                            </el-tag>
                        </el-col>
                    </el-row>
                    <el-row class="lyyresultbox" :gutter="20">
                        <el-col :span="4" :offset="3">内存</el-col>
                        <el-col :span="16">
                            <el-tag
                                :type="'info'"
                                disable-transitions>{{memory}}
                            </el-tag>
                        </el-col>
                    </el-row>
                    <el-row class="lyyresultbox" :gutter="20">
                        <el-col :span="4" :offset="3">                                
                            <el-button @click="handleClick()">查看题目链接</el-button>
                        </el-col>
                    </el-row>
                    <el-row class="lyyresultbox" :gutter="20">
                        <el-col :span="4" :offset="3">源码</el-col>
                    </el-row>

                    <el-row class="lyyresultbox" :gutter="20">
                        <el-col :span="20" :offset="2">
                            <pre v-highlightjs="sourceCode"><code class="python"></code></pre>
                        </el-col>
                    </el-row>
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
            time1 : '',
            time2 : '',
            time3 : '',
            activeIndex : 1,
            result : -10,
            runtime : -10,
            cpu : '-1 ms',
            memory : '-1 kB',
            sourceCode : '',
            problemId : '',
        }
    },
    created() {
        this.getAnswerDetail()
    },
    methods : {
        getAnswerDetail() {
            var answerId = this.$route.params.id
            this.$http.get(this.baseUrl + '/api/ojproblem/answer/'+answerId+'/detail').then(response => {
                console.log(response)
                var rejs = response.body
                this.time1 = rejs['data']['create_time']
                var status = rejs['data']['status']
                this.result = rejs['data']['result']
                this.runtime = rejs['data']['runtime']
                this.problemId = rejs['data']['problem']
                if (rejs['data']['cpu']!=-1) {
                    this.cpu = rejs['data']['cpu'] + ' ms'
                    this.memory = (rejs['data']['memory']/1024) + ' kB'
                }
                this.sourceCode = rejs['data']['source_code']

                switch (status) {
                    case 'pending':
                        this.activeIndex = 1
                        this.time2 = ''
                        this.time3 = ''
                        break
                    case 'started':
                        this.activeIndex = 2
                        this.time2 = rejs['data']['update_time']
                        this.time3 = ''
                        break
                    default: // failed and finished
                        this.activeIndex = 3
                        this.time3 = rejs['data']['update_time']
                        this.time2 = ''
                        break
                }

            }, response => {
                console.log(response)
            });        
        },
        handleClick() {
            this.$router.push({
                name : 'problemdetail', 
                params : 
                    {id : this.problemId}
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
.lyyresultbox {
    margin-top: 20px;
}
@import '//cdn.bootcss.com/highlight.js/9.12.0/styles/default.min.css'
</style>