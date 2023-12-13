<template>
  <container>
    <el-header style="height:10px; font-size: 22px" > 云南省就业率统计分析图</el-header>
    <div id="chart1"></div>
  </container>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import { Chart, registerAnimation } from '@antv/g2';
import conf from "@/web.conf";
// eslint-disable-next-line no-unused-vars
function handleData(source) {
  source.sort((a, b) => {
    return a.value - b.value;
  });

  return source;
}
export default {
  name: "index",
  data() {
    return {}
  },
  mounted() {
    this.registerlabelAppearAnimation()
    this.registerlabelUpdateAnimation()
    this.fetchDate()
  },
  methods: {
    registerlabelAppearAnimation: () => {
      // 初始化值
      registerAnimation('label-appear', (element, animateCfg, cfg) => {
        const label = element.getChildren()[0];
        const coordinate = cfg.coordinate;
        const startX = coordinate.start.x;
        const finalX = label.attr('x');
        const labelContent = label.attr('text');

        label.attr('x', startX);
        label.attr('text', 0);

        const distance = finalX - startX;
        label.animate((ratio) => {
          const position = startX + distance * ratio;
          const text = (labelContent * ratio).toFixed(0);

          return {
            x: position,
            text,
          };
        }, animateCfg);
      });
    },
    registerlabelUpdateAnimation: () => {
      registerAnimation('label-update', (element, animateCfg, cfg) => {
        const startX = element.attr('x');
        const startY = element.attr('y');
        // @ts-ignore
        const finalX = cfg.toAttrs.x;
        // @ts-ignore
        const finalY = cfg.toAttrs.y;
        const labelContent = element.attr('text');
        // @ts-ignore
        const finalContent = cfg.toAttrs.text;

        const distanceX = finalX - startX;
        const distanceY = finalY - startY;
        const numberDiff = +finalContent - +labelContent;

        element.animate((ratio) => {
          const positionX = startX + distanceX * ratio;
          const positionY = startY + distanceY * ratio;
          const text = (+labelContent + numberDiff * ratio).toFixed(0);

          return {
            x: positionX,
            y: positionY,
            text,
          };
        }, animateCfg);
      });
    },
    fetchDate: () => {
      window.fetch(conf.dev_base_url+'/api/employment_ratio')
          .then(res => res.json())
          .then(data => {
            data = data.data
            let count = 0;
            let chart;
            let interval;

            function countUp() {
              if (count === 0) {
                chart = new Chart({
                  container: 'chart1',
                  autoFit: true,
                  height: 500,
                  // 上右下左边距
                  padding: [ 40, 60, 18, 80]
                });
                // @ts-ignore
                chart.data(handleData(Object.values(data)[count]));
                chart.coordinate('rect').transpose();
                chart.legend(false);
                chart.tooltip(false);
                // chart.axis('value', false);
                // 文件城市的动画时间
                chart.axis('city', {
                  animateOption: {
                    update: {
                      duration: 1100,
                      easing: 'easeLinear'
                    }
                  }
                });
                chart.annotation().text({
                  position: ['95%', '90%'],
                  content: Object.keys(data)[count],
                  style: {
                    fontSize: 40,
                    fontWeight: 'bold',
                    fill: '#ddd',
                    textAlign: 'end'
                  },
                  animate: false,
                });
                chart
                    .interval()
                    .position('city*value')
                    .color('city')
                    .label( 'value' , (/*value*/) => {
                      // if (value !== 0) {
                      return {
                        animate: {
                          appear: {
                            animation: 'label-appear',
                            delay: 0,
                            duration: 1000,
                            easing: 'easeLinear'
                          },
                          // 标签值动画
                          update: {
                            animation: 'label-update',
                            duration: 1100,
                            easing: 'easeLinear'
                          }
                        },
                        offset: 5,
                      };
                      // }
                    }).animate({
                  appear: {
                    duration: 1000,
                    easing: 'easeLinear'
                  },
                  // 线条动画
                  update: {
                    duration: 1100,
                    easing: 'easeLinear'
                  }
                });

                chart.render();
              } else {
                chart.annotation().clear(true);
                chart.annotation().text({
                  position: ['95%', '90%'],
                  content: Object.keys(data)[count],
                  style: {
                    fontSize: 40,
                    fontWeight: 'bold',
                    fill: '#ddd',
                    textAlign: 'end'
                  },
                  animate: false,
                });
                // @ts-ignore
                chart.changeData(handleData(Object.values(data)[count]));
              }

              ++count;

              if (count === Object.keys(data).length) {
                clearInterval(interval);
                // count = 0
                // countUp()
              }
            }

            countUp();
            interval = setInterval(countUp, 1500);
          })
    }
  }
}
</script>

<style scoped>
  .el-header {
    /* background-color: #B3C0D1; */
    color: #333;
    text-align: center;
    line-height: 60px;
  }
.el-row {
  margin-bottom: 20px;
 /*last-child {*/
 /*  margin-bottom: 0;*/
 /*}*/
}
.el-col {
  border-radius: 4px;
}
.bg-purple-dark {
  background: #99a9bf;
}
.bg-purple {
  background: #d3dce6;
}
.bg-purple-light {
  background: #e5e9f2;
}
.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}
</style>
