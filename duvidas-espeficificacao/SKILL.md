---
name: apresentacao-html
description: monta uma apresentação em html com base em textos na mesma pasta
disable-model-invocation: true

## Ambiente Python

- Windows, Python via `python` (não `python3`)
- NUNCA crie virtualenvs ou ambientes temporários — use sempre o Python do sistema
- Se uma biblioteca não estiver instalada, instale com `pip install <lib>` globalmente no sistema
- Sempre usar `encoding="utf-8"` ao abrir/escrever arquivos
- Sempre incluir `PYTHONUTF8=1` ao rodar scripts Python via bash:
  `PYTHONUTF8=1 python script.py`
  ou definir no próprio script: `import os; os.environ["PYTHONUTF8"] = "1"`
- Preferir escrever scripts em arquivo `.py` temporário em vez de heredoc inline

## Preferências gerais

- Economize tokens: sem verbose desnecessário
- Manipulação de arquivos .docx, .xlsx, .pdf: use as libs já instaladas no sistema


---

## 1. ANALISAR

Analise criticamente a specification.
Atue como arquiteto cético.
Tente quebrar a specification.

Identifique:
- ambiguidades
- inconsistências
- requisitos conflitantes
- edge cases
- riscos técnicos
- gargalos
- decisões faltantes
- pontos que precisam de esclarecimento
- Questione premissas implícitas.
- Liste as decisões irreversíveis da arquitetura.
- risco de cybersegurança

Faça perguntas objetivas para convergir a arquitetura.
Não implemente ainda.


## Entrega:
- Escreva a saída de forma estruturada em um html usando o arquivo abaixo
- o html possui comentários identificando onde as informações devem ser inseridas de forma detalhada
- Linguagem: humanizada, informal, simples e conversada.
- Separe os parágrafos com duplo espaço.

