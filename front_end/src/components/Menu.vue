import axios from 'axios'
<template>
<div style="margin-top:0px">
  <div class='top_container'>
  <div class='word'>
  <p><font size="50" color='#845B83' font family='Helvetica Neue' style='font-weight:bolder;font-style:italic;'>Metis</font></p>
  </div>

  <div class='right_top'>
   <el-button style='color:#ffffff; background-color:#20749e'  round >Tutorial</el-button>
   <el-button style='color:#ffffff; background-color:#49b4ea'  round v-on:click="tologin">Sign in</el-button>
   <el-button style='color:#ffffff; background-color:#49b4ea'  round >Sign up</el-button>
  </div>

  <div class='upload'>
    <el-upload
    class="upload-demo"
    action="http://127.0.0.1:8000/file_upload/"
    :on-preview="handlePreview"
    :on-remove="handleRemove"
    :before-remove="beforeRemove"
    multiple
    :limit="1"
    :on-exceed="handleExceed"
    :file-list="fileList">
    <el-button size="small" style='color:#ffffff; background-color:#49b4ea'>UP LOAD</el-button>
    <div slot="tip" class="el-upload__tip" style='display:inline; margin-left:10px'>Pleas upload .csv file</div>
    </el-upload>
  </div>
  </div>

  <div class='center_container'>
   <el-button style='color:#ffffff; background-color:#845B83' round @click="visFormVisible = true" ><font class='button_font'>Data Visualisation</font></el-button>
   <el-button style='color:#fff; background-color:#845B83' round @click="abtestFormVisible = true" ><font class='button_font'>AB test</font></el-button>
   <el-button style='color:#fff; background-color:#845B83' round @click="didFormVisible = true" ><font class='button_font'>DID test</font></el-button>
   <el-button style='color:#fff; background-color:#845B83' round @click="ttestFormVisible = true" ><font class='button_font'>T test</font></el-button>
   <el-button style='color:#fff; background-color:#845B83' round @click="chitestFormVisible = true" ><font class='button_font'>Chi-squared Test</font></el-button>
   <el-button style='color:#fff; background-color:#845B83' round @click="ltFormVisible = true" ><font class='button_font'>Life Time Prediction</font></el-button>
   <el-button style='color:#fff; background-color:#845B83' round @click="matchingFormVisible = true" ><font class='button_font'>Matching</font></el-button>
   <el-button style='color:#fff; background-color:#845B83' round @click="cluFormVisible = true" ><font class='button_font'>Clustering</font></el-button>
   <el-button style='color:#fff; background-color:#845B83' round @click="claFormVisible = true" ><font class='button_font'>Classification</font></el-button>
   <el-button round @click="tores" style="background-color:#2b4b6b;">TEST</el-button>
  </div>

<el-dialog title="Data Visualisation" :visible.sync="visFormVisible">
  <el-form :model="vis_config">
    <el-form-item label="type" :label-width="formLabelWidth">
      <el-select v-model="vis_config.type" placeholder="diagram type">
        <el-option label="line" value="line"></el-option>
        <el-option label="bar" value="bar"></el-option>
        <el-option label="pie" value="pie"></el-option>
        <el-option label="scatter" value="scatter"></el-option>
      </el-select>
    </el-form-item>
  </el-form>
  <div slot="footer" class="dialog-footer">
    <el-button @click="visFormVisible = false">cancel</el-button>
    <el-button type="primary" @click="tovis">start</el-button>
  </div>
</el-dialog>

<el-dialog title="A/B test" :visible.sync="abtestFormVisible">
  <el-form :model="ab_config">
    <el-form-item label="significance level (alpha)" :label-width="formLabelWidth">
      <el-input v-model="ab_config.conf" placeholder='decimal required (default:0.05)' autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="columns for Chi-Squared Test" :label-width="formLabelWidth">
      <el-input v-model="ab_config.chi_squared_columns" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="decimal places" :label-width="formLabelWidth">
      <el-input v-model="ab_config.digit" placeholder='integer required (default:2)' autocomplete="off"></el-input>
    </el-form-item>
   <!-- <el-form-item label="segment on new/returning users">
     <el-switch v-model="ab_config.segment"></el-switch>
    </el-form-item> -->
  </el-form>
  <div slot="footer" class="dialog-footer">
    <el-button @click="abtestFormVisible = false">cancel</el-button>
    <el-button type="primary" @click="abtest_upload">start</el-button>
  </div>
</el-dialog>

<el-dialog title="Difference in Difference" :visible.sync="didFormVisible">
  <el-form :model="did_config">
      <el-form-item label="treatment column" :label-width="formLabelWidth">
      <el-input v-model="did_config.treatment_col" style="width: 100%;" placeholder='column to distinguish between treatment group and control group (default: treatment)' autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="id column" :label-width="formLabelWidth">
      <el-input v-model="did_config.id_col" placeholder='(default: id)' autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="date column" :label-width="formLabelWidth">
      <el-input v-model="did_config.date_col" placeholder='(default: date)' autocomplete="off"></el-input>
    </el-form-item>
  <el-form-item label="significance level (alpha)" :label-width="formLabelWidth">
      <el-input v-model="did_config.alpha" placeholder='decimal required (default:0.05)' autocomplete="off"></el-input>
  </el-form-item>
    <el-form-item label="outcome " :label-width="formLabelWidth">
      <el-input v-model="did_config.dv" placeholder='column name of the response variable' autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="time point" :label-width="formLabelWidth">
      <el-input v-model="did_config.treatment_date" autocomplete="off"></el-input>
    </el-form-item>
  </el-form>
  <div slot="footer" class="dialog-footer">
    <el-button @click="didFormVisible = false">cancel</el-button>
    <el-button type="primary" @click="did_upload">start</el-button>
  </div>
