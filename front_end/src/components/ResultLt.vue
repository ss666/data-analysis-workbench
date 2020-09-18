<template>
 <div><center>
 <el-table
      :data="tableData"
      style="width: 100%">
      <el-table-column
        prop="name"
        label="number of customers / period"
        width="300">
      </el-table-column>
      <el-table-column
        prop="data"
        label="total lifetime value($)"
        width="300">
      </el-table-column>
 </el-table>
 <div id="container" style="margin-top:30px;width:600px;height:400px;"></div>
 </center>
 </div>
</template>


<script type="text/javascript">
import echarts from "echarts";
export default {
  name: "App",
  data() {
    return {
      mse:'aeas',
      x:[],
      y:[],
      y_pred:[],
      tableData: [],
    };
  },
  methods: {
  },
  mounted() {
    this.$nextTick(function() {
      this.tableData = this.$route.params.tableData;
      this.x = this.$route.params.x;
      this.y = this.$route.params.y;
      this.y_pred = this.$route.params.y_pred;
      //this.ltv = this.$route.params.ltv;
      var myChart = echarts.init(document.getElementById("container"));
      myChart.setOption({
        title: {
          text: "Customers Retained"
        },
        tooltip:{formatter:function(datas) {
                    return datas.value.toFixed(0);
                }},
        legend:{
          data:['real','prediction']
        },
        xAxis: {
          data: this.x
        },
        yAxis: {},
        series: [
          {
            name: "prediction",
            data: this.y_pred,
            type: 'line',
            smooth:true,
            color:'#845B83',
          },
          {
            name: "real",
            data: this.y,
            type: 'line',
            smooth:true,
          },
        ]
       });
     myChart.setOption(this.option);

    });
  }
};
</script>
<style lang='less' scoped>
</style>