<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <title>Relatório de Especificação</title>

  <!-- Bootstrap -->
  <link
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
    rel="stylesheet"
  />

  <!-- Bootstrap Icons -->
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css"
  />

  <!-- Fonte -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

  <!-- Você pode trocar aqui -->
  <link
    href="https://fonts.googleapis.com/css2?family=Special+Elite&family=IBM+Plex+Mono:wght@300;400;500;600&display=swap"
    rel="stylesheet"
  >

  <style>
    :root {

      /* =========================
         CORES
      ========================== */

      --color-bg: #f8f7f4;
      --color-paper: #ffffff;

      --color-text: #2b2b2b;
      --color-text-soft: #4d4d4d;

      --color-border: #d8d5cf;

      --color-title: #1e1e1e;

      --color-highlight: #ece9e2;

      --color-shadow: rgba(0,0,0,0.04);

      /* =========================
         FONTES
      ========================== */

      --font-title: "Special Elite", serif;
      --font-body: "IBM Plex Mono", monospace;

      /* =========================
         TAMANHOS
      ========================== */

      --font-size-base: 15px;

      --font-size-title: 2.4rem;
      --font-size-subtitle: 1.1rem;

      --font-size-section: 1.2rem;
      --font-size-card-title: 1rem;

      --line-height: 1.85;

      /* =========================
         ESPAÇAMENTOS
      ========================== */

      --container-width: 1100px;

      --page-padding-y: 72px;
      --page-padding-x: 24px;

      --section-margin: 72px;

      --card-padding: 28px;

      --card-gap: 22px;

      --border-radius: 0px;

      /* =========================
         SOMBRAS
      ========================== */

      --shadow-paper:
        0 1px 2px rgba(0,0,0,0.04),
        0 8px 24px rgba(0,0,0,0.03);

      /* =========================
         TRANSIÇÕES
      ========================== */

      --transition-default: 180ms ease;

    }

    html {
      scroll-behavior: smooth;
    }

    body {
      background: var(--color-bg);
      color: var(--color-text);
      font-family: var(--font-body);
      font-size: var(--font-size-base);
      line-height: var(--line-height);

      -webkit-font-smoothing: antialiased;
      text-rendering: optimizeLegibility;

      padding:
        var(--page-padding-y)
        var(--page-padding-x);
    }

    .page {
      max-width: var(--container-width);
      margin: 0 auto;
      background: var(--color-paper);
      box-shadow: var(--shadow-paper);
      border: 1px solid var(--color-border);
      padding: 72px;
      position: relative;
    }

    .page::before {
      content: "";
      position: absolute;
      inset: 0;
      pointer-events: none;

      background:
        repeating-linear-gradient(
          to bottom,
          transparent,
          transparent 31px,
          rgba(0,0,0,0.015) 32px
        );
    }

    .hero {
      margin-bottom: 90px;
      border-bottom: 1px solid var(--color-border);
      padding-bottom: 36px;
    }

    .hero small {
      display: block;
      text-transform: uppercase;
      letter-spacing: 2px;
      margin-bottom: 12px;
      color: var(--color-text-soft);
    }

    .hero h1 {
      font-family: var(--font-title);
      font-size: var(--font-size-title);
      color: var(--color-title);
      margin-bottom: 18px;
      line-height: 1.3;
    }

    .hero p {
      max-width: 760px;
      color: var(--color-text-soft);
      margin: 0;
    }

    .section {
      margin-bottom: var(--section-margin);
    }

    .section-header {
      display: flex;
      align-items: center;
      gap: 14px;

      margin-bottom: 28px;
      padding-bottom: 12px;

      border-bottom: 1px dashed var(--color-border);
    }

    .section-header i {
      font-size: 1.1rem;
      color: var(--color-text-soft);
    }

    .section-header h2 {
      margin: 0;
      font-size: var(--font-size-section);
      font-family: var(--font-title);
      color: var(--color-title);
    }

    .summary-box {
      border: 1px solid var(--color-border);
      background: #fcfcfb;
      padding: 28px;
    }

    .item-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: var(--card-gap);
    }

    .analysis-card {
      border: 1px solid var(--color-border);
      background: white;
      padding: var(--card-padding);

      transition: var(--transition-default);

      position: relative;
    }

    .analysis-card:hover {
      transform: translateY(-2px);
      box-shadow:
        0 6px 18px rgba(0,0,0,0.04);
    }

    .analysis-card::before {
      content: "";
      position: absolute;
      top: 0;
      left: 0;

      width: 100%;
      height: 3px;

      background: var(--color-title);
      opacity: 0.08;
    }

    .analysis-card-header {
      display: flex;
      align-items: center;
      gap: 12px;

      margin-bottom: 18px;
    }

    .analysis-card-header i {
      font-size: 1rem;
      color: var(--color-text-soft);
    }

    .analysis-card-header h3 {
      margin: 0;
      font-size: var(--font-size-card-title);
      font-family: var(--font-title);
      color: var(--color-title);
    }

    .analysis-card p {
      margin: 0;
      color: var(--color-text-soft);
    }

    .footer-note {
      margin-top: 80px;
      padding-top: 24px;
      border-top: 1px dashed var(--color-border);

      font-size: 0.9rem;
      color: var(--color-text-soft);
    }

    @media (max-width: 768px) {

      .page {
        padding: 36px 24px;
      }

      .hero h1 {
        font-size: 1.9rem;
      }

      .item-grid {
        grid-template-columns: 1fr;
      }

    }

  </style>
