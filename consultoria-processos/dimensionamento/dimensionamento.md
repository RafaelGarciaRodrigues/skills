# dimensionamento dos recursos
- com base nos arquivos dentro de WORK_DIR\specs:
-- dimensione a equipe necessária para executar essa implementação
-- considere também os arquivos dentro de WORK_DIR\analise-spec, quanto mais issues descritas mais incerteza e mais tempo para tratá-las
-- leve em consideração as seguintes funções e suas descrições:

--- Data Scientist
---- CUSTO HORA: 185
---- Membro da equipe com expertise em ciência de dados, capaz de conduzir tarefas técnicas no modelo
---- Conhecimento profundo de python
---- Modelagem e códigos organizados
---- Comunicação clara e assertiva
---- Resiliência	e trabalho em equipe
---- Senso apurado de negócios
---- Fazer framing do problema a ser resolvido com features
---- Realizar modelagem matemática associada ao problema quando necessário
---- Executar tarefas técnicas envolvendo data science no código do produto
---- Propor soluções para desafios técnicos encontrados em suas tarefas e nas dos demais
---- Realizar interface com usuários e time do negócio
---- Garantir qualidade técnica da entrega das features
---- Cumprir tasks definidas no planejamento
---- Garantir resolução do problema de negócios

--- Data Engineer
---- CUSTO HORA: 185
---- Membro da equipe com expertise em engenharia de dados, capaz de suportar alimentação do modelo
---- Conhecimento profundo de ETL
---- Estruturação de pipelines de dados
---- Otimização de código para performance
---- Resiliência	e trabalho em equipe
---- Comunicação clara e assertiva
---- Realizar extrações de dados necessárias para viabilizar outras tarefas
---- Otimizar pipelines de dados que alimentam o modelo
---- Executar tarefas técnicas envolvendo engenharia de dados 
---- Documentar toda a estrutura de dados desenvolvida
---- Propor soluções para desafios técnicos encontrados em suas tarefas e nas dos demais
---- Garantir qualidade técnica da entrega das tarefas dentro do prazo

--- Product Manager
---- CUSTO HORA: 250
---- Gestor responsável pelo impacto do produto nos negócios, e representação do produto na interlocução com stakeholders 
---- Gestão de produto, técnicas de discovery
---- Priorização, geração de valor e gestão de risco
---- Comunicação e relacionamento
---- Desenvolvimento de pessoas
---- Profundo entendimento do negócio
---- Conhecimento de boas práticas de tecnologia
---- Garantir impacto nos OKRs de negócio ligados ao produto
---- Realizar discovery, garantindo um alto nível do upstream
---- Priorizar features por impacto, tomar decisões táticas
---- Definir e acompanhar KPIs de sucesso para o squad
---- Validar critérios de aceitação (DOR, DOD)
---- Representar o produto nas interfaces internas e externas
---- Escalar roadblocks significativos para BO/TO
---- Capacitar equipe para executar rotinas
---- Manter índices de aceitação do usuário
---- Construir com DM avaliações do squad (negócio e tech)
---- Garantir bom clima, integração e funcionamento do squad

--- Digital Manager
---- CUSTO HORA: 250
---- Gestor responsável pela qualidade técnica do produto, e alocação de recursos de tecnologia em tarefas
---- Gestão de Produto
---- Conhecimento em múltiplas disciplinas tech (com ênfase variando por produto)
---- Compreensão do produto fim-a-fim
---- Comunicação e relacionamento
---- Desenvolvimento de pessoas
---- Avaliar esforço no desenvolvimento de features 
---- Definir e acompanhar KPIs técnicos do produto
---- Elaborar critérios de aceitação (DOR, DOD)
---- Alocar pessoas em tarefas e coordenar interdependências
---- Representar o produto nas interface com demais áreas de tecnologia (discussões cross-chapters)
---- Fornecer insights do produto e pessoas para chapters/hubs
---- Escalar roadblocks significativos para BO/TO
---- Garantir qualidade da entrega técnica do squad
---- Executar orçamento do produto e garantir ROI
---- valiar membros de tech do squad, fornecer inputs para avaliação de membros de negócio do squad

--- Full Stack
---- CUSTO HORA: 185
---- Membro da equipe com expertise em desenvolvimento, capaz de garantir usabilidade do produto
---- Desenvolvimento front-end e back-end
---- Conhecimento em cloud computing
---- Conhecimento de UI
---- Boa interlocução com demais áreas tech
---- Desenhar, desenvolver e testar implementações de código no produto
---- Criar, ajustar e manter uma boa interface para usuários do produto
---- Auxiliar na otimização de código de tarefas de outras disciplinas
---- Propor soluções para desafios técnicos encontrados em suas tarefas e nas dos demais
---- Garantir qualidade técnica da entrega das tarefas dentro do prazo


