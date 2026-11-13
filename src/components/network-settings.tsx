"use client"

import { useState, useEffect } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"
import { NetworkStore, type NetworkAccount } from "@/lib/network-store"
import type { NetworkType } from "@/lib/types"
import { Link2, Unlink, CheckCircle2, AlertCircle, ExternalLink } from "lucide-react"

const networkInfo: Record<
  NetworkType,
  {
    name: string
    color: string
    icon: string
    description: string
    docsUrl: string
  }
> = {
  farcaster: {
    name: "Farcaster",
    color: "bg-purple-500",
    icon: "🟣",
    description: "Decentralized social network protocol",
    docsUrl: "https://docs.farcaster.xyz",
  },
  bluesky: {
    name: "BlueSky",
    color: "bg-blue-500",
    icon: "🦋",
    description: "Open social network protocol",
    docsUrl: "https://docs.bsky.app",
  },
  mastodon: {
    name: "Mastodon",
    color: "bg-indigo-500",
    icon: "🐘",
    description: "Federated microblogging platform",
    docsUrl: "https://docs.joinmastodon.org",
  },
}

export function NetworkSettings() {
  const [accounts, setAccounts] = useState<NetworkAccount[]>([])
  const [connectDialogOpen, setConnectDialogOpen] = useState(false)
  const [selectedNetwork, setSelectedNetwork] = useState<NetworkType | null>(null)
  const [username, setUsername] = useState("")
  const [accessToken, setAccessToken] = useState("")

  useEffect(() => {
    setAccounts(NetworkStore.getAccounts())
  }, [])

  const handleConnect = (network: NetworkType) => {
    setSelectedNetwork(network)
    setConnectDialogOpen(true)
    setUsername("")
    setAccessToken("")
  }

  const handleSaveConnection = () => {
    if (!selectedNetwork || !username || !accessToken) return

    const account = NetworkStore.connectAccount(selectedNetwork, username, accessToken)
    setAccounts([...NetworkStore.getAccounts()])
    setConnectDialogOpen(false)
    setSelectedNetwork(null)
    setUsername("")
    setAccessToken("")
  }

  const handleDisconnect = (network: NetworkType) => {
    NetworkStore.disconnectAccount(network)
    setAccounts([...NetworkStore.getAccounts()])
  }

  const getAccountForNetwork = (network: NetworkType) => {
    return accounts.find((a) => a.network === network)
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold mb-2">Network Connections</h2>
        <p className="text-muted-foreground">Manage your social network accounts for posting</p>
      </div>

      <div className="grid md:grid-cols-3 gap-4">
        {(Object.keys(networkInfo) as NetworkType[]).map((network) => {
          const info = networkInfo[network]
          const account = getAccountForNetwork(network)
          const isConnected = account?.connected || false

          return (
            <Card key={network} className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className={`w-12 h-12 rounded-lg ${info.color} flex items-center justify-center text-2xl`}>
                    {info.icon}
                  </div>
                  <div>
                    <h3 className="font-semibold">{info.name}</h3>
                    {isConnected ? (
                      <Badge className="bg-green-500 mt-1">
                        <CheckCircle2 className="w-3 h-3 mr-1" />
                        Connected
                      </Badge>
                    ) : (
                      <Badge variant="secondary" className="mt-1">
                        <AlertCircle className="w-3 h-3 mr-1" />
                        Not connected
                      </Badge>
                    )}
                  </div>
                </div>
              </div>

              <p className="text-sm text-muted-foreground mb-4">{info.description}</p>

              {isConnected && account && (
                <div className="mb-4 p-3 rounded-lg bg-muted/50">
                  <p className="text-xs text-muted-foreground mb-1">Connected as</p>
                  <p className="text-sm font-medium">@{account.username}</p>
                </div>
              )}

              <div className="flex gap-2">
                {isConnected ? (
                  <Button onClick={() => handleDisconnect(network)} variant="outline" size="sm" className="flex-1">
                    <Unlink className="w-4 h-4 mr-2" />
                    Disconnect
                  </Button>
                ) : (
                  <Button onClick={() => handleConnect(network)} size="sm" className="flex-1">
                    <Link2 className="w-4 h-4 mr-2" />
                    Connect
                  </Button>
                )}
                <Button variant="ghost" size="sm" asChild>
                  <a href={info.docsUrl} target="_blank" rel="noopener noreferrer">
                    <ExternalLink className="w-4 h-4" />
                  </a>
                </Button>
              </div>
            </Card>
          )
        })}
      </div>

      <Card className="p-6 bg-muted/50">
        <div className="flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-muted-foreground mt-0.5" />
          <div>
            <h4 className="font-semibold mb-1">API Keys & Authentication</h4>
            <p className="text-sm text-muted-foreground">
              To connect your accounts, you'll need to obtain API keys or access tokens from each platform. This demo
              stores credentials in local storage for demonstration purposes only. In production, use secure server-side
              authentication.
            </p>
          </div>
        </div>
      </Card>

      <Dialog open={connectDialogOpen} onOpenChange={setConnectDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Connect {selectedNetwork && networkInfo[selectedNetwork].name}</DialogTitle>
          </DialogHeader>

          <div className="space-y-4">
            <div>
              <Label htmlFor="username">Username</Label>
              <Input
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="your_username"
                className="mt-2"
              />
            </div>

            <div>
              <Label htmlFor="token">Access Token / API Key</Label>
              <Input
                id="token"
                type="password"
                value={accessToken}
                onChange={(e) => setAccessToken(e.target.value)}
                placeholder="Enter your access token"
                className="mt-2"
              />
              <p className="text-xs text-muted-foreground mt-1">
                Get your API key from the{" "}
                {selectedNetwork && (
                  <a
                    href={networkInfo[selectedNetwork].docsUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="underline"
                  >
                    {networkInfo[selectedNetwork].name} developer portal
                  </a>
                )}
              </p>
            </div>
          </div>

          <DialogFooter>
            <Button variant="outline" onClick={() => setConnectDialogOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleSaveConnection} disabled={!username || !accessToken}>
              Connect Account
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
