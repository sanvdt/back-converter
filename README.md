No Windows:

python -m venv venv
venv\Scripts\activate


No Linux/macOS:

python3 -m venv venv
source venv/bin/activate

salvar as libs instaladas:
pip freeze > requirements.txt


Execute sua API com:
uvicorn app.main:app --reload

Acesse a documentação automática em:
http://127.0.0.1:8000/docs

