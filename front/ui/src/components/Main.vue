<template>
  <div class="main">
    <h2 class="account-title">내 자산 평가</h2>
    <div class="divider"></div>
    <FinanceSummary />
    <div class="account-list">
      <h2 class="account-title">내 계좌 목록</h2>
      <div class="divider"></div>
      <AccountCard
        v-for="(account, index) in accounts"
        :key="index"
        :account="account"
      />
    </div>
    <button class="tax-calculator" @click="calculateTax">절세 계산하기</button>
  </div>
</template>

<script>
import AccountCard from "./AccountCard.vue"; // 계좌 카드 컴포넌트
import FinanceSummary from "./FinanceSummary.vue";

export default {
  name: "MainPage",
  components: {
    AccountCard,
    FinanceSummary,
  },
  data() {
    return {
      assets: {
        totalValue: 1000000,
        totalProfitLoss: 200000,
      },
      accounts: [
        {
          type: "연금저축펀드",
          totalProfitLoss: 50000,
          totalPurchaseAmount: 300000,
          totalEvaluationAmount: 350000,
          items: [
            { name: "종목 A", value: 150000 },
            { name: "종목 B", value: 200000 },
          ],
        },
        {
          type: "ISA",
          totalProfitLoss: -80000,
          totalPurchaseAmount: 400000,
          totalEvaluationAmount: 320000,
          items: [
            { name: "종목 C", value: 250000 },
            { name: "종목 D", value: 150000 },
          ],
        },
        {
          type: "IRP",
          totalProfitLoss: 30000,
          totalPurchaseAmount: 200000,
          totalEvaluationAmount: 230000,
          items: [
            { name: "종목 E", value: 100000 },
            { name: "종목 F", value: 90000 },
          ],
        },
      ],
    };
  },
  methods: {
    calculateTax() {
      this.$router.push({ name: "Report" });
    },
  },
};
</script>

<style scoped>
.main {
  margin-top: 5px;
  padding: 20px;
  width: 40%;
  margin: 0 auto;
}
.account-list {
  margin-top: 20px;
  background-color: white;
}
.account-title {
  text-align: left; /* 좌측 정렬 */
  font-size: 1.25rem; /* 글자 크기 줄이기 */
  margin: 0; /* 기본 여백 제거 */
}
.divider {
  height: 2px; /* 줄의 두께 */
  background-color: #ed6d1e; /* 줄 색상 */
  margin: 10px 0; /* 위 아래 여백 */
}
.tax-calculator {
  position: fixed; /* 고정 위치 */
  bottom: 20px; /* 상단에서의 위치 */
  left: 50%; /* 왼쪽에서의 위치 */
  transform: translate(-50%, -50%); /* 버튼을 중앙으로 이동 */
  padding: 10px 20px;
  background-color: #ed6d1e; /* 버튼 색상 */
  color: white; /* 글자 색상 */
  border: none; /* 테두리 없음 */
  border-radius: 5px; /* 모서리 둥글게 */
  cursor: pointer; /* 커서 포인터 */
  z-index: 1000; /* 다른 요소 위에 표시 */
}
</style>
