<template>
  <Layout>
    <router-view />
  </Layout>
</template>

<script setup>
import Layout from './components/Layout.vue'
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');

:root {
  --bg-primary: #0a0e1a;
  --bg-secondary: #0d1429;
  --bg-card: rgba(13, 20, 42, 0.7);
  --bg-card-hover: rgba(20, 30, 60, 0.8);
  --border-glow: rgba(0, 198, 255, 0.3);
  --text-primary: #e0e6f0;
  --text-secondary: #8892a4;
  --accent-cyan: #00c6ff;
  --accent-blue: #3366ff;
  --accent-purple: #7b2ff7;
  --accent-pink: #ff2d95;
  --accent-green: #00ff88;
  --neon-glow: 0 0 10px rgba(0, 198, 255, 0.3), 0 0 40px rgba(0, 198, 255, 0.1);
  --card-glow: 0 0 15px rgba(0, 198, 255, 0.08);
}

* { box-sizing: border-box; }

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: var(--bg-primary);
  color: var(--text-primary);
}

/* Grid background */
body::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(0, 198, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 198, 255, 0.03) 1px, transparent 1px);
  background-size: 40px 40px;
  pointer-events: none;
  z-index: 0;
}

/* Radial gradient overlay */
body::after {
  content: '';
  position: fixed;
  inset: 0;
  background: radial-gradient(ellipse at 20% 0%, rgba(51, 102, 255, 0.1) 0%, transparent 60%),
              radial-gradient(ellipse at 80% 100%, rgba(123, 47, 247, 0.08) 0%, transparent 60%);
  pointer-events: none;
  z-index: 0;
}

/* Global Element Plus overrides */
.el-container { position: relative; z-index: 1; }

.el-main {
  background: transparent !important;
  padding: 24px !important;
}

.el-aside {
  background: transparent !important;
}

/* Cards - glass-morphism */
.el-card {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-glow) !important;
  border-radius: 8px !important;
  box-shadow: var(--card-glow) !important;
  backdrop-filter: blur(12px);
}

.el-card:hover {
  background: var(--bg-card-hover) !important;
  box-shadow: var(--neon-glow) !important;
  border-color: rgba(0, 198, 255, 0.5) !important;
}

.el-card__header {
  border-bottom-color: rgba(0, 198, 255, 0.15) !important;
  color: var(--accent-cyan) !important;
  font-weight: 600;
}

.el-card__body {
  color: var(--text-primary);
}

/* Table */
.el-table {
  --el-table-bg-color: transparent !important;
  --el-table-header-bg-color: rgba(0, 198, 255, 0.08) !important;
  --el-table-tr-bg-color: transparent !important;
  --el-table-row-hover-bg-color: rgba(0, 198, 255, 0.06) !important;
  --el-table-border-color: rgba(0, 198, 255, 0.1) !important;
  --el-table-text-color: var(--text-primary) !important;
  --el-table-header-text-color: var(--accent-cyan) !important;
  --el-table-fixed-bg-color: transparent !important;
  background: transparent !important;
}

.el-table th {
  color: var(--accent-cyan) !important;
  font-weight: 600 !important;
  letter-spacing: 0.5px;
}

.el-table td {
  color: var(--text-primary) !important;
  border-bottom-color: rgba(0, 198, 255, 0.08) !important;
}

.el-table--enable-row-hover tr:hover > td {
  background: rgba(0, 198, 255, 0.06) !important;
}

.el-table--striped .el-table__body tr.el-table__row--striped td {
  background: rgba(0, 198, 255, 0.02) !important;
}

/* Buttons */
.el-button--primary {
  --el-button-bg-color: linear-gradient(135deg, var(--accent-blue), var(--accent-cyan)) !important;
  --el-button-border-color: var(--accent-cyan) !important;
  background-image: linear-gradient(135deg, var(--accent-blue), var(--accent-cyan)) !important;
  border: none !important;
  border-radius: 6px !important;
  box-shadow: 0 0 15px rgba(0, 198, 255, 0.25) !important;
  font-weight: 600;
}

.el-button--primary:hover {
  box-shadow: 0 0 25px rgba(0, 198, 255, 0.4) !important;
}

