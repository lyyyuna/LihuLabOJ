<template>
    <div>
    <div>
        <el-row :gutter="20">
            <el-col :span="18" :offset="3" >
                <el-card shadow="hover">
                    <el-table
                        stripe
                        class="lyybox"
                        :data="tableData"
                        border
                        style="width: 100%">
                        <el-table-column
                        prop="id"
                        label="题目编号">
                            <template slot-scope="scope">
                                {{scope.row.id}}   
                                <el-button size="mini" type="success" icon="el-icon-check" circle v-show="mapPassToFlag(scope.row.is_passed)"></el-button>
                            </template>
                        </el-table-column>
                        <el-table-column
                        prop="title"
                        label="标题">
                        </el-table-column>
                        <el-table-column
                        prop="pass_num"
                        label="通过提交数">
                        </el-table-column>
                        <el-table-column
                        prop="total_num"
                        label="总提交数">
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
        this.getUserRanks()
    },
    methods : {
        getUserRanks() {
            this.$http.get(this.baseUrl + '/api/ojproblem/all').then(response => {
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
            this.$http.get(this.baseUrl + '/api/ojproblem/all'+'?page='+current).then(response => {
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
        mapPassToFlag(ispass) {
            if (ispass == 'pass') {
                return true
            }
            return false
        },
        handleClick(row) {
            this.$router.push({
                name : 'problemdetail', 
                params : 
                    {id : row.id}
            })
        },
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