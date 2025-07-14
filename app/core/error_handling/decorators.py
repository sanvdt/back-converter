from functools import wraps
from .exceptions import ProcessingError
import traceback
import subprocess
import os
import rq

def handle_job_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except subprocess.CalledProcessError as e:
            msg = str(e)
            if "Could not open the file" in msg or "Unable to open the initial device" in msg:
                raise ProcessingError("Erro ao comprimir o PDF: o nome do arquivo pode estar muito longo ou inválido.")
            raise ProcessingError(f"Erro ao executar subprocesso: {e}")

        except FileNotFoundError as e:
            raise ProcessingError(f"Arquivo não encontrado: {e}")

        except OSError as e:
            raise ProcessingError(f"Erro de sistema: {e}")

        except Exception as e:
            tb = traceback.format_exc()
            raise ProcessingError(f"Erro inesperado: {str(e)}\n{tb}")

    return wrapper
