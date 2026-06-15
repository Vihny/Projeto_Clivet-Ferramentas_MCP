from mcp.client.stdio import stdio_client
from mcp import ClientSession as session, StdioServerParameters as session_parameters
from dotenv import load_dotenv
from ia import conectar_gemini
import asyncio

MODEL = "openai/gpt-oss-120b:free"

SYSTEM_PROMPT = """
Você é um arquiteto de software que deve ajudar desenvolvedores a concretizar decisões arquiteturais.

Quando o usuário solicitar recomendações sobre o uso de um estilo arquitetural:
- Obtenha a lista de decisões arquiteturais disponíveis
- Considere somente as decisões escritas no formato ADR
- Identifique a ADR que determina o estilo arquitetural relevante
- Use ferramentas para buscar detalhes e validar a decisão
- Forneça, no maximo, 2 analises de riscos das decisao arquitetural.
- Compare as duas ADRs(utilizadas na analise de riscos anterior) e identifique se sao complementares, conflitantes ou independentes,.

Sempre utilize ferramentas quando necessário e seja capaz de encadear chamadas de tool para obter o resultado.
"""

async def get_response(ai_connection, mensagem):
    params = session_parameters(command="python", args=["adrs.py"])
    async with stdio_client(params) as (read, write):
        async with session(read, write) as s:
            await s.initialize()

            list_tools = await s.list_tools()
            arch_tools = [
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    }
                } for tool in list_tools.tools
            ]

            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": mensagem}
            ]

            while True:
                response = ai_connection.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    tools=arch_tools,
                    tool_choice="auto"
                )

                choice = response.choices[0]

                if choice.finish_reason == "stop":
                    print(f"resposta final: {choice.message.content}")
                    break

                if choice.finish_reason == "tool_calls":
                    messages.append(choice.message)

                    for tool in choice.message.tool_calls:
                        tool_response = await s.call_tool(
                            name=tool.function.name,
                            arguments=eval(tool.function.arguments)
                        )
                        print(f"tool '{tool.function.name}' executada")

                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool.id,
                            "name": tool.function.name,
                            "content": str(tool_response.content)
                        })

if __name__ == "__main__":
    load_dotenv()
    openai_key = None
    try:
        connection = conectar_gemini()
    except Exception as e:
        raise

    asyncio.run(get_response(connection, "Me forneça riscos de duas ADRs e compare-as para recomendar um estilo arquitetural para o framework Flutter"))