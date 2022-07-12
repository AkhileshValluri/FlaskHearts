<template>
    <!-- <div v-for="deck in this.$store.decks">
        {{ deck.name }}
        {{ this.$store.decks }}
        <div class="card" style="width: 18rem;">
            <div class="card-body">
                <h5 class="card-title">Card title</h5>
                <h6 class="card-subtitle mb-2 text-muted">Card subtitle</h6>
                <p class="card-text">Some quick example text to build on the card title and make up the bulk of the
                    card's content.</p>
                <a href="#" class="card-link">Card link</a>
                <a href="#" class="card-link">Another link</a>
            </div>
        </div>
    </div> -->
    <button v-on:click="showme">click me</button>
    {{ this.$store.state.deck.decks }}
</template>

<script>
import { mapActions } from 'vuex'
import { mapGetters } from 'vuex'
export default {
    name: 'FlashCards',
    methods: {
        ...mapActions({
            AllDecks: 'AllDecks',
            DeleteDeck: 'DeleteDeck',
            AddDeck: 'AddDeck',
            UpdateDeck: 'UpdateDeck'
        }),
        showme() {
            this.AllDecks()
            console.log(this.getDecks)
        }
    },
    computed: {
        ...mapGetters({ getDecks: 'getDecks' })
    },
}
</script>