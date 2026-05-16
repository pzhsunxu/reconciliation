import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(ElementPlus)
app.use(router)
app.mount('#app')

// Catch unhandled promise rejections that could leave overlays stuck
window.addEventListener('unhandledrejection', (event) => {
  console.error('Unhandled promise rejection:', event.reason)
  event.preventDefault()
})

app.config.errorHandler = (err, instance, info) => {
  console.error('Vue error in', info, ':', err)
}

// Fix: clean up stale invisible overlay elements that block clicks
// Element Plus leaves .el-overlay elements with opacity:0 briefly after dialog close.
// Rapid dialog open/close can stack these, making new dialogs unclickable.
setInterval(() => {
  const overlays = document.querySelectorAll('.el-overlay')
  overlays.forEach((overlay) => {
    const style = window.getComputedStyle(overlay)
    const opacity = parseFloat(style.opacity)
    if (opacity === 0 && overlay.childElementCount === 0) {
      overlay.remove()
    }
  })
}, 500)

// Also watch for stuck overlays via MutationObserver
const overlayObserver = new MutationObserver(() => {
  requestAnimationFrame(() => {
    const overlays = document.querySelectorAll('.el-overlay')
    if (overlays.length > 2) {
      // Too many overlays stacked — remove empty invisible ones
      overlays.forEach((overlay) => {
        if (overlay.childElementCount === 0) {
          overlay.remove()
        }
      })
    }
  })
})
overlayObserver.observe(document.body, { childList: true, subtree: false })
