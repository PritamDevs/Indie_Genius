# Week 02 — Step 3: Baseline Verification Report (Gate A)

**Repository:** `https://github.com/PritamDevs/Indie_Genius.git`  
**Branch:** `week-02-storyboard-experiments`  
**Baseline Commit Hash:** `af47a91`  
**Windows Version:** Microsoft Windows 11 Home Single Language (`10.0.26300` Build `26300`)  
**Python Version:** `Python 3.14.3` (`C:\Users\USER\Downloads\Indie_Genius\Indie_Genius\venv\Scripts\python.exe`)  
**Gate A Decision:** **GO — [VERIFIED WORKING]** (Existing Week 01 service starts, passes validation tests, responds to `/health`, generates a valid PNG on disk, and appends structured JSON metadata to `experiments/experiment_log.json`).

---

## 1. Exact Commands Executed

### Terminal 1 (Service Host)
```powershell
python -m uvicorn backend.api:app --host 127.0.0.1 --port 8000