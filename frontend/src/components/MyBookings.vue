<template>
  <div>

    <h4>My Bookings</h4>
    <button
      class="btn btn-primary mb-3"
      @click="emit('export')"
    >
      Export Booking History
    </button>
    <ul class="list-group">

      <li
        v-for="booking in bookings"
        :key="booking.booking_id"
        class="list-group-item"
      >

        <strong>{{ booking.trek_name }}</strong>

        <br>

        Booking Date :
        {{
          new Date(booking.booking_date).toLocaleDateString(
            "en-GB"
          )
        }}

        <br>

        Status : {{ booking.status }}

      </li>

    </ul>

  </div>
</template>

<script setup>
defineProps({
  bookings: Array
})

const emit = defineEmits(["export"])
</script>