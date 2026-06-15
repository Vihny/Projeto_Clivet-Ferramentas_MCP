from mcp.server.fastmcp import FastMCP
from utilidades import carregar_adrs
from ia import conectar_gemini, ia_riscos_para_adr, ia_comparar_adrs
import os
import logging

from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

ARQUIVO_ADRs = os.path.join("arquitetura", "clivet-adrs_2.md")

NOME = "Clivet.IA"
mcp = FastMCP(NOME)
logger = logging.getLogger(NOME)

INFO = {
    "Descrição": "Servidor MCP para processamento e análise de ADRs (CLIVET)",
    "versão": "1.0"
}

global adrs
adrs = None
global adrs_carregadas
adrs_carregadas = False

global ai_connection
ai_connection = None

load_dotenv()

def conectar_ia():
    global ai_connection

    if ai_connection is None:
        ai_connection = conectar_gemini()

    return ai_connection

def iniciar_adrs():
    global adrs, adrs_carregadas

    if not adrs or len(adrs) == 0:
        adrs_carregadas, adrs = carregar_adrs(ARQUIVO_ADRs)

        if adrs_carregadas:
            logger.info(f"ADRs carregados com sucesso: {len(adrs)} ADRs encontrados.")
        else:
            logger.error("Falha ao carregar ADRs.")

    return adrs_carregadas, adrs


@mcp.tool(name="decisoes_arquiteturais", title="lista de decisoes arquiteturais", description="retorna a lista completa de decisoes arquiteturais")
def get_adrs():
    decisoes = []

    carregadas, adrs = iniciar_adrs()
    if carregadas:
        for adr in adrs.values():
            decisoes.append({
                "id": adr["id"],
                "titulo": adr["titulo"]
            })

    return decisoes


@mcp.tool(name="decisao_arquitetural", title="lista detalhes de uma decisao arquitetural", description="retorna a lista de detalhes sobre uma decisao arquitetural")
def get_detalhes_adr(id_adr):
    detalhes = {}

    carregadas, adrs = iniciar_adrs()
    if carregadas:
        detalhes = adrs[id_adr]

    return detalhes


@mcp.tool(name="riscos_adr", title="analisa riscos de uma decisao arquitetural", description="dado o identificador de uma decisao arquitetural, usa IA para identificar riscos tecnicos e de negocio, e sugerir estrategias de mitigacao")
def get_riscos_adr(id_adr):
    riscos = {}

    carregadas, adrs = iniciar_adrs()
    if carregadas:
        riscos = ia_riscos_para_adr(conectar_ia(), adrs[id_adr.strip()])

    return riscos


@mcp.tool(name="comparar_adrs", title="compara duas decisoes arquiteturais", description="dados os identificadores de duas decisoes arquiteturais, usa IA para analisar se sao complementares, conflitantes ou independentes, e identificar possiveis inconsistencias entre elas")
def get_comparar_adrs(id_adr_a, id_adr_b):
    comparacao = {}

    carregadas, adrs = iniciar_adrs()
    if carregadas:
        comparacao = ia_comparar_adrs(conectar_ia(), adrs[id_adr_a.strip()], adrs[id_adr_b.strip()])

    return comparacao


if __name__ == "__main__":
    try:
        iniciar_adrs()
        mcp.run()
    except Exception as e:
        raise
