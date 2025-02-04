<template>
  <div class="report-history">
    <h2>내 절세전략 목록</h2>
    <div v-for="(item, index) in history" :key="index" class="report-item">
      <v-card :title="item.created_at" @click="calculateTax"></v-card>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ReportHistory",
  data() {
    return {
      history: [], // 초기화된 빈 배열
    };
  },
  mounted() {
    this.fetchHistory();
  },
  methods: {
    fetchHistory() {
      axios
        .get("http://221.168.39.188:8000/")
        .then((response) => {
          console.log(response);
          this.history = response.data.history
            .map((item) => {
              // created_at이 존재하는지 검증
              const dateOnly = item.created_at
                ? item.created_at.split("T")[0]
                : "날짜 없음"; // 'YYYY-MM-DD' 형식으로 변환 또는 기본값 설정
              return {
                ...item,
                created_at: dateOnly, // 날짜만 남긴 created_at
              };
            })
            .filter((item) => item.created_at !== "날짜 없음"); // created_at이 없으면 해당 항목 제거
        })
        .catch((error) => {
          console.error("API 호출 오류:", error);
        });
    },
    formatDate(dateString) {
      const options = {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      };
      return new Date(dateString).toLocaleString("ko-KR", options);
    },
    calculateTax() {
      this.$router.push({ name: "Report" });
    },
  },
};
</script>

<style scoped>
.report-history {
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  margin: 10px auto; /* 상하 여백 10px, 좌우 자동으로 중앙 정렬 */
  width: 60%;
  max-width: 800px; /* 최대 너비 설정 */
  text-align: center; /* 텍스트 중앙 정렬 */
}
.report-item {
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #eee;
  border-radius: 5px;
}
pre {
  white-space: pre-wrap; /* 줄 바꿈을 유지 */
  word-wrap: break-word; /* 긴 단어 줄 바꿈 */
}
</style>
