import axios from 'axios'

const api = axios.create({
  baseURL: '/api'
})

export default {
  login(credentials) {
    return api.post('/login', credentials)
  },
  register(userData) {
    return api.post('/signup', userData)
  }
}