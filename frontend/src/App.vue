<template>
  <NavBar> </NavBar>
  <ErrorMessage></ErrorMessage>
  <div id="viewele">
    <router-view> </router-view>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
import ErrorMessage from '@/components/ErrorMessage.vue'

export default {
  name: "App",
  components: {
    NavBar,
    ErrorMessage
  }
} 
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #313131;
  opacity: 60;
}

#viewele {
  margin-top: 3em;
  display: flex;
  justify-content: center;
}
</style>
