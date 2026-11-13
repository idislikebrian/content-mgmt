import type { NetworkType } from "./types"

export interface NetworkAccount {
  network: NetworkType
  username: string
  connected: boolean
  accessToken?: string
  lastSync?: Date
}

const ACCOUNTS_KEY = "network_accounts"

export const NetworkStore = {
  getAccounts(): NetworkAccount[] {
    if (typeof window === "undefined") return []
    const data = localStorage.getItem(ACCOUNTS_KEY)
    if (!data) return []
    return JSON.parse(data, (key, value) => {
      if (key === "lastSync") {
        return value ? new Date(value) : undefined
      }
      return value
    })
  },

  saveAccounts(accounts: NetworkAccount[]) {
    if (typeof window === "undefined") return
    localStorage.setItem(ACCOUNTS_KEY, JSON.stringify(accounts))
  },

  connectAccount(network: NetworkType, username: string, accessToken: string): NetworkAccount {
    const accounts = this.getAccounts()
    const existing = accounts.findIndex((a) => a.network === network)

    const account: NetworkAccount = {
      network,
      username,
      connected: true,
      accessToken,
      lastSync: new Date(),
    }

    if (existing >= 0) {
      accounts[existing] = account
    } else {
      accounts.push(account)
    }

    this.saveAccounts(accounts)
    return account
  },

  disconnectAccount(network: NetworkType) {
    const accounts = this.getAccounts().filter((a) => a.network !== network)
    this.saveAccounts(accounts)
  },

  getAccount(network: NetworkType): NetworkAccount | undefined {
    return this.getAccounts().find((a) => a.network === network)
  },

  isConnected(network: NetworkType): boolean {
    const account = this.getAccount(network)
    return account?.connected || false
  },
}
