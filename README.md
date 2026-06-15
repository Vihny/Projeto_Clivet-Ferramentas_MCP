# Clivet-ach.IA

Projeto de exemplo para a disciplina de Arquitetura de Software que contém agentes/IA e um cliente para desenvolvimento local.

## Estrutura principal
- `adrs.py` — ponto principal do agente/desenvolvimento (rodado com `mcp dev`).
- `cliente_mcp.py` — cliente que interage com o agente.
- `ia.py`, `utilidades.py` — módulos auxiliares.

## Pré-requisitos
- Python 3.8 ou superior
- Ter o comando `mcp` disponível no PATH (ambiente de desenvolvimento do MCP/agent)

## Instalação (Windows - PowerShell)
Abra um terminal na raiz do projeto e execute:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

Se preferir CMD (prompt):

```cmd
python -m venv venv
.\venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Executando o projeto

- Para rodar o agente em modo de desenvolvimento (requere o runtime/CLI `mcp`):

```powershell
mcp dev adrs.py
```

Execute esse comando a partir da raiz do repositório. Se ocorrer o erro "`mcp` não é reconhecido", verifique se o MCP está instalado e no PATH.

- Para executar o cliente localmente:

```powershell
python cliente_mcp.py
```

## Dicas de resolução de problemas
- Se `mcp dev adrs.py` falhar, verifique a saída do terminal para mensagens de erro e confirme as dependências em `requirements.txt`.
- Confirme que você ativou o `venv` antes de instalar dependências e executar scripts.