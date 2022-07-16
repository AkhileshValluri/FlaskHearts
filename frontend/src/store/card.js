const axios = require('axios')

const axiosInstance = axios.create({
    baseURL: 'http://localhost:5000/',
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
        'token': document.cookie.split(';').length > 1 ? document.cookie.split(';')[1] : document.cookie.split(';')[0]
    }
})

const card = {
    state: {
        cards: []
    },

    getters: {
        getCards: (state) => state.cards,

        getCardById: (state) => (id) => {
            return state.cards.find(card => card.id === id)
        }
    },

    mutations: {
        setCards(state, payload) {
            state.cards = []
            state.cards = payload
        },

        addCard(state, payload) {
            if (state.cards.find(card => card.id === payload.id)) return;
            state.cards.push(payload)
        },

        deleteCard(state, id) {
            state.cards = state.cards.filter(card => {
                return !(card.id === id)
            })
        },

        updateCard(state, { payload, id }) {
            let modCard = state.cards.find(card => card.id === id)
            state.cards = state.cards.filter(card => card.id !== id)
            modCard.front = payload.front;
            modCard.back = payload.back;
            state.cards.push(modCard)
        }
    },

    actions: {
        async GetCards(context, did) {
            let res = await axiosInstance.get('deck/card/' + did)
            if (res.status === 200) {
                context.commit('setCards', res.data)
                console.log(res.data)
            } else {
                console.log('Error' + res.data)
            }
        },

        async DeleteCard(context, cid) {
            console.log('Deleting card : ', cid)
            let res = await axiosInstance.delete('card/' + cid)
            if (res.status === 200) {
                context.commit('deleteCard', cid)
                console.log(res.data)
            } else {
                console.log('Error : ', res.data)
            }
        },

        async UpdateCard(context, { id, payload }) {
            console.log('Updating deck : ', id, 'to', payload)
            let res = await axiosInstance.patch('card/' + id, payload)
            if (res.status === 200) {
                context.commit('updateCard', { id: id, payload: payload })
            } else {
                console.log(res.data)
            }
        },

        async AddCard(context, formData) {
            console.log(formData)
            let res = await axiosInstance.post('card',
                {
                    'front': formData.front,
                    'back': formData.back,
                    'deck_id': formData.deck_id
                })
            if (res.status === 200) {
                console.log(res.data)
                let resGet = await axiosInstance.get('card/' + res.data.cid)
                if (resGet.status === 200) {
                    context.commit('addCard', resGet.data)
                } else {
                    console.log(resGet.data)
                }
            } else {
                console.log(res.data)
            }
        }
    }
}
export default card