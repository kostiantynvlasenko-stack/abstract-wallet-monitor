# Abstract Wallet Monitor

ETH balance monitoring system for wallets on Abstract L2 network with automatic Slack alerts.

## 🎯 Features

- Monitors 6 wallets every 5 minutes
- Slack DM alert when balance < 0.0015 ETH
- Recovery alert when balance is restored
- Status table on startup

## 🚀 Quick Start

### Option 1: Local Setup

```bash
# Clone repository
git clone https://github.com/AceKonstantin/abstract-wallet-monitor.git
cd abstract-wallet-monitor

# Install dependencies
pip3 install -r requirements.txt

# Set environment variable and run
export SLACK_BOT_TOKEN="your-slack-bot-token"
python3 main.py
```

### Option 2: Railway Deploy

1. Go to https://railway.app
2. Login with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your repository
5. Go to **Variables** → Add:
   ```
   SLACK_BOT_TOKEN = <your-slack-bot-token>
   ```
6. Deploy will start automatically

## 📊 Monitored Wallets

| Wallet | Address |
|--------|---------|
| Settler Wallet | `0xA3f8c5E0037f9f70b38d5140542432f40BcE71CB` |
| Organizer Admin #1 | `0xcd835fa14e546f55b0e4b4fcfccce6dc756ae3d5` |
| Organizer Admin #2 | `0x08c83c4bf828c846f062d8bc6ddb02101e67e81c` |
| Organizer Admin #3 | `0x519e8a7c7c195d98068bbd849169c476892b662d` |
| Organizer Admin #4 | `0xcff06e5c3838c8fabf5b53f8a69ef943f94e07f3` |
| Organizer Admin #5 | `0x662dd356442943a34a83ad0f18067875dfc72474` |

## ⚙️ Configuration

| Parameter | Value |
|-----------|-------|
| Alert threshold | 0.0015 ETH |
| Check interval | 5 minutes |
| RPC | https://api.mainnet.abs.xyz |

## 🔔 Alert Types

- 🔴 **LOW BALANCE** — balance dropped below threshold
- ✅ **BALANCE RECOVERED** — balance restored above threshold
- ⚠️ **MONITORING ERROR** — RPC unavailable for 15+ minutes

## 🔧 Getting Slack Bot Token

1. Go to https://api.slack.com/apps
2. Click **"Create New App"** → **"From scratch"**
3. Name: `Wallet Monitor`, Workspace: yours
4. In left menu: **"OAuth & Permissions"**
5. In **"Scopes"** → **"Bot Token Scopes"** add:
   - `chat:write`
   - `im:write`
6. Scroll up → **"Install to Workspace"**
7. Copy **"Bot User OAuth Token"** (starts with `xoxb-`)

## 📝 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SLACK_BOT_TOKEN` | Yes | Slack Bot OAuth Token |
