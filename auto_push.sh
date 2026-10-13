#!/bin/bash
while true; do
  cp ~/qdexxbot/allowed_miners.json ./allowed_miners.json
  cp ~/qdexxbot/bonus_claims.json ./bonus_claims.json 2>/dev/null
  git add allowed_miners.json bonus_claims.json
  if ! git diff --cached --quiet; then
    git config user.email "qdexx@bot.local"
    git config user.name "QDEXX Bot"
    git commit -m "Auto: $(date '+%H:%M %d/%m') new miner"
    git push origin main
    echo "✅ PUSHED $(date)"
  else
    echo "No change $(date)"
  fi
  sleep 300
done
