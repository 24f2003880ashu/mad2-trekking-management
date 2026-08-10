<template>
  <div>

    <h4>Available Treks</h4>

    <input
      class="form-control mb-3"
      type="text"
      placeholder="Search Trek"
      v-model="search"
    >

    <select
      class="form-select mb-3"
      v-model="difficultyFilter"
    >
      <option value="">All Difficulties</option>
      <option value="Easy">Easy</option>
      <option value="Moderate">Moderate</option>
      <option value="Hard">Hard</option>
    </select>

    <input
      class="form-control mb-3"
      type="text"
      placeholder="Filter by Location"
      v-model="locationFilter"
    >

    <input
      class="form-control mb-3"
      type="number"
      placeholder="Filter by Duration (Days)"
      v-model="durationFilter"
    >

    <ul class="list-group">

      <li
        v-for="trek in filteredTreks"
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

        <br><br>

        <button
          class="btn btn-link p-0"
          @click="bookTrek(trek.id)"
        >
          Book Trek
        </button>

      </li>

    </ul>

  </div>
</template>

<script setup>
import { ref, computed } from "vue"
import api from "../services/api"

const props = defineProps({
  treks: Array
})

const search = ref("")
const difficultyFilter = ref("")
const locationFilter = ref("")
const durationFilter = ref("")

const filteredTreks = computed(() => {

  return props.treks.filter(trek => {

    const nameMatch =
      trek.name.toLowerCase().includes(
        search.value.toLowerCase()
      )

    const difficultyMatch =
      difficultyFilter.value === "" ||
      trek.difficulty === difficultyFilter.value

    const locationMatch =
      trek.location.toLowerCase().includes(
        locationFilter.value.toLowerCase()
      )

    const durationMatch =
      durationFilter.value === "" ||
      trek.duration == durationFilter.value

    return (
      nameMatch &&
      difficultyMatch &&
      locationMatch &&
      durationMatch
    )

  })

})

const bookTrek = async (trekId) => {

  try {

    const response = await api.post(`/book/${trekId}`)

    alert(response.data.message)

  }

  catch (error) {

    if (error.response) {

      alert(error.response.data.message)

    }

    else {

      alert("Server Error")

    }

  }

}
</script>