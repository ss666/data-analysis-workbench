import axios from 'axios'
<template>
<div>

  <div class='right_top'>
   <el-button type="primary" round v-on:click="tologin">Sign in</el-button>
   <el-button type="primary" round >Sign up</el-button>
  </div>

  <div>
    <el-upload
    class="upload-demo"
    style="left:30px;position:absolute"
    action="http://127.0.0.1:8000/file_upload/"
    :on-preview="handlePreview"
    :on-remove="handleRemove"
    :before-remove="beforeRemove"
    multiple
    :limit="1"
    :on-exceed="handleExceed"
    :file-list="fileList">
    <el-button size="small" type="primary">UP LOAD</el-button>
    <div slot="tip" class="el-upload__tip" style='display:inline; margin-left:10px'>Pleas upload .csv file</div>
    </el-upload>
  </div>

  <div class='center_container'>
   <el-button style='color:#ffffff; background-color:#303133' round @click="visFormVisible = true" >Data Visualisation</el-button>
   <el-button style='color:#fff; background-color:#303133' round @click="abtestFormVisible = true" >AB test</el-button>
   <el-button style='color:#fff; background-color:#303133' round @click="didFormVisible = true" >DID test</el-button>
   <el-button style='color:#fff; background-color:#303133' round @click="ttestFormVisible = true" >T test</el-button>
   <el-button style='color:#fff; background-color:#303133' round @click="chitestFormVisible = true" >Chi-squared Test</el-button>
   <el-button style='color:#fff; background-color:#303133' round @click="ltFormVisible = true" >Life Time Prediction</el-button>
   <el-button style='color:#fff; background-color:#303133' round @click="matchingFormVisible = true" >Matching</el-button>
   <el-button style='color:#fff; background-color:#303133' round @click="cluFormVisible = true" >Clustering</el-button>
   <el-button style='color:#fff; background-color:#303133' round @click="claFormVisible = true" >Classification</el-button>
   <el-button round @click="testFormVisible = true" style="background-color:#2b4b6b;">TEST</el-button>
  </div>

<el-dialog title="Data Visualisation" :visible.sync="visFormVisible">
  <el-form :model="vis_config">
    <el-form-item label="type" :label-width="formLabelWidth">
      <el-select v-model="vis_config.type" placeholder="diagram type">
        <el-option label="line" value="line"></el-option>
        <el-option label="bar" value="bar"></el-option>
        <el-option label="pie" value="pie"></el-option>
      </el-select>
    </el-form-item>
  </el-form>
  <div slot="footer" class="dialog-footer">
    <el-button @click="visFormVisible = false">cancel</el-button>
    <el-button type="primary" @click="tovis">start</el-button>
  </div>
</el-dialog>

<el-dialog title="AB test" :visible.sync="abtestFormVisible">
  <el-form :model="ab_config">
    <el-form-item label="significance level" :label-width="formLabelWidth">
      <el-input v-model="ab_config.conf" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="columns for Chi-Squared Test" :label-width="formLabelWidth">
      <el-input v-model="ab_config.chi_squared_columns" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="digit" :label-width="formLabelWidth">
      <el-input v-model="ab_config.digit" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="segment on new/returning users">
     <el-switch v-model="ab_config.segment"></el-switch>
    </el-form-item>
  </el-form>
  <div slot="footer" class="dialog-footer">
    <el-button @click="abtestFormVisible = false">cancel</el-button>
    <el-button type="primary" @click="abtest_upload">start</el-button>
  </div>
</el-dialog>

<el-dialog title="Difference in Difference" :visible.sync="didFormVisible">
  <el-form :model="did_config">
    <el-form-item label="the response variable" :label-width="formLabelWidth">
      <el-input v-model="did_config.dv" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="time" :label-width="formLabelWidth">
      <el-input v-model="did_config.date" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="treatment columns" :label-width="formLabelWidth">
      <el-input v-model="did_config.treatment_col" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="id columns" :label-width="formLabelWidth">
      <el-input v-model="did_config.id_col" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="date columns" :label-width="formLabelWidth">
      <el-input v-model="did_config.date_col" autocomplete="off"></el-input>
    </el-form-item>
  </el-form>
  <div slot="footer" class="dialog-footer">
    <el-button @click="didFormVisible = false">cancel</el-button>
    <el-button type="primary" @click="did_upload">start</el-button>
  </div>
</el-dialog>

