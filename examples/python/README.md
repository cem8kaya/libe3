# Python dApp Examples for libe3

This directory contains standalone Python examples showcasing how to use `libe3py` and `dApp-library` to implement O-RAN Near-RT RIC dApps.

## Files

- **`mock_du_e3_agent.py`**: Emulates an O-DU radio telemetry publisher streaming I/Q power frames over ZeroMQ IPC (`/tmp/e3_sockets/e3_indication.ipc`), periodically injecting synthetic narrow-band interference (jamming).
- **`my_first_dapp.py`**: Implements a real-time spectrum guardian dApp consuming indications, analyzing PRB power levels with SNR thresholding, and dispatching `E3_DAPP_CONTROL` (PRB blacklist) PDUs to the DU.
- **`e3_config.json`**: Standard JSON configuration for endpoints, transport, and radio parameters.
- **`verify_dapp.py`**: Regression verification script running automated health checks.
- **`test_python_sim.sh`**: Launch script running the DU simulator and dApp in parallel with automated validation.

## Running the Python Simulation

In terminal 1:
```bash
python3 mock_du_e3_agent.py
```

In terminal 2:
```bash
python3 my_first_dapp.py
```

Or execute both with the automated runner:
```bash
bash test_python_sim.sh
```

