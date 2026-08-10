<template>
  <div>

    <h4>Manage Treks</h4>

    <button
      class="btn btn-link p-0 mb-3"
      @click="showCreateForm = !showCreateForm"
    >
      {{ showCreateForm ? "Hide Create Trek" : "Create Trek" }}
    </button>

    <div v-if="showCreateForm || editMode">

      <h5>{{ editMode ? "Update Trek" : "Create Trek" }}</h5>

      <div class="mb-2">
        <input
          class="form-control"
          placeholder="Trek Name"
          v-model="trek.name"
        >
      </div>

      <div class="mb-2">
        <input
          class="form-control"
          placeholder="Location"
          v-model="trek.location"
        >
      </div>

      <div class="mb-2">
        <select
          class="form-control"
          v-model="trek.difficulty"
        >
          <option disabled value="">
            Select Difficulty
          </option>
          <option>Easy</option>
          <option>Moderate</option>
          <option>Hard</option>
        </select>
      </div>
      <div class="mb-2">
        <select
          class="form-control"
          v-model="trek.assigned_staff_id"
        >
          <option :value="null">
            Select Staff
          </option>

          <option
            v-for="staff in staffs"
            :key="staff.id"
            :value="staff.id"
          >
            {{ staff.name }}
          </option>
        </select>
      </div>

      <div class="mb-2">
        <input
          class="form-control"
          type="number"
          placeholder="Duration"
          v-model="trek.duration"
        >
      </div>

      <div class="mb-2">
        <input
          class="form-control"
          type="number"
          placeholder="Available Slots"
          v-model="trek.available_slots"
        >
      </div>

      <div class="mb-2">
        <input
          class="form-control"
          type="date"
          v-model="trek.start_date"
        >
      </div>

      <div class="mb-2">
        <input
          class="form-control"
          type="date"
          v-model="trek.end_date"
        >
      </div>

      <button
        class="btn btn-link p-0 me-3"
        @click="saveTrek"
      >
        {{ editMode ? "Update Trek" : "Add Trek" }}
      </button>

      <button
        v-if="editMode"
        class="btn btn-link p-0"
        @click="cancelEdit"
      >
        Cancel
      </button>

    </div>

    <hr>

    <input
      class="form-control mb-3"
      type="text"
      placeholder="Search Trek"
      v-model="search"
    >

    <ul class="list-group">

      <li
        v-for="trekItem in filteredTreks"
        :key="trekItem.id"
        class="list-group-item"
      >

        <strong>{{ trekItem.name }}</strong>

      <br>

      Location : {{ trekItem.location }}

      <br>

      Difficulty : {{ trekItem.difficulty }}

      <br>

      Duration : {{ trekItem.duration }} Days

      <br>

      Available Slots : {{ trekItem.available_slots }}

      <br>

      Status : {{ trekItem.status }}

      <br>

      Assigned Staff : {{ trekItem.assigned_staff }}

      <br>

      Start Date : {{ trekItem.start_date }}

      <br>

      End Date : {{ trekItem.end_date }}

        <div class="mt-2">

          <button
            class="btn btn-link p-0 me-3"
            @click="editTrek(trekItem)"
          >
            Edit
          </button>

          <button
            class="btn btn-link p-0"
            @click="deleteTrek(trekItem.id)"
          >
            Delete
          </button>

        </div>

      </li>

    </ul>

  </div>
</template>

<script setup>
import { ref, computed , onMounted } from 'vue'
import api from '../services/api'

const props = defineProps({
  treks: Array
})

const emit = defineEmits(['trek-added'])
const staffs = ref([])

const search = ref("")

const showCreateForm = ref(false)

const emptyTrek = () => ({
  id: null,
  name: '',
  location: '',
  difficulty: '',
  duration: '',
  available_slots: '',
  status: 'Upcoming',
  start_date: '',
  end_date: '' ,
  assigned_staff_id: null

})

const trek = ref(emptyTrek())

const editMode = ref(false)

const filteredTreks = computed(() => {

  return props.treks.filter(trek =>

    trek.name.toLowerCase().includes(
      search.value.toLowerCase()
    )

  )

})

const resetForm = () => {

  trek.value = emptyTrek()

  editMode.value = false

  showCreateForm.value = false

}
const loadStaffs = async () => {

  try {

    const response = await api.get("/staff")

    staffs.value = response.data

  }

  catch (error) {

    console.log(error.response?.data || error)

  }

}

const saveTrek = async () => {

  try {

    if (editMode.value) {

      await api.put(
        `/treks/${trek.value.id}`,
        trek.value
      )

      if (trek.value.assigned_staff_id) {

        await api.put(
          `/assign/${trek.value.id}`,
          {
            staff_id: trek.value.assigned_staff_id
          }
        )

      }

      alert("Trek Updated Successfully")

    } else {

      const response = await api.post(
        "/treks",
        trek.value
      )

      if (trek.value.assigned_staff_id) {

        await api.put(
          `/assign/${response.data.id}`,
          {
            staff_id: trek.value.assigned_staff_id
          }
        )

      }

      alert("Trek Added Successfully")

    }

    emit("trek-added")
    resetForm()

  } catch (error) {

    alert(
      error.response?.data?.message ||
      "Something went wrong"
    )

  }

}

const editTrek = (item) => {

  trek.value = { ...item }

  editMode.value = true

  showCreateForm.value = true

}

const cancelEdit = () => {

  resetForm()

}

const deleteTrek = async (id) => {

  if (!confirm("Delete this trek?")) return

  try {

    await api.delete(`/treks/${id}`)

    alert("Trek Deleted Successfully")

    emit("trek-added")

  }

  catch (error) {

    alert(
      error.response?.data?.message ||
      "Something went wrong"
    )

  }

}

onMounted(() => {

  loadStaffs()

})
</script>