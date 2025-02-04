<template>
  <div class="main">
    <div v-if="loading" class="loading-screen">로딩 중...</div>
    <div v-else>
      <h2 class="account-title">절세 전략 보고서</h2>
      <div class="divider"></div>
      <div class="container">
        <div class="report">
          <h2>AI 보고서</h2>
          <div class="divider"></div>
          <div class="report-content" v-html="formattedReportText"></div>
        </div>
        <div class="align-items: center;">
          <div class="recommendation-graph">
            <h2>납입 현황</h2>
            <div class="divider"></div>
            <div class="chart-container">
              <BarChart :dataResult="this.dataResult" />
            </div>
          </div>
        </div>
      </div>
      <div></div>
      <div class="AI-container">
        <div class="recommendation" style="border-right: 1px solid #ccc">
          <h2>절세 가능 금액</h2>
          <div class="divider"></div>
          <ProfitChart :dataResult="graphData" />
        </div>
        <div class="recommendation-AI">
          <h2>AI 추천 상품</h2>
          <div class="divider"></div>
          <div class="stock-info">
            <button @click="prevStock" class="nav-button">◀</button>
            <div
              class="stock-title"
              OnClick="location.href ='https://securities.miraeasset.com/hks/hks4325/n02.do'"
              style="cursor: pointer"
            >
              <h1>{{ stock.name }}</h1>
              <h2>{{ stock.price }}</h2>
            </div>
            <button @click="nextStock" class="nav-button">▶</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { marked } from "marked";
import axios from "axios";
import BarChart from "./BarChart.vue";
import ProfitChart from "./ProfitChart.vue";

export default {
  name: "ReportPage",
  components: {
    BarChart,
    ProfitChart,
  },
  data() {
    return {
      accounts: "",
      loading: true, // 로딩 상태 추가
      reportText: "",
      dataResult: {
        remain_pb: 5300000,
        remain_irp: 1500000,
        isa_total_profit: 5700000,
        pb_exist: 1,
        irp_exist: 1,
        isa_exist: 1,
        save_tax: 709500,
        overseas_total_profit: 3300000,
        overseas_min: "손실 중인 종목 매도",
        created_at: "2025-02-04T01:31:47.764000",
      },
      stock: {
        name: "청년형 장기집합투자증권저축",
        price: "연 600만원 한도. 40%소득공제 혜택(연240만원한도)",
      },
      stocks: [
        {
          name: "청년형 장기집합투자증권저축",
          price: "연 600만원 한도. 40%소득공제 혜택(연240만원한도)",
        },
        {
          name: "벤처기업투자신탁(펀드)",
          price: " 투자금액 중 3천만원까지에 대해 투자금액의 10% 소득공제",
        },
        // 추가 종목을 여기에 추가
      ],
      currentIndex: 0,
      news: {
        name: "\"배당 재투자 금지\"…6조원 '해외주식 TR ETF' 사라진다",
        description:
          "7월부터 운용방식 변경 배당 재투자로 복리효과 'TR ETF'매도 때 세금 내 과세이연 혜택도 직장인들은 연말정산 시 세금 관련 혜택을 받을 수 있는 연금저축과 IRP(개인형퇴직연금), ISA(개인종합자산관리계좌) 등 세 가지 절세통장을 알아두면 좋습니다.",
      },
      newses: [
        {
          name: "\"배당 재투자 금지\"…6조원 '해외주식 TR ETF' 사라진다",
          description:
            "7월부터 운용방식 변경 배당 재투자로 복리효과 'TR ETF'매도 때 세금 내 과세이연 혜택도 직장인들은 연말정산 시 세금 관련 혜택을 받을 수 있는 연금저축과 IRP(개인형퇴직연금), ISA(개인종합자산관리계좌) 등 세 가지 절세통장을 알아두면 좋습니다.",
        },
        {
          name: "연말정산 '절세계좌' 삼총사 알아두세요[금알못]",
          description:
            "'13월의 월급'이라 불리는 연말정산 기간이 다가오면서 세액공제에 관심이 커지고 있습니다. 직장인들은 연말정산 시 세금 관련 혜택을 받을 수 있는 연금저축과 IRP(개인형퇴직연금), ISA(개인종합자산관리계좌) 등 세 가지 절세통장을 알아두면 좋습니다.",
        },
      ],
      currentIndexNews: 0,
    };
  },
  computed: {
    formattedReportText() {
      return marked(this.reportText);
    },
    formattedText() {
      return marked(this.stock.description);
    },
  },
  mounted() {
    this.fetchHistory();
  },

  methods: {
    fetchHistory() {
      try {
        axios.post("http://221.168.39.188:8000/login").then((response) => {
          axios
            .post(
              "http://221.168.39.188:8000/generate_report?user_id=0011",
              response.data, // 로그인 응답 데이터를 요청 본문으로 전달
              {
                headers: {
                  "Content-Type": "application/json", // JSON 형식으로 전송
                },
              }
            )
            .then((res) => {
              this.reportText = res.data.report;
              this.dataResult = res.data.data_result;

              // 그래프 데이터 준비
              this.graphData = {
                labels: ["(연소득) 5500만원 이하", "(연소득) 5500만원 초과"], // 그래프의 레이블
                datasets: [
                  {
                    label: "현재 절세액", // 'my_under_now'와 'my_under_max' 비교
                    data: [
                      res.data.data_result.my_under_now,
                      res.data.data_result.my_over_now,
                    ],
                    backgroundColor: [
                      "rgba(140, 140, 140, 1)",
                      "rgba(140, 140, 140, 1)",
                    ],
                  },
                  {
                    label: "최대 가능 절세액", // 'my_over_now'와 'my_over_max' 비교
                    data: [
                      res.data.data_result.my_under_max,
                      res.data.data_result.my_over_max,
                    ],
                    backgroundColor: [
                      "rgba(237, 108, 29, 1)",
                      "rgba(237, 108, 29, 1)",
                    ],
                  },
                ],
              };

              this.loading = false; // 5초 후 로딩 상태 변경
            })
            .catch((error) => {
              console.error("API 호출 오류:", error);
            });
        });
      } catch (error) {
        console.error("계좌 정보를 가져오는 데 실패했습니다.", error);
      }
    },
    prevStock() {
      if (this.currentIndex === 0) {
        this.currentIndex = this.stocks.length - 1;
      } else {
        this.currentIndex--;
      }
      this.updateStock();
    },
    nextStock() {
      if (this.currentIndex === this.stocks.length - 1) {
        this.currentIndex = 0;
      } else {
        this.currentIndex++;
      }
      this.updateStock();
    },
    updateStock() {
      this.stock = this.stocks[this.currentIndex];
    },
    // news
    prevNews() {
      if (this.currentIndexNews === 0) {
        this.currentIndexNews = this.newses.length - 1;
      } else {
        this.currentIndexNews--;
      }
      this.updateNews();
    },
    nextNews() {
      if (this.currentIndexNews === this.newses.length - 1) {
        this.currentIndexNews = 0;
      } else {
        this.currentIndexNews++;
      }
      this.updateNews();
    },
    updateNews() {
      this.news = this.newses[this.currentIndexNews];
    },
  },
};
</script>

