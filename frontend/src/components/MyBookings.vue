<template>
  <div>

    <h4>My Bookings</h4>

    <ul class="list-group">

      <li
        v-for="booking in bookings"
        :key="booking.booking_id"
        class="list-group-item"
      >

        <strong>{{ booking.trek_name }}</strong>

        <br>

        Booking Date : {{ booking.booking_date }}

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

</script>