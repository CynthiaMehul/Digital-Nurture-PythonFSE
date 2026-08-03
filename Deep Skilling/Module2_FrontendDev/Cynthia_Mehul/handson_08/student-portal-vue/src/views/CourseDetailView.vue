<template>
  <main>
    <h1>Course Details</h1>

    <div v-if="course" class="course-details">
      <h2>{{ course.name }}</h2>

      <p><strong>Course ID:</strong> {{ course.id }}</p>
      <p><strong>Course Code:</strong> {{ course.code }}</p>
      <p><strong>Credits:</strong> {{ course.credits }}</p>
      <p><strong>Grade:</strong> {{ course.grade }}</p>

      <button @click="enrollCourse">
        Enroll
      </button>
    </div>

    <p v-else>
      Course not found.
    </p>
  </main>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const courses = [
  {
    id: 1,
    name: 'Introduction to Vue',
    code: 'VUE101',
    credits: 4,
    grade: 'A'
  },
  {
    id: 2,
    name: 'JavaScript Fundamentals',
    code: 'JS201',
    credits: 3,
    grade: 'A+'
  },
  {
    id: 3,
    name: 'Database Management Systems',
    code: 'DBMS301',
    credits: 4,
    grade: 'B+'
  },
  {
    id: 4,
    name: 'Computer Networks',
    code: 'CN401',
    credits: 3,
    grade: 'A'
  },
  {
    id: 5,
    name: 'Machine Learning',
    code: 'ML501',
    credits: 4,
    grade: 'A+'
  }
]

const course = computed(() => {
  return courses.find(
    (course) => course.id === Number(route.params.id)
  )
})
function enrollCourse() {
  router.push('/profile')
}
</script>

<style scoped>
main {
  padding: 40px;
}

.course-details {
  max-width: 500px;
  margin-top: 25px;
  padding: 25px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: white;
}

.course-details h2 {
  margin-bottom: 20px;
}

.course-details p {
  margin: 10px 0;
}

button {
  margin-top: 20px;
  padding: 10px 18px;
  border: none;
  border-radius: 6px;
  background-color: #333;
  color: white;
  cursor: pointer;
  font-size: 16px;
}

button:hover {
  opacity: 0.85;
}
</style>