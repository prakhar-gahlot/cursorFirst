## Chat Demo (FastAPI + Frontend)

### Quick Deployment (No Docker)

## Option 1: Railway (2 minutes) 🚀
1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/chat-demo.git
   git push -u origin main
   ```

2. **Deploy**:
   - Go to [railway.app](https://railway.app) → Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repo
   - Add environment variable: `OPENAI_API_KEY=sk-yourkeyhere`
   - Railway auto-deploys! ✨

3. **Frontend**: Upload `frontend/index.html` to any static host (Netlify/Vercel/GitHub Pages)

## Option 2: Render.com (3 minutes)
1. **Push to GitHub** (same as above)
2. **Deploy**:
   - Go to [render.com](https://render.com) → Connect GitHub
   - Create "Web Service" from your repo
   - Runtime: Python 3
   - Build: `pip install -r backend/requirements.txt`
   - Start: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - Add env var: `OPENAI_API_KEY=sk-yourkeyhere`

## Option 3: Fly.io (4 minutes)
```bash
# Install flyctl, then:
fly launch
fly secrets set OPENAI_API_KEY=sk-yourkeyhere
fly deploy
```

---

### Local Development

#### Backend (FastAPI)
1. Create and activate a virtual environment (PowerShell):
   ```powershell
   cd D:\cursorFirst
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
2. Install dependencies:
   ```powershell
   pip install -r backend\requirements.txt
   ```
3. Set environment variable (replace with your key):
   ```powershell
   $env:OPENAI_API_KEY = "sk-..."
   ```
4. Run the API:
   ```powershell
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Frontend
Serve the static file:
```powershell
cd D:\cursorFirst\frontend
python -m http.server 5500
```
Open `http://localhost:5500/index.html` in your browser.

### Test API directly
```powershell
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message":"Hello"}'
```


