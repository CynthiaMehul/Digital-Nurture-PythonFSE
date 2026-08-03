<template>
  <main>
    <h1>Courses</h1>

    <p>Number of courses: {{ courses.length }}</p>

    <input
    v-model="searchTerm"
    type="text"
    placeholder="Search courses..."
  />

    <div class="courses-container">
      <div
        v-for="course in filteredCourses"
        :key="course.id"
        class="course-item"
      >
        <CourseCard
          :id="course.id"
          :name="course.name"
          :code="course.code"
          :credits="course.credits"
          :grade="course.grade"
        />

        <button @click="store.enroll(course)">
          Enroll
        </button>
      </div>
    </div>
  </main>
</template>

<script setup>
import { useEnrollmentStore } from '../stores/enrollment'
import { ref, onMounted, computed } from 'vue'
import CourseCard from '../components/CourseCard.vue'

const courses = ref([])
const searchTerm = ref('')
const store = useEnrollmentStore()

onMounted(() => {
  courses.value = [
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
})

const filteredCourses = computed(() => {
  return courses.value.filter((course) =>
    course.name.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
})

</script>

<style scoped>
main {
  padding: 40px;
}

h1 {
  margin-bottom: 15px;
}

.courses-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-top: 25px;
}
input {
  width: 300px;
  padding: 10px;
  margin-top: 15px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 16px;
}
.course-item {
  display: flex;
  flex-direction: column;
}

button {
  margin-top: 10px;
  padding: 10px;
  border: none;
  border-radius: 6px;
  background-color: #333;
  color: white;
  cursor: pointer;
  font-size: 15px;
}

button:hover {
  opacity: 0.85;
}
</style>