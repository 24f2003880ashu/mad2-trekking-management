<template>
  <div>

    <h4>Assigned Treks</h4>

    <ul class="list-group">

      <li
        v-for="trek in treks"
        :key="trek.id"
        class="list-group-item"
      >

        <strong>{{ trek.name }}</strong>

        <br>

        {{ trek.location }}

        <br>

        Difficulty : {{ trek.difficulty }}

        <br>

        Duration : {{ trek.duration }} Days

        <br>

        Slots : {{ trek.available_slots }}

        <br>

        Status : {{ trek.status }}

        <br>

        Participants : {{ trek.participant_count }}

        <br>

        <button
          v-if="editId !== trek.id"
          class="btn btn-link p-0 me-3"
          @click="editId = trek.id"
        >
          Edit
        </button>

        <button
          class="btn btn-link p-0"
          @click="viewParticipants(trek.id)"
        >
          Participants
        </button>

        <div v-if="editId === trek.id">

          <br><br>

          <label>Available Slots</label>

          <input
            class="form-control mb-2"
            type="number"
            v-model="trek.available_slots"
          >

          <label>Status</label>

          <select
            class="form-control mb-2"
            v-model="trek.status"
          >
            <option>Upcoming</option>
            <option>Open</option>
            <option>Closed</option>
            <option>Completed</option>
          </select>

          <button
            class="btn btn-link p-0 me-3"
            @click="updateTrek(trek)"
          >
            Update
          </button>

          <button
            class="btn btn-link p-0"
            @click="editId = null"
          >
            Cancel
          </button>

        </div>

        <div
          v-if="participantTrekId === trek.id"
          class="mt-3"
        >

          <h6>Participants</h6>

          <ul>

            <li
              v-for="participant in participants"
              :key="participant.id"
            >

              {{ participant.name }}

              -

              {{ participant.email }}

              -

              {{ participant.status }}

            

            </li>

          </ul>

        </div>

      </li>

    </ul>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import api from "../services/api"

const treks = ref([])

const editId = ref(null)

const participants = ref([])

const participantTrekId = ref(null)

const loadTreks = async () => {

  try {

    const response = await api.get("/staff/treks")

    treks.value = response.data

  }

  catch (error) {

    console.log(error.response?.data || error)

  }

}

const updateTrek = async (trek) => {

  try {

    const response = await api.put(`/staff/treks/${trek.id}`, {

      available_slots: trek.available_slots,
      status: trek.status

    })

    alert(response.data.message)

    editId.value = null

    loadTreks()

  }

  catch (error) {

    alert(error.response?.data?.message || "Update Failed")

  }

}

const viewParticipants = async (trekId) => {

  try {

    const response = await api.get(`/staff/treks/${trekId}/participants`)

    participants.value = response.data

    participantTrekId.value = trekId

  }

  catch (error) {

    alert(error.response?.data?.message || "Failed")

  }

}

onMounted(() => {

  loadTreks()

})

</script>