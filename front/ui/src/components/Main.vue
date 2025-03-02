<template>
  <div v-if="loading" class="loading-screen">로딩 중...</div>
  <div v-else>
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
      <button class="tax-calculator" @click="calculateTax">
        절세 계산하기
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios"; // axios를 사용하여 API 호출
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
      loading: true,
      assets: {
        totalValue: 1000000,
        totalProfitLoss: 200000,
      },
      accounts: [], // 초기에는 빈 배열로 설정
    };
  },
  methods: {
    async fetchAccounts() {
      try {
        const response = await axios.post("http://221.168.39.188:8000/login", {
          // 필요한 로그인 데이터
        });
        this.accounts = response.data.map((account) => ({
          type: account.account_category,
          totalProfitLoss: account.profit,
          totalPurchaseAmount: account.purchase,
          totalEvaluationAmount: account.balance,
          items: account.stocks.map((stock) => ({
            name: stock.stock_name,
            value: stock.valuation,
          })),
        }));
      } catch (error) {
        console.error("계좌 정보를 가져오는 데 실패했습니다.", error);
      }
    },
    calculateTax() {
      this.$router.push({ name: "Report" });
    },
  },
  mounted() {
    this.fetchAccounts(); // 컴포넌트가 마운트될 때 계좌 데이터 가져오기
    setTimeout(() => {
      this.loading = false; // 5초 후 로딩 상태 변경
    }, 5000);
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
.loading-screen {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* 전체 화면 높이 */
  font-size: 24px; /* 로딩 텍스트 크기 */
}
</style>
