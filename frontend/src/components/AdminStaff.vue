<template>
  <div>

    <h4>Add Staff</h4>

    <div class="mb-2">
      <input
        class="form-control"
        placeholder="Name"
        v-model="staff.name"
      >
    </div>

    <div class="mb-2">
      <input
        class="form-control"
        placeholder="Email"
        v-model="staff.email"
      >
    </div>

    <div class="mb-2">
      <input
        class="form-control"
        type="password"
        placeholder="Password"
        v-model="staff.password"
      >
    </div>

    <button
      class="btn btn-link p-0"
      @click="addStaff"
    >
      Add Staff
    </button>

    <hr>

    <hr>

    <h4>Staff List</h4>

    <input
      class="form-control mb-3"
      placeholder="Search Staff"
      v-model="search"
    >

    <ul class="list-group">

      <li
        v-for="item in filteredStaffs"
        :key="item.id"
        class="list-group-item"
      >

        <strong>{{ item.name }}</strong>

        <br>

        {{ item.email }}

        <br>

        {{ item.active ? "Active" : "Inactive" }}

        <br><br>

        <button
          class="btn btn-link p-0"
          @click="toggleStaff(item.id)"
        >
          {{ item.active ? "Deactivate" : "Activate" }}
        </button>

      </li>

    </ul>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue"
import api from "../services/api"

const staff = ref({
  name: "",
  email: "",
  password: ""
})

const staffs = ref([])
const search = ref("")
const filteredStaffs = computed(() => {

  return staffs.value.filter(item =>

    item.name.toLowerCase().includes(
      search.value.toLowerCase()
    )

  )

})

const loadStaff = async () => {

  try {

    const response = await api.get("/staff")

    staffs.value = response.data

  }

  catch (error) {

    console.log(error.response?.data || error)

  }

}

const toggleStaff = async (id) => {

  try {

    const response = await api.put(`/staff/${id}`)

    alert(response.data.message)

    loadStaff()

  }

  catch (error) {

    alert(error.response?.data?.message || "Failed")

  }

}

const addStaff = async () => {

  try {

    const response = await api.post("/staff", staff.value)

    alert(response.data.message)

    staff.value = {
      name: "",
      email: "",
      password: ""
    }

    loadStaff()

  }

  catch (error) {

    alert(error.response?.data?.message || "Failed")

  }

}

onMounted(() => {

  loadStaff()

})
</script>