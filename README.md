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



⚙️ Tecnologias Utilizadas
🔧 Backend (FastAPI + RQ)
FastAPI: framework web rápido e moderno em Python

Redis: banco de dados em memória, usado como fila de tarefas

RQ (Redis Queue): fila de tarefas para execução assíncrona

LibreOffice: usado para converter .docx para .pdf

Pillow (PIL): usado para converter imagens .jpg / .png para .pdf

Ghostscript: utilizado para comprimir arquivos PDF gerados

Uvicorn: servidor ASGI para rodar o FastAPI



📂 Estrutura das Rotas da API

📝 Conversão de Word para PDF
POST /convert/word → Envia .docx para conversão
GET /convert/status/{job_id} → Verifica status e retorna o PDF pronto

🖼️ Conversão de Imagem para PDF
POST /convert/image → Envia .jpg ou .png para conversão
GET /convert/image/status/{job_id} → Verifica status e retorna o PDF pronto

🗜️ Compressão de PDF
POST /compress/pdf → Envia PDF para compressão
GET /compress/pdf/status/{job_id} → Verifica status e retorna o PDF comprimido



🚀 Como funciona
O usuário envia um arquivo via frontend

O backend armazena o arquivo localmente e cria um job assíncrono

O job é processado em segundo plano (usando RQ + Redis)

O frontend consulta o status e, quando estiver pronto, baixa o PDF convertido

