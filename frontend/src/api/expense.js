import api from './index'

export function getExpenses(params) {
  return api.get('/expenses', { params })
}

export function createExpense(data) {
  return api.post('/expenses', data)
}

export function updateExpense(id, data) {
  return api.put(`/expenses/${id}`, data)
}

export function deleteExpense(id) {
  return api.delete(`/expenses/${id}`)
}
