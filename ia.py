import os
from openai import OpenAI
import json
import re

MODEL = "openai/gpt-oss-120b:free"

def conectar_gemini():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise Exception("OPENROUTER_API_KEY não encontrada no .env")
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )
    return client


def gerar_resposta_gemini(conn, prompt: str, model: str = MODEL):
    response = conn.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def ia_riscos_para_adr(conn, adr):
    """Analisa riscos técnicos e de negócio de uma ADR via Gemini.

    Retorna um dicionário com os campos: decisao, riscos_tecnicos,
    riscos_negocio e mitigacoes.
    """
    prompt = f"""
Você é um arquiteto de software sênior. Analise a ADR abaixo e identifique:
1. Riscos técnicos decorrentes desta decisão
2. Riscos de negócio associados
3. Estratégias de mitigação para cada risco

Instruções:
- A decisão foi escrita no formato de um Architecture Decision Record (ADR).
- Organize a resposta em um JSON com os campos: (i) "decisao" com a descrição
  original da ADR, (ii) "riscos_tecnicos" com lista de riscos técnicos,
  (iii) "riscos_negocio" com lista de riscos de negócio,
  (iv) "mitigacoes" com lista de estratégias de mitigação.

Restrições:
- Retorne apenas o JSON. Não inclua explicações, comentários ou texto adicional.
- Cada item das listas deve ser conciso e claro.

ADR:
{adr}
"""
    resposta = gerar_resposta_gemini(conn, prompt)
    resposta = re.search(r'\{.*\}', resposta, re.DOTALL)
    if resposta:
        resposta = resposta.group(0)
    return json.loads(resposta)


def ia_comparar_adrs(conn, adr_a, adr_b):
    """Compara duas ADRs e analisa sua relação via Gemini.

    Retorna um dicionário com os campos: relacao, impacto_a_em_b,
    impacto_b_em_a e inconsistencias.
    """
    prompt = f"""
Você é um arquiteto de software sênior. Analise as duas ADRs abaixo e responda:
1. As decisões são complementares, conflitantes ou independentes?
2. Qual o impacto da ADR-A sobre a ADR-B e vice-versa?
3. Existe alguma inconsistência entre elas?

Instruções:
- Ambas foram escritas no formato de um Architecture Decision Record (ADR).
- Organize a resposta em um JSON com os campos: (i) "relacao" indicando se são
  complementares, conflitantes ou independentes, (ii) "impacto_a_em_b" descrevendo
  o impacto da ADR-A sobre a ADR-B, (iii) "impacto_b_em_a" descrevendo o impacto
  da ADR-B sobre a ADR-A, (iv) "inconsistencias" listando inconsistências encontradas.

Restrições:
- Retorne apenas o JSON. Não inclua explicações, comentários ou texto adicional.

ADR-A:
{adr_a}

ADR-B:
{adr_b}
"""
    resposta = gerar_resposta_gemini(conn, prompt)
    resposta = re.search(r'\{.*\}', resposta, re.DOTALL)
    if resposta:
        resposta = resposta.group(0)
    return json.loads(resposta)
