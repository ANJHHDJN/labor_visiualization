<template>
<div class='picSearch'>
<el-form :inline="true" :model="formInline" :rules="rules" ref="formInline" class="demo-form-inline" size="small" v-show="pt">
  <el-form-item label="月份" prop="time">
    <el-select v-model="formInline.month" placeholder="请选择月份查询">
      <el-option label="2月" value="2" ></el-option>
      <el-option label="3月" value="3"></el-option>
      <el-option label="4月" value="4"></el-option>
      <el-option label="5月" value="5"></el-option>
      <el-option label="6月" value="6"></el-option>
      <el-option label="7月" value="7"></el-option>
    </el-select>
  </el-form-item>
  <el-form-item label="地区" prop="area">
    <el-select v-model="formInline.area_code" placeholder="请选择地区查询">
      <el-option label="昆明市" value="530100"></el-option>
      <el-option label="昭通市" value="530600"></el-option>
      <el-option label="曲靖市" value="530300"></el-option>
      <el-option label="玉溪市" value="530400"></el-option>
      <el-option label="普洱市" value="530800"></el-option>
      <el-option label="保山市" value="530500"></el-option>
      <el-option label="楚雄州" value="532300"></el-option>
      <el-option label="丽江市" value="530700"></el-option>
      <el-option label="红河州" value="532500"></el-option>
      <el-option label="西双版纳州" value="532800"></el-option>
      <el-option label="临沧市" value="530900"></el-option>
      <el-option label="大理州" value="532900"></el-option>
      <el-option label="德宏州" value="533100"></el-option>
      <el-option label="文山州" value="532600"></el-option>
      <el-option label="怒江州" value="533300"></el-option>
      <el-option label="迪庆州" value="533400"></el-option>
    </el-select>
  </el-form-item>
  <el-form-item>
    <el-button type="primary" @click="onSubmit">查询</el-button>
  </el-form-item>
  <el-form-item>
    <el-button type="primary" @click="downLoad" >下载报告</el-button>
  </el-form-item>
</el-form>
<el-row  type="flex"  justify="space-around">
    <el-col :span="10">
    <p>就业人口和未就业人口统计对比图<p/>
    <div id="empPopulationData_container" />
    </el-col>
    <el-col :span="10">
    <p>新增就业人口和失业人口统计对比图<p/>
    <div id="empPopulationChangeData_container" />
    </el-col>
</el-row>

    <el-row type="flex"  justify="space-around">
      <el-col :span="10">
        <p>就业行业分布图<p/>
        <div id="industryData_container"/>
      </el-col>
      <el-col :span="10">
        <p>劳动力流入和流出统计对比图<p/>
        <div id="laborInData_container"/>
      </el-col>
    </el-row>
    

    <el-row type="flex"  justify="space-around">
      <el-col :span="10">
        <p>新增就业人口年龄分布图<p/>
        <div id="empAgeData_container"/>
      </el-col>
      <el-col :span="10">
        <p>新增失业人口年龄分布图<p/>
        <div id="firedAgeData_container"/>
      </el-col>
    </el-row>
</div>
</template>

<script>

