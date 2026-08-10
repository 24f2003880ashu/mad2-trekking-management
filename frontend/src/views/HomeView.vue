<template>
  <div class="container text-center d-flex flex-column justify-content-center" style="min-height: 80vh;">

    <h1 class="mb-3">Trekking Management App</h1>

    <p class="mb-4">
      Welcome to Trekking Management App
    </p>

    <div>
      <router-link
        to="/register"
        class="btn btn-link me-4"
      >
        Register
      </router-link>

      <router-link
        to="/login"
        class="btn btn-link"
      >
        Login
      </router-link>
    </div>

  </div>
</template>