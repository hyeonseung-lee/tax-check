<template>
  <div class="asset-status">
    <h2>자산 현황</h2>
    <p>총 평가 금액: {{ assets.totalValue }} 원</p>
    <p>총 평가 손익: {{ assets.totalProfitLoss }} 원</p>
  </div>
</template>

<script>
export default {
  name: "AssetStatus",
  props: {
    assets: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped>
.asset-status {
  border: 1px solid #ccc;
  padding: 15px;
  margin-bottom: 20px;
}
</style>
