<template>
  <div>
    <h2>日常开支管理</h2>
    <div class="search-bar">
      <el-form inline>
        <el-form-item label="酒店">
          <el-select v-model="search.hotel_id" clearable style="width: 200px">
            <el-option v-for="h in hotelList" :key="h.id" :label="h.name" :value="h.id" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadExpenses">查询</el-button>
          <el-button type="success" @click="openDialog()">新增</el-button>
        </el-form-item>
      </el-form>
    </div>

    <el-table :data="expenses" stripe style="width: 100%">
      <el-table-column prop="id" label="ID" width="50" fixed />
      <el-table-column label="酒店" min-width="120">
        <template #default="{ row }">{{ getHotelName(row.hotel_id) }}</template>
      </el-table-column>
      <el-table-column label="类别" width="80">
        <template #default="{ row }">
          <span class="cat-badge" :class="row.category">{{ categoryLabel(row.category) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="金额" min-width="110">
        <template #default="{ row }"><span class="amount">¥{{ Number(row.amount).toFixed(2) }}</span></template>
      </el-table-column>
      <el-table-column prop="description" label="说明" min-width="100" />
      <el-table-column label="日期" width="110">
        <template #default="{ row }"><span class="mono">{{ row.expense_date }}</span></template>
      </el-table-column>
      <el-table-column prop="created_by" label="录入人" width="80" />
      <el-table-column label="操作" width="120" align="center" fixed="right">
        <template #default="{ row }">
          <div class="action-btns">
            <el-button link class="btn-edit" @click="openDialog(row)">编辑</el-button>
            <el-button link class="btn-delete" @click="handleDelete(row.id)">删除</el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑开支' : '新增开支'" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="酒店">
          <el-select v-model="form.hotel_id">
            <el-option v-for="h in hotelList" :key="h.id" :label="h.name" :value="h.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="类别">
          <el-select v-model="form.category">
            <el-option label="水电" value="utility" />
            <el-option label="人工" value="labor" />
            <el-option label="维修" value="maintenance" />
            <el-option label="清洁" value="cleaning" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="金额"><el-input-number v-model="form.amount" :min="0" :precision="2" /></el-form-item>
        <el-form-item label="日期">
          <el-date-picker v-model="form.expense_date" type="date" format="YYYY-MM-DD" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="说明"><el-input v-model="form.description" /></el-form-item>
        <el-form-item label="录入人"><el-input v-model="form.created_by" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getExpenses, createExpense, updateExpense, deleteExpense } from '../api/expense'
import { getHotels } from '../api/hotel'

const expenses = ref([])
const hotelList = ref([])
const search = ref({ hotel_id: null })
const dialogVisible = ref(false)
const submitting = ref(false)
const form = ref({})

const categoryMap = { utility: '水电', labor: '人工', maintenance: '维修', cleaning: '清洁', other: '其他' }
const categoryLabel = (c) => categoryMap[c] || c

const getHotelName = (id) => {
  const h = hotelList.value.find((x) => x.id === id)
  return h ? h.name : ''
}

const loadExpenses = async () => {
  try {
    const res = await getExpenses(search.value)
    expenses.value = res.data
  } catch (e) {
    console.error('Failed to load expenses', e)
  }
}

const openDialog = (row) => {
  form.value = row ? { ...row } : { hotel_id: null, category: 'utility', amount: 0, description: '', expense_date: '', created_by: '' }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (submitting.value) return
  submitting.value = true
  try {
    if (form.value.id) {
      await updateExpense(form.value.id, form.value)
      ElMessage.success('更新成功')
    } else {
      await createExpense(form.value)
      ElMessage.success('新增成功')
    }
    dialogVisible.value = false
    loadExpenses()
  } catch (e) {
    ElMessage.error('操作失败')
  } finally {
    submitting.value = false
  }
}

const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm('确认删除？')
    await deleteExpense(id)
    ElMessage.success('删除成功')
    loadExpenses()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('删除失败')
  }
}

onMounted(async () => {
  try {
    const res = await getHotels()
    hotelList.value = res.data
    loadExpenses()
  } catch (e) {
    console.error('Failed to load hotels', e)
  }
})
</script>

<style scoped>
.search-bar {
  background: var(--bg-card);
  border: 1px solid var(--border-glow);
  border-radius: 8px;
  padding: 16px 20px;
  margin-bottom: 20px;
  backdrop-filter: blur(12px);
}

.mono {
  font-family: 'Share Tech Mono', monospace;
  color: var(--text-secondary);
}

.amount {
  font-family: 'Share Tech Mono', monospace;
  color: var(--accent-pink);
}

.cat-badge {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  display: inline-block;
}

.cat-badge.utility { background: rgba(255, 170, 0, 0.15); color: #ffaa33; }
.cat-badge.labor { background: rgba(0, 198, 255, 0.12); color: var(--accent-cyan); }
.cat-badge.maintenance { background: rgba(255, 45, 149, 0.12); color: var(--accent-pink); }
.cat-badge.cleaning { background: rgba(0, 255, 136, 0.12); color: #66ffaa; }
.cat-badge.other { background: rgba(123, 47, 247, 0.12); color: var(--accent-purple); }

.action-btns {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
}

.action-btns :deep(.el-button) {
  padding: 0 4px !important;
  min-width: auto !important;
  height: auto !important;
  line-height: 1.5 !important;
  font-size: 13px !important;
}

.btn-edit {
  color: var(--accent-cyan) !important;
}

.btn-edit:hover {
  color: #4dd9ff !important;
}

.btn-delete {
  color: var(--accent-pink) !important;
}

.btn-delete:hover {
  color: #ff6699 !important;
}

</style>
