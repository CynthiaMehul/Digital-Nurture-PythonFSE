<template>
  <header>
    <div class="logo">
    <h2>Student Portal</h2>

    <span>
      Enrolled: {{ store.enrolledCourses.length }}
    </span>
  </div>

```
<nav>
  <RouterLink to="/">Home</RouterLink>
  <RouterLink to="/courses">Courses</RouterLink>
  <RouterLink to="/profile">Profile</RouterLink>
</nav>
```

  </header>
</template>

<script setup>
import { useEnrollmentStore } from '../stores/enrollment'

const store = useEnrollmentStore()
</script>

<style scoped>
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 30px;
  background-color: #f2f2f2;
}

nav {
  display: flex;
  gap: 20px;
}

a {
  color: #333;
  text-decoration: none;
}

.logo {
  display: flex;
  align-items: center;
  gap: 15px;
}

.logo span {
  padding: 5px 10px;
  border-radius: 15px;
  background-color: white;
  font-size: 14px;
}
</style>
