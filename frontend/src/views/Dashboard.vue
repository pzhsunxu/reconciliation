<template>
  <div>
    <h2>首页仪表盘</h2>
    <div class="company-banner">
      <div class="company-icon">&#9670;</div>
      <div class="company-info">
        <div class="company-name">四川百星辉能科技有限公司</div>
        <div class="company-subtitle">酒店对账管理系统</div>
      </div>
      <div class="company-glow"></div>
    </div>
    <el-row :gutter="20" style="margin-top: 24px">
      <el-col :span="6">
        <div class="stat-card stat-cyan">
          <div class="stat-icon">&#9632;</div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.total_hotels }}</div>
            <div class="stat-label">酒店总数</div>
          </div>
          <div class="stat-glow"></div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card stat-blue">
          <div class="stat-icon">&#9632;</div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.split_hotels }}</div>
            <div class="stat-label">分润酒店</div>
          </div>
          <div class="stat-glow"></div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card stat-purple">
          <div class="stat-icon">&#9632;</div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.total_jobs }}</div>
            <div class="stat-label">对账任务数</div>
          </div>
          <div class="stat-glow"></div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card stat-pink">
          <div class="stat-icon">&#9632;</div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.pending_review }}</div>
            <div class="stat-label">待复核报表</div>
          </div>
          <div class="stat-glow"></div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 24px">
      <!-- Left: 本月销售额 + 对账完成率 + 结算进度 -->
      <el-col :span="12">
        <el-card class="tech-card full-height">
          <template #header>
            <div class="card-header">
              <span class="header-dot"></span>
              <span>数据概览</span>
            </div>
          </template>
          <div class="left-panel">
            <div class="big-number">
              <span class="currency">¥</span>
              <span class="number">{{ stats.this_month_sales.toFixed(2) }}</span>
              <span class="number-label">本月销售额</span>
            </div>
            <div class="left-sub-row">
              <div class="sub-card">
                <div class="sub-card-title">对账完成率</div>
                <div class="reconciliation-section">
                  <div ref="ringChartRef" class="ring-chart"></div>
                  <div class="ring-stats">
                    <div class="stat-line">
                      <span class="stat-dot cyan"></span>
                      <span>本月对账任务：<b>{{ stats.total_jobs }}</b> 项</span>
                    </div>
                    <div class="stat-line">
                      <span class="stat-dot green"></span>
                      <span>已完成：<b>{{ stats.completed_jobs }}</b> 项</span>
                    </div>
                    <div class="stat-line highlight">
                      <span>完成率：<b class="rate">{{ completionRate }}%</b></span>
                    </div>
                  </div>
                </div>
              </div>
              <div class="sub-card">
                <div class="sub-card-title">结算进度</div>
                <div class="settlement-stats">
                  <div class="settle-item">
                    <span class="settle-label">已结算</span>
                    <span class="settle-value green">{{ stats.reviewed_reports }}</span>
                    <span class="settle-unit">家</span>
                  </div>
                  <div class="settle-divider"></div>
                  <div class="settle-item">
                    <span class="settle-label">应结算</span>
                    <span class="settle-value">{{ stats.split_hotels }}</span>
                    <span class="settle-unit">家</span>
                  </div>
                  <div class="settle-divider"></div>
                  <div class="settle-item">
                    <span class="settle-label">结算率</span>
                    <span class="settle-value cyan">{{ settlementRate }}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      <!-- Right: 各平台销售额 -->
      <el-col :span="12">
        <el-card class="tech-card full-height">
          <template #header>
            <div class="card-header">
              <span class="header-dot"></span>
              <span>各平台销售额</span>
            </div>
          </template>
          <div ref="chartRef" class="platform-chart tall"></div>
          <el-table :data="stats.platform_sales" style="width: 100%; margin-top: 12px;">
            <el-table-column prop="platform" label="平台" width="80">
              <template #default="{ row }">
                <span class="platform-tag" :class="row.platform">{{ platformLabel(row.platform) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="amount" label="销售额">
              <template #default="{ row }">
                <span class="amount-text">¥{{ row.amount.toFixed(2) }}</span>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import { getDashboardStats } from '../api/dashboard'

const platformMap = { meituan: '美团', ctrip: '携程', fliggy: '飞猪', douyin: '抖音', pms: 'PMS' }
const platformLabel = (p) => platformMap[p] || p

const platformColors = { meituan: '#ffce00', ctrip: '#4da6ff', fliggy: '#ff8c41', douyin: '#ff6b95', pms: '#66ffaa' }

const stats = ref({
  total_hotels: 0,
  split_hotels: 0,
  total_jobs: 0,
  completed_jobs: 0,
  pending_review: 0,
  reviewed_reports: 0,
  this_month_sales: 0,
  platform_sales: [],
})

const completionRate = computed(() => {
  if (!stats.value.total_jobs) return 0
  return Math.round((stats.value.completed_jobs / stats.value.total_jobs) * 100)
})

const settlementRate = computed(() => {
  if (!stats.value.split_hotels) return 0
  return Math.round((stats.value.reviewed_reports / stats.value.split_hotels) * 100)
})

const chartRef = ref(null)
const ringChartRef = ref(null)
let chartInstance = null
let ringInstance = null

const initBarChart = (data) => {
  if (!chartInstance) {
    chartInstance = echarts.init(chartRef.value)
  }
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(13, 20, 42, 0.95)',
      borderColor: 'rgba(0, 198, 255, 0.3)',
      textStyle: { color: '#e0e6f0', fontSize: 12 },
      formatter: (params) => {
        const row = params[0]
        return `<b>${row.name}</b><br/>¥${row.value.toLocaleString('zh-CN', { minimumFractionDigits: 2 })}`
      },
    },
    grid: { top: 12, right: 16, bottom: 30, left: 56 },
    xAxis: {
      type: 'category',
      data: data.map((d) => platformMap[d.platform] || d.platform),
      axisLine: { lineStyle: { color: 'rgba(0,198,255,0.2)' } },
      axisLabel: { color: '#8892a4', fontSize: 11, fontFamily: 'Share Tech Mono' },
      axisTick: { show: false },
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: 'rgba(0,198,255,0.08)' } },
      axisLabel: {
        color: '#8892a4',
        fontSize: 10,
        fontFamily: 'Share Tech Mono',
        formatter: (v) => v >= 10000 ? (v / 10000).toFixed(1) + '万' : v,
      },
    },
    series: [{
      type: 'bar',
      data: data.map((d) => ({
        value: d.amount,
        itemStyle: {
          color: platformColors[d.platform] || '#00c6ff',
          borderRadius: [4, 4, 0, 0],
        },
      })),
      barWidth: '45%',
    }],
  }
  chartInstance.setOption(option)
}

