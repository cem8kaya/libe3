import os
import time
import json
import zmq
import numpy as np

SOCKET_DIR = "/tmp/e3_sockets"
os.makedirs(SOCKET_DIR, exist_ok=True)

def run_e3_agent():
    ctx = zmq.Context()
    
    pub_sock = ctx.socket(zmq.PUB)
    pub_sock.bind(f"ipc://{SOCKET_DIR}/e3_indication.ipc")
    
    pull_sock = ctx.socket(zmq.PULL)
    pull_sock.bind(f"ipc://{SOCKET_DIR}/e3_control.ipc")
    
    poller = zmq.Poller()
    poller.register(pull_sock, zmq.POLLIN)

    num_prbs = 51
    subcarriers = num_prbs * 12
    blocked_prbs = []
    tti_counter = 0

    print("[E3 Agent] DU Simülatörü başlatıldı. I/Q ve KPM akışı (1ms TTI) başlıyor...")

    try:
        while True:
            t_start = time.perf_counter()
            tti_counter += 1

            iq_real = np.random.normal(0, 0.1, subcarriers).astype(np.float32)
            iq_imag = np.random.normal(0, 0.1, subcarriers).astype(np.float32)

            # Her 500 TTI'da bir 18-24. PRB'ler arasına Jammer/Parazit enjekte et
            jammer_active = (tti_counter % 1000) > 500
            if jammer_active:
                jam_start, jam_end = 18 * 12, 24 * 12
                iq_real[jam_start:jam_end] += np.random.normal(0, 1.5, jam_end - jam_start)
                iq_imag[jam_start:jam_end] += np.random.normal(0, 1.5, jam_end - jam_start)

            payload = {
                "msgType": "E3_RAN_INDICATION",
                "tti": tti_counter,
                "timestampNs": time.time_ns(),
                "numPrbs": num_prbs,
                "activeBlockedPrbs": blocked_prbs,
                "iqSamplesReal": iq_real.tolist(),
                "iqSamplesImag": iq_imag.tolist()
            }
            pub_sock.send_string(json.dumps(payload))

            socks = dict(poller.poll(timeout=0))
            if pull_sock in socks:
                ctrl_msg = json.loads(pull_sock.recv_string())
                if ctrl_msg.get("msgType") == "E3_DAPP_CONTROL":
                    blocked_prbs = ctrl_msg.get("blacklistPrbs", [])
                    latency_us = (time.time_ns() - ctrl_msg["indicationTsNs"]) / 1000.0
                    print(f"[DU MAC Scheduler] dApp Kontrolü Uygulandı! "
                          f"Yasaklanan PRB'ler: {blocked_prbs} | Döngü Gecikmesi: {latency_us:.1f} us")

            elapsed = time.perf_counter() - t_start
            if elapsed < 0.001:
                time.sleep(0.001 - elapsed)

    except KeyboardInterrupt:
        print("\n[E3 Agent] Kapatılıyor...")

if __name__ == "__main__":
    run_e3_agent()

