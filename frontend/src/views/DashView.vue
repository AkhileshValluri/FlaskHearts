<template>
    <div class="jumbotron">
        <h1 class="display-4">Hello, {{ usr.username }}!</h1>
        <p class="lead">This is the dashboard. You can view you data here</p>
        <hr class="my-4">
        <p>You will be able to view your statistics here</p>
        <br>
        <p> We will also mail you monthly reports at : {{usr.email}}</p>
        <p>
        <div class="row" style="margin-left:-20%">


            <div v-for="(deck, index) in this.$store.state.deck.decks" v-bind:key="deck.id" class='column'>
                <div class="card mx-5 " style="width:100%; background-color: whitesmoke">
                    <div class="card-body" style="background-colour:{{deck.colour}}">
                        <h3 class="card-title">{{ deck.name }}</h3>
                        <h4>{{deck.description}}</h4>
                        <h6 class="card-subtitle mb-2 text-muted">Score : {{ deck.score}}</h6>
                        <h5>Last Seen : {{deck.last_seen}}</h5>
                    </div>

                </div>
                <br>
            </div>



        </div>
        </p>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
    name: 'DashView',
    data() {
        return {
            usr: null,
        }
    },
    computed: {
        ...mapGetters({
            getUser: 'getUserObj'
        })
    },
    created() {
        this.usr = this.getUser
    }
}
</script>

<style>
* {
  box-sizing: border-box;

}
.column {
  float: left;
width: 100%;
  padding: 0 10px;
}

/* Remove extra left and right margins, due to padding */
.row {margin:0, -5px; }

/* Clear floats after the columns */
.row:after {
  content: "";
  display: table;
  clear: both;
}
@media screen and (max-width: 300px) {
    .column {
        width: 50%;
        display : block; 
        margin-bottom: 20px;
    }
}
</style>