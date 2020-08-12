<template>
 <div class='login_container'>
    <div class='login_box'>
       <el-form label-width="80px">
          <el-form-item label="Username" style='width:300px;;margin-left:30px;margin-top:20px;'>
            <el-input></el-input>
          </el-form-item>

          <el-form-item label="Password" style='width:300px;margin-left:30px'>
            <el-input></el-input>
          </el-form-item>

        <el-button type="success">Sign in</el-button>
        </el-form>
    </div>
 </div>
</template>

<script>
export default{};
</script>

<style lang='less' scoped>
  .login_container{}
  .login_box{
    width:400px;
    height:200px;
    background-color:;
    position:absolute;
    left:50%;
    top:50%;
    transform:translate(-50%,-50%);
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  }
</style>
