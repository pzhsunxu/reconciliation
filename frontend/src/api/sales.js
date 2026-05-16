import api from './index'

export function getSales(params) {
  return api.get('/sales', { params })
}

export function pullSales(data) {
  return api.post('/sales/pull', data)
}
