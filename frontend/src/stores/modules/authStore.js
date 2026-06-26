import { defineStore } from "pinia"

import {
  login as loginRequest, 
  logout as logoutRequest
} from "@/api/modules/auth"
import {
  clearAccessToken,
  refreshAccessToken,
  setAccessToken
} from "@/api/core/authSession"
 

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    initialized: false,
    loading: false
  }),

  getters: {
    isAuthenticated: (state) => Boolean(state.user),
    roles: (state) => state.user?.roles || [],
    permissions: (state) => state.user?.permissions || []
  },

  actions: {
    async initialize() {
      if (this.initialized) return

      this.loading = true

      try {
        const data = await refreshAccessToken()
        this.user = data.user
      } catch {
        clearAccessToken()
        this.user = null
      } finally {
        this.loading = false
        this.initialized = true
      }
    },

    async login(credentials) {
      this.loading = true

      try {
        const data = await loginRequest(credentials)
        setAccessToken(data.access_token)
        this.user = data.user
        this.initialized = true

        return data.user
      } finally {
        this.loading = false
      }
    },

    async logout() {
      try {
        await logoutRequest()
      } finally {
        clearAccessToken()
        this.user = null
        this.initialized = true
      }
    },

    hasPermission(permission) {
      return Boolean(
        this.user?.is_superuser
        || this.permissions.includes(permission)
      )
    },

    hasRole(role) {
      return Boolean(
        this.user?.is_superuser
        || this.roles.includes(role)
      )
    }
  }
})
