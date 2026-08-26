# Priorização Comercial — Ranking de Oportunidades por Empresa

*Parte da série **Databricks de Ponta a Ponta***

![CI](https://github.com/<seu-usuario>/priorizacao-comercial-databricks/actions/workflows/ci.yml/badge.svg) ![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Problema de negócio
O time comercial não tem capacidade de abordar todas as empresas do mercado-alvo num trimestre. É preciso decidir, com critério defensável, quais empresas priorizar para maximizar a conversão dado um time de tamanho fixo — não é uma pergunta de "quem comprar", é uma pergunta de alocação de capacidade escassa.

## Base de dados
- **CNPJ** (Receita Federal) — https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/dados-abertos/cadastros (espelho mais rápido: https://dados-abertos-rf-cnpj.casadosdados.com.br/) — cadastro de empresas: porte, CNAE, tempo de atividade, situação cadastral, localização
- **Complemento interno:** base já unificada (BACEN + SEBRAE + dados hospitalares por CNPJ) usada no Projeto Mezzo real

## Métrica-alvo
- **Métrica primária:** aumento de X pontos percentuais na taxa de conversão nas contas priorizadas pelo ranking vs. abordagem sem priorização (o valor de X é definido com o time comercial após o primeiro ciclo de uso real)
- **Métrica operacional:** ranking atualizado sem intervenção manual, disponível no dashboard antes do início de cada ciclo comercial

## Hipóteses
1. **H1 — Porte e setor combinados com saúde financeira regional:** empresas de determinado porte/CNAE, combinadas com um indicador de crédito regional favorável (via SCR.data), têm maior probabilidade de conversão do que empresas isoladas apenas por porte.
2. **H2 — Maturidade da empresa como fator de conversão:** empresas com CNPJ ativo há mais tempo convertem mais do que empresas recém-abertas, porque tendem a ter maior estabilidade financeira e menor risco percebido pelo time comercial.

## Perguntas de investigação
1. **Quais variáveis** (porte, CNAE, tempo de atividade, indicador de crédito regional) mais explicam a variação no score de oportunidade?
2. **Os clusters gerados pelo K-Means** resultam em segmentos com perfis de conversão realmente distintos e acionáveis pelo time comercial, ou os grupos se sobrepõem demais para orientar decisão prática?
3. **A capacidade do time comercial é suficiente** para atender ao volume do segmento de maior prioridade, ou o ranking precisa ser fatiado por sub-região para ser executável?
4. **O ranking se mantém estável mês a mês**, ou há rotatividade alta o suficiente para prejudicar a confiança do time comercial na ferramenta?

## Modelo
- **Modelo principal:** scoring ponderado (regras de negócio com pesos definidos e justificados) + K-Means para segmentação — é a abordagem já validada no Projeto Mezzo real, escolhida por ser interpretável e fácil de ajustar junto ao time comercial
- **Evolução planejada:** migração para Random Forest/XGBoost assim que houver histórico de vendas suficiente para treinar um modelo supervisionado de conversão — documentar explicitamente por que o scoring ponderado é a escolha certa nesta fase (falta de rótulo histórico) e não um modelo mais sofisticado

## Arquitetura no Databricks (pipeline ponta a ponta)
1. **Bronze** — ingestão via Delta Live Tables do cadastro CNPJ + bases internas
2. **Silver** — join por CNPJ, limpeza, padronização
3. **Gold** — tabela de scoring + segmentos K-Means
4. **Consumo** — Databricks SQL + dashboard para o time comercial
5. **Governança** — Unity Catalog controlando o acesso do time comercial à tabela Gold

## Limitações assumidas
- Sem histórico de vendas rotulado, o score é baseado em regras de negócio ponderadas, não em um modelo supervisionado — a validação de que os pesos escolhidos realmente predizem conversão só é possível depois de um ciclo real de uso
- O cruzamento com SCR.data é agregado por UF/CNAE, não por empresa individual — funciona como contexto, não como variável exata da empresa

## Status
Extensão direta do Projeto Mezzo já em produção interna, adaptado para simulação com dado público de CNPJ.
