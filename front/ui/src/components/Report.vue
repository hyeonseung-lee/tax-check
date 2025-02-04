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
          <h2>AI 추천 상품</h2>
          <div class="divider"></div>
          <div class="stock-info">
            <h3>{{ stock.name }} {{ stock.price }}원</h3>
            <div class="description-nav">
              <button @click="prevStock" class="nav-button">◀</button>
              <span class="news-contents">{{ stock.description }}</span>
              <button @click="nextStock" class="nav-button">▶</button>
            </div>
          </div>
        </div>
        <div class="recommendation">
          <h2>Tax-Check 파트너 세무사</h2>
          <div class="divider"></div>
          <div class="stock-info">
            <h3>{{ news.name }}</h3>
            <div class="description-nav">
              <button @click="prevNews" class="nav-button">◀</button>
              <span class="news-contents">{{ news.description }}</span>
              <button @click="nextNews" class="nav-button">▶</button>
            </div>
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

export default {
  name: "ReportPage",
  components: {
    BarChart,
  },
  data() {
    return {
      accounts: "",
      loading: true, // 로딩 상태 추가
      reportText:
        "# 절세 전략 보고서\n\n안녕하세요! 절세를 위한 금융 전략을 안내해 드리겠습니다. 이 보고서는 연금저축계좌, IRP, ISA 계좌, 그리고 해외주식 양도소득세에 대한 절세 전략을 포함하고 있습니다. 각 항목별로 자세히 설명드리겠습니다.\n\n## 1. 연금저축계좌 및 IRP\n\n### 연금저축계좌와 IRP란?\n\n연금저축계좌와 IRP(Individual Retirement Pension)는 노후를 대비하여 돈을 모으는 계좌입니다. 이 계좌에 돈을 넣으면 세금 혜택을 받을 수 있습니다. 즉, 세금을 줄일 수 있는 좋은 방법입니다.\n\n### 계좌 개설 여부 확인\n\n- 연금저축계좌: 현재 연금저축계좌가 없으신 경우, 이 계좌를 개설하시는 것을 추천드립니다. 연금저축계좌는 노후 대비뿐만 아니라 세액 공제를 통해 세금을 줄일 수 있는 장점이 있습니다.\n  \n- IRP 계좌: IRP 계좌가 없으신 경우, 이 계좌도 개설하시는 것이 좋습니다. IRP는 연금저축계좌와 함께 사용하면 더 큰 세액 공제를 받을 수 있습니다.\n\n### 추가 납입 권장 금액\n\n- 연금저축계좌: 이미 계좌가 있으신 경우, 최대 세액 공제를 받기 위해 추가로 5,300,000원을 납입하시는 것이 좋습니다.\n  \n- IRP 계좌: IRP 계좌가 있으신 경우, 추가로 1,500,000원을 납입하시면 세액 공제를 극대화할 수 있습니다.\n\n## 2. ISA 계좌\n\n### ISA 계좌란?\n\nISA(Individual Savings Account)는 다양한 금융 상품에 투자할 수 있는 계좌로, 이 계좌를 통해 얻은 수익에 대해 일정 금액까지 비과세 혜택을 받을 수 있습니다. 즉, 투자 수익에 대한 세금을 줄일 수 있는 좋은 방법입니다.\n\n### 계좌 개설 여부 확인\n\n- ISA 계좌: 현재 ISA 계좌가 없으신 경우, 이 계좌를 개설하시는 것을 추천드립니다. ISA 계좌를 통해 얻은 수익은 비과세 혜택을 받을 수 있어 절세에 큰 도움이 됩니다.\n\n### 지금까지의 수익 및 절세 금액\n\nISA 계좌를 통해 지금까지 5,700,000원의 수익을 얻으셨고, 이를 통해 709,500원의 세금을 절약하셨습니다. 이는 ISA 계좌의 큰 장점 중 하나입니다.\n\n## 3. 해외주식 양도소득세\n\n### 해외주식 양도소득세란?\n\n해외 주식을 매도하여 얻은 이익에 대해 부과되는 세금입니다. 손익통산을 통해 손실과 이익을 합산하여 세금을 줄일 수 있습니다.\n\n### 절세 전략\n\n- 손익통산: 현재 해외 주식에서 손익통산한 금액은 3,300,000원입니다. 손익통산은 손실이 난 주식을 매도하여 이익과 상쇄시키는 방법으로, 이를 통해 세금을 줄일 수 있습니다.\n  \n- 손실 중인 종목 매도: 손실이 난 종목을 매도하여 손익통산을 활용하면, 세금을 줄이는 데 큰 도움이 됩니다.\n\n이 보고서를 통해 절세 전략을 이해하시고, 각 계좌의 장점을 최대한 활용하여 세금을 절약하시길 바랍니다. 추가적인 질문이 있으시면 언제든지 문의해 주세요. 감사합니다!",
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
        name: "삼성전자",
        price: "51,000",
        description:
          "삼성전자는 현재 주가 하락과 함께 여러 도전 과제에 직면해 있지만, 일부 전문가들은 향후 실적 개선을 기대하고 있습니다.",
      },
      stocks: [
        {
          name: "삼성전자",
          price: "51,000",
          description:
            "삼성전자는 현재 주가 하락과 함께 여러 도전 과제에 직면해 있지만, 일부 전문가들은 향후 실적 개선을 기대하고 있습니다.",
        },
        {
          name: "LG전자",
          price: "100,000",
          description:
            "LG전자의 주식은 CES 2025에서의 신기술 발표와 외국인 투자자의 순매수세로 긍정적인 반응을 얻고 있지만, 실적 저조가 우려되는 상황입니다. 앞으로의 시장 반응과 실적 개선 여부가 주가에 중요한 영향을 미칠 것으로 보입니다.",
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
  height: 300px;
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

.recommendation-graph {
  width: 500px;
  padding: 20px;
}

.stock-info {
  margin-bottom: 20px;
}

.description-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100px;
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
</style>
