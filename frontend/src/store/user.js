const axios = require('axios');
const user = {
    state: {
        isAuthenticated: false,
        username: null,
        reputation: null,
        phoneNumber: null,
        email: null,
        loginError: '',
    },
    mutations: {
        updateDetails(state, payload) {
            state.isAuthenticated = true;
            state.username = payload['username'];
            state.reputation = payload['reputation'];
            state.phoneNumber = payload['phoneNumber'];
            state.email = payload['email'];
        },
        changeError(state, payload) {
            state.loginError = payload
        }
    },
    actions: {
        async signIn(context, formData) {
            url = 'http://localhost:5000/login';
            let res = await axios.post(url, {
                'username': formData['username'],
                'password': formData['password']
            })

            let data = await res.json()

            if (data.status === 201) {
                console.log('Login unsuccesful')
            } else {
                id = data.data['id'];
                url = 'http://localhost:5000/user/' + id
                let res = await axios.get(url)
                let data = await res.json()
                const userObj = {
                    'username': data.data['username'],
                    'reputation': data.data['reputation'],
                    'phoneNumber': data.data['phoneNumber'],
                    'email': data.data['email']
                }
                context.commit('updateDetails', userObj);
            }
        },
        async signUp(context, formData) {
            url = 'http://localhost:5000/user'
            let res = await axios.post(url, formData)
            let data = res.json()
            if (data.status === 200) {
                id = data.data['id']
                url = 'http://localhost:5000/user/' + id
                let res = await axios.get(url)
                let data = await res.json()
                userObj = {
                    'username': data.data['username'],
                    'reputation': data.data['reputation'],
                    'phoneNumber': data.data['reputation'],
                    'email': data.data['email']
                }

            } else {
                error = data.data['msg']
                console.log(error)
                context.commit('changeError', error)
            }
        }
    }

}

export default user