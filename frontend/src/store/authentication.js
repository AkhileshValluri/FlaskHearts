const axios = require('axios')

const axiosInstance = axios.create({
    baseURL: 'http://localhost:5000/',
    withCredentials: true,
    headers: {
        Accept: 'application/json',

    }
})

const authentication = {
    state: {
        username: null,
        reputation: null,
        phone_number: null,
        email: null,
        login_error: null,
        id: null
    },

    getters: {
        getUserObj: (state) => {
            let userObj = {
                'username': state.username,
                'reputation': state.reputation,
                'phone_number': state.phone_number,
                'email': state.email,
                'id': state.id
            }
            return userObj
        },

    },

    mutations: {
        updateUserDetails(state, payload) {
            ['username', 'reputation', 'phone_number', 'email', 'id'].forEach((attr) => {
                if (payload[attr]) state[attr] = payload[attr]
            })
        },
        updateError(state, payload) {
            state.login_error = payload
        }
    },

    actions: {

        async signIn(context, form_data) {
            console.log(form_data)
            let res = await axiosInstance.post('login', form_data)
            if (res.status === 200) {
                console.log(res.headers['Content-Type'])
                // console.log(document.cookie) //checking if cookie added
                let uid = res.data.uid
                let resGet = await axiosInstance.get('user/' + uid)

                if (resGet.status === 200) {
                    context.commit('updateUserDetails', resGet.data)
                }
                else console.log(resGet.data)
            }
            else console.log(resGet.data)
        },

        async signUp(context, form_data) {
            let postObj = {
                'username': form_data.username,
                'password': form_data.password,
                'email': form_data.email,
                'phone_number': form_data.phone_number
            }

            let res = await axiosInstance.post('user', postObj)

            console.log(res.data)
            if (res.status !== 200) {
                context.commit('updateError', res.data.msg)
            }
        },

        async logout(context) {
            let res = await axiosInstance.post('logout')
            console.log(res.data)
        }
    }
}

export default authentication