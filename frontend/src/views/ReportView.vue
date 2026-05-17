<template>
  <div>
    <h2>报表中心</h2>
    <div class="search-bar">
      <el-form inline>
        <el-form-item label="酒店">
          <el-select v-model="search.hotel_id" clearable style="width: 200px">
            <el-option v-for="h in hotelList" :key="h.id" :label="h.name" :value="h.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="search.status" clearable style="width: 130px">
            <el-option label="待复核" value="draft" />
            <el-option label="已复核" value="reviewed" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadReports">查询</el-button>
        </el-form-item>
      </el-form>
    </div>

    <el-table :data="reports" stripe style="width: 100%">
      <el-table-column prop="id" label="ID" width="50" fixed />
      <el-table-column label="酒店" min-width="110">
        <template #default="{ row }">{{ getHotelName(row.hotel_id) }}</template>
      </el-table-column>
      <el-table-column label="对账周期" width="130">
        <template #default="{ row }">
          <span class="mono">{{ row.period_start }} ~ {{ row.period_end }}</span>
        </template>
      </el-table-column>
      <el-table-column label="总销售额" min-width="100">
        <template #default="{ row }"><span class="val green">¥{{ fmt(row.total_sales) }}</span></template>
      </el-table-column>
      <el-table-column label="净收入" min-width="100">
        <template #default="{ row }"><span class="val cyan">¥{{ fmt(row.total_net_income) }}</span></template>
      </el-table-column>
      <el-table-column label="公司应得" min-width="100">
        <template #default="{ row }"><span class="val green">¥{{ fmt(row.company_amount) }}</span></template>
      </el-table-column>
      <el-table-column label="房东应得" min-width="100">
        <template #default="{ row }"><span class="val purple">¥{{ fmt(row.owner_amount) }}</span></template>
      </el-table-column>
      <el-table-column label="状态" width="80">
        <template #default="{ row }">
          <span class="report-status" :class="row.status">
            {{ row.status === 'reviewed' ? '已复核' : '待复核' }}
          </span>
        </template>
      </el-table-column>
      <el-table-column label="复核人" width="80" />
      <el-table-column label="操作" min-width="180" align="center" fixed="right">
        <template #default="{ row }">
          <div class="action-btns">
            <el-button link class="btn-link" @click="openDetail(row)">详情</el-button>
            <el-button
              link
              class="btn-link"
              :class="row.status === 'reviewed' ? 'btn-reviewed' : 'btn-review'"
              :disabled="row.status === 'reviewed'"
              @click="row.status !== 'reviewed' && handleReview(row.id)"
            >
              {{ row.status === 'reviewed' ? '已复核' : '复核' }}
            </el-button>
            <el-button link class="btn-link btn-export" @click="handleExport(row.id)">导出</el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="detailVisible" title="报表详情" width="650px">
      <el-descriptions :column="2" border v-if="currentReport">
        <el-descriptions-item label="酒店">{{ getHotelName(currentReport.hotel_id) }}</el-descriptions-item>
        <el-descriptions-item label="对账周期">{{ currentReport.period_start }} 至 {{ currentReport.period_end }}</el-descriptions-item>
        <el-descriptions-item label="总销售额"><span class="val green">¥{{ fmt(currentReport.total_sales) }}</span></el-descriptions-item>
        <el-descriptions-item label="平台佣金"><span class="val pink">¥{{ fmt(currentReport.total_commission) }}</span></el-descriptions-item>
        <el-descriptions-item label="净收入"><span class="val cyan">¥{{ fmt(currentReport.total_net_income) }}</span></el-descriptions-item>
        <el-descriptions-item label="日常开支"><span class="val orange">¥{{ fmt(currentReport.total_expense) }}</span></el-descriptions-item>
        <el-descriptions-item label="公司应得"><span class="val green">¥{{ fmt(currentReport.company_amount) }}</span></el-descriptions-item>
        <el-descriptions-item label="房东应得"><span class="val purple">¥{{ fmt(currentReport.owner_amount) }}</span></el-descriptions-item>
        <el-descriptions-item label="复核人">{{ currentReport.reviewer || '-' }}</el-descriptions-item>
        <el-descriptions-item label="复核时间">{{ currentReport.reviewed_at || '-' }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getReports, reviewReport, exportReport } from '../api/report'
import { getHotels } from '../api/hotel'

const reports = ref([])
const hotelList = ref([])
const search = ref({ hotel_id: null, status: '' })
const detailVisible = ref(false)
const currentReport = ref(null)
const reviewing = ref(false)

const fmt = (v) => Number(v).toFixed(2)
const getHotelName = (id) => {
  const h = hotelList.value.find((x) => x.id === id)
  return h ? h.name : ''
}

const loadReports = async () => {
  try {
    const res = await getReports(search.value)
    reports.value = res.data
  } catch (e) {
    console.error('Failed to load reports', e)
  }
}

const openDetail = (row) => {
  currentReport.value = row
  detailVisible.value = true
}

const handleReview = async (id) => {
  if (reviewing.value) return
  reviewing.value = true
  try {
    const { value } = await ElMessageBox.prompt('请输入复核人姓名', '复核签字')
    await reviewReport(id, { reviewer: value })
    ElMessage.success('复核完成')
    loadReports()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('复核失败')
  } finally {
    reviewing.value = false
  }
}

const handleExport = (id) => {
  exportReport(id)
}

onMounted(async () => {
  try {
    const res = await getHotels()
    hotelList.value = res.data
    loadReports()
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
  font-size: 12px;
}

.val {
  font-family: 'Share Tech Mono', monospace;
  font-size: 13px;
}

.val.green { color: var(--accent-green); }
.val.cyan { color: var(--accent-cyan); }
.val.purple { color: var(--accent-purple); }
.val.pink { color: var(--accent-pink); }
.val.orange { color: #ffaa33; }

.report-status {
  font-weight: 600;
  font-size: 13px;
}

.report-status.draft { color: var(--text-secondary); }
.report-status.reviewed {
  color: var(--accent-green);
  text-shadow: 0 0 6px rgba(0, 255, 136, 0.3);
}

/* Action buttons - link style for compact layout */
.action-btns {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
}

.btn-link {
  font-size: 13px !important;
  padding: 0 4px !important;
  min-width: auto !important;
  height: auto !important;
  line-height: 1.5 !important;
  color: var(--text-primary) !important;
}

.btn-link:hover {
  color: var(--accent-cyan) !important;
}

.btn-review {
  color: var(--accent-cyan) !important;
}

.btn-review:hover {
  color: #4dd9ff !important;
}

.btn-reviewed {
  color: rgba(0, 255, 136, 0.5) !important;
  cursor: not-allowed;
}

.btn-reviewed:hover {
  color: rgba(0, 255, 136, 0.5) !important;
}

.btn-export {
  color: var(--accent-green) !important;
}

.btn-export:hover {
  color: #66ffbb !important;
}
</style>
