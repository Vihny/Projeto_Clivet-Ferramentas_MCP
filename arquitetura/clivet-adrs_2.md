# Architecture Decision Records — CliVet

---

## ADR-01: Utilização da Arquitetura MVC

**Contexto:**
O sistema possui múltiplos módulos administrativos e necessita de organização estrutural para facilitar manutenção e evolução futura.

**Decisão:**
Adotar o padrão arquitetural MVC (Model-View-Controller).

**Status:** Aceito

**Consequências:**
- Separação clara entre interface, regras de negócio e persistência
- Facilidade de manutenção e escalabilidade
- Maior complexidade estrutural inicial

---

## ADR-02: Utilização de Banco de Dados Relacional

**Contexto:**
O sistema manipula dados estruturados relacionados a clientes, produtos, estoque, medicamentos e vendas.

**Decisão:**
Utilizar banco de dados relacional MySQL para persistência das informações.

**Status:** Aceito

**Consequências:**
- Maior integridade e consistência dos dados
- Facilidade para consultas relacionais
- Necessidade de modelagem mais rigorosa

---

## ADR-03: Desenvolvimento de Interface WEB

**Contexto:**
O requisito NF002 determina a utilização de componentes WEB e facilidade de uso.

**Decisão:**
Desenvolver o sistema como aplicação WEB responsiva.

**Status:** Aceito

**Consequências:**
- Facilidade de acesso em diferentes dispositivos
- Não necessita instalação local
- Dependência de um servidor acessível na rede local ou via internet

---

## ADR-04: Implementação de Controle de Estoque com Validade

**Contexto:**
O sistema necessita controlar validade de produtos e medicamentos presentes no estoque.

**Decisão:**
Implementar módulo de estoque integrado aos módulos de produtos e medicamentos.

**Status:** Aceito

**Consequências:**
- Melhor controle operacional
- Redução de perdas por vencimento
- Maior complexidade na lógica de atualização de estoque

---

## ADR-05: Implementação de Mecanismos de Pesquisa

**Contexto:**
Diversos requisitos funcionais exigem pesquisa rápida de informações cadastradas.

**Decisão:**
Implementar mecanismos de busca em clientes, produtos, medicamentos, estoque e vendas.

**Status:** Aceito

**Consequências:**
- Maior agilidade operacional
- Melhor experiência do usuário
- Necessidade de otimização de consultas no banco de dados

---

## ADR-06: Centralização das Regras de Negócio

**Contexto:**
O sistema possui diversas validações relacionadas a cadastro, edição e exclusão de informações.

**Decisão:**
Centralizar regras de negócio na camada de serviços da aplicação.

**Status:** Aceito

**Consequências:**
- Redução de duplicidade de código
- Maior organização do sistema
- Maior complexidade arquitetural, exigindo maior esforço de abstração e desenvolvimento inicial

---

## ADR-07: Priorização de Desempenho nas Operações

**Contexto:**
O requisito NF005 exige agilidade nas operações do sistema.

**Decisão:**
Otimizar consultas ao banco de dados e utilização de paginação nas listagens.

**Status:** Aceito

**Consequências:**
- Melhor desempenho do sistema
- Redução de consumo de recursos
- Maior complexidade de implementação
