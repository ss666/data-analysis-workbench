<template>
 <div>
<center>
 <el-table
      :data="tableData"
      style="width: 100%">
      <el-table-column
        prop="name"
        label="name"
        width="300">
      </el-table-column>
      <el-table-column
        prop="data"
        label="value"
        width="300">
      </el-table-column>
 </el-table>
</center>
<p style='margin-top: 50px;'><font size="6" color='#845B83' font family='Helvetica Neue' style='font-weight:bolder;font-style:italic;'>Metis</font></p>
 </div>
</template>

<script>
export default{
data () {
      return {
        msg: ''
      ,
      tableData: [{
            date: '2016-05-02',
            name: '王小虎',
            address: '上海市普陀区金沙江路 1518 弄'
          }, {
            date: '2016-05-04',
            name: '王小虎',
            address: '上海市普陀区金沙江路 1517 弄'
          }, {
            date: '2016-05-01',
            name: '王小虎',
            address: '上海市普陀区金沙江路 1519 弄'
          }, {
            date: '2016-05-03',
            name: '王小虎',
            address: '上海市普陀区金沙江路 1516 弄'
      }]
      }
        },
mounted: function () {
          this.tableData = this.$route.params.tableData
        }

};
</script>

<style lang='less' scoped>
</style>
