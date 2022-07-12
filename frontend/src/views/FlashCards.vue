<template>
    <div v-for="(deck, index) in this.decks" v-bind:key="deck.id">
        <div class="card mx-5" style="width: 18rem;">
            <div class="card-body">
                <h3 class="card-title">{{ deck.name }}</h3>
                <h6 class="card-subtitle mb-2 text-muted">Score : {{ deck.deck_score ? 0 : deck.deck_score }}</h6>
                <p class="card-text" v-on:mouseover="this.showOptions[index] = true"
                    v-on:mouseleave="this.showOptions[index] = false" style="">{{ deck.description }}
                <ul class="list-group" v-show="this.showOptions[index]">
                    <li class="list-group-item">
                        <button type="button" class="btn btn-outline-success">View</button>
                    </li>
                    <li class="list-group-item">
                        <button type="button" class="btn btn-outline-primary">Edit</button>
                    </li>
                    <li class="list-group-item">
                        <button type="button" class="btn btn-outline-danger">Delete</button>
                    </li>
                </ul>
                </p>
            </div>
        </div>
    </div>

</template>

<script>
import { mapActions } from 'vuex'
import { mapGetters } from 'vuex'
export default {
    name: 'FlashCards',
    data() {
        return {
            decks: [],
            showOptions: [],
        }
    },
    methods: {
        ...mapActions({
            GetDecks: 'GetDecks',
        }),
        toggleOptions() {
            this.showOptions = true;
        }
    },
    mounted() {
        this.GetDecks()
        this.decks = this.getDecks
        for (let i = 0; i < this.decks.length; i++) this.showOptions.push(false)
    },
    computed: {
        ...mapGetters({ getDecks: 'getDecks' })
    },
}
</script>