</head>
<body>

  <main class="page">

    <!-- HERO -->

    <section class="hero">

      <small>Relatório Técnico de Especificação</small>

      <h1>
        Análise Estruturada da Solução
      </h1>

      <p>
	  
		<!-- JÁ COLOQUE AQUI O RESUMO DO RESULTADO DA ANÁLISE DA ESPECIFICAÇÃO DETALHADAMENTE-->

      </p>

    </section>

    <!-- RESUMO -->

    <section class="section">

      <div class="section-header">
        <i class="bi bi-file-earmark-text"></i>
        <h2>Resumo do Pedido</h2>
      </div>

      <div class="summary-box">
        <p>
			<!--
				Inserir aqui um resumo executivo da demanda original, contendo os objetivos
				do sistema, principais requisitos, contexto operacional e visão geral da solução proposta.
				texto com 500 palavras
			-->
        </p>
      </div>

    </section>

    <!-- AMBIGUIDADES -->

    <section class="section">

      <div class="section-header">
        <i class="bi bi-question-circle"></i>
        <h2>Ambiguidades</h2>
      </div>

      <div class="item-grid">



		<!--LISTE TODAS AS AMBIGUIDADES CADA article DEVE CONTER UMA COM O TÍTULO E A DESCRIÇÃO-->
        <article class="analysis-card">
          <div class="analysis-card-header">
            <i class="bi bi-dot"></i>
            <h3><!--Título da Ambiguidade--></h3>
          </div>
          <p>
            <!--Pequena explicação descrevendo o ponto ambíguo identificado na especificação.-->
          </p>
        </article>
		
		
		

      </div>

    </section>

    <!-- INCONSISTÊNCIAS -->

    <section class="section">

      <div class="section-header">
        <i class="bi bi-exclamation-circle"></i>
        <h2>Inconsistências</h2>
      </div>

      <div class="item-grid">

		<!--LISTE TODAS AS INCONSISTÊNCIAS CADA article DEVE CONTER UMA COM O TÍTULO E A DESCRIÇÃO-->
        <article class="analysis-card">
          <div class="analysis-card-header">
            <i class="bi bi-dot"></i>
            <h3><!--Título da Inconsistência--></h3>
          </div>
          <p>
            <!--Explicação da inconsistência encontrada e impacto potencial.-->
          </p>
        </article>

      </div>

    </section>

    <!-- REQUISITOS CONFLITANTES -->

    <section class="section">


      <div class="section-header">
        <i class="bi bi-shuffle"></i>
        <h2>Requisitos Conflitantes</h2>
      </div>

      <div class="item-grid">


		<!--LISTE TODAS AS REQUISITOS CONFLITANTES CADA article DEVE CONTER UMA COM O TÍTULO E A DESCRIÇÃO-->
        <article class="analysis-card">
          <div class="analysis-card-header">
            <i class="bi bi-dot"></i>
            <h3><!-- Titulo do Conflito Identificado--></h3>
          </div>

          <p>
            <!--Explicação do conflito entre requisitos funcionais, técnicos ou operacionais.-->
          </p>
        </article>

      </div>

    </section>

    <!-- EDGE CASES -->

    <section class="section">

      <div class="section-header">
        <i class="bi bi-bezier2"></i>
        <h2>Edge Cases</h2>
      </div>

      <div class="item-grid">

		<!--LISTE TODAS OS EDGE CASES CADA article DEVE CONTER UMA COM O TÍTULO E A DESCRIÇÃO-->
        <article class="analysis-card">
          <div class="analysis-card-header">
            <i class="bi bi-dot"></i>
            <h3><!-- Titulo do EDGE CASES--></h3>
          </div>
          <p>
            <!--Descrição de comportamento extremo ou situação não convencional.-->
          </p>
        </article>

      </div>

    </section>

    <!-- RISCOS -->

    <section class="section">

      <div class="section-header">
        <i class="bi bi-radioactive"></i>
        <h2>Riscos Técnicos</h2>
      </div>

      <div class="item-grid">

		<!--LISTE TODAS OS Riscos Técnicos CADA article DEVE CONTER UMA COM O TÍTULO E A DESCRIÇÃO-->
        <article class="analysis-card">
          <div class="analysis-card-header">
            <i class="bi bi-dot"></i>
            <h3><!-- titulo do Risco Técnico--></h3>
          </div>
          <p>
            <!--Explicação do risco, impacto esperado e possíveis consequências.-->
          </p>
        </article>
		

      </div>

    </section>

    <!-- GARGALOS -->

    <section class="section">

      <div class="section-header">
        <i class="bi bi-hourglass-split"></i>
        <h2>Gargalos</h2>
      </div>

      <div class="item-grid">

		<!--LISTE TODAS OS GARGALOS CADA article DEVE CONTER UMA COM O TÍTULO E A DESCRIÇÃO-->
        <article class="analysis-card">
          <div class="analysis-card-header">
            <i class="bi bi-dot"></i>
            <h3><!--Titulo do Possível Gargalo--></h3>
          </div>
          <p>
            <!--Descrição do potencial gargalo operacional, técnico ou arquitetural.-->
          </p>
        </article>

      </div>

    </section>

    <!-- DECISÕES FALTANTES -->

    <section class="section">

      <div class="section-header">
        <i class="bi bi-diagram-3"></i>
        <h2>Decisões Faltantes</h2>
      </div>

      <div class="item-grid">

		<!--LISTE TODAS as DECISÕES FALTANTES CADA article DEVE CONTER UMA COM O TÍTULO E A DESCRIÇÃO-->
        <article class="analysis-card">
          <div class="analysis-card-header">
            <i class="bi bi-dot"></i>
            <h3><!-- Titulo da Decisão Necessária--></h3>
          </div>
          <p>
            <!--Explicação da decisão arquitetural ou funcional ainda não definida.-->
          </p>
        </article>

      </div>

    </section>

    <!-- ESCLARECIMENTOS -->

    <section class="section">

      <div class="section-header">
        <i class="bi bi-chat-left-text"></i>
        <h2>Pontos que Precisam de Esclarecimento</h2>
      </div>

      <div class="item-grid">

		<!--LISTE TODAS OS ESCLARECIMENTOS CADA article DEVE CONTER UMA COM O TÍTULO E A DESCRIÇÃO-->
        <article class="analysis-card">
          <div class="analysis-card-header">
            <i class="bi bi-dot"></i>
            <h3><!--Titulo da Pergunta em Aberto--></h3>
          </div>
          <p>
            <!--Descrição do ponto que necessita alinhamento adicional.-->
          </p>
        </article>

      </div>

    </section>

    <!-- PREMISSAS -->

    <section class="section">

      <div class="section-header">
        <i class="bi bi-lightbulb"></i>
        <h2>Questionamento de Premissas Implícitas</h2>
      </div>

      <div class="item-grid">


		<!--LISTE TODAS As Premissas CADA article DEVE CONTER UMA COM O TÍTULO E A DESCRIÇÃO-->
        <article class="analysis-card">
          <div class="analysis-card-header">
            <i class="bi bi-dot"></i>
            <h3><!-- Titulo da Premissa Implícita--></h3>
          </div>
          <p>
            <!--Questionamento sobre hipóteses assumidas sem validação explícita.-->
          </p>
        </article>

      </div>

    </section>

    <!-- DECISÕES IRREVERSÍVEIS -->
    <section class="section">
      <div class="section-header">
        <i class="bi bi-lock"></i>
        <h2>Decisões Irreversíveis da Arquitetura</h2>
      </div>
      <div class="item-grid">
		<!--LISTE TODAS AS DECISÕES IRREVERSÍVEIS CADA article DEVE CONTER UMA COM O TÍTULO E A DESCRIÇÃO-->
        <article class="analysis-card">
          <div class="analysis-card-header">
            <i class="bi bi-dot"></i>
            <h3><!--titulo da Decisão Estrutural--></h3>
          </div>
          <p>
            <!--Descrição de decisão arquitetural com alto custo de reversão futura.-->
          </p>
        </article>
      </div>
    </section>
	
	
    <!-- CYBER SEGURANÇA -->
    <section class="section">
      <div class="section-header">
        <i class="bi bi-exclamation-triangle"></i>
        <h2>Cyber Segurança</h2>
      </div>
      <div class="item-grid">
		<!--LISTE TODOS RISCOS DE CYBER SEGURANÇA CADA article DEVE CONTER UMA COM O TÍTULO E A DESCRIÇÃO-->
        <article class="analysis-card">
          <div class="analysis-card-header">
            <i class="bi bi-dot"></i>
            <h3><!--titulo da Decisão Estrutural--></h3>
          </div>
          <p>
            <!--Descrição do risco de cyber segurança com alto custo de reversão futura.-->
          </p>
        </article>
      </div>
    </section>
	
	
    <!-- DETALHAMENTO DA ESPECIFICAÇÃO -->
    <section class="section">
      <div class="section-header">
        <i class="bi bi-pencil-square"></i>
        <h2>Cyber Segurança</h2>
      </div>
      <div class="item-grid">
		<!--LISTE TODOS RISCOS DE CYBER SEGURANÇA CADA article DEVE CONTER UMA COM O TÍTULO E A DESCRIÇÃO-->
        <article class="analysis-card">
          <p>
            <!--Aqui vai o detalhamento da especificação, apenas insira o conteúdo do arquivo spec.md gerado anteriormente dentro de uma subpasta que está dentro da pasta \specs-->
          </p>
        </article>
      </div>
    </section>
	

    <!-- FOOTER -->

    <footer class="footer-note">
      Documento gerado para análise crítica de especificação e convergência arquitetural.
    </footer>

  </main>

</body>
</html>

**Gerar apenas:** `Analise.html` nenhum outro arquivo.