<template>
  <div class="main">
    <AssetStatus :assets="assets" />
    <div class="account-list">
      <h2>내 계좌 목록</h2>
      <AccountCard
        v-for="(account, index) in accounts"
        :key="index"
        :account="account"
      />
    </div>
  </div>
</template>

<script>
import AssetStatus from "./AssetStatus.vue"; // 자산 현황 컴포넌트
import AccountCard from "./AccountCard.vue"; // 계좌 카드 컴포넌트

export default {
  name: "MainPage",
  components: {
    AssetStatus,
    AccountCard,
  },
  data() {
    return {
      assets: {
        totalValue: 1000000, // 서버에서 가져올 값
        totalProfitLoss: 200000, // 서버에서 가져올 값
      },
      accounts: [
        {
          type: "연금저축펀드",
          totalProfitLoss: 50000,
          totalPurchaseAmount: 300000,
          totalEvaluationAmount: 350000,
        },
        {
          type: "ISA",
          totalProfitLoss: 80000,
          totalPurchaseAmount: 400000,
          totalEvaluationAmount: 480000,
        },
        {
          type: "IRP",
          totalProfitLoss: 30000,
          totalPurchaseAmount: 200000,
          totalEvaluationAmount: 230000,
        },
      ],
    };
  },
};
</script>

<style scoped>
.main {
  padding: 20px;
}
.account-list {
  margin-top: 20px;
}
</style>
