<template>
    <div style="display:block; justify-content:center; ">
        <div style="display:block;">
            <SingleCard :front="this.$store.state.view.items[index].front"
                :back="this.$store.state.view.items[index].back" @hard="this.current = 1" @medium="this.current = 2"
                @easy="this.current = 3">
            </SingleCard>
        </div>
        <div>
            <button type="button" class="btn btn-outline-info" @click="nextClick()" v-show="!showSubmit">Next</button>
            <button type="button" class="btn btn-outline-success" @click="submit()" v-show="showSubmit">
                <a href="http://localhost:8080/#/flashcards" style="text-decoration:none; color:black"> Return </a>
            </button>
        </div>
    </div>
    <div>
        <p v-show="!showSubmit">{{ this.index + 1 }} / {{ this.$store.state.view.items.length }}</p>
        <p v-show="showSubmit"> ✅</p>
    </div>
</template>

<script>
import { mapActions, mapMutations } from 'vuex'
import SingleCard from '@/components/SingleCard.vue'
export default {
    name: 'DeckView',
    data() {
        return {
            deck_id: this.$route.params.did,
            index: 0,
            current: null,
            score: 0,
            showSubmit: false
        }
    },
    methods: {
        ...mapActions({
            LoadItems: 'LoadItems',
            finishReview: 'finishReview',
            UpdateDeck: 'UpdateDeck'
        }),
        ...mapMutations({ modifyScore: 'modifyScore' }),
        nextClick() {
            let len = this.$store.state.view.items.length;
            if (this.index == len - 1) {
                //make index 0 again and cycle through
                console.log(this.score)
                this.modifyScore(this.score)
                this.index = 0;
                this.showSubmit = true;
            }
            else {
                this.index++;
                this.score += this.current;
                // this.current = null; if user doesn't change option, score doesn't change
            }
        },
        async submit() {
            this.UpdateDeck({
                id: this.deck_id,
                payload: {
                    'score': this.score
                }
            })
        }
    },
    created() {
        this.LoadItems(this.$route.params.did)
    },
    components: {
        SingleCard
    }
}
</script>