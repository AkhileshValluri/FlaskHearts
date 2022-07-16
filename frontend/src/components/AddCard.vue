<template>
    <span style="width: 100%;">

        <div class="card mx-5" style=" background-color:whitesmoke; width:33%; display:flex; justify-content: center; ">
            <div class="card-body">
                <h3 class="card-title">Add to {{ did }}</h3>
                <p class="card-text">
                <div class="input-group input-group-sm mb-3">
                    <div style="width:100%">
                        <input type="text" class="form-control" placeholder="Front" aria-describedby="basic-addon1"
                            v-model="front" style="text-align:center">
                    </div>
                    <div style="width:100%">
                        <input type="text" class="form-control" placeholder="Back" aria-describedby="basic-addon1"
                            v-model="back" style="text-align:center">
                    </div>
                </div>
                </p>
            </div>
            <button type="button" class="btn btn-outline-success" v-on:click="onSubmit()">Add</button>
        </div>
    </span>

</template>

<script>

import { mapActions } from 'vuex'
const axios = require('axios')


export default {
    name: 'AddCard',
    data() {
        return {
            front: '',
            back: '',
        }
    },
    methods: {
        ...mapActions({
            AddCard: 'AddCard'
        }),
        onSubmit() {
            if (!this.front || !this.back) return;

            this.AddCard({
                'front': this.front,
                'back': this.back,
                'deck_id': this.did
            })
        }
    },
    props: ['did']
}
</script>