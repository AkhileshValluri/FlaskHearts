<template>
    <div class="card" style="width: 30rem;" styl="justf">
        <div class="card-body">
            <div class="card-title">
                <div class="btn-group" role="group" aria-label="Basic example">
                    <button type="button" class="btn btn-outline-info" v-on:click="changeSeen(false)">Sign In</button>
                    <button type="button" class="btn btn-outline-info" v-on:click="changeSeen(true)">Sign Up</button>
                </div>
            </div>
            <h6 class="card-subtitle mb-2 text-muted" v-show="this.newUser">Make a new account to start your journey
            </h6>
            <h6 class="card-subtitle mb-2 text-muted" v-show="!this.newUser">Welcome back</h6>
            <p class="card-text">

            <div class="input-group mb-3">
                <input type="text" class="form-control" placeholder="Username" aria-label="Username"
                    v-model="this.username">
                <span class="input-group-text">@</span>

            </div>
            <div class="input-group mb-3" v-show="newUser">
                <span class="input-group-text">+91</span>
                <input type="text" class="form-control" aria-label="Phone Number" v-model="this.phoneNumber">
            </div>

            <div class="input-group mb-3" v-show="newUser">
                <input type="text" class="form-control" placeholder="Your Gmail" aria-label="Recipient's username"
                    aria-describedby="basic-addon2" v-model="this.email">
                <span class="input-group-text" id="basic-addon2">@gmail.com</span>
            </div>

            <div class="input-group mb-3" v-show="newUser">
                <div class="form-group">
                    <input type="password" class="form-control" id="password" placeholder="Password"
                        v-model="this.password">
                </div>
                <div class="form-group">
                    <input type="password" class="form-control" id="confimpasword" placeholder="Confirm"
                        v-model="this.confirmPassword">
                </div>
            </div>
            <input type="password" class="form-control " id="login" placeholder="Enter password" v-model="password" />
            <button class="btn btn-outline-success" type="button" v-on:click="onSubmit"> Continue </button>

            </p>
        </div>
    </div>
</template>

<script>

export default {
    name: 'LoginView',
    data() {
        return {
            newUser: false,
            username: '',
            phoneNumber: '',
            email: '',
            password: '',
            confirmPassword: '',
        }
    },
    methods: {
        changeSeen(val) {
            this.newUser = val
        },
        onSubmit() {

        }
    }
}
</script>

<style>
button {
    margin-top: 1em;
    margin-bottom: 1em;
}
</style>