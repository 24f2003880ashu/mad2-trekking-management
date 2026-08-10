<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-5">

        <div class="card shadow">
          <div class="card-body">

            <h3 class="text-center mb-4">Login</h3>

            <div
              v-if="message"
              class="alert alert-danger"
            >
              {{ message }}
            </div>

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
                  class="btn btn-link"
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
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()

const email = ref('')
const password = ref('')
const message = ref('')

const handleLogin = async () => {
  try {

    message.value = ''

    const response = await api.post('/login', {
      email: email.value,
      password: password.value
    })

    localStorage.setItem("token", response.data.access_token)

    router.push('/dashboard')

  } catch (error) {

    if (error.response) {
      message.value = error.response.data.message
    } else {
      message.value = "Something went wrong"
    }

  }
}
</script>