<template>
  <div class="main">
    <h2 class="account-title">절세 전략 보고서</h2>
    <div class="divider"></div>
    <div class="container">
      <div class="report">
        <h2>AI 보고서</h2>
        <div class="divider"></div>
        <p>{{ reportText }}</p>
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
              <span>{{ stock.description }}</span>
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
              <span>{{ news.description }}</span>
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
        "삼성전자는 현재 주가 하락과 함께 여러 도전 과제에 직면해 있지만, 일부 전문가들은 향후 실적 개선을 기대하고 있습니다. 목표 주가는 75,000원으로 설정되었으며, 저점 매수 기회를 노리는 전략이 권장되고 있습니다. 삼성전자의 주식은 여전히 투자자들에게 주목받고 있으며, 향후 시장 상황에 따라 변동성이 클 것으로 예상됩니다. 삼성전자의 주식에 대한 분석은 복잡하지만, 현재의 시장 상황과 전문가 의견을 종합적으로 고려할 때, 신중한 접근이 필요합니다.",
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
            "LG전자는 현재 주가 하락과 함께 여러 도전 과제에 직면해 있지만, 일부 전문가들은 향후 실적 개선을 기대하고 있습니다.",
        },
        // 추가 종목을 여기에 추가
      ],
      currentIndex: 0,
      news: {
        name: "삼성전자",
        description:
          "삼성전자는 현재 주가 하락과 함께 여러 도전 과제에 직면해 있지만, 일부 전문가들은 향후 실적 개선을 기대하고 있습니다.",
      },
      newses: [
        {
          name: "삼성전자",
          description:
            "삼성전자는 현재 주가 하락과 함께 여러 도전 과제에 직면해 있지만, 일부 전문가들은 향후 실적 개선을 기대하고 있습니다.",
        },
        {
          name: "LG전자",
          description:
            "LG전자는 현재 주가 하락과 함께 여러 도전 과제에 직면해 있지만, 일부 전문가들은 향후 실적 개선을 기대하고 있습니다.",
        },
        // 추가 종목을 여기에 추가
      ],
      currentIndexNews: 0,
    };
  },
  methods: {
    prevStock() {
      if (this.currentIndex === 0) {
        // 현재 인덱스가 0일 때 가장 마지막 인덱스로 이동
        this.currentIndex = this.stocks.length - 1;
      } else {
        this.currentIndex--;
      }
      this.updateStock();
    },
    nextStock() {
      if (this.currentIndex === this.stocks.length - 1) {
        // 현재 인덱스가 마지막일 때 가장 처음 인덱스로 이동
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
        // 현재 인덱스가 0일 때 가장 마지막 인덱스로 이동
        this.currentIndexNews = this.newses.length - 1;
      } else {
        this.currentIndexNews--;
      }
      this.updateNews();
    },
    nextNews() {
      if (this.currentIndexNews === this.newses.length - 1) {
        // 현재 인덱스가 마지막일 때 가장 처음 인덱스로 이동
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

.recommendation {
  width: 100%;
  padding: 20px;
}

.stock-info {
  margin-bottom: 20px;
}

.description-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
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
</style>
