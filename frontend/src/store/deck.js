const axios = require('axios')

const axiosInstance = axios.create({
    baseURL: 'http://localhost:5000/',
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
        'token': document.cookie
    }
})

const deck = {
    state: {
        decks: []
    },

    getters: {
        getSortedDecks: (state) => {
            return state.sort((a, b) => {
                (a.created > b.created) ? 1 : ((b.created > a.created) ? -1 : 0)
            })
        },
        getDecks: (state) => {
            return state.decks
        },
        getDeckById: (state) => (id) => {
            return state.decks.find(deck => deck.id === id)
        }
    },

    mutations: {
        setDecks(state, payload) {
            state.decks = []
            state.decks = payload
        },
        addDecks(state, payload) {
            if (state.decks.find(deck => deck.id === payload.id)) return
            state.decks.push(payload)
        },
        deleteDeck(state, id) {
            state.decks = state.decks.filter((deck) => {
                return !(deck.id === id)
            })
        },
        updateDeck(state, { payload, id }) {
            modDeck = state.decks.find(deck => deck.id === id)
            this.deleteDeck(state, id)
            for (let attr in ['name', 'description', 'colour']) {
                if (payload[attr]) modDeck[attr] = payload[attr]
            }
            this.addDecks(modDeck)
        }

    },

    actions: {
        async GetDecks(context) {
            console.log(document.cookie)
            let res = await axiosInstance.get('user/deck')
            if (res.status === 200) {
                context.commit('setDecks', res.data)
                console.log(res.data)
            } else {
                console.log('Error' + res.data)
            }
        }
    }
}

export default deck 