const axios = require('axios')

const axiosInstance = axios.create({
    baseURL: 'http://localhost:5000/',
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
        'token': document.cookie.split(';').length > 1 ? document.cookie.split(';')[1] : document.cookie.split(';')[0]
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
            console.log(state.decks)
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
        updateDeck(state, data) {
            let modDeck = state.decks.find(deck => deck.id === data.id)
            state.decks = state.decks.filter(deck => !(deck.id === data.id))
            let payload = data.payload;
            if (payload.name) 
            modDeck.name = payload.name
            if (payload.description) 
            modDeck.description = payload.description
            try {
                if (payload.score)
                    modDeck.score = payload.score
            }
            catch (TypeError) {
                console.log(modDeck)
            }
            state.decks.push(modDeck)
        }

    },

    actions: {
        async GetDecks(context) {
            console.log(document.cookie.split(';').length > 1 ? document.cookie.split(';')[1] : document.cookie.split(';')[0])
            try {
                let res = await axiosInstance.get('user/deck')
                if (res.status === 200) {
                    context.commit('setDecks', res.data)
                } else {
                    console.log('Error' + res.data)
                }
            }
            catch (err) {
                console.log(err);
                let error = 'Session Timed-Out. Please log in again'
                context.commit('setError', error)
            }
        },

        async DeleteDeck(context, id) {
            let res = await axiosInstance.delete('deck/' + id)
            console.log('Deleting deck : ', id)
            if (res.status === 200) {
                context.commit('deleteDeck', id)
                console.log(res.data)
            } else {
                console.log('Error : ', res.data)
            }
        },

        async UpdateDeck(context, { id, payload }) {
            console.log('Updating deck : ', id, 'to', payload)
            let res = await axiosInstance.patch('deck/' + id, payload)
            if (res.status === 200) {
                context.commit('updateDeck', { id, payload })
            } else {
                console.log(res.data)
            }
        },

        async AddDeck(context, formData) {
            console.log(formData)
            let res = await axiosInstance.post('deck',
                {
                    'name': formData.name,
                    'description': formData.description,
                    'colour': formData.colour
                })

            if (res.status === 200) {
                console.log(res.data)
                let resGet = await axiosInstance.get('deck/' + res.data.did)
                if (resGet.status === 200) {
                    context.commit('addDecks', resGet.data)
                } else {
                    console.log(resGet.data)
                }
            } else {
                console.log(res.data)
            }
        }
    }
}

export default deck 