</el-dialog>

<el-dialog title="Student's t-test" :visible.sync="ttestFormVisible">
  <el-form :model="ttest_config">
  <el-form-item label="significance level (alpha)" :label-width="formLabelWidth">
      <el-input v-model="ttest_config.conf" placeholder='decimal required (default:0.05)' autocomplete="off"></el-input>
  </el-form-item>
  <el-form-item label="test value" :label-width="formLabelWidth">
      <el-input v-model="ttest_config.y" placeholder='required for one sample t-test' autocomplete="off"></el-input>
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

<el-dialog title="Chi-Squared Test" :visible.sync="chitestFormVisible">
  <el-form :model="ttest_config">
  <el-form-item label="significance level (alpha)" :label-width="formLabelWidth">
      <el-input v-model="chitest_config.alpha" placeholder='decimal required (default:0.05)' autocomplete="off"></el-input>
  </el-form-item>
  </el-form>
  <div slot="footer" class="dialog-footer">
    <el-button @click="chitestFormVisible = false">cancel</el-button>
    <el-button type="primary" @click="chitest_upload">start</el-button>
  </div>
</el-dialog>

<el-dialog title="Life Time Prediction" :visible.sync="ltFormVisible">
  <el-form :model="lt_config">
    <el-form-item label="ARPU ($)" :label-width="formLabelWidth">
        <el-input v-model="lt_config.arup" placeholder="e.g.: 1.00" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="train days" :label-width="formLabelWidth">
        <el-input v-model="lt_config.days" placeholder="e.g.: 20 (if you want to predict LTV using retention in 20 days)" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="pred. days " :label-width="formLabelWidth">
        <el-input v-model="lt_config.pred_days" placeholder="e.g.: 100 (if you want to predict LTV in the future 100 days) "autocomplete="off"></el-input>
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
              <el-option label="Logistic Regression (popular method)" value="LR"></el-option>
              <el-option label="Random Forest" value="line"></el-option>
              <el-option label="Light GBM" value="bar"></el-option>
              <el-option label="XGBoost" value="XGBoost"></el-option>
          </el-select>
          </el-form-item>
        <el-form-item label="treatment column" :label-width="formLabelWidth">
          <el-input v-model="psm_config.treatment_col" placeholder='column to distinguish between treatment group and control group' autocomplete="off"></el-input>
          </el-form-item>
        <el-form-item label="id column" :label-width="formLabelWidth">
          <el-input v-model="psm_config.id_col" placeholder='(default: id)' autocomplete="off"></el-input>
          </el-form-item>
        <el-form-item label="indices of features" :label-width="formLabelWidth">
          <el-input v-model="psm_config.features"  placeholder="observed baseline variables (for example: 2:9)" autocomplete="off"></el-input>
         </el-form-item>
        <el-form-item label="label" :label-width="formLabelWidth">
          <el-input v-model="psm_config.label"  placeholder="outcome or specific variable related to treatment participation" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="caliper" :label-width="formLabelWidth">
          <el-input v-model="psm_config.caliper" placeholder="a maximum allowable distance between propensity scores (default: 0.05)" autocomplete="off"></el-input>
         </el-form-item>
       <!-- <el-form-item label="top" :label-width="formLabelWidth">
          <el-input v-model="psm_config.top"  autocomplete="off"></el-input>
        </el-form-item> -->
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
      <el-input v-model="cla_config.cluster" placeholder='the number of clusters to form' autocomplete="off"></el-input>
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
          <el-option label="K-nearest Neighbors" value="knn"></el-option>
        </el-select>
    </el-form-item>
    <el-form-item label="the length of train dataset" :label-width="formLabelWidth">
        <el-input v-model="cla_config.length" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="kernel" :label-width="formLabelWidth">
         <el-select v-model="cla_config.kernel" placeholder="required for SVM">
          <el-option label="linear" value="linear"></el-option>
          <el-option label="radial basis function" value="rbf"></el-option>
          <el-option label="sigmoid" value="sigmoid"></el-option>
        </el-select>
    </el-form-item>
    <el-form-item label="number of neighbours" :label-width="formLabelWidth">
        <el-input v-model="cla_config.neighbors"  placeholder="required for KNN" autocomplete="off"></el-input>
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
          treatment_date:'',
          alpha:''},
        ttest_config:{
          conf:'',
          y:'',
          mode:''},
        chitest_config:{
          alpha:''},
        lt_config:{
          arup:'',
          days:'',
          pred_days:''},
        cem_config:{
          first_feature:'',
          last_feature:''},
        psm_config:{
          treatment_col:'',
          id_col:'',
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
  	  var arr = that.ab_config.chi_squared_columns.split(',');
  	  this.$axios.post('http://127.0.0.1:8000/abtest/', {
         conf: that.ab_config.conf,
         chi_squared_columns: arr,
         digit: that.ab_config.digit
      })
      .then(res => {
            const fileName = 'abtest_result.csv';
            const elink = document.createElement('a');
            elink.download = fileName;
            elink.style.display = 'none';
            elink.href = "../../static/abtest_result.csv";
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
         date: that.did_config.treatment_date,
         alpha: that.did_config.alpha,
      })
      .then(function (response) {
         that.res= response.data.res;
         that.p_value=response.data.p_value;
         that.effect=response.data.effect;
  	     that.$router.push({
					 name:'Result',
					 params:{
					 tableData: [{
					  name: 'confidence level',
            data: "95%"
            },{
					  },{
            name: 'result',
            data: that.res
            }, {
            name: 'p-value',
            data: that.p_value,
            }, {
            name: 'effect',
            data: that.effect,
            }]
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
  	  this.$axios.post('http://127.0.0.1:8000/ttest/', {
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
					 tableData: [{
					  name:'hypothesized population mean',
					  data: that.ttest_config.y
					  },{
            name: 'confidence level',
            data: (1-that.ttest_config.conf)*100+"%"
            },{
					  },{
            name: 'result',
            data: that.res
            }, {
            name: 'p-value',
            data: that.p_value,
            }]
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
  	  this.$axios.post('http://127.0.0.1:8000/chitest/', {
         alpha: that.chitest_config.alpha,
      })
      .then(function(response){
  	    that.msg = response.data; //JSON.stringify(response);
  	    that.$router.push({
					 name:'Result',
					 params:{
					 tableData: [{
            name: 'result',
            data: that.res
          }, {
            name: 'p value',
            data: that.p_values,
          }]
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
					 name:'ResultLt', //ResultLt
					 params:{
					 x: response.data.x,
					 y:  response.data.y,
					 y_pred: response.data.y_pred,
					 tableData: [{
            name: response.data.base_cnt+' / '+response.data.pred_days+'(days)',
            data: response.data.ltv.toFixed(2)
            }]
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
  	     treatment_col: that.psm_config.treatment_col,
         id_col: that.psm_config.id_col,
         features: that.psm_config.features,
         model: that.psm_config.model,
         label: that.psm_config.label,
         caliper: that.psm_config.caliper,
         top: that.psm_config.top,
      })
      .then(res => {
            const fileName = 'matching_psm_result.csv';
            const elink = document.createElement('a');
            elink.download = fileName;
            elink.style.display = 'none';
            elink.href = "../../static/matching_psm_result.csv";
            document.body.appendChild(elink);
            elink.click();
            URL.revokeObjectURL(elink.href);
            document.body.removeChild(elink);
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
        // responseType: 'blob'
      })
      .then(res => {
            const fileName = 'clustering_result.csv';
            const elink = document.createElement('a');
            elink.download = fileName;
            elink.style.display = 'none';
            elink.href = "../../static/clustering_result.csv";
            document.body.appendChild(elink);
            elink.click();
            URL.revokeObjectURL(elink.href);
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
  	     ml_type: 'cla',
         model: that.cla_config.model,
         length: that.cla_config.length,
         kernel: that.cla_config.kernel,
         neighbors: that.cla_config.neighbors
         //responseType: 'blob'
      })
      .then(res => {
            const fileName = 'classification_result.csv';
            const elink = document.createElement('a');
            elink.download = fileName;
            elink.style.display = 'none';
            elink.href = "../../static/classification_result.csv";
            document.body.appendChild(elink);
            elink.click();
            URL.revokeObjectURL(elink.href);
            document.body.removeChild(elink);
       })
      .catch(function (error) {
          console.log('ERROR');
      });
    	},

    test_tores(){
      console.log('tores() success');
      this.$router.push({
        path:'/result',
        name:'Result',
        params:{
          tableData: [{
            date: '2016-05-02',
            name: '王小虎',
            address: '上海市普陀区金沙江路 1518 弄'
          }, {
            date: '2016-05-04',
            name: '王2虎',
            address: '上海市普陀区金沙江路 1517 弄'
          }, {
            date: '2016-05-03',
            name: '王4虎',
            address: '上海市普陀区金沙江路 1516 弄'
      }]
      }
      })
      }
 }
};

</script>

<style lang="less" scoped>
.body{
  margin:0px;
}
.top_container{
  weigh:200px;
  height:150px;
  margin:0 auto;
}

.top_container .word{
    float:left;
    height:30px;
    margin-left:40px;
}

.top_container .right_top{
    float:right;
    height:100px;
    margin-right:10px;
    margin-top:10px;

}
.top_container .upload{
  position:absolute;
  margin-top:90px;
  margin-left:10px;
}

.center_container{
    position: absolute;
    left: 50%;
    top: 64%;
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

.button_font{
 font-weight:bolder;
 font-size:20px;
}
</style>
