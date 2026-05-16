import api from './index'

export function getHotels(params) {
  return api.get('/hotels', { params })
}

export function getHotel(id) {
  return api.get(`/hotels/${id}`)
}

export function createHotel(data) {
  return api.post('/hotels', data)
}

export function updateHotel(id, data) {
  return api.put(`/hotels/${id}`, data)
}

export function deleteHotel(id) {
  return api.delete(`/hotels/${id}`)
}
