# INSTALL
```bash
git clone https://github.com/your-username/mini-soar.git
cd mini-soar
pip install -r requirements.txt && python train_model.py && streamlit run app.py

#Run with Docker
docker compose up --build
http://localhost:8501/