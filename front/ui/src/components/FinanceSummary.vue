<template>
  <div class="finance-card">
    <!-- Total Profit/Loss Section -->
    <div class="profit-loss-section border-bottom">
      <div class="profit-loss-amount">
        <h2 class="label">총 손익</h2>
        <div>
          <span :class="['amount', profitLossColor]">
            {{ prefixMinus(totalProfitLoss)
            }}{{ formatCurrency(Math.abs(totalProfitLoss)) }}원
          </span>
          <span :class="['percentage', profitLossColor]">
            {{ prefixMinus(profitLossPercent)
            }}{{ Math.abs(profitLossPercent) }}%
          </span>
        </div>
      </div>
    </div>

    <!-- Main Information Grid -->
    <div class="info-grid">
      <div class="info-item border-right border-bottom">
        <div class="info-label">총 매입</div>
        <div class="info-value">{{ formatCurrency(totalPurchase) }}</div>
      </div>
      <div class="info-item border-bottom">
        <div class="info-label">총 평가</div>
        <div class="info-value">{{ formatCurrency(totalValue) }}</div>
      </div>
      <div class="info-item border-right">
        <div class="info-label">실현손익</div>
        <div class="info-value">{{ formatCurrency(realizedProfitLoss) }}</div>
      </div>
      <div class="info-item">
        <div class="info-label">추정자산</div>
        <div class="info-value">{{ formatCurrency(estimatedAssets) }}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "FinanceSummary",
  data() {
    return {
      totalProfitLoss: 8300000,
      totalPurchase: 39900000,
      totalValue: 48200000,
      realizedProfitLoss: 0,
      estimatedAssets: 48200000,
    };
  },
  computed: {
    profitLossPercent() {
      return ((this.totalProfitLoss / this.totalPurchase) * 100).toFixed(2);
    },
    profitLossColor() {
      return this.totalProfitLoss < 0 ? "negative" : "positive";
    },
  },
  methods: {
    formatCurrency(value) {
      return new Intl.NumberFormat("ko-KR").format(value);
    },
    prefixMinus(value) {
      return value < 0 ? "-" : "";
    },
  },
};
</script>

<style scoped>
.finance-card {
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.profit-loss-amount {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 8px;
}

.amount {
  font-size: 20px;
  font-weight: 600;
}

.percentage {
  font-size: 18px;
  font-weight: 500;
}

.negative {
  color: #1a73e8;
}

.positive {
  color: #d93025;
}

.arrow {
  color: #666;
  font-size: 14px;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
}

.info-item {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.border-right {
  border-right: 3px solid #e0e0e0;
}

.border-bottom {
  border-bottom: 3px solid #e0e0e0;
}

.info-label {
  color: #666;
  font-size: 14px;
}

.info-value {
  font-size: 16px;
  font-weight: 500;
  color: #333;
}
</style>
