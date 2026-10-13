cp ~/qdexxbot/allowed_miners.json ./allowed_miners.json
cp ~/qdexxbot/bonus_claims.json ./bonus_claims.json 2>/dev/null
git add allowed_miners.json bonus_claims.json
git commit -m "Update miners $(date)" 2>/dev/null
git push origin main
echo "Done push"
