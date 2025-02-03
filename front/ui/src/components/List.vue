<template>
  <div class="main">
    <div class="card" v-for="item in results" :key="item.id">
      <p><strong>Date:</strong> {{ item.date }}</p>
      <p><strong>ID:</strong> {{ item.id }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "ListPage",
  data() {
    return {
      results: [
        { date: "2025-02-01", id: "23456" },
        { date: "2025-02-02", id: "23456" },
        { date: "2025-02-03", id: "23456" },
      ],
    };
  },
};
</script>

<style scoped>
/* 여기에 스타일을 추가하세요 */
.main {
  margin-top: 5px;
  padding: 20px;
  width: 40%;
  margin: 0 auto;
}
.card {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  margin: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
  width: 100%;
}

.card:hover {
  transform: translateY(-5px);
}

.card p {
  margin: 0;
  padding: 4px 0;
}

.card p strong {
  color: #333;
}
</style>