--- Tech Owner
---- CUSTO HORA: 330
---- Gestor responsável pela entrega técnica
---- Atuação parcial em todos os projetos
---- Estima-se 10% de dedicação


- Todos os perfis com disponibilidade de trabalho de 185 horas por mês
- Considere que 40% do tempo as equipes estarão em reuniões, logo irão produzir somente em 60% do tempo disponível
- Horas produtivas por pessoa por mês = 185 × 0,6 = 111h

## Modelo de custo

O custo é calculado sobre o tempo CONTRATADO das pessoas, não sobre as horas de entrega.
Fórmula obrigatória:

  Horas = Quantidade × 185 × meses_do_cenário
  Custo Total = Horas × Custo/hora da função

Para o Tech Owner (10% de dedicação):
  Horas = 1 × 185 × 0,10 × meses_do_cenário
  (use esse cálculo como validação da fórmula antes de aplicar às demais funções)

## Regra de compressão de prazo

Comprimir o prazo exige paralelizar atividades que seriam sequenciais, aumentando a equipe e o overhead de coordenação. Isso eleva o custo total:

- 12 meses → cenário base: equipe mínima, trabalho majoritariamente sequencial
- 8 meses → compressão moderada: aumente Quantidade dos perfis técnicos em ~30% em relação ao cenário de 12 meses; adicione 15% de overhead nas horas de gestão pelo aumento de coordenação
- 4 meses → compressão agressiva: aumente Quantidade dos perfis técnicos em ~70% em relação ao cenário de 12 meses; adicione 40% de overhead nas horas de gestão pela alta coordenação e retrabalho esperado

## Regra de ordenação OBRIGATÓRIA

CUSTO TOTAL 4 meses > CUSTO TOTAL 8 meses > CUSTO TOTAL 12 meses

Se após calcular os valores essa regra não for respeitada para qualquer função, REVISE as quantidades e horas até que ela seja satisfeita antes de gerar o JSON.

## Calibração de ocupação

Em projetos de alta complexidade técnica (solver de otimização, múltiplos FRs com interdependências, decisões de arquitetura em aberto), os perfis técnicos devem operar próximos a 80-100% da capacidade produtiva no cenário de 12 meses. Se a estimativa de ocupação de qualquer perfil técnico ficar abaixo de 70% no cenário de 12 meses, justifique explicitamente na "Premissas" por que esse perfil terá baixa ocupação.

- retorne um json com os seguintes campos:

"Função": Nome da função necessária
"Atividades": Breve descrição das atividades que esta função executará no contexto da especificação
"Horas": Valor numérico inteiro = Quantidade × 185 × meses (ou × 0,10 × 185 × meses para Tech Owner)
"Quantidade": Quantidade de profissionais alocados neste cenário (respeitando a regra de compressão)
"Custo Total": Valor numérico inteiro = Horas × Custo/hora da função
"Premissas": Condições para que seja possível executar as atividades dessa função no período desse cenário; inclua justificativa se ocupação < 70%
"Analise": Um texto com dois parágrafos que inicia explicando a diferença entre os cenários e o segundo parágrafo analisa qual o maior fator que aumenta os custos, faça uma análise do quanto as incertezas e inconsistêcias identificadas no WORK_DIR\analise-spec afetam os custos.

- Estrutura do json

{
  "Funcoes": [
    {
      "Função": "",
      "Atividades": "",
      "Cenarios": [
        {
          "Periodo": "4 Meses",
          "Horas": 0,
          "Quantidade": 0,
		  "Custo Total": 0,
		  "Premissas": ""
        },
        {
          "Periodo": "8 Meses",
          "Horas": 0,
          "Quantidade": 0,
		  "Custo Total": 0,
		  "Premissas": ""
        },
        {
          "Periodo": "12 Meses",
          "Horas": 0,
          "Quantidade": 0,
		  "Custo Total": 0,
		  "Premissas": ""
        }
      ]
    }
  ],
  "Analise":""
}


grave a saída em um arquivo temporário e em seguida execute:

```powershell
python "<SKILL_DIR>\scripts\salvar-dimensionamento.py" "<WORK_DIR>" "<ARQUIVO_TEMP>"
```