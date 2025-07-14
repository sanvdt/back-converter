class ProcessingError(Exception):
    """Erro genérico durante o processamento do PDF."""
    pass

class InvalidFilenameError(Exception):
    """Erro relacionado a nomes de arquivos inválidos ou longos demais."""
    pass
