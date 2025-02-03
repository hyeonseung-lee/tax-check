<template>
  <div class="account-card">
    <h3>{{ account.type }}</h3>
    <p>총 평가 손익: {{ account.totalProfitLoss }} 원</p>
    <p>총 매입 금액: {{ account.totalPurchaseAmount }} 원</p>
    <p>총 평가 금액: {{ account.totalEvaluationAmount }} 원</p>
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
};
</script>

<style scoped>
.account-card {
  border: 1px solid #ccc;
  padding: 15px;
  margin-bottom: 10px;
}
</style>
