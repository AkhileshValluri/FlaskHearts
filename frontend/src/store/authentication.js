const axios = require('axios')

const axiosInstance = axios.create({
    baseURL: 'http://localhost:5000/',
    withCredentials: true,
})

const authentication = {
    state: {
        username: null,
        reputation: null,
        phone_number: null,
        email: null,
        login_error: null,
        id: null,
        token: '',
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
        getToken: (state) => {
            return state.token
        }
    },

    mutations: {
        updateUserDetails(state, payload) {
            ['username', 'reputation', 'phone_number', 'email', 'id'].forEach((attr) => {
                if (payload[attr]) state[attr] = payload[attr]
            })
        },
        updateError(state, payload) {
            state.login_error = payload
        },
        updateToken(state, payload) {
            state.token = payload
            document.cookie = payload
            console.log(document.cookie) 
        }
    },

    actions: {

        async signIn(context, form_data) {
            console.log(form_data)

            let res = await axiosInstance.get('login', {
                auth: {
                    'username': form_data.username,
                    'password': form_data.password
                }
            })
            if (res.status === 200) {
                // console.log(res.data)

                context.commit('updateToken', res.data.token)
                context.commit('updateUserDetails', res.data.usr)


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
            context.commit('updateToken', res.token)
            // console.log(res.data)
            if (res.status !== 200) {
                context.commit('updateError', res.data.msg)
            } else {
                context.commit('updateError', 'User registered. Log in')
            }
        },

        async logout(context) {
            let res = await axiosInstance.post('logout')
            console.log(res.data)
        }
    }
}

export default authentication