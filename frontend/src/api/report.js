import api from './index'

export function getReports(params) {
  return api.get('/reports', { params })
}

export function getReport(id) {
  return api.get(`/reports/${id}`)
}

export function reviewReport(id, data) {
  return api.post(`/reports/${id}/review`, data)
}

export function exportReport(id) {
  window.open(`/api/reports/${id}/excel`, '_blank')
}
