<template>
  <div>

    <h4>Users</h4>

    <input
      class="form-control mb-3"
      placeholder="Search User"
      v-model="search"
    >

    <ul class="list-group">

      <li
        v-for="user in filteredUsers"
        :key="user.id"
        class="list-group-item"
      >

        <strong>{{ user.name }}</strong>

        <br>

        {{ user.email }}

        <br>

        {{ user.active ? "Active" : "Inactive" }}

        <br><br>

        <button
          class="btn btn-link p-0"
          @click="toggleUser(user.id)"
        >
          {{ user.active ? "Deactivate" : "Activate" }}
        </button>

      </li>

    </ul>

  </div>
</template>

<script setup>
import { ref, computed } from "vue"
import api from "../services/api"

const props = defineProps({
  users: Array
})

const search = ref("")

const filteredUsers = computed(() => {

  return props.users.filter(user =>

    user.name.toLowerCase().includes(
      search.value.toLowerCase()
    )

  )

})

const toggleUser = async (id) => {

  try {

    const response = await api.put(`/users/${id}`)

    alert(response.data.message)

    const usersResponse = await api.get("/users")

    props.users.splice(
      0,
      props.users.length,
      ...usersResponse.data
    )

  }

  catch (error) {

    alert(error.response?.data?.message || "Failed")

  }

}
</script>