const initRingChart = () => {
  if (!ringInstance) {
    ringInstance = echarts.init(ringChartRef.value)
  }
  const rate = completionRate.value
  const option = {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(13, 20, 42, 0.95)',
      borderColor: 'rgba(0, 198, 255, 0.3)',
      textStyle: { color: '#e0e6f0', fontSize: 12 },
    },
    series: [{
      type: 'pie',
      radius: ['60%', '85%'],
      center: ['50%', '50%'],
      avoidLabelOverlap: false,
      label: {
        show: true,
        position: 'center',
        formatter: () => `{rate|${rate}%}\n{label|完成率}`,
        rich: {
          rate: { fontSize: 22, fontWeight: 'bold', color: '#00c6ff', fontFamily: 'Share Tech Mono', lineHeight: 28 },
          label: { fontSize: 11, color: '#8892a4', lineHeight: 16 },
        },
      },
      labelLine: { show: false },
      data: [
        {
          value: stats.value.completed_jobs,
          name: '已完成',
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
              { offset: 0, color: '#3366ff' },
              { offset: 1, color: '#00c6ff' },
            ]),
          },
        },
        {
          value: Math.max(stats.value.total_jobs - stats.value.completed_jobs, 0),
          name: '未完成',
          itemStyle: { color: 'rgba(255,255,255,0.06)' },
        },
      ],
    }],
  }
  ringInstance.setOption(option)
}

