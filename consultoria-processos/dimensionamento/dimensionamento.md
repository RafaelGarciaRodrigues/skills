# Dimensionamento de Recursos

Com base nos arquivos dentro de `WORK_DIR\specs` e `WORK_DIR\analise-spec`:

---

## Passo 1 — Identifique o escopo completo antes de dimensionar

Leia a spec e identifique **tudo o que precisa ser entregue** — inclua as User Stories P1, P2 e P3 se estiverem descritas. O dimensionamento cobre o **mesmo escopo nos três cenários** — o que muda entre eles é o prazo e a composição da equipe, não o que é entregue.

> **Regra crítica:** não reduza o escopo para tornar os números mais baratos. Se a spec inclui ETL automático, ele entra no escopo dos três cenários. Simplificações de escopo são papel da Convergência, não do Dimensionamento.

---

## Passo 2 — Estime o cenário base (12 meses) de baixo para cima

Construa o cenário de 12 meses a partir do **esforço mínimo necessário** para entregar o escopo completo com qualidade, com o time trabalhando de forma sequencial e organizada:

- Para cada entregável, pergunte: quantas pessoas, com qual perfil, por quantas semanas?
- Some os esforços e converta para cabeças dedicadas no período de 12 meses
- Valide: para projetos de software de médio porte, **3 a 6 profissionais técnicos** em 12 meses são a referência razoável. Justifique cada pessoa adicional com um entregável específico

---

## Perfis disponíveis

### Data Scientist
- **CUSTO/HORA:** R$ 185
- Framing do problema, modelagem matemática, implementação em Python, validação com usuário, geração de outputs

### Data Engineer
- **CUSTO/HORA:** R$ 185
- Pipelines ETL, extração de dados, infraestrutura de dados, deploy

### Product Manager
- **CUSTO/HORA:** R$ 250
- Discovery, priorização, KPIs, alinhamento com stakeholders, critérios de aceite

### Digital Manager
- **CUSTO/HORA:** R$ 250
- Arquitetura técnica, qualidade de entrega, coordenação de interdependências, decisões de stack

### Full Stack
- **CUSTO/HORA:** R$ 185
- Front-end, back-end, interface do produto

### Tech Owner
- **CUSTO/HORA:** R$ 330
- Supervisão técnica com **10% de dedicação** (não inclua na contagem de equipe central)

---

## Modelo de custo

O custo é calculado sobre o tempo **contratado**, não sobre horas entregues.

```
Horas       = Quantidade × 185 × meses_do_cenário
Custo_base  = Horas × Custo/hora da função
Custo_final = Custo_base × Fator_overhead_cenário
```

Para o Tech Owner (10% de dedicação):
```
Horas = 1 × 185 × 0,10 × meses_do_cenário
```

Todos os perfis têm disponibilidade de **185 horas/mês**. Considere que **40% do tempo é gasto em reuniões**, logo a capacidade produtiva é de **111h/mês por pessoa**.

---

## Fator de overhead por compressão de prazo

Comprimir o prazo exige trabalho paralelo, mais reuniões de sincronização, overhead de integração entre squads, e aceitar mais risco técnico. Esses custos não aparecem na conta simples de pessoa × hora — por isso existe o **fator de overhead**:

| Cenário | Equipe técnica | Fator de overhead | O que o overhead representa |
|---------|---------------|-------------------|-----------------------------|
| 12 meses | Mínima para o escopo (sequencial) | **1,0** (sem overhead) | Trabalho planejado, sequencial, sem pressa |
| 8 meses | +40% a +60% vs. 12m | **1,5** (+50%) | Parallelism moderado, coordenação extra, integração entre módulos |
| 4 meses | +80% a +120% vs. 12m | **2,5** (+150%) | Alta paralelização, horas extras, risco de retrabalho, integração complexa |

> **Como aplicar:** calcule o `Custo_base` de cada cenário (soma dos perfis × horas × taxa), depois multiplique pelo `Fator_overhead` para obter o `Custo_final`. O campo `Custo Total` no JSON deve conter o **Custo_final** (já com overhead).

> **Regra de ordenação resultante:** CUSTO_FINAL (4 meses) > CUSTO_FINAL (8 meses) > CUSTO_FINAL (12 meses). Esta regra deve ser satisfeita. Se não estiver, revise a composição de equipe ou o fator de overhead.

> **Regra de sanidade:** o time técnico total (DS + DE + Full Stack) em qualquer cenário não deve exceder 10 pessoas. Um número maior indica que o escopo foi mal estimado no Passo 1.

---

## Calibração de ocupação

Em projetos de alta complexidade técnica, os perfis técnicos devem operar próximos a **80-100% da capacidade produtiva** no cenário de 12 meses. Se a estimativa de qualquer perfil ficar abaixo de 70%, justifique explicitamente nas "Premissas" daquele perfil.

---

## Formato de saída

Retorne **apenas** o JSON abaixo, sem texto fora dele:

```json
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
  "Analise": ""
}
```

> **Importante:** o campo `Custo Total` de cada cenário deve incluir o fator de overhead. Informe nas Premissas o custo base (antes do overhead) e o overhead aplicado, para que o leitor entenda a composição.

**Campo `Analise`:** dois parágrafos. O primeiro explica que todos os cenários cobrem o mesmo escopo e por que cenários mais comprimidos custam mais (overhead de coordenação, paralelismo, risco). O segundo analisa como as incertezas e inconsistências identificadas em `WORK_DIR\analise-spec` afetam os custos — seja honesto sobre o que ainda está indefinido.

---

Grave a saída em um arquivo temporário e em seguida execute:

```powershell
python "<SKILL_DIR>\scripts\salvar-dimensionamento.py" "<WORK_DIR>" "<ARQUIVO_TEMP>"
```
