import { defineStore } from "pinia"

export const useUIStore = defineStore("ui", {
  state: () => ({
    loading: false,
    sidebarOpen: true,
    isWarningVisible: false
  }),

  actions: {
    setLoading(val) {
      this.loading = val
    },
    toggleSidebar() {
      this.sidebarOpen = !this.sidebarOpen
    },
    showWarning() {
      this.isWarningVisible = true
    },
    hideWarning() {
      this.isWarningVisible = false
    }
  }
})