import conf from "@/web.conf";
import { Chart, Util } from '@antv/g2';
import DataSet from '@antv/data-set';

  export default {
    data() {
      return {
        pt: true,
        // ptt:false,
        fullscreenLoading: true,
        formInline: {
          month: '',
          area_code: ''
        },
        rules:{
            time:[{required:true,message:"请选择月份",trigger:'blur'}],
            area:[{required:true,message:"请选择地区",trigger:'blur'}]
        }
      }
    },

    inject: ["reload"],
    methods: {
      onSubmit() {

        if(this.formInline.month=='' || this.formInline.area_code==''){
          this.$message('请选择月份和地区');
          return
        }

        this.reload();

        console.log(this.formInline);
        window.fetch(conf.dev_base_url+'/api/report?year=2020&month='+this.formInline.month+'&area_code='+this.formInline.area_code)
        .then(res => res.json())
        .then(data => {
        data = data.data['emp_population_data']
        const chart = new Chart({
        container: 'empPopulationData_container',
        autoFit: true,
        height: 500,
        });

        chart.data(data);
        // chart.changeData(data);
        chart.scale('月均降雨量', {
        nice: true,
        });
        chart.tooltip({
        showMarkers: false,
        shared: true,
        });

        chart
        .interval()
        .position('月份*月均降雨量')
        .color('name')
        .adjust([
            {
            type: 'dodge',
            marginRatio: 0,
            },
        ]);

        chart.interaction('active-region');
        chart.render();

          })
        window.fetch(conf.dev_base_url+'/api/report?year=2020&month='+this.formInline.month+'&area_code='+this.formInline.area_code)
            .then(res => res.json())
            .then(data => {
              data = data.data['emp_population_change_data']
              const chart = new Chart({
              container: 'empPopulationChangeData_container',
              autoFit: true,
              height: 500,
            });

            chart.data(data);
            chart.scale('月均降雨量', {
              nice: true,
            });
            chart.tooltip({
              showMarkers: false,
              shared: true,
            });

            chart
              .interval()
              .position('月份*月均降雨量')
              .color('name')
              .adjust([
                {
                  type: 'dodge',
                  marginRatio: 0,
                },
              ]);

            chart.interaction('active-region');

            chart.render();
          })
         window.fetch(conf.dev_base_url+'/api/report?year=2020&month='+this.formInline.month+'&area_code='+this.formInline.area_code)
            .then(res => res.json())
            .then(data => {
              data = data.data['industry_data']
              const chart = new Chart({
              container: 'industryData_container',
              autoFit: true,
              height: 500,
            });

            chart.data(data);
            chart.scale({
              value: {
                // max: 90000,
                min: 0,
                alias: '人数',
              },
            });
            chart.axis('type', {
              title: null,
              tickLine: null,
              line: null,
            });

            chart.axis('value', {
              label: null,
              title: {
                offset: 30,
                style: {
                  fontSize: 12,
                  fontWeight: 300,
                },
              },
            });
            chart.legend(false);
            chart.coordinate().transpose();
            chart
              .interval()
              .position('type*value')
              .size(26)
              .label('value', {
                style: {
                  fill: '#8d8d8d',
                },
                offset: 10,
              });
            chart.interaction('element-active');
            chart.render();
          })
        window.fetch(conf.dev_base_url+'/api/report?year=2020&month='+this.formInline.month+'&area_code='+this.formInline.area_code)
            .then(res => res.json())
            .then(data => {
              data = data.data['emp_age_data']
              const chart = new Chart({
              container: 'empAgeData_container',
              autoFit: true,
              height: 500,

            });
          chart.data(data);

          chart.coordinate('theta', {
            radius: 0.75
          });
          chart.tooltip({
            showMarkers: false
          });

          chart
            .interval()
            .adjust('stack')
            .position('value')
            .color('type', ['#063d8a', '#1770d6', '#47abfc', '#38c060'])
            .style({ opacity: 0.4 })
            .state({
              active: {
                style: (element) => {
                  const shape = element.shape;
                  return {
                    matrix: Util.zoom(shape, 1.1),
                  }
                }
              }
            })
            .label('type', (val) => {
              const opacity = val === '55岁以上' ? 1 : 0.5;
              return {
                offset: -30,
                style: {
                  opacity,
                  fill: 'white',
                  fontSize: 12,
                  shadowBlur: 2,
                  shadowColor: 'rgba(0, 0, 0, .45)',
                },
                content: (obj) => {
                  return obj.type + '\n' + obj.value ;
                },
              };
            });

          chart.interaction('element-single-selected');

          chart.render();

          })
        window.fetch(conf.dev_base_url+'/api/report?year=2020&month='+this.formInline.month+'&area_code='+this.formInline.area_code)
            .then(res => res.json())
            .then(data => {
              data = data.data['fired_age_data']
              const chart = new Chart({
              container: 'firedAgeData_container',
              autoFit: true,
              height: 500,

            });
          chart.data(data);

          chart.coordinate('theta', {
            radius: 0.75
          });
          chart.tooltip({
            showMarkers: false
          });

          chart
            .interval()
            .adjust('stack')
            .position('value')
            .color('type', ['#063d8a', '#1770d6', '#47abfc', '#38c060'])
            .style({ opacity: 0.4 })
            .state({
              active: {
                style: (element) => {
                  const shape = element.shape;
                  return {
                    matrix: Util.zoom(shape, 1.1),
                  }
                }
              }
            })
            .label('type', (val) => {
              const opacity = val === '55岁以上' ? 1 : 0.5;
              return {
                offset: -30,
                style: {
                  opacity,
                  fill: 'white',
                  fontSize: 12,
                  shadowBlur: 2,
                  shadowColor: 'rgba(0, 0, 0, .45)',
                },
                content: (obj) => {
                  return obj.type + '\n' + obj.value;
                },
              };
            });

          chart.interaction('element-single-selected');

          chart.render();

          })
          window.fetch(conf.dev_base_url+'/api/report?year=2020&month='+this.formInline.month+'&area_code='+this.formInline.area_code)
            .then(res => res.json())
            .then(data => {
              data = data.data['labor_in_data']
              const chart = new Chart({
              container: 'laborInData_container',
              autoFit: true,
              height: 500,

            });

            const { DataView } = DataSet;
            const dv = new DataView().source(data);
            dv.transform({
              type: 'fold',
              fields: ['劳动力流入', '劳动力流出'], // 展开字段集
              key: 'user', // key字段
              value: 'score', // value字段
            });

            chart.data(dv.rows);
            chart.scale('score', {
              min: 0,
              max: 1100,
            });
            chart.coordinate('polar', {
              radius: 0.8,
            });
            chart.tooltip({
              shared: true,
              showCrosshairs: true,
              crosshairs: {
                line: {
                  style: {
                    lineDash: [4, 4],
                    stroke: '#333'
                  }
                }
              }
            });
            chart.axis('item', {
              line: null,
              tickLine: null,
              grid: {
                line: {
                  style: {
                    lineDash: null,
                  },
                },
              },
            });
            chart.axis('score', {
              line: null,
              tickLine: null,
              grid: {
                line: {
                  type: 'line',
                  style: {
                    lineDash: null,
                  },
                },
              },
            });

            chart
              .line()
              .position('item*score')
              .color('user')
              .size(2);
            chart
              .point()
              .position('item*score')
              .color('user')
              .shape('circle')
              .size(4)
              .style({
                stroke: '#fff',
                lineWidth: 1,
                fillOpacity: 1,
              });
            chart
              .area()
              .position('item*score')
              .color('user');
            chart.render();
          })
      },
      downLoad(){
        // this.onSubmit();

        // http://127.0.0.1:5000/api/report_download?year=2020&month=6&area_code=530100
      this.pt = false
     setTimeout(() => {
          this.fullscreenLoading = false
          this.$nextTick(() => {
            window.print()
            this.pt = true
          })
        }, 3000)
        
      }
      

    }
  }
</script>

<style lang='scss'>
.picSearch{
    .demo-form-inline{
        text-align: left;
        padding: 10px;
    }
}
</style>