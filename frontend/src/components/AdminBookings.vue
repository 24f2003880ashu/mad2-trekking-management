<template>
  <div>

    <h4>Manage Bookings</h4>

    
    <ul class="list-group">

      <li
        v-for="booking in bookings"
        :key="booking.booking_id"
        class="list-group-item"
      >

        <strong>{{ booking.user_name }}</strong>

        <br>

        Trek : {{ booking.trek_name }}

        <br>

        Booking Date : {{ booking.booking_date }}

        <br>

        Status : {{ booking.status }}

        <br><br>
      <button
        class="btn btn-link p-0"
        @click="approveBooking(booking.booking_id)"
      >
        Approve
      </button>

      </li>

    </ul>

  </div>
</template>

<script setup>
import api from "../services/api"

const exportCSV = () => {

  window.open(
    "http://127.0.0.1:5000/export/bookings",
    "_blank"
  )

}

defineProps({
  bookings: Array
})

const emit = defineEmits(["booking-updated"])

const approveBooking = async (bookingId) => {

  try {

    const response = await api.put(`/approve/${bookingId}`)

    alert(response.data.message)

    emit("booking-updated")

  }

  catch (error) {

    alert(error.response?.data?.message || "Approval Failed")

  }

}
</script>