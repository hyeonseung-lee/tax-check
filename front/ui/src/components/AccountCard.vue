<template>
  <div class="account-card">
    <div class="account-header">
      <h3>{{ account.type }}</h3>
      <button @click="toggleExpand">
        <span v-if="isExpanded">▲</span>
        <span v-else>▼</span>
      </button>
    </div>
    <div class="content">
      <div class="profit-content">
        <span>총 손익:</span>
        <span :class="[profitLossColor]"
          >{{ formatCurrency(account.totalProfitLoss) }} 원</span
        >
      </div>
      <div class="profit-content">
        <span>총 매입:</span>
        <span>{{ formatCurrency(account.totalPurchaseAmount) }} 원</span>
      </div>
      <div class="profit-content">
        <span>총 평가 손익:</span>
        <span>{{ formatCurrency(account.totalEvaluationAmount) }} 원</span>
      </div>
    </div>
    <div v-if="isExpanded" class="details">
      <div class="divider"></div>
      <h4 class="stocks-header">종목 정보</h4>
      <ul class="stocks">
        <li v-for="(item, index) in account.items" :key="index">
          <div class="stocks-content">
            <span>{{ item.name }}</span>
            <span>{{ formatCurrency(item.value) }} 원</span>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: "AccountCard",
  props: {
    account: {
      type: Object,
      required: true,
    },
  },
  computed: {
    profitLossColor() {
      return this.account.totalProfitLoss < 0 ? "negative" : "positive";
    },
  },
  data() {
    return {
      isExpanded: false, // 카드 확장 상태
    };
  },
  methods: {
    toggleExpand() {
      this.isExpanded = !this.isExpanded; // 상태 토글
    },
    formatCurrency(value) {
      return new Intl.NumberFormat("ko-KR").format(value);
    },
  },
};
</script>

<style scoped>
.account-card {
  border: 1px solid #ccc;
  margin-bottom: 10px;
  border-radius: 10px; /* 테두리 둥글게 */
}
.account-header {
  display: flex; /* 수평 정렬 */
  justify-content: space-between; /* 공간을 균등하게 분배 */
  align-items: center; /* 수직 중앙 정렬 */
  margin-left: 10px;
  margin-right: 10px;
}
.divider {
  height: 2px; /* 줄의 두께 */
  background-color: #ccc; /* 줄 색상 */
  margin: 0px 5px 0px 5px;
}
.content {
  text-align: right;
  margin-right: 10px;
  line-height: 25px;
}
.stocks {
  list-style-type: none;
}
.stocks-header {
  display: flex; /* 수평 정렬 */
  justify-content: space-between; /* 공간을 균등하게 분배 */
  align-items: center; /* 수직 중앙 정렬 */
  margin-left: 10px;
  margin-right: 10px;
}
.stocks-content {
  display: flex; /* 수평 정렬 */
  justify-content: space-between; /* 양쪽 끝으로 정렬 */
  width: 95%; /* 전체 너비 사용 */
  margin-left: 10px;
}
.profit-content {
  display: flex; /* 수평 정렬 */
  justify-content: space-between; /* 양쪽 끝으로 정렬 */
  width: 95%; /* 전체 너비 사용 */
  margin-left: 10px;
  margin-bottom: 5px;
}
.negative {
  color: #1a73e8;
}

.positive {
  color: #d93025;
}
</style>
