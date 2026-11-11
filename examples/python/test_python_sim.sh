#!/usr/bin/env bash
set -e

WS_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$WS_ROOT"

echo "=== TEST 2: Python I/Q Spectrum Protection & PRB Barring Simulation ==="
rm -rf /tmp/e3_sockets
mkdir -p /tmp/e3_sockets

source .venv/bin/activate

# Start mock_du_e3_agent.py in background (unbuffered output)
python3 -u mock_du_e3_agent.py > agent.log 2>&1 &
AGENT_PID=$!
echo "Started mock_du_e3_agent.py (PID $AGENT_PID)"

# Wait for socket initialization
sleep 0.5

# Start my_first_dapp.py in background (unbuffered output)
python3 -u my_first_dapp.py > dapp.log 2>&1 &
DAPP_PID=$!
echo "Started my_first_dapp.py (PID $DAPP_PID)"

# Let them run for 3 seconds to observe several jammer cycles
sleep 3

echo "Stopping test processes..."
kill -9 $DAPP_PID $AGENT_PID 2>/dev/null || true
wait $DAPP_PID 2>/dev/null || true
wait $AGENT_PID 2>/dev/null || true

echo ""
echo "--- [dApp Output (dapp.log)] ---"
head -n 15 dapp.log

echo ""
echo "--- [DU Agent Output (agent.log)] ---"
head -n 15 agent.log

echo "=== TEST 2 COMPLETE ==="