.el-button--success {
  background: linear-gradient(135deg, #00b36a, var(--accent-green)) !important;
  border: none !important;
  border-radius: 6px !important;
  box-shadow: 0 0 15px rgba(0, 255, 136, 0.2) !important;
  color: #000 !important;
  font-weight: 600;
}

.el-button--success:hover {
  box-shadow: 0 0 25px rgba(0, 255, 136, 0.35) !important;
}

.el-button--danger {
  background: linear-gradient(135deg, #ff1744, var(--accent-pink)) !important;
  border: none !important;
  border-radius: 6px !important;
  box-shadow: 0 0 12px rgba(255, 45, 149, 0.2) !important;
  font-weight: 600;
}

.el-button {
  border-radius: 6px !important;
  font-weight: 500;
}

.el-button--default {
  background: rgba(255, 255, 255, 0.05) !important;
  border-color: rgba(0, 198, 255, 0.25) !important;
  color: var(--text-primary) !important;
}

.el-button--default:hover {
  background: rgba(0, 198, 255, 0.1) !important;
  border-color: var(--accent-cyan) !important;
}

/* Input / Select */
.el-input__wrapper,
.el-textarea__inner {
  background: rgba(0, 15, 30, 0.5) !important;
  border-color: rgba(0, 198, 255, 0.2) !important;
  border-radius: 6px !important;
  box-shadow: 0 0 0 1px rgba(0, 198, 255, 0.08) !important;
  color: var(--text-primary) !important;
}

.el-input__wrapper:focus,
.el-textarea__inner:focus {
  border-color: var(--accent-cyan) !important;
  box-shadow: 0 0 15px rgba(0, 198, 255, 0.2) !important;
}

.el-input__inner,
.el-textarea__inner {
  color: var(--text-primary) !important;
}

.el-select-dropdown {
  background: var(--bg-secondary) !important;
  border: 1px solid var(--border-glow) !important;
  border-radius: 8px !important;
}

.el-select-dropdown__item {
  color: var(--text-primary) !important;
}

.el-select-dropdown__item.hover,
.el-select-dropdown__item:hover {
  background: rgba(0, 198, 255, 0.1) !important;
  color: var(--accent-cyan) !important;
}

/* Form labels */
.el-form-item__label {
  color: var(--text-secondary) !important;
}

/* Tag */
.el-tag {
  border-radius: 4px !important;
  border: none !important;
  font-weight: 500;
}

/* Dialog overlay - prevent invisible overlays from blocking clicks */
.el-overlay {
  background-color: rgba(0, 0, 0, 0.7) !important;
}

/* Fix: make ALL overlays non-clickable, then re-enable only the content inside */
.el-overlay-fade-enter-from,
.el-overlay-fade-leave-from,
.el-overlay-fade-leave-to {
  pointer-events: none !important;
}

/* Only center dialog overlays, not message/popover overlays */
.el-overlay-dialog {
  display: flex !important;
  align-items: center !important;
}

/* Ensure dialog content is always clickable even when overlay stacking is off */
.el-dialog {
  pointer-events: auto !important;
}

.el-dialog {
  background: var(--bg-secondary) !important;
  border: 1px solid var(--border-glow) !important;
  border-radius: 12px !important;
  box-shadow: var(--neon-glow) !important;
}

.el-dialog__header {
  border-bottom-color: rgba(0, 198, 255, 0.15) !important;
}

.el-dialog__title {
  color: var(--accent-cyan) !important;
  font-family: 'Orbitron', sans-serif;
  font-weight: 700;
  letter-spacing: 1px;
}

.el-dialog__body {
  color: var(--text-primary);
}

/* Switch */
.el-switch__core {
  background: rgba(255, 255, 255, 0.1) !important;
  border-color: rgba(255, 255, 255, 0.2) !important;
}

.el-switch.is-checked .el-switch__core {
  background: var(--accent-cyan) !important;
  border-color: var(--accent-cyan) !important;
  box-shadow: 0 0 10px rgba(0, 198, 255, 0.4) !important;
}

/* Statistic */
.el-statistic__content {
  color: var(--accent-cyan) !important;
  font-family: 'Share Tech Mono', monospace !important;
}

.el-statistic__head {
  color: var(--text-secondary) !important;
}

/* Descriptions */
.el-descriptions__label {
  color: var(--text-secondary) !important;
  background: rgba(0, 198, 255, 0.04) !important;
}

.el-descriptions__content {
  color: var(--text-primary) !important;
}

.el-descriptions__content.el-descriptions__content--string {
  color: var(--accent-cyan) !important;
}

.el-descriptions__body {
  border-color: rgba(0, 198, 255, 0.12) !important;
}

.el-descriptions__header {
  border-bottom-color: rgba(0, 198, 255, 0.12) !important;
}

/* Date picker */
.el-picker-panel {
  background: var(--bg-secondary) !important;
  border: 1px solid var(--border-glow) !important;
  border-radius: 8px !important;
  color: var(--text-primary) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(0, 198, 255, 0.25); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(0, 198, 255, 0.4); }

/* Section titles */
h2 {
  font-family: 'Orbitron', sans-serif;
  color: var(--accent-cyan);
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 20px;
  letter-spacing: 2px;
  text-shadow: 0 0 20px rgba(0, 198, 255, 0.3);
  position: relative;
  padding-bottom: 10px;
}

h2::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 2px;
  background: linear-gradient(90deg, var(--accent-cyan), transparent);
}

/* Input number */
.el-input-number {
  --el-fill-color-blank: rgba(0, 15, 30, 0.5) !important;
}

.el-input-number__increase,
.el-input-number__decrease {
  background: rgba(0, 198, 255, 0.15) !important;
  color: var(--accent-cyan) !important;
  border-color: rgba(0, 198, 255, 0.3) !important;
}

/* Message / Notification */
.el-message {
  background: var(--bg-secondary) !important;
  border: 1px solid var(--border-glow) !important;
  border-radius: 8px !important;
  box-shadow: var(--neon-glow) !important;
  color: var(--text-primary) !important;
}

.el-message__content {
  color: var(--text-primary) !important;
}

.el-message__closeBtn {
  color: var(--accent-cyan) !important;
  font-size: 16px !important;
}

.el-message__closeBtn:hover {
  color: #fff !important;
}

/* MessageBox */
.el-message-box {
  background: var(--bg-secondary) !important;
  border: 1px solid var(--border-glow) !important;
  border-radius: 12px !important;
}

.el-message-box__title {
  color: var(--accent-cyan) !important;
}

.el-message-box__content,
.el-message-box__message {
  color: var(--text-primary) !important;
}

.el-message-box__input {
  color: var(--text-primary) !important;
}

.el-message-box__errmsg {
  color: var(--accent-pink) !important;
  font-size: 12px !important;
}

/* Popper / Tooltip overlays (portaled) */
.el-popper,
.el-popper.is-light {
  background: var(--bg-secondary) !important;
  border: 1px solid var(--border-glow) !important;
  border-radius: 8px !important;
  box-shadow: var(--neon-glow) !important;
  color: var(--text-primary) !important;
}

.el-popper .el-popper__arrow::before {
  background: var(--bg-secondary) !important;
  border-color: var(--border-glow) !important;
}

/* Select inner arrow button */
.el-select .el-input__suffix-inner {
  color: var(--accent-cyan) !important;
}

/* Pagination */
.el-pagination button {
  background: transparent !important;
  color: var(--text-primary) !important;
  border: 1px solid rgba(0, 198, 255, 0.15) !important;
  border-radius: 4px !important;
}

.el-pagination button:hover {
  color: var(--accent-cyan) !important;
}

.el-pagination .el-pager li {
  background: transparent !important;
  color: var(--text-primary) !important;
  border: 1px solid rgba(0, 198, 255, 0.12) !important;
  border-radius: 4px !important;
}

.el-pagination .el-pager li:hover {
  color: var(--accent-cyan) !important;
}

.el-pagination .el-pager li.is-active {
  background: var(--accent-cyan) !important;
  border-color: var(--accent-cyan) !important;
  color: #000 !important;
  box-shadow: 0 0 8px rgba(0, 198, 255, 0.4) !important;
}

.el-pagination span {
  color: var(--text-secondary) !important;
}

/* Checkbox / Radio */
.el-checkbox__input.is-checked + .el-checkbox__label {
  color: var(--text-primary) !important;
}

.el-checkbox__inner {
  background: rgba(0, 15, 30, 0.5) !important;
  border-color: rgba(0, 198, 255, 0.25) !important;
}

.el-checkbox__input.is-checked .el-checkbox__inner {
  background: var(--accent-cyan) !important;
  border-color: var(--accent-cyan) !important;
  box-shadow: 0 0 6px rgba(0, 198, 255, 0.3) !important;
}

/* Loading overlay */
.el-loading-mask {
  background: rgba(10, 14, 26, 0.8) !important;
}

.el-loading-spinner .circular {
  stroke: var(--accent-cyan) !important;
}

/* Skeleton */
.el-skeleton__item {
  background: linear-gradient(90deg, rgba(0, 198, 255, 0.04) 25%, rgba(0, 198, 255, 0.08) 50%, rgba(0, 198, 255, 0.04) 75%) !important;
}

/* Dialog close button */
.el-dialog__headerbtn {
  color: var(--text-secondary) !important;
}

.el-dialog__headerbtn .el-dialog__close {
  color: var(--text-secondary) !important;
}

.el-dialog__headerbtn:hover .el-dialog__close {
  color: var(--accent-cyan) !important;
}

/* Table placeholder */
.el-table__empty-text {
  color: var(--text-secondary) !important;
}

.el-table__empty-block {
  background: transparent !important;
}

/* Divider */
.el-divider__text {
  color: var(--accent-cyan) !important;
}

.el-divider--horizontal {
  border-top-color: rgba(0, 198, 255, 0.15) !important;
}

</style>
