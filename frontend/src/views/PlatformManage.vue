<template>
  <div>
    <h2>平台账号管理</h2>
    <div class="search-bar">
      <el-form inline>
        <el-form-item label="酒店">
          <el-select v-model="search.hotel_id" clearable style="width: 200px">
            <el-option v-for="h in hotelList" :key="h.id" :label="h.name" :value="h.id" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadPlatforms">查询</el-button>
          <el-button type="success" @click="openDialog()">新增</el-button>
        </el-form-item>
      </el-form>
    </div>

    <el-table :data="platforms" stripe style="width: 100%">
      <el-table-column prop="id" label="ID" width="50" fixed />
      <el-table-column label="酒店" min-width="120">
        <template #default="{ row }">{{ getHotelName(row.hotel_id) }}</template>
      </el-table-column>
      <el-table-column label="平台" width="90">
        <template #default="{ row }">
          <span class="platform-tag" :class="row.platform">{{ platformLabel(row.platform) }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="account_name" label="账号名称" min-width="100" />
      <el-table-column prop="account_id" label="账号ID" min-width="100">
        <template #default="{ row }"><span class="mono">{{ row.account_id || '-' }}</span></template>
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

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑平台账号' : '新增平台账号'" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="酒店">
          <el-select v-model="form.hotel_id">
            <el-option v-for="h in hotelList" :key="h.id" :label="h.name" :value="h.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="平台">
          <el-select v-model="form.platform">
            <el-option label="美团" value="meituan" />
            <el-option label="携程" value="ctrip" />
            <el-option label="飞猪" value="fliggy" />
            <el-option label="抖音" value="douyin" />
            <el-option label="PMS" value="pms" />
          </el-select>
        </el-form-item>
        <el-form-item label="账号名称"><el-input v-model="form.account_name" /></el-form-item>
        <el-form-item label="账号ID"><el-input v-model="form.account_id" /></el-form-item>
        <el-form-item label="状态"><el-switch v-model="form.status" /></el-form-item>
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
import { getPlatforms, createPlatform, updatePlatform, deletePlatform } from '../api/platform'
import { getHotels } from '../api/hotel'

const platforms = ref([])
const hotelList = ref([])
const search = ref({ hotel_id: null })
const dialogVisible = ref(false)
const submitting = ref(false)
const form = ref({})

const platformMap = { meituan: '美团', ctrip: '携程', fliggy: '飞猪', douyin: '抖音', pms: 'PMS' }
const platformLabel = (p) => platformMap[p] || p

const getHotelName = (id) => {
  const h = hotelList.value.find((x) => x.id === id)
  return h ? h.name : ''
}

const loadPlatforms = async () => {
  try {
    const res = await getPlatforms(search.value)
    platforms.value = res.data
  } catch (e) {
    console.error('Failed to load platforms', e)
  }
}

const loadHotels = async () => {
  try {
    const res = await getHotels()
    hotelList.value = res.data
  } catch (e) {
    console.error('Failed to load hotels', e)
  }
}

const openDialog = (row) => {
  form.value = row ? { ...row } : { hotel_id: null, platform: 'meituan', account_name: '', account_id: '', status: true }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (submitting.value) return
  submitting.value = true
  try {
    if (form.value.id) {
      await updatePlatform(form.value.id, form.value)
      ElMessage.success('更新成功')
    } else {
      await createPlatform(form.value)
      ElMessage.success('新增成功')
    }
    dialogVisible.value = false
    loadPlatforms()
  } catch (e) {
    ElMessage.error('操作失败')
  } finally {
    submitting.value = false
  }
}

const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm('确认删除？')
    await deletePlatform(id)
    ElMessage.success('删除成功')
    loadPlatforms()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('删除失败')
  }
}

onMounted(() => { loadPlatforms(); loadHotels() })
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
  color: var(--accent-cyan);
}

.platform-tag {
  padding: 2px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  display: inline-block;
}

.platform-tag.meituan { background: rgba(255, 206, 0, 0.15); color: #ffce00; }
.platform-tag.ctrip { background: rgba(0, 128, 255, 0.15); color: #4da6ff; }
.platform-tag.fliggy { background: rgba(255, 103, 0, 0.15); color: #ff8c41; }
.platform-tag.douyin { background: rgba(255, 0, 80, 0.15); color: #ff6b95; }
.platform-tag.pms { background: rgba(0, 255, 136, 0.12); color: #66ffaa; }

.status-dot {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  margin-right: 4px;
  vertical-align: middle;
}

.status-dot.on { background: var(--accent-green); box-shadow: 0 0 6px var(--accent-green); }
.status-dot.off { background: #555; }

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
