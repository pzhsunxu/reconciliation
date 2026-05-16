import api from './index'

export function getReconciliations(params) {
  return api.get('/reconciliations', { params })
}

export function createReconciliation(data) {
  return api.post('/reconciliations', data)
}

export function getReconciliation(id) {
  return api.get(`/reconciliations/${id}`)
}
