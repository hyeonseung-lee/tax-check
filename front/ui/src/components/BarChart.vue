<template>
  <div class="chart-container">
    <div style="font-size: 1.4rem">연금 저축 계좌</div>
    <canvas id="myChart1"></canvas>
    <div style="font-size: 1.4rem">IRP 계좌</div>
    <canvas id="myChart2"></canvas>
  </div>
</template>

<script>
import { Chart, registerables } from "chart.js";

export default {
  name: "BarChart",
  props: {
    dataResult: {
      type: Object,
      required: true,
    },
  },
  mounted() {
    Chart.register(...registerables);
    this.createCharts();
  },
  methods: {
    createCharts() {
      const ctx1 = document.getElementById("myChart1").getContext("2d");
      const ctx2 = document.getElementById("myChart2").getContext("2d");

      const remainPb = this.dataResult.remain_pb;
      const additionalPbValue = 6000000 - remainPb; // 6000000이 되도록 추가할 값

      const remainIrp = this.dataResult.remain_irp;
      const additionalIrpValue = 3000000 - remainIrp; // 6000000이 되도록 추가할 값

      // 첫 번째 그래프
      new Chart(ctx1, {
        type: "bar", // 막대그래프 타입
        data: {
          labels: ["추가 납입 금액", "현재 납입 금액"], // 각각의 항목 이름 변경
          datasets: [
            {
              label: "금액 (원)",
              data: [remainPb, additionalPbValue], // 각각의 데이터
              backgroundColor: [
                "rgba(75, 192, 192, 0.2)", // remain_pb 색상
                "rgba(255, 99, 132, 0.2)", // 추가 값 색상
              ],
              borderColor: [
                "rgba(75, 192, 192, 1)", // remain_pb 테두리 색상
                "rgba(255, 99, 132, 1)", // 추가 값 테두리 색상
              ],
              borderWidth: 1,
            },
          ],
        },
        options: {
          indexAxis: "y", // 가로 막대그래프 설정
          scales: {
            x: {
              beginAtZero: true,
              title: {
                display: true,
                text: "금액 (원)",
              },
            },
            y: {
              title: {
                display: true,
              },
            },
          },
        },
      });

      // 두 번째 그래프
      new Chart(ctx2, {
        type: "bar", // 막대그래프 타입
        data: {
          labels: ["추가 납입 금액", "현재 납입 금액"], // 각각의 항목 이름 변경
          datasets: [
            {
              label: "금액 (원)",
              data: [remainIrp, additionalIrpValue], // 각각의 데이터
              backgroundColor: [
                "rgba(75, 192, 192, 0.2)", // remain_irp 색상
                "rgba(255, 99, 132, 0.2)", // 추가 값 색상
              ],
              borderColor: [
                "rgba(75, 192, 192, 1)", // remain_irp 테두리 색상
                "rgba(255, 99, 132, 1)", // 추가 값 테두리 색상
              ],
              borderWidth: 1,
            },
          ],
        },
        options: {
          indexAxis: "y", // 가로 막대그래프 설정
          scales: {
            x: {
              beginAtZero: true,
              title: {
                display: true,
                text: "금액 (원)",
              },
            },
            y: {
              title: {
                display: true,
                font: {
                  size: 20, // 제목 글자 크기 설정
                },
              },
            },
          },
        },
      });
    },
  },
};
</script>

<style scoped>
.chart-container {
  display: flex;
  flex-direction: column; /* 세로 방향으로 정렬 */
  width: 100%;
  max-width: 600px; /* 최대 너비 설정 */
  margin: 0 auto; /* 중앙 정렬 */
}
</style>
