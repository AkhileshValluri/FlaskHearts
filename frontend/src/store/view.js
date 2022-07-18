const axios = require('axios')

const axiosInstance = axios.create({
    baseURL: 'http://localhost:5000/',
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
        'token': document.cookie.split(';').length > 1 ? document.cookie.split(';')[1] : document.cookie.split(';')[0]
    }
})

const view = {
    state: {
        items: [],
        score: 0
    },
    mutations: {

        setItems(state, payload) {
            state.items = payload
            console.log(payload)
        },

        modifyScore(state, payload) {
            state.score += payload
        }
    },
    actions: {
        async LoadItems(context, did) {
            console.log(document.cookie)
            let res = await axiosInstance.get('deck/card/' + did)
            if (res.status === 200) {
                context.commit('setItems', res.data)
                // console.log(res.data)
            } else {
                console.log('Error :', + res.data)
            }
        },
        async finishReview(context, { id, payload }) {
            console.log(context.state.score)

            let res = await axiosInstance.patch('deck/' + id, payload)
            if (res.status === 200) {
                console.log(res.data)
                context.state.score = 0;
                context.state.items = 0
            } else {
                console.log(res.data)
            }
        },
    }
}

export default view