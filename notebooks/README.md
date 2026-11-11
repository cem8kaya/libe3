# O-RAN dApp Interactive Analysis & Development Notebooks

This directory contains interactive Jupyter notebooks demonstrating end-to-end O-RAN dApp development, low-latency telemetry processing, and spectrum protection algorithms powered by **libe3** and **dApp-library**.

## Notebooks

### [`oran_dapp_development_and_analysis.ipynb`](oran_dapp_development_and_analysis.ipynb)
A complete, runnable workflow covering:
1. **Self-Healing Environment Setup**: Auto-detects `libe3py`, SWIG bindings, and Python dependencies.
2. **E3AP Configuration**: Configures ZeroMQ IPC sockets, radio parameters (51 PRBs, SCS = 30 kHz, carrier frequency = 3.6192 GHz).
3. **Serialization Benchmarks**: Latency and size comparisons between ASN.1 APER, Protobuf, and JSON.
4. **Real-time I/Q Spectrogram Analysis**: Waterfall plots and PRB energy distribution of incoming radio frames.
5. **Jammer Detection & Dynamic Blacklisting**:
   - Energy Detection
   - Moving Average Filter
   - Robust Median Absolute Deviation (MedMAD)
   - `SmartGuardBandPolicy` for adjacent channel leakage protection
6. **Automated Testing Suite**: 47 embedded unit and integration test assertions.

## How to Run

1. Activate your virtual environment:
   ```bash
   source ../.venv/bin/activate
   ```

2. Start the Jupyter server:
   ```bash
   jupyter notebook --ip=127.0.0.1 --port=8888 --no-browser --NotebookApp.token='oran'
   ```

3. Open `http://127.0.0.1:8888/?token=oran` in your browser and select the **Python 3 (.venv - O-RAN dApp)** kernel.

