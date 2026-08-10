<template>
  <div>

    <h4>Update Profile</h4>

    <div class="mb-2">
      <input
        class="form-control"
        placeholder="Name"
        v-model="profile.name"
      >
    </div>

    <div class="mb-2">
      <input
        class="form-control"
        placeholder="Email"
        v-model="profile.email"
      >
    </div>

    <button
      class="btn btn-link p-0"
      @click="updateProfile"
    >
      Update Profile
    </button>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import api from "../services/api"

const emit = defineEmits(["profileUpdated"])

const profile = ref({
  name: "",
  email: ""
})

onMounted(async () => {

  const response = await api.get("/profile")

  profile.value = response.data

})

const updateProfile = async () => {

  try {

    const response = await api.put(
      "/profile",
      profile.value
    )

    alert(response.data.message)

    emit("profileUpdated")

  }

  catch (error) {

    alert(error.response?.data?.message || "Failed")

  }

}
</script>