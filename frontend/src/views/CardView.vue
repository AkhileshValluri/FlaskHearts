<template>


    <div class="row">
        <div v-for="(deck, index) in this.$store.state.card.cards" v-bind:key="deck.id" class='column'>

            <div class="card mx-5 " style="width:100%; background-color: whitesmoke">
                <div class="card-body" style="background-colour:{{deck.colour}}">
                    <div v-on:mouseover="this.showBack[index] = true" v-show="!this.showBack[index]">
                        <h3 class="card-title">Front</h3>
                        <br>
                        <h2>
                            {{ deck.front }}
                        </h2>
                    </div>
                    <div v-on:mouseleave="this.showBack[index] = false" v-show="this.showBack[index]">
                        <h3 class="card-title">Back</h3>
                        <br>
                        <h2>
                            {{ deck.back }}
                        </h2>
                    </div>
                    <br>
                    <span class="card-text" v-on:mouseover="this.showOptions[index] = true"
                        v-on:mouseleave="this.showOptions[index] = false" style="">
                        <h6 style="opacity:60%">
                            Hover to Edit
                        </h6>
                        <ul class="list-group" v-show="this.showOptions[index]">
                            <li class="list-group-item d-grid gap-2">
                                <button type="button" class="btn btn-outline-primary dropdown-toggle"
                                    data-bs-toggle="collapse" data-bs-target="#collapseExample" aria-expanded="false"
                                    aria-controls="collapseExample">Edit</button>
                            </li>
                            <li class="list-group-item d-grid gap-2">
                                <button type="button" class="btn btn-outline-danger"
                                    v-on:click="DeleteCard(deck.id)">Delete
                                </button>
                            </li>
                        </ul>
                    </span>
                </div>
                <div class="collapse" id="collapseExample">
                    <div class="card card-body">
                        <CardEdit v-bind:cardObj="deck"></CardEdit>
                    </div>
                </div>
            </div>
            <br>
        </div>
        <div style="width:100%">
            <AddCard v-bind:did=this.deckid></AddCard>

            <span style=" width:100%" @click="">
                <button type="button" class="btn btn-outline-info" @click="exportDeck(1)">Export Deck as HTML</button>
                <button type="button" class="btn btn-outline-info" @click="exportDeck(0)">Export Deck as CSV</button>

            </span>
            <br>
        </div>

    </div>

</template>
<script>
import { mapActions, mapGetters, mapState } from 'vuex';
import AddCard from '@/components/AddCard.vue'
import CardEdit from '@/components/CardEdit.vue'
import ErrorMessage from '@/components/ErrorMessage.vue'

export default {
    name: 'CardView',
    data() {
        return {
            showOptions: [],
            showBack: [],
            showEdit: false,
            deckid: this.$route.params.did
        }
    },
    methods: {
        ...mapActions({
            GetCards: 'GetCards',
            DeleteCard: 'DeleteCard',
            UpdateCard: 'UpdateCard'

        }),
        toggleOptions() {
            this.showOptions = true;
        },
        clickEdit() {

        },
        async exportDeck(type) {
            const axios = require('axios');
            const axiosInstance = axios.create({
                baseURL: 'http://localhost:5000/flashcards',
                withCredentials: true,
                headers: {
                    'Content-Type': 'application/json',
                    'token': document.cookie.split(';').length > 1 ? document.cookie.split(';')[1] : document.cookie.split(';')[0]
                }
            })

            if (type) {
                //export as HTML
                let res = await axiosInstance.get('/html/' + this.deckid)
                let info = 'Your deck should be emailed as html shortly'
                if (res.status === 200) {
                } else {
                    let info = 'Something went wrong'
                }
                this.$store.commit('setError', info)
            } else {
                let res = await axiosInstance.get('/csv/' + this.deckid)
                let info = 'Your deck should be emailed as csv shortly'
                if (res.status === 200) {
                } else {
                    let info = 'Something went wrong'
                }
                this.$store.commit('setError', info);
            }

        }
    },
    mounted() {
        this.GetCards(this.deckid)
        for (let i = 0; i < this.$store.state.card.cards.length; i++) {
            this.showOptions.push(false)
            this.showBack.push(false)
        }
    },
    computed: {
        ...mapGetters({ getCards: 'getCards' }),
        ...mapState({ cards: 'card/cards' })
    },
    components: {
        AddCard,
        CardEdit,
        ErrorMessage
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