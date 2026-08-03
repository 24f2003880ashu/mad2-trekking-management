<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-5">

        <div class="card shadow">
          <div class="card-body">

            <h3 class="text-center mb-4">Register</h3>

            <form @submit.prevent="handleRegister">

              <div class="mb-3">
                <label class="form-label">Name</label>
                <input
                  type="text"
                  class="form-control"
                  placeholder="Enter name"
                  v-model="name"
                >
              </div>

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
                class="btn btn-success w-100"
              >
                Register
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

const name = ref('')
const email = ref('')
const password = ref('')

const handleRegister = async () => {

  try {

    const response = await api.post('/register', {
      name: name.value,
      email: email.value,
      password: password.value
    })

    alert(response.data.message)

    router.push('/login')

  } catch (error) {

    alert(error.response?.data?.message || "Registration Failed")

  }

}
</script>