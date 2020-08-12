<template>
 <div>
 <p>{{ msg }} </p>
 </div>
</template>

<script>
export default{
data () {
      return {
        msg: ''
      }
        },
mounted: function () {
          this.msg = this.$route.params
        }

};
</script>

<style lang='less' scoped>
</style>
