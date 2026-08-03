<template>
  <main>
    <h1>Student Profile</h1>

    <h2>Enrolled Courses</h2>

    <p v-if="store.enrolledCourses.length === 0">
      You have not enrolled in any courses yet.
    </p>

    <div v-else>
      <div
        v-for="course in store.enrolledCourses"
        :key="course.id"
        class="enrolled-course"
      >
        <h3>{{ course.name }}</h3>

        <p><strong>Course Code:</strong> {{ course.code }}</p>
        <p><strong>Credits:</strong> {{ course.credits }}</p>
        <p><strong>Grade:</strong> {{ course.grade }}</p>
        <button @click="store.unenroll(course.id)">
        Unenroll
        </button>
      </div>

      <h3>
        Total Credits: {{ store.totalCredits }}
      </h3>
    </div>
  </main>
</template>

<script setup>
import { useEnrollmentStore } from '../stores/enrollment'

const store = useEnrollmentStore()
</script>

<style scoped>
main {
  padding: 40px;
}

h1 {
  margin-bottom: 25px;
}

h2 {
  margin-bottom: 15px;
}

.enrolled-course {
  max-width: 500px;
  margin: 15px 0;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: white;
}

.enrolled-course h3 {
  margin-bottom: 12px;
}

.enrolled-course p {
  margin: 7px 0;
}

button {
  margin-top: 12px;
  padding: 8px 14px;
  border: none;
  border-radius: 6px;
  background-color: #333;
  color: white;
  cursor: pointer;
}

button:hover {
  opacity: 0.85;
}
</style>