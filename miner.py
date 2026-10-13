import json, time, hashlib, random, os
from datetime import datetime

CHAIN="qdexx_chain.json"
WALLET="qdexx_wallets.json"

def load_chain():
    try:
        with open(CHAIN,'r') as f: return json.load(f)
    except:
        return [{"index":0,"hash":"0000genesis_qdexx","prev_hash":"0","timestamp":"2026-05-13","data":"Genesis by @qdexxx","miner":"ryzkii_brc"}]

def save_chain(c):
    with open(CHAIN,'w') as f: json.dump(c,f,indent=2)

def update_wallet():
    try:
        with open(WALLET,'r') as f:
            w=json.load(f)
        # cari alamat Rizky
        for addr in w:
            if w[addr].get("nama")=="Rizky" or "QDX4F37" in addr:
                w[addr]["saldo"]=w[addr].get("saldo",50)+0.5
                print(f"💰 Saldo {w[addr]['nama']} -> {w[addr]['saldo']} QDX")
                break
        with open(WALLET,'w') as f:
            json.dump(w,f,indent=2)
    except Exception as e:
        print(f"Wallet error: {e}")

print("⛏️ QDEXX MINER V2.1 FIXED WALLET")

count=0
while True:
    chain=load_chain()
    last=chain[-1]
    idx=last["index"]+1
    prev=last["hash"]
    ts=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    raw=f"{idx}{prev}{ts}{random.random()}"
    nh="0000"+hashlib.sha256(raw.encode()).hexdigest()[:32]
    block={"index":idx,"hash":nh,"prev_hash":prev,"timestamp":ts,"data":f"Block mined by ryzkii_brc #{idx}","miner":"ryzkii_brc"}
    chain.append(block)
    save_chain(chain)
    update_wallet()
    print(f"✅ Block #{idx} mined {ts}")
    count+=1
    if count>=3:
        os.system('git add qdexx_chain.json qdexx_wallets.json && git commit -m "⛏️ block #'+str(idx)+'" && git push origin main')
        count=0
    time.sleep(8)