<style scoped>
.main {
  margin-top: 5px;
  padding: 20px;
  width: 100%;
  margin: 0 auto;
}
.divider {
  height: 2px; /* 줄의 두께 */
  background-color: #ed6d1e; /* 줄 색상 */
  margin: 10px 0; /* 위 아래 여백 */
}
.container {
  display: flex;
  justify-content: space-between;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  height: 550px;
}

.AI-container {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  height: 450px;
}

.report {
  width: 1500px;
  padding: 20px;
  border-right: 1px solid #ccc;
}

.report-content {
  font-size: 1.2rem;
  text-align: left;
  height: 90%; /* 원하는 높이 설정 */
  overflow-y: auto; /* 세로 방향으로 스크롤 가능 */
  text-overflow: ellipsis; /* 넘치는 텍스트는 생략 표시 */
}

.chart-container {
  height: 430px; /* 원하는 높이 설정 */
  overflow-y: auto; /* 세로 방향으로 스크롤 가능 */
}

.recommendation {
  width: 800px;
  padding: 20px;
}
.recommendation-AI {
  width: 850px;
  padding: 20px;
}

.recommendation-graph {
  width: 500px;
  padding: 20px;
}

.stock-info {
  display: flex;
  justify-content: space-between;
  margin-top: 120px;
}

.description-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100px;
  text-align: left;
}

.navigation {
  display: flex;
  justify-content: space-between;
}

.nav-button {
  background-color: #ed6d1e;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px;
  cursor: pointer;
  height: 50px;
}

.nav-button:hover {
  background-color: #ed6d1e;
}

.news-contents {
  display: inline-block;
  overflow: hidden;
  text-overflow: ellipsis;
}
.loading-screen {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* 전체 화면 높이 */
  font-size: 24px; /* 로딩 텍스트 크기 */
}
.stock-title {
  height: 150px;
}
</style>
