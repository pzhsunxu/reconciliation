<template>
  <div>
    <h2>酒店管理</h2>
    <div class="search-bar">
      <el-form inline :model="search">
        <el-form-item label="酒店名称">
          <el-input v-model="search.name" placeholder="搜索酒店" clearable style="width: 200px" />
        </el-form-item>
        <el-form-item label="合作模式">
          <el-select v-model="search.cooperation_type" clearable style="width: 140px">
            <el-option label="分润" value="split" />
            <el-option label="全租" value="full" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadHotels">查询</el-button>
          <el-button type="success" @click="openDialog()">新增</el-button>
        </el-form-item>
      </el-form>
    </div>

    <el-table :data="hotels" stripe style="width: 100%">
      <el-table-column prop="id" label="ID" width="50" fixed />
      <el-table-column prop="name" label="酒店名称" min-width="140" />
      <el-table-column prop="location" label="地址" min-width="120" />
      <el-table-column label="合作模式" width="100">
        <template #default="{ row }">
          <span class="type-badge" :class="row.cooperation_type">{{ row.cooperation_type === 'split' ? '分润' : '全租' }}</span>
        </template>
      </el-table-column>
      <el-table-column label="公司占比" width="90">
        <template #default="{ row }"><span class="mono">{{ (row.company_share * 100).toFixed(0) }}%</span></template>
      </el-table-column>
      <el-table-column label="房东占比" width="90">
        <template #default="{ row }"><span class="mono">{{ (row.owner_share * 100).toFixed(0) }}%</span></template>
      </el-table-column>
      <el-table-column label="状态" width="80">
        <template #default="{ row }">
          <span class="status-dot" :class="row.status ? 'on' : 'off'"></span>
          <span>{{ row.status ? '启用' : '停用' }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" min-width="140" align="center" fixed="right">
        <template #default="{ row }">
          <div class="action-btns">
            <el-button size="small" @click="openDialog(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑酒店' : '新增酒店'" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="酒店名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="地址"><el-input v-model="form.location" /></el-form-item>
        <el-form-item label="合作模式">
          <el-select v-model="form.cooperation_type" @change="onCoopChange">
            <el-option label="分润" value="split" />
            <el-option label="全租" value="full" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="form.cooperation_type === 'split'" label="公司占比">
          <el-input-number v-model="form.company_share" :min="0" :max="1" :step="0.1" />
        </el-form-item>
        <el-form-item v-if="form.cooperation_type === 'split'" label="房东占比">
          <el-input-number v-model="form.owner_share" :min="0" :max="1" :step="0.1" />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="form.status" />
        </el-form-item>
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
import { getHotels, createHotel, updateHotel, deleteHotel } from '../api/hotel'

const hotels = ref([])
const search = ref({ name: '', cooperation_type: '' })
const dialogVisible = ref(false)
const submitting = ref(false)
const form = ref({})

const resetForm = () => {
  form.value = { name: '', location: '', cooperation_type: 'split', company_share: 0.6, owner_share: 0.4, status: true }
}

const loadHotels = async () => {
  try {
    const res = await getHotels(search.value)
    hotels.value = res.data
  } catch (e) {
    console.error('Failed to load hotels', e)
  }
}

const openDialog = (row) => {
  resetForm()
  if (row) form.value = { ...row }
  dialogVisible.value = true
}

const onCoopChange = () => {
  if (form.value.cooperation_type === 'full') {
    form.value.company_share = 1
    form.value.owner_share = 0
  }
}

const handleSubmit = async () => {
  if (submitting.value) return
  submitting.value = true
  try {
    if (form.value.id) {
      await updateHotel(form.value.id, form.value)
      ElMessage.success('更新成功')
    } else {
      await createHotel(form.value)
      ElMessage.success('新增成功')
    }
    dialogVisible.value = false
    loadHotels()
  } catch (e) {
    ElMessage.error('操作失败')
  } finally {
    submitting.value = false
  }
}

const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm('确认删除？')
    await deleteHotel(id)
    ElMessage.success('删除成功')
    loadHotels()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('删除失败')
  }
}

onMounted(loadHotels)
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
  color: var(--accent-green);
}

.type-badge {
  padding: 2px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.type-badge.split {
  background: rgba(0, 198, 255, 0.12);
  color: var(--accent-cyan);
  border: 1px solid rgba(0, 198, 255, 0.25);
}

.type-badge.full {
  background: rgba(123, 47, 247, 0.12);
  color: var(--accent-purple);
  border: 1px solid rgba(123, 47, 247, 0.25);
}

.status-dot {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  margin-right: 4px;
  vertical-align: middle;
}

.status-dot.on {
  background: var(--accent-green);
  box-shadow: 0 0 6px var(--accent-green);
}

.status-dot.off {
  background: #555;
  box-shadow: none;
}

.action-btns {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
}

.action-btns :deep(.el-button) {
  padding: 5px 10px;
  min-width: auto;
  font-size: 12px;
}

</style>
