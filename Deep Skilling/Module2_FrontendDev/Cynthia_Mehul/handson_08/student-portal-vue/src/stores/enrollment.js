import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useEnrollmentStore = defineStore('enrollment', () => {
  const enrolledCourses = ref([])

  const totalCredits = computed(() => {
    return enrolledCourses.value.reduce(
      (total, course) => total + course.credits,
      0
    )
  })

  function enroll(course) {
    const alreadyEnrolled = enrolledCourses.value.some(
      (enrolledCourse) => enrolledCourse.id === course.id
    )

    if (!alreadyEnrolled) {
      enrolledCourses.value.push(course)
    }
  }

  function unenroll(courseId) {
    enrolledCourses.value = enrolledCourses.value.filter(
      (course) => course.id !== courseId
    )
  }

  return {
    enrolledCourses,
    totalCredits,
    enroll,
    unenroll
  }
})