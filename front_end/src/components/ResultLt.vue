<template>
 <div>
 <div id="container" style="width: 600px;height:400px;"></div>
 </div>
</template>


<script type="text/javascript">
import echarts from "echarts";
export default {
  name: "App",
  data() {
    return {
      mse:'',
      x:[],
      y:[],
      y_pred:[],
      ltv
    };
  },
  methods: {
  },
  mounted() {
    this.$nextTick(function() {
      this.mse = this.$route.params.mse;
      this.x = this.$route.params.x;
      this.y = this.$route.params.y;
      this.y_pred = this.$route.params.y_pred;
      this.ltv = this.$route.params.ltv;
      var myChart = echarts.init(document.getElementById("container"));
      myChart.setOption({        //加载数据图表
        title: {
          text: "Life Time"
        },
        tooltip:{
          trigger:'axis'
        },
        legend:{
          data:['real','true']
        },
        xAxis: {
          data: this.index
        },
        yAxis: {},
        series: [
          {
            name: "prediction",
            data: this.y_pred,
            type: 'line',
            smooth:true,
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
<style>
</style>
