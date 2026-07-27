<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-5">

        <div class="card shadow">
          <div class="card-body">

            <h3 class="text-center mb-4">Login</h3>

            <form @submit.prevent="handleLogin">

              <div class="mb-3">
                <label class="form-label">Email</label>
                <input
                  type="email"
                  class="form-control"
                  placeholder="Enter email"
                  v-model="email"
                >
              </div>

              <div class="mb-3">
                <label class="form-label">Password</label>
                <input
                  type="password"
                  class="form-control"
                  placeholder="Enter password"
                  v-model="password"
                >
              </div>

              <button
                type="submit"
                class="btn btn-primary w-100"
              >
                Login
              </button>

            </form>

          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../services/api'

const email = ref('')
const password = ref('')

const handleLogin = async () => {
  try {
    const response = await api.post('/login', {
      email: email.value,
      password: password.value
    })

    localStorage.setItem("token", response.data.access_token)

    console.log(response.data)

  } catch (error) {
    console.log(error.response.data)
  }
}
</script>