<el-dialog title="Student's t-test" :visible.sync="ttestFormVisible">
  <el-form :model="ttest_config">
  <el-form-item label="significance level" :label-width="formLabelWidth">
      <el-input v-model="ttest_config.conf" autocomplete="off"></el-input>
  </el-form-item>
  <el-form-item label="the test value for one sample t-test" :label-width="formLabelWidth">
      <el-input v-model="ttest_config.y" autocomplete="off"></el-input>
  </el-form-item>
  <el-form-item label="type" :label-width="formLabelWidth">
      <el-select v-model="ttest_config.mode" placeholder="types of t-test">
        <el-option label="one sample t-test" value="1"></el-option>
        <el-option label="unpaired t-test" value="2"></el-option>
        <el-option label="paired t-test" value="3"></el-option>
      </el-select>
  </el-form-item>
  </el-form>
  <div slot="footer" class="dialog-footer">
    <el-button @click="ttestFormVisible = false">cancel</el-button>
    <el-button type="primary" @click="ttest_upload">start</el-button>
  </div>
</el-dialog>

<el-dialog title="Life Time Prediction" :visible.sync="ltFormVisible">
  <el-form :model="lt_config">
    <el-form-item label="ARUP" :label-width="formLabelWidth">
        <el-input v-model="lt_config.arup" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="days" :label-width="formLabelWidth">
        <el-input v-model="lt_config.days" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="days pred" :label-width="formLabelWidth">
        <el-input v-model="lt_config.days_pred" autocomplete="off"></el-input>
    </el-form-item>
  </el-form>
  <div slot="footer" class="dialog-footer">
    <el-button @click="ltFormVisible = false">cancel</el-button>
    <el-button type="primary" @click="lt_upload">start</el-button>
  </div>
</el-dialog>

<el-dialog title="Matching" :visible.sync="matchingFormVisible">
   <el-tabs v-model="activeName" @tab-click="handleClick">
    <el-tab-pane label="PSM" name="second">
     <el-form :model="psm_config">
        <el-form-item label="model" :label-width="formLabelWidth">
          <el-select v-model="psm_config.model" placeholder="model type">
              <el-option label="Logistic Regression" value="LR"></el-option>
              <el-option label="Random Forest" value="line"></el-option>
              <el-option label="Light GBM" value="bar"></el-option>
              <el-option label="XGBoost" value="XGBoost"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="features" :label-width="formLabelWidth">
          <el-input v-model="psm_config.features" autocomplete="off"></el-input>
         </el-form-item>
        <el-form-item label="label" :label-width="formLabelWidth">
          <el-input v-model="psm_config.label" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="caliper" :label-width="formLabelWidth">
          <el-input v-model="psm_config.caliper" autocomplete="off"></el-input>
         </el-form-item>
        <el-form-item label="top" :label-width="formLabelWidth">
          <el-input v-model="psm_config.top" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <el-button @click="matchingFormVisible = false">cancel</el-button>
      <el-button type="primary" @click="psm_upload">start</el-button>
  </el-tab-pane>
  <el-tab-pane label="CEM" name="first">
      <el-form :model="cem_config">
      <el-form-item label="first feature column" :label-width="formLabelWidth">
          <el-input v-model="cem_config.first_feature" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="last feature column" :label-width="formLabelWidth">
        <el-input v-model="cem_config.last_feature" autocomplete="off"></el-input>
      </el-form-item>
      </el-form>
      <!-- <div slot="footer" class="dialog-footer"> -->
        <el-button @click="matchingFormVisible = false">cancel</el-button>
         <el-button type="primary" @click="cem_upload">start</el-button>
  </el-tab-pane>
  </el-tabs>
</el-dialog>

<el-dialog title="Clustering" :visible.sync="cluFormVisible">
  <el-form :model="clu_config">
  <el-form-item label="model" :label-width="formLabelWidth">
      <el-select v-model="clu_config.model" placeholder="model">
        <el-option label="k means" value="kmeans"></el-option>
      </el-select>
  </el-form-item>
  <el-form-item label="cluster" :label-width="formLabelWidth">
      <el-input v-model="cla_config.cluster" autocomplete="off"></el-input>
  </el-form-item>
  </el-form>
  <div slot="footer" class="dialog-footer">
    <el-button @click="cluFormVisible = false">cancel</el-button>
    <el-button type="primary" @click="clu_upload">start</el-button>
  </div>
</el-dialog>

