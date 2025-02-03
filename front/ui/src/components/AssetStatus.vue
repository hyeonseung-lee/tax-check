<template>
  <div class="asset-status">
    <h2 class="title">자산 현황</h2>
    <div class="status-info">
      <p class="total-value">총 평가 금액: {{ assets.totalValue }} 원</p>
      <p class="total-profit-loss">
        총 평가 손익: {{ assets.totalProfitLoss }} 원
      </p>
    </div>
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
  background-color: #ed6d1e; /* 주황색 배경 */
  border-radius: 10px; /* 테두리 둥글게 */
  padding: 15px; /* 내부 여백 */
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* 그림자 추가 */
  margin-bottom: 20px; /* 아래쪽 여백 */
  color: white; /* 글씨를 하얀색으로 */
}
.title {
  text-align: left; /* 제목 좌측 정렬 */
  margin: 0; /* 기본 여백 제거 */
}

.status-info {
  text-align: right; /* 나머지 정보 우측 정렬 */
}

.total-value,
.total-profit-loss {
  margin: 5px 0; /* 각 항목의 여백 */
}
</style>
