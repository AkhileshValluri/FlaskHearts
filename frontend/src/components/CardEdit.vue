<template>
    <div class="input-group-sm mb-3">
        <div style="width:100%">
            <input type="text" class="form-control" placeholder="Name" aria-label="Front" v-model="front"
                style="text-align:center">
        </div>
        <br>
        <div style="width:100%">
            <input type="text" class="form-control" placeholder="Name" aria-label="Back" v-model="back"
                style="text-align:center">
        </div>
        <div class="d-grid gap-0" style="justify-content: center;">
            <button type="button" class="btn btn-outline-primary" v-on:click="onSubmit()"
                style="width:100%">Edit</button>
        </div>
    </div>

</template>

<script>
import { mapActions } from 'vuex'

export default {
    name: 'CardEdit',
    data() {
        return {
            front: '',
            back: ''
        }
    },
    props: ['cardObj'],
    methods: {
        ...mapActions({
            UpdateCard: 'UpdateCard'
        }),
        onSubmit() {
            this.UpdateCard({
                id: this.cardObj.id,
                payload: {
                    'front': this.front,
                    'back': this.back
                }
            })
        }
    },
    mounted() {
        this.front = this.cardObj.front;
        this.back = this.cardObj.back
    }
}
</script>


<style scoped = true>
* {
    box-sizing: border-box;

}

.column {
    float: left;
    width: 33%;
    padding: 0 10px;
}

/* Remove extra left and right margins, due to padding */
.row {
    margin: 0 -5px;
}

/* Clear floats after the columns */
.row:after {
    content: "";
    display: table;
    clear: both;
}

@media screen and (max-width: 800px) {
    .column {
        width: 50%;
        display: block;
        margin-bottom: 20px;
    }
}

@media screen and (max-width: 600px) {
    .column {
        width: 100%;
        display: block;
        margin-bottom: 20px;
    }
}
</style>