onMounted(async () => {
  try {
    const res = await getDashboardStats()
    const data = res.data
    stats.value = {
      total_hotels: data.total_hotels || 0,
      split_hotels: data.split_hotels || 0,
      total_jobs: data.total_jobs || 0,
      completed_jobs: data.completed_jobs || 0,
      pending_review: data.pending_review || 0,
      reviewed_reports: data.reviewed_reports || 0,
      this_month_sales: Number(data.this_month_sales) || 0,
      platform_sales: data.platform_sales || [],
    }
    await nextTick()
    initBarChart(stats.value.platform_sales)
    initRingChart()
  } catch (e) {
    console.error('Failed to load dashboard stats', e)
    ElMessage.error('加载数据失败')
  }
})

watch(() => stats.value, (newVal) => {
  nextTick(() => {
    if (newVal.platform_sales) initBarChart(newVal.platform_sales)
    initRingChart()
  })
})

onUnmounted(() => {
  if (chartInstance) chartInstance.dispose()
  if (ringInstance) ringInstance.dispose()
  window.removeEventListener('resize', handleResize)
})

const handleResize = () => {
  chartInstance?.resize()
  ringInstance?.resize()
}
window.addEventListener('resize', handleResize)
</script>

<style scoped>
/* Stat cards */
.stat-card {
  background: var(--bg-card);
  border: 1px solid var(--border-glow);
  border-radius: 10px;
  padding: 20px;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(12px);
  transition: all 0.3s ease;
  cursor: default;
  display: flex;
  align-items: center;
  gap: 16px;
}

.company-banner {
  background: linear-gradient(135deg, rgba(0, 198, 255, 0.08), rgba(123, 47, 247, 0.06));
  border: 1px solid rgba(0, 198, 255, 0.25);
  border-radius: 10px;
  padding: 24px 32px;
  margin-bottom: 24px;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(12px);
  display: flex;
  align-items: center;
  gap: 20px;
}

.company-icon {
  font-size: 12px;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  background: linear-gradient(135deg, rgba(0, 198, 255, 0.2), rgba(123, 47, 247, 0.15));
  color: var(--accent-cyan);
  text-shadow: 0 0 10px rgba(0, 198, 255, 0.6);
  flex-shrink: 0;
}

.company-name {
  font-family: 'Orbitron', sans-serif;
  font-size: 20px;
  font-weight: 700;
  background: linear-gradient(90deg, var(--accent-cyan), var(--accent-purple));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 2px;
  margin-bottom: 4px;
}

.company-subtitle {
  color: var(--text-secondary);
  font-size: 13px;
  letter-spacing: 1px;
}

.company-glow {
  position: absolute;
  top: -30%;
  right: 5%;
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
  filter: blur(50px);
  opacity: 0.1;
  pointer-events: none;
}

.stat-card:hover {
  transform: translateY(-2px);
  border-color: rgba(0, 198, 255, 0.5);
}

.stat-icon {
  font-size: 10px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  flex-shrink: 0;
}

.stat-cyan .stat-icon { background: rgba(0, 198, 255, 0.15); color: var(--accent-cyan); text-shadow: 0 0 8px rgba(0, 198, 255, 0.6); }
.stat-blue .stat-icon { background: rgba(51, 102, 255, 0.15); color: var(--accent-blue); text-shadow: 0 0 8px rgba(51, 102, 255, 0.6); }
.stat-purple .stat-icon { background: rgba(123, 47, 247, 0.15); color: var(--accent-purple); text-shadow: 0 0 8px rgba(123, 47, 247, 0.6); }
.stat-pink .stat-icon { background: rgba(255, 45, 149, 0.15); color: var(--accent-pink); text-shadow: 0 0 8px rgba(255, 45, 149, 0.6); }

.stat-value {
  font-family: 'Share Tech Mono', monospace;
  font-size: 32px;
  font-weight: 700;
  line-height: 1;
  margin-bottom: 6px;
}

.stat-cyan .stat-value { color: var(--accent-cyan); text-shadow: 0 0 12px rgba(0, 198, 255, 0.4); }
.stat-blue .stat-value { color: var(--accent-blue); text-shadow: 0 0 12px rgba(51, 102, 255, 0.4); }
.stat-purple .stat-value { color: var(--accent-purple); text-shadow: 0 0 12px rgba(123, 47, 247, 0.4); }
.stat-pink .stat-value { color: var(--accent-pink); text-shadow: 0 0 12px rgba(255, 45, 149, 0.4); }

