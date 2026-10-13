#!/bin/bash
while true; do
  cd ~/qdexxcoin
  cp ~/qdexxbot/allowed_miners.json ./allowed_miners.json
  cp ~/qdexxbot/bonus_claims.json ./bonus_claims.json 2>/dev/null
  git pull --rebase origin main > /dev/null 2>&1
  git add -f allowed_miners.json bonus_claims.json
  if ! git diff --cached --quiet; then
    git commit -m "Auto miner $(date '+%H:%M')" > /dev/null
    git push origin main > /dev/null 2>&1
    echo "✅ PUSHED $(date)"
  else
    echo "No change $(date)"
  fi
  sleep 300
done
