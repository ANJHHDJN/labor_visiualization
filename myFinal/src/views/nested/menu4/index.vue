<template>
  <container>
    <!-- <h1>分析报告</h1> -->
    <el-header style="height:50px; font-size: 22px" > 2020年5月云南省劳动力流向视图</el-header>
    <el-row  type="flex"  justify="space-around">
      <el-col :span="12">
        <div id="map" />
      </el-col>
      <el-col :span="10">
        <p>劳动力流入、流出数量<p/>
        <div id="empPopulationFlowData_container" />
      </el-col>
    </el-row>
    <!-- <el-header style="height:50px; font-size: 22px" > 云南省劳动力流向视图</el-header> -->
    <!-- <h1 class="title">云南省劳动力流向视图</h1> -->
    <!-- <div id="map"  class="map-contain"></div> -->
  </container>
</template>

<script>
import { Scene, LineLayer, PointLayer } from '@antv/l7';
import {  GaodeMap } from '@antv/l7-maps';
// eslint-disable-next-line no-unused-vars
import conf from "../../../web.conf";
import { Chart } from '@antv/g2';


export default {
  name: "index",
  data() {
    return {}
  },
  mounted() {
    let year_month = 202005
    this.empPopulationFlowData(year_month)
    const scene = new Scene({
      id: 'map',
      map: new GaodeMap({
        pitch: 0,
        style: 'light',
        center: [ 101.54, 23.71 ],
        // 初始化地图层级
        zoom: 7
      })
    });
    scene.on('loaded', () => {
      // + year_month
      fetch(conf.dev_base_url + '/api/labor_flow?year_month=202005' )
          .then(res => res.json())
          .then(data => {
            data=data.data
            const pointLayer = new PointLayer({})
                .source(data, {
                  parser: {
                    type: 'csv',
                    x: 'lng1',
                    y: 'lat1'
                  }
                })
                .shape('circle')
                .active(true)
                .animate({
                  enable: true,
                  speed: 0.5 ,
                  rings: 4
                })
                .size(30)
                .color('rgb(249,176,71)')
                .style({
                  opacity: 0.8
                });
            const lineLayer = new LineLayer({
              blend: 'normal'
            })
                .source(data, {
                  parser: {
                    type: 'csv',
                    x: 'lng1',
                    y: 'lat1',
                    x1: 'lng2',
                    y1: 'lat2'
                  }
                })
                .size('value', (value)=>{
                  return value*0.1
                })
                .shape('arc')
                .animate({
                  enable: true,
                  interval: 1,
                  trailLength: 0.9,
                  duration: 2
                })
                .color('rgb(141,177,227)')
                .style({
                  opacity: 0.8
                });
            scene.addLayer(pointLayer);
            scene.addLayer(lineLayer)
          });
    });
    },

  methods: {
    empPopulationFlowData:(year_month)=>{
      // window.fetch(conf.dev_base_url + '/api/labor_flow?year_month=202003' )
      window.fetch('http://127.0.0.1:5000/api/labor_flow_data?year_month=202005')
      // window.fetch(conf.dev_base_url+'/api/report?year='+year+'&month='+month+'&area_code='+area_code)
            .then(res => res.json())
            .then(data => {
              data = data.data
             const chart = new Chart({
              container: 'empPopulationFlowData_container',
              autoFit: true,
              height: 500,
            });

            chart.data(data);

            chart
              .coordinate()
              .transpose()
              .scale(1, -1);

            chart.axis('value', {
              position: 'right',
            });
            chart.axis('label', {
              label: {
                offset: 12,
              },
            });

            chart.tooltip({
              shared: true,
              showMarkers: false,
            });

            chart
              .interval()
              .position('label*value')
              .color('type')
              .adjust([
                {
                  type: 'dodge',
                  marginRatio: 0,
                },
              ]);

            chart.interaction('active-region');

            chart.render();
          })
    }
  }
}
</script>

<style scoped>
#map{
  position: relative;
  min-height: 550px; 
  /* min-width: 10px;
  justify-content: center;  */
 } 
 .map-contain{
    width:50%;
    /* height: 600px; */
    float: left;
    position: relative;
  }
  .el-dropdown-link {
    cursor: pointer;
    color: #409EFF;
  }
  .el-icon-arrow-down {
    font-size: 12px;
  }
/* .title{
  display: inline-block;
    width: fit-content;
    position: absolute;
    left: 20px;
    z-index: 2;
    writing-mode: vertical-lr;
    top: 13%;
    letter-spacing: 7px;
    color:#e6a342;
    border: 1px dashed grey;
    padding: 10px 20px;
} */
.el-header {
    /* background-color: #B3C0D1; */
    color: #333;
    text-align: center;
    line-height: 60px;
  }
</style>
