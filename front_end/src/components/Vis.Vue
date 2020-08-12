<template>
 <div>
 <div id="main" class='center_container'></div>
 </div>
</template>


<script type="text/javascript">
import echarts from "echarts";
export default {
  name: "App",
  data() {
    return {
     type:'',
     index:[],
     data:[]
    };
  },
  methods: {
  },
  mounted() {
    this.$nextTick(function() {
      this.type = this.$route.params.type;
      this.index = this.$route.params.index;
      this.data = this.$route.params.data;
      var myChart = echarts.init(document.getElementById("main"));
      myChart.setOption({        //加载数据图表
        title: {
          text: "title"
        },
        tooltip: {},
        //legend: {
        //  data: ["销量"]
        //},
        xAxis: {
          data: this.index
        },
        yAxis: {},
        series: [
          {
            name: "销量",
            type: this.type,
            data: this.data
          }
        ]
       });
     myChart.setOption(this.option);
    });
  }
};
</script>
<style lang="less" scoped>
.center_container{
    position: absolute;
    left: 50%;
    top: 58%;
    transform: translate(-50%,-50%);
    width: 800px;
    height: 600px;
}
</style>
