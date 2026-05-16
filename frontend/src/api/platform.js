import api from './index'

export function getPlatforms(params) {
  return api.get('/platforms', { params })
}

export function createPlatform(data) {
  return api.post('/platforms', data)
}

export function updatePlatform(id, data) {
  return api.put(`/platforms/${id}`, data)
}

export function deletePlatform(id) {
  return api.delete(`/platforms/${id}`)
}
