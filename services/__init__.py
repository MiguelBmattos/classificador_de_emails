from .file_service import ler_arquivo
from .openai_service import gerar_classificacao_e_resposta
from .historico_service import (
    carregar_historico,
    ordenar_historico,
    obter_ultima_classificacao,
    adicionar_email  
)