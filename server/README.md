1. pip install -r requirements.txt
2. uvicorn app.main:app --reload
3. deploy
   - uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
