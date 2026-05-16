<template>
  <el-container style="height: 100vh">
    <el-aside width="220px">
      <div class="logo">
        <div class="logo-icon">&#9670;</div>
        <div class="logo-text">对账系统</div>
        <div class="logo-line"></div>
      </div>
      <el-menu
        :default-active="$route.path"
        router
        background-color="transparent"
        text-color="#8892a4"
        active-text-color="#00c6ff"
      >
        <el-menu-item index="/">
          <span class="menu-icon">&#9632;</span>
          <span>首页</span>
        </el-menu-item>
        <el-menu-item index="/hotels">
          <span class="menu-icon">&#9632;</span>
          <span>酒店管理</span>
        </el-menu-item>
        <el-menu-item index="/platforms">
          <span class="menu-icon">&#9632;</span>
          <span>平台账号</span>
        </el-menu-item>
        <el-menu-item index="/sales">
          <span class="menu-icon">&#9632;</span>
          <span>销售数据</span>
        </el-menu-item>
        <el-menu-item index="/expenses">
          <span class="menu-icon">&#9632;</span>
          <span>日常开支</span>
        </el-menu-item>
        <el-menu-item index="/reconciliation">
          <span class="menu-icon">&#9632;</span>
          <span>对账管理</span>
        </el-menu-item>
        <el-menu-item index="/reports">
          <span class="menu-icon">&#9632;</span>
          <span>报表中心</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-main>
      <slot />
    </el-main>
  </el-container>
</template>

<style scoped>
.el-aside {
  background: linear-gradient(180deg, rgba(8, 12, 28, 0.97) 0%, rgba(5, 10, 22, 0.99) 100%) !important;
  border-right: 1px solid rgba(0, 198, 255, 0.12);
  box-shadow: 2px 0 20px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
}

.logo {
  height: 72px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  border-bottom: 1px solid rgba(0, 198, 255, 0.1);
}

.logo-icon {
  font-size: 10px;
  color: var(--accent-cyan);
  text-shadow: 0 0 8px rgba(0, 198, 255, 0.6);
  margin-bottom: 2px;
}

.logo-text {
  color: #e0e6f0;
  font-family: 'Orbitron', sans-serif;
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 4px;
  text-shadow: 0 0 15px rgba(0, 198, 255, 0.4);
}

.logo-line {
  position: absolute;
  bottom: 0;
  width: 60%;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--accent-cyan), transparent);
}

/* Menu overrides */
.el-menu {
  background: transparent !important;
  border-right: none !important;
  padding: 8px 0;
}

.el-menu-item {
  margin: 2px 8px;
  border-radius: 6px;
  transition: all 0.2s ease;
  position: relative;
  font-size: 14px;
  border: 1px solid transparent;
}

.el-menu-item .menu-icon {
  color: var(--accent-cyan);
  margin-right: 2px;
  font-size: 8px;
  opacity: 0.5;
  transition: opacity 0.2s;
}

.el-menu-item:hover {
  background: rgba(0, 198, 255, 0.08) !important;
  border-color: rgba(0, 198, 255, 0.15) !important;
}

.el-menu-item:hover .menu-icon {
  opacity: 1;
}

.el-menu-item.is-active {
  background: linear-gradient(90deg, rgba(0, 198, 255, 0.15), rgba(0, 198, 255, 0.03)) !important;
  color: var(--accent-cyan) !important;
  border-color: rgba(0, 198, 255, 0.25) !important;
  box-shadow: 0 0 15px rgba(0, 198, 255, 0.1), inset 2px 0 0 var(--accent-cyan);
}

.el-menu-item.is-active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 20%;
  bottom: 20%;
  width: 2px;
  background: var(--accent-cyan);
  border-radius: 0 2px 2px 0;
  box-shadow: 0 0 8px rgba(0, 198, 255, 0.6);
}

</style>
