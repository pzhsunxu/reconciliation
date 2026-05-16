<template>
  <div>
    <h2>销售数据</h2>
    <div class="search-bar">
      <el-form inline>
        <el-form-item label="酒店">
          <el-select v-model="search.hotel_id" clearable style="width: 180px">
            <el-option v-for="h in hotelList" :key="h.id" :label="h.name" :value="h.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="平台">
          <el-select v-model="search.platform" clearable style="width: 120px">
            <el-option label="美团" value="meituan" />
            <el-option label="携程" value="ctrip" />
            <el-option label="飞猪" value="fliggy" />
            <el-option label="抖音" value="douyin" />
            <el-option label="PMS" value="pms" />
          </el-select>
        </el-form-item>
        <el-form-item label="起始日期">
          <el-date-picker v-model="search.start_date" type="date" format="YYYY-MM-DD" value-format="YYYY-MM-DD" style="width: 150px" />
        </el-form-item>
        <el-form-item label="结束日期">
          <el-date-picker v-model="search.end_date" type="date" format="YYYY-MM-DD" value-format="YYYY-MM-DD" style="width: 150px" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadSales">查询</el-button>
          <el-button type="success" @click="openPullDialog">拉取数据</el-button>
        </el-form-item>
      </el-form>
    </div>

    <el-table :data="sales" stripe style="width: 100%">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column label="平台" width="70">
        <template #default="{ row }">
          <span class="platform-tag" :class="row.platform">{{ platformLabel(row.platform) }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="order_no" label="订单号">
        <template #default="{ row }"><span class="mono">{{ row.order_no }}</span></template>
      </el-table-column>
      <el-table-column label="入住日期" width="110">
        <template #default="{ row }"><span class="mono">{{ row.check_in }}</span></template>
      </el-table-column>
      <el-table-column label="离店日期" width="110">
        <template #default="{ row }"><span class="mono">{{ row.check_out }}</span></template>
      </el-table-column>
      <el-table-column prop="room_type" label="房型" width="100" />
      <el-table-column label="金额" width="110">
        <template #default="{ row }"><span class="amount">¥{{ row.amount.toFixed(2) }}</span></template>
      </el-table-column>
      <el-table-column label="佣金" width="110">
        <template #default="{ row }"><span class="commission">¥{{ row.commission.toFixed(2) }}</span></template>
      </el-table-column>
      <el-table-column label="净收入" width="110">
        <template #default="{ row }"><span class="net">¥{{ row.net_amount.toFixed(2) }}</span></template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="pullDialogVisible" title="拉取销售数据" width="500px">
      <el-form :model="pullForm" label-width="80px">
        <el-form-item label="酒店">
          <el-select v-model="pullForm.hotel_id">
            <el-option v-for="h in hotelList" :key="h.id" :label="h.name" :value="h.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="起始日期">
          <el-date-picker v-model="pullForm.start_date" type="date" format="YYYY-MM-DD" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="结束日期">
          <el-date-picker v-model="pullForm.end_date" type="date" format="YYYY-MM-DD" value-format="YYYY-MM-DD" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="pullDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handlePull">拉取</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getSales, pullSales } from '../api/sales'
import { getHotels } from '../api/hotel'

const sales = ref([])
const hotelList = ref([])
const search = ref({ hotel_id: null, platform: '', start_date: '', end_date: '' })
const pullDialogVisible = ref(false)
const pulling = ref(false)
const pullForm = ref({ hotel_id: null, start_date: '', end_date: '' })

const platformMap = { meituan: '美团', ctrip: '携程', fliggy: '飞猪', douyin: '抖音', pms: 'PMS' }
const platformLabel = (p) => platformMap[p] || p

const loadSales = async () => {
  try {
    const res = await getSales(search.value)
    sales.value = res.data
  } catch (e) {
    console.error('Failed to load sales', e)
  }
}

const openPullDialog = () => { pullDialogVisible.value = true }

const handlePull = async () => {
  if (pulling.value) return
  pulling.value = true
  try {
    const res = await pullSales(pullForm.value)
    ElMessage.success(`成功拉取 ${res.data.pulled} 条记录`)
    pullDialogVisible.value = false
    loadSales()
  } catch (e) {
    ElMessage.error('拉取失败')
  } finally {
    pulling.value = false
  }
}

onMounted(async () => {
  const res = await getHotels()
  hotelList.value = res.data
  loadSales()
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

.amount { font-family: 'Share Tech Mono', monospace; color: var(--accent-green); }
.commission { font-family: 'Share Tech Mono', monospace; color: var(--accent-pink); }
.net { font-family: 'Share Tech Mono', monospace; color: var(--accent-cyan); }

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

</style>
