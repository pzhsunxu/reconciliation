<template>
  <div>
    <h2>对账管理</h2>
    <div class="search-bar">
      <el-form inline>
        <el-form-item label="任务类型">
          <el-select v-model="search.job_type" clearable style="width: 130px">
            <el-option label="自动" value="auto" />
            <el-option label="手动" value="manual" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="search.status" clearable style="width: 130px">
            <el-option label="待执行" value="pending" />
            <el-option label="执行中" value="running" />
            <el-option label="已完成" value="completed" />
            <el-option label="失败" value="failed" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadJobs">查询</el-button>
          <el-button type="success" @click="openDialog()">手动对账</el-button>
        </el-form-item>
      </el-form>
    </div>

    <el-table :data="jobs" stripe style="width: 100%">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column label="类型" width="80">
        <template #default="{ row }">
          <span class="type-badge" :class="row.job_type">{{ row.job_type === 'auto' ? '自动' : '手动' }}</span>
        </template>
      </el-table-column>
      <el-table-column label="起始日期" width="120">
        <template #default="{ row }"><span class="mono">{{ row.start_date }}</span></template>
      </el-table-column>
      <el-table-column label="结束日期" width="120">
        <template #default="{ row }"><span class="mono">{{ row.end_date }}</span></template>
      </el-table-column>
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <span class="job-status" :class="row.status">
            <span class="status-dot" :class="row.status"></span>
            {{ statusLabel(row.status) }}
          </span>
        </template>
      </el-table-column>
      <el-table-column label="酒店数" width="80">
        <template #default="{ row }"><span class="mono">{{ row.hotels_count }}</span></template>
      </el-table-column>
      <el-table-column label="创建时间" width="170">
        <template #default="{ row }"><span class="mono">{{ row.created_at }}</span></template>
      </el-table-column>
      <el-table-column label="完成时间" width="170">
        <template #default="{ row }"><span class="mono">{{ row.completed_at || '-' }}</span></template>
      </el-table-column>
      <el-table-column prop="error_msg" label="错误信息" :show-overflow-tooltip="true">
        <template #default="{ row }">
          <span :class="{ 'error-text': row.error_msg }">{{ row.error_msg || '-' }}</span>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" title="手动对账" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="起始日期">
          <el-date-picker v-model="form.start_date" type="date" format="YYYY-MM-DD" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="结束日期">
          <el-date-picker v-model="form.end_date" type="date" format="YYYY-MM-DD" value-format="YYYY-MM-DD" />
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
import { ElMessage } from 'element-plus'
import { getReconciliations, createReconciliation } from '../api/reconciliation'

const jobs = ref([])
const search = ref({ job_type: '', status: '' })
const dialogVisible = ref(false)
const submitting = ref(false)
const form = ref({ start_date: '', end_date: '' })

const statusMap = { pending: '待执行', running: '执行中', completed: '已完成', failed: '失败' }
const statusLabel = (s) => statusMap[s] || s

const loadJobs = async () => {
  try {
    const res = await getReconciliations(search.value)
    jobs.value = res.data
  } catch (e) {
    console.error('Failed to load jobs', e)
  }
}

const openDialog = () => {
  form.value = { start_date: '', end_date: '' }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (submitting.value) return
  submitting.value = true
  try {
    await createReconciliation(form.value)
    ElMessage.success('对账任务已创建，正在后台执行')
    dialogVisible.value = false
    loadJobs()
  } catch (e) {
    ElMessage.error('创建任务失败')
  } finally {
    submitting.value = false
  }
}

onMounted(loadJobs)
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

.type-badge {
  padding: 2px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.type-badge.auto {
  background: rgba(0, 198, 255, 0.12);
  color: var(--accent-cyan);
  border: 1px solid rgba(0, 198, 255, 0.25);
}

.type-badge.manual {
  background: rgba(123, 47, 247, 0.12);
  color: var(--accent-purple);
  border: 1px solid rgba(123, 47, 247, 0.25);
}

.job-status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-weight: 500;
}

.status-dot {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.status-dot.pending { background: #555; }
.status-dot.running { background: #ffaa33; box-shadow: 0 0 6px #ffaa33; animation: pulse 1.5s infinite; }
.status-dot.completed { background: var(--accent-green); box-shadow: 0 0 6px var(--accent-green); }
.status-dot.failed { background: var(--accent-pink); box-shadow: 0 0 6px var(--accent-pink); }

.job-status.pending { color: var(--text-secondary); }
.job-status.running { color: #ffaa33; }
.job-status.completed { color: var(--accent-green); }
.job-status.failed { color: var(--accent-pink); }

.error-text {
  color: var(--accent-pink);
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

</style>
