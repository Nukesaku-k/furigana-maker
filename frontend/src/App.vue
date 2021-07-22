<template>
  <div id="app" >
    <h2>ルビ振りひらがな変換ツール</h2>

    <div class="callout is-helpful">
      <header>ルビ振りひらがな変換</header>
      <p>漢字かな交じりの日本語文章にふりがな（ルビ）をつけるツールです。<br>
      小学1〜6年生向け、中学生以上向け、一般向けとルビ付けのレベルの指定もできます。</p>
    </div>
    <el-form :model="ruleForm" :rules="rules" ref="ruleForm">
      <el-form-item prop="value">
        <el-select v-model="ruleForm.value" placeholder="学年（難易度）を選択">
          <el-option
            v-for="item in cities"
            :key="item.value"
            :label="item.label"
            :value="item.value"
            :remark="item.remark">
            <span style="float: left">{{ item.label }}</span>
            <span style="float: left; color: #8492a6; font-size: 11px; margin-left:10px ">{{ item.remark }}</span>
          </el-option>
        </el-select>
      </el-form-item>
      <div class="remark">
        注1：学年は「小学校学習指導要領」の付録「学年別漢字配当表」を参考に設定されています。<br>
        注2：JIS X 0208が定める漢字</div>
      <el-form-item prop="textarea">
        <el-input
          type="textarea"
          clearable="true"
          :rows="2"
          :autosize="{ minRows: 4, maxRows: 10}"
          placeholder="ルビ振りひらがな変換したいテキストを入力"
          v-model="ruleForm.textarea">
        </el-input>
      </el-form-item>

      <el-form-item style="margin-botom: 5px">
        <el-radio-group v-model="ruleForm.type">
          <el-radio label="1" border>ルビを振る</el-radio>
          <el-radio label="2" border>括弧で括る</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-row>
        <el-button
          type="primary"
          style="margin-top:10px; padding: 16px 72px; font-size:16px"
          @click="submitForm('ruleForm')">変換実行</el-button>
      </el-row>
      <el-progress :percentage="progress"></el-progress>
    </el-form>
    <p style="margin-top:20px">実行結果</p>
    <div class="result">
      <div v-html="test"></div>
    </div>

  </div>

</template>
<style lang="scss">

.remark {
  color: #8492a6;
  font-size: 13px;
  // padding: 8px 16px;
  margin:20px 0 20px 0;
}
.callout.is-helpful{
  margin-bottom: 20px;
}
.callout.is-helpful header {
  background: teal;
}

.callout header {
  color: rgb(255, 255, 255);
  line-height: 2.4rem;
  font-weight: 500;
  text-transform: uppercase;
  padding: 8px 16px;
  margin: 0px;
  border-radius: 4px 4px 0px 0px;
  // border: 1px solid #DCDFE6;
}
.callout > :not(:first-child) {
  padding: 10px 15px;
  background-color:rgb(235, 236, 238);
  border-radius: 0px 0px 4px 4px;
}
.callout p {
    font-size: 13px;
    padding: 16px;
    margin: 0px;
}

.result {
  line-height: 2.4rem;
  // font-weight: 500;
  // text-transform: uppercase;
  font-size: 24px;
  padding: 8px 16px;
  margin: 0px;
  margin-bottom: 30px;
  border-radius: 4px 4px 4px 4px;
  border: 1px solid #DCDFE6;
  // background-color:rgb(235, 236, 238);
  min-height: 200px;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  width: 80%;
  height: 50%;
  margin:auto auto;
  color: #2c3e50;
}
a {
  text-decoration: none;
}
ruby > rt {
  display: block;
  font-size: 12px;
  text-align: start;
}
</style>

<script>
const axios = require('axios').create()
export default {

  data() {
    return {
      progress:'0',
      test:'',
      cities: [
        {
          value: '1',
          label: '小学1年生向け',
          remark:'漢字（注2）にふりがなを付けます。'
        },
        {
          value: '2',
          label: '小学2年生向け',
          remark:'1年生で習う漢字にはふりがなを付けません。'
        },
        {
          value: '3',
          label: '小学3年生向け',
          remark:'1～2年生で習う漢字にはふりがを付けません。'
        },
        {
          value: '4',
          label: '小学4年生向け',
          remark:'1～3年生で習う漢字にはふりがなを付けません。'
        },
        {
          value: '5',
          label: '小学5年生向け',
          remark:'1～4年生で習う漢字にはふりがなを付けません。'
        },
        {
          value: '6',
          label: '小学6年生向け',
          remark:'1～5年生で習う漢字にはふりがなを付けません。'
        },
        {
          value: '7',
          label: '中学生以上向け',
          remark:'小学校で習う漢字にはふりがなを付けません。'
        },
        {
          value: '8',
          label: '一般向け',
          remark:'常用漢字にはふりがなを付けません。'
        },
      ],
      rules: {
        value: [
          {
            required: true,
            message: '学年（難易度）を選択してください',
            trigger: 'change'
          },
        ],
        textarea: [
          {
            required: true,
            message: 'ルビ振りひらがな変換したいテキストを入力してください。',
            trigger: 'blur'
          },
        ],
      },
      ruleForm: {
        value: '',
        textarea: '',
        type: '1',
      },
    }
  },
  methods: {
    submitForm(formName) {
      this.progress = '0'
      this.$refs[formName].validate(valid => {
        if (valid) {
          const params = new URLSearchParams()
          params.append('type', this.$refs[formName].model.type)
          params.append('sentence', this.$refs[formName].model.textarea)
          params.append('grade', this.$refs[formName].model.value)
          axios.post('api/list', params).then(respose => {
            this.progress = '100'
            this.test = respose.data})
        } else {
          return false
        }
      })
    }
  }
}
</script>
