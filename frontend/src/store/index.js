import { createStore } from 'vuex'

import authentication from '@/store/authentication'
import deck from '@/store/deck'
import card from '@/store/card'

export default createStore({
  state: {
    error: null,
  },
  getters: {
    getError: (state) => state.error
  },
  mutations: {
    setError(state, payload) {
      if (payload.length) { //set a timer and delete the error after 3 seconds
        state.error = payload //set the error
        console.log('Error set')
        setTimeout(() => {
          state.error = null;
          console.log('Error: ', this.getters.getError)
        }, 3000)
        console.log('Error:', this.getters.getError)
        // clearTimeout(id)
      } else { console.log('Set a proper error') }
    }
  },
  actions: {
  },
  modules: {
    authentication: authentication,
    deck: deck,
    card: card
  }
})
