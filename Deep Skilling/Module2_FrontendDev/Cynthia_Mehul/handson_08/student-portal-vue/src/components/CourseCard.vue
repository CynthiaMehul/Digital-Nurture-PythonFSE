<template>
  <div class="course-card">
    <h2>{{ name }}</h2>

    <p><strong>Course Code:</strong> {{ code }}</p>
    <p><strong>Credits:</strong> {{ credits }}</p>
    <p><strong>Grade:</strong> {{ grade }}</p>

    <RouterLink :to="`/courses/${id}`">
      View Details
    </RouterLink>
  </div>
</template>

<script setup>
defineProps({
  id: Number,
  name: String,
  code: String,
  credits: Number,
  grade: String
})
</script>

<style scoped>
.course-card {
  width: 280px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: white;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.course-card h2 {
  margin-bottom: 15px;
}

.course-card p {
  margin: 8px 0;
}
</style>