.stat-label {
  color: var(--text-secondary);
  font-size: 13px;
}

.stat-glow {
  position: absolute;
  top: -50%;
  right: -20%;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  filter: blur(40px);
  opacity: 0.15;
  pointer-events: none;
}

.stat-cyan .stat-glow { background: var(--accent-cyan); }
.stat-blue .stat-glow { background: var(--accent-blue); }
.stat-purple .stat-glow { background: var(--accent-purple); }
.stat-pink .stat-glow { background: var(--accent-pink); }

/* Card header */
.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--accent-cyan);
  box-shadow: 0 0 6px var(--accent-cyan);
}

/* Full height card */
.full-height {
  height: 100%;
}

/* Left panel */
.left-panel {
  display: flex;
  flex-direction: column;
  gap: 0;
}

/* Big number */
.big-number {
  display: flex;
  align-items: baseline;
  gap: 8px;
  padding: 12px 0 20px;
}

.big-number .currency {
  font-size: 24px;
  color: var(--accent-green);
  text-shadow: 0 0 10px rgba(0, 255, 136, 0.4);
}

.big-number .number {
  font-family: 'Share Tech Mono', monospace;
  font-size: 36px;
  font-weight: 700;
  color: var(--accent-green);
  text-shadow: 0 0 15px rgba(0, 255, 136, 0.3);
}

.big-number .number-label {
  font-size: 13px;
  color: var(--text-secondary);
  margin-left: 8px;
}

/* Platform tag */
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

.amount-text {
  font-family: 'Share Tech Mono', monospace;
  color: var(--accent-green);
}

.platform-chart {
  width: 100%;
  height: 220px;
}

.platform-chart.tall {
  height: 280px;
}

/* Ring chart */
.left-sub-row {
  display: flex;
  gap: 16px;
}

.sub-card {
  flex: 1;
  background: rgba(0, 198, 255, 0.03);
  border: 1px solid rgba(0, 198, 255, 0.1);
  border-radius: 8px;
  padding: 16px;
}

.sub-card-title {
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.sub-card-title::before {
  content: '';
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: var(--accent-cyan);
  box-shadow: 0 0 4px var(--accent-cyan);
}

.reconciliation-section {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 4px 0;
}

.ring-chart {
  width: 100px;
  height: 100px;
  flex-shrink: 0;
}

.ring-stats {
  display: flex;
  flex-direction: column;
  gap: 8px;
  justify-content: center;
}

.stat-line {
  font-size: 13px;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 6px;
}

.stat-line b {
  color: var(--text-primary);
  font-family: 'Share Tech Mono', monospace;
}

.stat-line.highlight {
  color: var(--accent-cyan);
  margin-top: 4px;
}

.stat-line.highlight b.rate {
  font-size: 20px;
  font-weight: 700;
  color: var(--accent-green);
  text-shadow: 0 0 8px rgba(0, 255, 136, 0.3);
}

.stat-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}

.stat-dot.cyan { background: var(--accent-cyan); box-shadow: 0 0 4px var(--accent-cyan); }
.stat-dot.green { background: var(--accent-green); box-shadow: 0 0 4px var(--accent-green); }

/* Settlement stats */
.settlement-stats {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: flex-start;
  gap: 20px;
  padding: 12px 0;
}

.settle-item {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 2px;
}

.settle-label {
  font-size: 12px;
  color: var(--text-secondary);
}

.settle-value {
  font-size: 28px;
  font-weight: 700;
  font-family: 'Share Tech Mono', monospace;
}

.settle-value.green { color: var(--accent-green); text-shadow: 0 0 8px rgba(0, 255, 136, 0.3); }
.settle-value.cyan { color: var(--accent-cyan); text-shadow: 0 0 8px rgba(0, 198, 255, 0.3); }

.settle-unit {
  font-size: 11px;
  color: var(--text-secondary);
}

.settle-divider {
  width: 1px;
  height: 40px;
  background: rgba(0, 198, 255, 0.15);
}

.section-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0, 198, 255, 0.2), rgba(123, 47, 247, 0.15), transparent);
  margin: 8px 0;
}

</style>
