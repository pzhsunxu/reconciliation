import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

api.interceptors.response.use(
  (res) => res,
  (err) => {
    // Re-throw so callers can catch; don't silently swallow
    return Promise.reject(err)
  }
)

export default api
