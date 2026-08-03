<template>
  <div class="container mt-5">

    <div class="card shadow">
      <div class="card-body">

        <h2>Dashboard</h2>

        <hr>

        <h5>Welcome {{ user.name }}</h5>

        <p><strong>ID:</strong> {{ user.id }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Role:</strong> {{ user.role }}</p>

        <hr>

        <div class="mb-3">

          <!-- USER -->

          <template v-if="user.role === 'user'">

            <button
              class="btn btn-link p-0 me-3"
              @click="activeTab = 'treks'"
            >
              Treks
            </button>

            <button
              class="btn btn-link p-0"
              @click="activeTab = 'bookings'"
            >
              My Bookings
            </button>

          </template>

          <!-- ADMIN -->

          <template v-else-if="user.role === 'admin'">

            <button
              class="btn btn-link p-0 me-3"
              @click="activeTab = 'treks'"
            >
              Treks
            </button>

            <button
              class="btn btn-link p-0 me-3"
              @click="activeTab = 'bookings'"
            >
              Bookings
            </button>

            <button
              class="btn btn-link p-0"
              @click="activeTab = 'staff'"
            >
              Staff
            </button>

          </template>

          <!-- STAFF -->

          <template v-else-if="user.role === 'staff'">

            <button
              class="btn btn-link p-0"
              @click="activeTab = 'stafftreks'"
            >
              Assigned Treks
            </button>

          </template>

        </div>

        <!-- USER -->

        <UserTreks
          v-if="user.role === 'user' && activeTab === 'treks'"
          :treks="treks"
        />

        <MyBookings
          v-if="user.role === 'user' && activeTab === 'bookings'"
          :bookings="bookings"
        />

        <!-- ADMIN -->

        <AdminTreks
          v-if="user.role === 'admin' && activeTab === 'treks'"
          :treks="treks"
          @trek-added="loadTreks"
        />

        <AdminBookings
          v-if="user.role === 'admin' && activeTab === 'bookings'"
          :bookings="bookings"
          @booking-updated="loadBookings"
        />

        <AdminStaff
          v-if="user.role === 'admin' && activeTab === 'staff'"
        />

        <!-- STAFF -->

        <StaffTreks
          v-if="user.role === 'staff' && activeTab === 'stafftreks'"
        />

        <button
          class="btn btn-link p-0 mt-4"
          @click="logout"
        >
          Logout
        </button>

      </div>
    </div>

  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

import UserTreks from '../components/UserTreks.vue'
import MyBookings from '../components/MyBookings.vue'
import AdminTreks from '../components/AdminTreks.vue'
import AdminBookings from '../components/AdminBookings.vue'
import AdminStaff from '../components/AdminStaff.vue'
import StaffTreks from '../components/StaffTreks.vue'

const router = useRouter()

const user = ref({})
const treks = ref([])
const bookings = ref([])

const activeTab = ref("")

const logout = () => {

  localStorage.removeItem("token")
  router.push("/login")

}

const loadTreks = async () => {

  const response = await api.get("/treks")
  treks.value = response.data

}

const loadBookings = async () => {

  if (user.value.role === "admin") {

    const response = await api.get("/allbookings")
    bookings.value = response.data

  }

  else if (user.value.role === "user") {

    const response = await api.get("/mybookings")
    bookings.value = response.data

  }

}

onMounted(async () => {

  try {

    const profileResponse = await api.get("/profile")
    user.value = profileResponse.data

    if (user.value.role !== "staff") {

      activeTab.value = "treks"

    }

    await loadTreks()
    await loadBookings()

  }

  catch (error) {

    console.log(error.response?.data || error)

  }

})
</script>