<template>

    <div class="alert alert-danger" role="alert" v-show="this.$store.getters.getError">
        {{ this.$store.getters.getError }}
    </div>

</template>

<script>

export default {
    name: 'ErrorMessage',
}
</script>