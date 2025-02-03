<template>
  <div class="main">
    <h2 class="account-title">절세 전략 보고서</h2>
    <div class="divider"></div>
    <div class="container">
      <div class="report">
        <h2>AI 보고서</h2>
        <div class="divider"></div>
        <p class="report-content" v-html="formattedReportText"></p>
      </div>
      <div class="align-items: center;">
        <div class="recommendation">
          <h2>AI 추천 종목</h2>
          <div class="divider"></div>
          <div class="stock-info">
            <h3>{{ stock.name }}</h3>
            <p>{{ stock.price }}원</p>
            <div class="description-nav">
              <button @click="prevStock" class="nav-button">◀</button>
              <span class="news-contents">{{ stock.description }}</span>
              <button @click="nextStock" class="nav-button">▶</button>
            </div>
          </div>
        </div>
        <div class="recommendation">
          <h2>참고 뉴스</h2>
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
export default {
  name: "ReportPage",
  data() {
    return {
      reportText:
        "# 절세 보고서\n" +
        "안녕하세요, 고객님. 저는 대한민국의 증권 계좌를 통한 절세 도우미입니다. 고객님의 계좌 정보를 분석한 결과를 바탕으로 절세 전략을 제안드리고자 합니다. 아래의 내용을 참고해 주시기 바랍니다.\n\n" +
        "## 1. 연금저축계좌/IRP\n" +
        "연금저축계좌와 IRP는 고객님의 장기적인 자산 운용에 도움이 될 수 있는 계좌입니다. 이 계좌들에 납입하신 금액은 소득세에서 공제받을 수 있어, 세금 절약에 큰 도움이 됩니다.\n" +
        "현재 고객님께서는 **연금저축계좌에 530만원**, **IRP에 150만원**을 추가로 납입하시면 최대한의 세액 공제를 받을 수 있습니다. 이 금액을 납입하시면 고객님의 소득세 부담을 크게 줄일 수 있을 것입니다.\n\n" +
        "## 2. ISA 계좌\n" +
        "ISA 계좌는 고객님의 자산을 효율적으로 관리하고 세금을 절약할 수 있는 좋은 도구입니다. 현재 고객님의 ISA 계좌에서는 **570만원의 수익**을 얻으셨고, 이로 인해 **709,500원의 세금**을 절약하셨습니다. 이 계좌를 통해 고객님의 자산 운용이 효율적으로 이루어지고 있음을 알 수 있습니다.\n\n" +
        "## 3. 해외주식 양도소득세 계산\n" +
        "해외 주식 투자는 고수익을 기대할 수 있지만, 동시에 세금 부담도 커질 수 있습니다. 현재 고객님의 해외 주식 손익통산 금액은 **330만원**입니다. 이를 통해 고객님의 해외 주식 매도 전략을 '손실 중인 종목 매도'로 설정하였습니다. 이 전략을 통해 고객님의 세금 부담을 줄일 수 있을 것입니다.\n\n" +
        "이상의 내용을 바탕으로 고객님의 절세 전략을 수립하시는 데 도움이 되었기를 바랍니다. 각 계좌별로 세부적인 전략을 수립하시고, 필요한 경우 전문가의 도움을 받으시는 것도 좋은 방법입니다. 감사합니다.",
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
      return this.reportText.replace(/\n/g, "<br>");
    },
  },
  methods: {
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

.report {
  width: 1500px;
  padding: 20px;
  border-right: 1px solid #ccc;
}

.report-content {
  font-size: 1.2rem;
  height: 90%; /* 원하는 높이 설정 */
  overflow-y: auto; /* 세로 방향으로 스크롤 가능 */
  text-overflow: ellipsis; /* 넘치는 텍스트는 생략 표시 */
}

.recommendation {
  width: 600px;
  padding: 20px;
  font-size: 1.2rem;
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
</style>
