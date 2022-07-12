const axios = require('axios');

const user = {
    state: {
        isAuthenticated: false,
        username: null,
        reputation: null,
        phoneNumber: null,
        email: null,
        loginError: '',
        Cookie: ''
    },
    getters: {
        getUser: (state) => {
            let userObj = {
                'username': state.username,
                'reputation': state.reputation,
                'phoneNumber': state.phoneNumber,
                'email': state.email,
                'uid': state.uid
            }
            return userObj
        }
    },
    mutations: {
        updateDetails(state, payload) {
            state.isAuthenticated = true;
            state.username = payload['username'];
            state.reputation = payload['reputation'];
            state.phoneNumber = payload['phoneNumber'];
            state.email = payload['email'];
            state.id = payload['id'];
        },
        changeError(state, payload) {
            state.loginError = payload
        },
        setCookie(state, payload) {
            state.Cookie = payload
            console.log(payload) 
        }
    },
    actions: {

        async signIn(context, formData) {
            console.log(formData)
            let url = 'http://localhost:5000/login';
            let res = await axios.post(url, {
                'username': formData['username'],
                'password': formData['password']
            }, { 'withCredentials': true })

            if (res.status === 200) {
                console.log(res.headers)
                document.cookie = res.headers['Set-Cookie']
                let uid = res.data.uid
                let urlNew = 'http://localhost:5000/user/'
                url = urlNew + uid
                let resGet = await axios.get(url)
                // console.log(resGet.data)

                context.commit('updateDetails', resGet.data)
            } else {
                console.log(res.data)
                context.commit('changeError', res.data.error) 
            }
        },
        async signUp(context, formData) {
            let header = {
                "Content-Type": "application/json",
                "Cookie": document.cookie,
                "withCredentials": true
            }
            console.log(formData)
            let url = 'http://localhost:5000/user'
            let userObj = {
                'username': formData.username,
                'password': formData.password,
                'email': formData.email,
                'phone_number': formData.phoneNumber,
            }
            let resPost = await axios.post(url, userObj, header)

            if (resPost.status === 200) {
                console.log('User has been registered') 
            } else {
                context.commit('changeError', resPost.data.msg) 
            }
        },
        async logout(context) {
            let header = {
                "Content-Type": "application/json",
                "Cookie": document.cookie,
                "withCredentials": true
            }
            let url = 'http://localhost:5000/logout'
            let res = await axios.get(url, header)
            console.log(res.data)
        }

    }

}

export default user