<el-dialog title="Classification" :visible.sync="claFormVisible">
  <el-form :model="cla_config">
    <el-form-item label="model" :label-width="formLabelWidth">
        <el-select v-model="cla_config.model" placeholder="model">
          <el-option label="Support Vector Machine" value="svm"></el-option>
        </el-select>
    </el-form-item>
    <el-form-item label="the length of train dataset" :label-width="formLabelWidth">
        <el-input v-model="cla_config.length" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="kernel" :label-width="formLabelWidth">
        <el-input v-model="cla_config.kernel" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="number of neighbours" :label-width="formLabelWidth">
        <el-input v-model="cla_config.neighbors" autocomplete="off"></el-input>
    </el-form-item>
  </el-form>
  <div slot="footer" class="dialog-footer">
    <el-button @click="claFormVisible = false">cancel</el-button>
    <el-button type="primary" @click="cla_upload">start</el-button>
  </div>
</el-dialog>

</div>
</template>


<script>
export default{
//name: 'HelloWorld',
  data () {
    result:[];
    return {
       dialogTableVisible: false,
        visFormVisible:false,
        abtestFormVisible:false,
        didFormVisible: false,
        ttestFormVisible: false,
        chitestFormVisible: false,
        ltFormVisible: false,
        matchingFormVisible: false,
        cluFormVisible: false,
        claFormVisible: false,

        file_list:[],
        vis_config:{
          type:''
        },
        ab_config:{
          conf:'',
          chi_squared_columns:'',
          segment: false,
          digit:''},
        did_config:{
          treatment_col:'',
          id_col:'',
          date_col:'',
          dv:'',
          date:''},
        ttest_config:{
          conf:'',
          mode:''},
        lt_config:{
          arup:'',
          days:'',
          days_pred:''},
        cem_config:{
          first_feature:'',
          last_feature:''},
        psm_config:{
          features:'',
          model:'',
          label:'',
          caliper:'',
          top:''},
        clu_config:{
          model:'',
          cluster:''},
        cla_config:{
          model:'',
          length:'',
          kernel:'',
          neighbors:''},

        form: {
          name: '',
          region: '',
          date1: '',
          date2: '',
          delivery: false,
          type: [],
          resource: '',
          desc: ''
        },
    };
  },
  methods:{
  	tologin(){
  		this.$router.push('/login')
  	},

  	tovis(){
  	  this.visFormVisible = false;
			var that = this;
  	  this.$axios.get('http://127.0.0.1:8000/vis/').then(function(response){
  	      that.index = response.data.index;
  	      that.data = response.data.data;
  	    that.$router.push({
					name:'Vis',
					params:{
					  type: that.vis_config.type,
						index: that.index,
						data: that.data
					}
				});
  	  });
  	},

  	abtest_upload(){
      this.didFormVisible = false;
  	  var that = this;
  	  //console.log(that.ab_config.name);
  	  this.$axios.post('http://127.0.0.1:8000/abtest/', {
         data:{
         conf: that.ab_config.conf,
         age: that.ab_config.age
         },
         responseType: 'blob'
      })
      .then(res => {
            const blob = new Blob([res]);
            const fileName = 'abtest_result.xlsx';
            const elink = document.createElement('a');
            elink.download = fileName;
            elink.style.display = 'none';
            elink.href = URL.createObjectURL(blob);
            document.body.appendChild(elink);
            elink.click();
            URL.revokeObjectURL(elink.href);
            document.body.removeChild(elink);
       })
      .catch(function (error) {
          console.log('ERROR');
      });
    	},

    did_upload(){
      this.didFormVisible = false;
  	  var that = this;
  	  this.$axios.post('http://127.0.0.1:8000/did/', {
         treatment_col: that.did_config.treatment_col,
         id_col: that.did_config.id_col,
         date_col: that.did_config.date_col,
         dv: that.did_config.dv,
         date: that.did_config.treatment_date
      })
      .then(function (response) {
         //console.log(response);
         //that.msg = JSON.stringify(response);
         that.res= response.data.res;
         that.p_value=response.data.p_value;
         that.coef=response.data.coef;
  	     that.$router.push({
					 name:'Result',
					 params:{
					 res:that.res,
					 p_value:that.p_values,
					 coef:that.coef
					 }
					});
      })
      .catch(function (error) {
          console.log('ERROR');
      });
    	},

  	ttest_upload(){
      this.ttestFormVisible = false;
  	  var that = this;
  	  this.$axios.post('http://127.0.0.1:8000/test/', {
         mode: that.ttest_config.mode,
         conf: that.ttest_config.conf,
         y: that.ttest_config.y
      })
      .then(function (response) {
         //console.log(response);
         //that.msg = JSON.stringify(response);
         that.res= response.data.res;
         that.p_value=response.data.p_value;
  	     that.$router.push({
					 name:'Result',
					 params:{
					 res:that.res,
					 p_value:that.p_values
					 }
					});
      })
      .catch(function (error) {
          console.log('ERROR');
      });
    	},

  	chitest_upload(){
      this.chitestFormVisible = false;
  	  var that = this;
  	  this.$axios.get('http://127.0.0.1:8000/chitest/').then(function(response){
  	    that.msg = response.data; //JSON.stringify(response);
  	    that.$router.push({
					 name:'Result',
					 params:{
					 res:that.res,
					 p_value:that.p_values
					 }
					});
      })
      .catch(function (error) {
          console.log('ERROR');
      });
    	},

  	lt_upload(){
      this.ltFormVisible = false;
  	  var that = this;
  	  this.$axios.post('http://127.0.0.1:8000/lt/', {
  	     arup: that.lt_config.arup,
         days: that.lt_config.days,
         pred_days: that.lt_config.pred_days
      })
      .then(function (response) {
  	     that.$router.push({
					 name:'ResultLt',
					 params:{
					 mses: that.mse,
					 x: that.x,
					 y: that.y,
					 y_pred: that.y_pred,
					 ltv: that.ltv
					 }
					});
      })
      .catch(function (error) {
          console.log('ERROR');
      });
    	},

     cem_upload(){
      this.cemFormVisible = false;
  	  var that = this;
  	  this.$axios.post('http://127.0.0.1:8000/cem/', {
         first_feature: that.cem_config.first_feature,
         last_feature: that.cem_config.last_feature
      })
      .then(function (response) {
  	     that.$router.push({
					 name:'Result',
					 params:{
					 res:'cem_undefined'
					 }
					});
      })
      .catch(function (error) {
          console.log('ERROR');
      });
    	},

    psm_upload(){
      this.psmFormVisible = false;
  	  var that = this;
  	  this.$axios.post('http://127.0.0.1:8000/psm/', {
         features: that.psm_config.features,
         model: that.psm_config.model,
         label: that.psm_config.label,
         caliper: that.psm_config.caliper,
         top: that.psm_config.top,
      })
      .then(function (response) {
  	     that.$router.push({
					 name:'Result',
					 params:{
					 res:'psm_undefined'
					 }
					});
      })
      .catch(function (error) {
          console.log('ERROR');
      });
    	},

  	clu_upload(){
      this.didFormVisible = false;
  	  var that = this;
  	  this.$axios.post('http://127.0.0.1:8000/ml/', {
         data:{
  	     ml_type: 'clu',
         model: that.cla_config.model,
         cluster: that.cla_config.cluster
         },
         responseType: 'blob'
      })
      .then(res => {
            const blob = new Blob([res]);
            const fileName = 'clustering_result.xlsx';
            const elink = document.createElement('a');
            elink.download = fileName;
            elink.style.display = 'none';
            elink.href = URL.createObjectURL(blob);
            document.body.appendChild(elink);
            elink.click();
            URL.revokeObjectURL(elink.href); // 释放URL 对象
            document.body.removeChild(elink);
       })
      .catch(function (error) {
          console.log('ERROR');
      });
    	},

  	cla_upload(){
      this.didFormVisible = false;
  	  var that = this;
  	  this.$axios.post('http://127.0.0.1:8000/ml/', {
         data:{
  	     ml_type: 'cla',
         model: that.cla_config.model,
         length: that.cla_config.length,
         kernel: that.cla_config.kernel,
         neighbors: that.cla_config.neighbors,
         },
         responseType: 'blob'
      })
      .then(res => {
            const blob = new Blob([res]);
            const fileName = 'classification_result.xlsx';
            const elink = document.createElement('a');
            elink.download = fileName;
            elink.style.display = 'none';
            elink.href = URL.createObjectURL(blob);
            document.body.appendChild(elink);
            elink.click();
            URL.revokeObjectURL(elink.href);
            document.body.removeChild(elink);
       })
      .catch(function (error) {
          console.log('ERROR');
      });
    	},

 }
};

</script>

<style lang="less" scoped>
.right_top{
    position: absolute;
    top: 20px;
    right: 30px;
}

.center_container{
    position: absolute;
    left: 50%;
    top: 58%;
    transform: translate(-50%,-50%);

    display: grid;
    grid-template-columns: 300px 300px 300px;
    grid-template-rows: 200px 200px 200px;
    grid-row-gap: 20px;
    grid-column-gap: 20px;
}

.test{
  background-color:#2b4b6b;
  width:300px;
  height:200px;
}
</style>
