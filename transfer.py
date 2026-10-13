import json, time, hashlib, sys, os

CHAIN_FILE = "qdexx_chain.json"
MY_ADDR = "QDX4F37B68A5C7FF70AF7F6CE1C746B4F6259E"

def load_chain():
    with open(CHAIN_FILE, 'r') as f:
        data = json.load(f)
        return data if isinstance(data, list) else data.get('chain', [])

def save_chain(chain):
    with open(CHAIN_FILE, 'w') as f:
        json.dump(chain, f, indent=2)

def get_balance(chain, addr):
    bal = 50.0 # genesis
    for b in chain:
        # reward miner
        if b.get('miner') == 'ryzkii_brc' or b.get('miner_address') == addr:
            if b.get('index', 0) > 0:
                bal += 0.5
        # tx
        tx = b.get('transaction') or b.get('data') or {}
        if isinstance(tx, dict):
            if tx.get('from') == addr:
                bal -= float(tx.get('amount', 0))
            if tx.get('to') == addr:
                bal += float(tx.get('amount', 0))
    return bal

def hash_block(block):
    s = json.dumps(block, sort_keys=True)
    return hashlib.sha256(s.encode()).hexdigest()

if len(sys.argv) < 3:
    print(f"Usage: python transfer.py <TO_ADDRESS> <AMOUNT>")
    print(f"Contoh: python transfer.py QDXABCD123 10")
    sys.exit(1)

to_addr = sys.argv[1]
amount = float(sys.argv[2])

chain = load_chain()
bal = get_balance(chain, MY_ADDR)

print(f"Saldo lu sekarang: {bal} QDX")
if amount > bal:
    print(f"❌ Saldo gak cukup! Lu punya {bal}, mau kirim {amount}")
    sys.exit(1)

# bikin block baru
last = chain[-1]
new_block = {
    "index": len(chain),
    "timestamp": int(time.time()),
    "prev_hash": last.get('hash') or last.get('prev_hash'),
    "miner": "ryzkii_brc",
    "miner_address": MY_ADDR,
    "transaction": {
        "from": MY_ADDR,
        "to": to_addr,
        "amount": amount,
        "note": f"Transfer by @qdexxx"
    },
    "nonce": 0
}
new_block["hash"] = hash_block(new_block)

chain.append(new_block)
save_chain(chain)

print(f"\n✅ TRANSFER BERHASIL!")
print(f"Block #{new_block['index']} | {amount} QDX -> {to_addr}")
print(f"Hash: {new_block['hash'][:20]}...")
print(f"Sisa saldo: {bal - amount} QDX")

# auto push ke github
os.system("git add qdexx_chain.json")
os.system(f'git commit -m "transfer {amount} QDX to {to_addr[:10]} block #{new_block["index"]}"')
os.system("git push origin main")
print("\n🚀 Chain udah ke-push! Cek web lu bakal update Block #418+")
