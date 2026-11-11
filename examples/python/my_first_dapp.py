import json
import zmq
import numpy as np

SOCKET_DIR = "/tmp/e3_sockets"
SNR_THRESHOLD_DB = 8.0

def run_dapp():
    ctx = zmq.Context()

    sub_sock = ctx.socket(zmq.SUB)
    sub_sock.connect(f"ipc://{SOCKET_DIR}/e3_indication.ipc")
    sub_sock.setsockopt_string(zmq.SUBSCRIBE, "")

    push_sock = ctx.socket(zmq.PUSH)
    push_sock.connect(f"ipc://{SOCKET_DIR}/e3_control.ipc")

    print("[dApp] E3 Manager bağlandı. I/Q akışı bekleniyor...")
    last_blocked = []

    try:
        while True:
            raw_msg = sub_sock.recv_string()
            msg = json.loads(raw_msg)

            num_prbs = msg["numPrbs"]
            iq_real = np.array(msg["iqSamplesReal"], dtype=np.float32)
            iq_imag = np.array(msg["iqSamplesImag"], dtype=np.float32)

            # PRB başına güç spektral yoğunluğunu (PSD) hesapla
            power = (iq_real ** 2 + iq_imag ** 2).reshape(num_prbs, 12).mean(axis=1)
            median_noise = np.median(power)
            snr_db = 10 * np.log10(power / (median_noise + 1e-12))

            compromised_prbs = np.where(snr_db > SNR_THRESHOLD_DB)[0].tolist()

            if compromised_prbs != last_blocked:
                ctrl_payload = {
                    "msgType": "E3_DAPP_CONTROL",
                    "action": "PRB_BLACKLIST",
                    "blacklistPrbs": compromised_prbs,
                    "indicationTsNs": msg["timestampNs"]
                }
                push_sock.send_string(json.dumps(ctrl_payload))
                last_blocked = compromised_prbs

                if compromised_prbs:
                    print(f"[dApp -> E2 Bridge] ANOMALİ! TTI: {msg['tti']} | "
                          f"Parazitli PRB'ler: {compromised_prbs} | Max SNR: {snr_db.max():.1f} dB")
                else:
                    print(f"[dApp -> E2 Bridge] Spektrum temizlendi. TTI: {msg['tti']} | Tüm PRB'ler serbest.")

    except KeyboardInterrupt:
        print("\n[dApp] Durduruldu.")

if __name__ == "__main__":
    run_dapp()

