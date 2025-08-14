Crypto Wallet (Testnet)
============================

A simple Ethereum testnet wallet built with HTML + JavaScript that connects to MetaMask.
Send ETH on a testnet (e.g., Sepolia) directly from your browser — no servers or domains required.

------------------------------------------------------------
Project Structure
------------------------------------------------------------
frontend/
   index.html    -> Main wallet UI — open in browser
backend/
   app.py        -> Optional Flask server to log transactions locally

------------------------------------------------------------
Getting Started
------------------------------------------------------------

1. Prerequisites
   - MetaMask browser extension installed
   - Node.js or Python (for running a simple static server)
   - Testnet ETH (get from a faucet — e.g., Sepolia faucet)

2. Run the Frontend
   You can open frontend/index.html directly, but most browsers work better if you serve it via a local HTTP server.

   Option A — Using Python:
       cd frontend
       python -m http.server 8000
       Visit: http://localhost:8000

   Option B — Using Node.js:
       npm install -g serve
       cd frontend
       serve
       Visit the URL shown in the terminal.

3. Connect MetaMask
   - Open your browser and load the page.
   - In MetaMask, switch to Sepolia (or another testnet).
   - Get free test ETH from a faucet (search for "Sepolia faucet").

4. Send Test ETH
   - Click "Connect Wallet" in the UI.
   - Enter a recipient address and amount.
   - Click "Send" — approve in MetaMask.

------------------------------------------------------------
Optional: Run the Backend (Flask Logger)
------------------------------------------------------------
The backend is NOT required for sending ETH. It only logs transactions locally for testing.

   cd backend
   pip install flask flask-cors
   python app.py

------------------------------------------------------------
Notes
------------------------------------------------------------
- This is TESTNET ONLY — do not use with real ETH.
- Works best in Chrome/Brave with MetaMask installed.
- If you get connection errors, make sure MetaMask is unlocked and on the correct network.

