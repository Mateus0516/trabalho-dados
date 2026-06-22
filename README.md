# Trabalho Final — Recuperação da Informação (2026.1)

**Disciplina:** Ciências de Dados
**Curso:** Bacharelado em Ciências da Computação — CEUB
**Professor:** MSc. Weslley Rodrigues
**Entrega e apresentação:** 23/06/2026

> Este é o repositório-modelo da disciplina. Façam um **fork** deste repositório, renomeiem para o grupo de vocês (ex.: `trabalho-final-rdi-grupo-3`) e sigam as orientações abaixo.

---

# Estados mais ricos possuem melhores oportunidades para profissionais de dados?
 
> Análise comparativa entre as edições 2023 e 2024 da pesquisa *State of Data Brazil* (Data Hackers + Bain) e o PIB per capita por estado, investigando se a riqueza estadual está associada a melhores salários e maior concentração de profissionais de dados.
 
---
 
## Sumário
 
- [Sobre o projeto](#sobre-o-projeto)
- [Fontes de dados](#fontes-de-dados)
- [Estrutura do notebook](#estrutura-do-notebook)
- [Pré-requisitos](#pré-requisitos)
- [Como executar](#como-executar)
- [Principais achados](#principais-achados)
- [Limitações](#limitações)
- [Arquivos gerados](#arquivos-gerados)
---
 
## Sobre o projeto
 
Este projeto de ciência de dados investiga a relação entre a riqueza econômica dos estados brasileiros e as condições oferecidas a profissionais de dados. Para isso, integra duas fontes de dados distintas:
 
1. **State of Data Brazil** — pesquisa voluntária anual da comunidade de dados brasileira (Data Hackers + Bain), coletada nas edições de 2023 e 2024.
2. **PIB per capita e população por estado** — dados coletados via *web scraping* de tabelas públicas da Wikipédia, com base em fontes do IBGE.
A pergunta central é respondida por meio de 7 gráficos que contam uma narrativa visual progressiva, complementados por métricas estatísticas de robustez (correlação de Pearson e Spearman, regressão linear, intervalo de confiança via bootstrap e análise de pool temporal).
 
---
 
## Fontes de dados
 
| Fonte | Como é coletada | Descrição |
|---|---|---|
| State of Data Brazil 2024 | Download via API do Kaggle | `datahackers/state-of-data-brazil-20242025` |
| State of Data Brazil 2023 | Download via API do Kaggle | `datahackers/state-of-data-brazil-2023` |
| PIB per capita por estado | Web scraping (Wikipédia) | Ano-base 2023, fonte IBGE |
| População por estado | Web scraping (Wikipédia) | Censo 2022, fonte IBGE |
 
> **Nota:** foram investigadas e descartadas fontes alternativas para a métrica de "profissionais de dados" (PNAD Contínua via SIDRA e RAIS via Base dos Dados). Os motivos estão documentados na Seção 6.2 do notebook.
 
---
 
## Estrutura do notebook
 
```
estados_ricos_dados_REVISADO.ipynb
│
├── 1. Setup e bibliotecas
├── 2. Carregamento da base State of Data Brazil (2024)
│   └── 2.4 Encontrar as colunas relevantes
├── 3. Web Scraping
│   ├── 3.1 PIB per capita por estado (Wikipédia)
│   └── 3.2 População por estado (Wikipédia)
├── 4. Padronização — chave de junção (UF)
│   └── 4.1 Incorporar a população ao PIB
├── 5. Integração das bases (2024 + 2023)
│   ├── 5.1 Integrar a edição 2024
│   ├── 5.2 Baixar e carregar a edição 2023
│   └── 5.3 Padronizar, agregar 2023 e juntar com 2024
├── 6. Análise comparativa
│   ├── 6.1 Métricas avançadas (Spearman, robustez sem DF, R², bootstrap, pool)
│   └── 6.2 Densidade de respondentes e salário relativo ao PIB
├── 7. Narrativa visual (7 gráficos em sequência)
├── 8. Conclusão
└── 9. Gerar relatório em PDF
```
 
---
 
## Pré-requisitos
 
- Python 3.10 ou superior
- [Conta no Kaggle](https://www.kaggle.com) (gratuita) para download das bases
### Instalação das dependências
 
As bibliotecas necessárias são instaladas automaticamente pelas primeiras células do notebook. Se preferir instalar manualmente:
 
```bash
pip install beautifulsoup4 lxml plotly kaggle fpdf2 scipy pandas matplotlib seaborn
```
 
---
 
## Como executar
 
### 1. Configurar a autenticação do Kaggle
 
No Kaggle, acesse **Settings → API → Create New Token**. Um token no formato `KGAT_...` será gerado.
 
Salve o token no local que o pacote `kaggle` procura automaticamente:
 
**Mac/Linux:**
```bash
mkdir -p ~/.kaggle
echo "SEU_TOKEN_AQUI" > ~/.kaggle/access_token
chmod 600 ~/.kaggle/access_token
```
 
**Windows (PowerShell):**
```powershell
mkdir $env:USERPROFILE\.kaggle -Force
"SEU_TOKEN_AQUI" | Out-File -FilePath "$env:USERPROFILE\.kaggle\access_token" -Encoding ascii -NoNewline
```
 
> ⚠️ Trate o token como uma senha — nunca cole em código, prints públicos ou repositórios.
 
Alternativamente, autentique via OAuth com:
```bash
kaggle auth login
```
 
### 2. Clonar ou baixar este projeto
 
Coloque o arquivo `estados_ricos_dados_REVISADO.ipynb` em uma pasta de trabalho.
 
### 3. Abrir e executar o notebook
 
Abra o notebook no **Cursor**, **VS Code** ou **Jupyter** e execute todas as células em ordem:
 
```
Restart Kernel and Run All
```
 
> ⚠️ **Importante:** sempre rode do início ao fim em ordem. Células de baixo dependem de variáveis criadas nas de cima.
 
### 4. Ajustar antes de gerar o PDF (Seção 9)
 
Na célula de configuração da Seção 9, preencha:
 
```python
interpretacao_pessoal = "(...seu texto final aqui...)"
nome_aluno   = "Seu nome"
disciplina   = "Nome da disciplina"
data_entrega = "Data"
```
 
O PDF é gerado automaticamente ao rodar a última célula.
 
---
 
## Principais achados
 
| Métrica | Valor | Interpretação |
|---|---|---|
| Pearson (PIB x salário, 2024) | r = 0,45 (p = 0,023) | Moderada, positiva, estatisticamente significativa |
| Spearman (PIB x salário, 2024) | r = 0,45 (p = 0,024) | Idêntica ao Pearson — relação bem comportada |
| Pearson sem o DF (outlier) | r = 0,41 (p = 0,045) | Mantém-se significativa sem o outlier |
| Pearson pool 2023+2024 (n=50) | r = 0,57 (p < 0,001) | Relação se fortalece ao adicionar o ano anterior |
| R² da regressão | 20,6% | PIB explica parte, mas não a maioria, da variação salarial |
| IC 95% do r (bootstrap) | [0,11; 0,70] | Amplo, reflete incerteza de amostra pequena |
| Pearson (PIB x respondentes bruto) | r = 0,37 (p = 0,071) | **Não significativo** — não usar sem normalizar |
| Pearson (PIB x densidade por 100k) | r = 0,82 (p < 0,001) | Forte — tamanho populacional mascarava a relação |
 
**Destaques da narrativa visual:**
- O **Maranhão** é o estado onde o profissional de dados é *proporcionalmente mais valorizado* frente à riqueza local (razão salário/PIB = 0,420).
- O **Distrito Federal** paga os maiores salários absolutos, mas é onde o profissional é *relativamente menos valorizado* (razão = 0,089).
- O **Amapá** pagou R$ 4.866 abaixo do que sua riqueza local previa — o maior desvio em relação à tendência geral.
---
 
## Limitações
 
- A amostra de 2024 cobriu **25 dos 27 estados** (sem Roraima e Acre, que não tiveram respondentes).
- A correlação entre PIB e respondentes **brutos** não foi estatisticamente significativa (p = 0,071) — só ganha robustez ao normalizar por população.
- PIB per capita mede riqueza agregada, não necessariamente o quanto chega ao setor de tecnologia.
- Faixas salariais foram convertidas pelo ponto médio da faixa, o que é uma aproximação.
- No pool 2023+2024, cada estado aparece duas vezes — as observações não são totalmente independentes.
- A "densidade de respondentes" é proxy do lado da oferta (quem já trabalha com dados e participa da comunidade), não um censo do mercado — fontes alternativas (PNAD e RAIS) foram avaliadas e descartadas (ver Seção 6.2).
---
 
## Arquivos gerados
 
Após a execução completa, os seguintes arquivos serão criados na mesma pasta do notebook:
 
| Arquivo | Descrição |
|---|---|
| `pib_per_capita_estados.csv` | PIB per capita raspado da Wikipédia (27 estados) |
| `populacao_estados.csv` | População por estado raspada da Wikipédia (censo 2022) |
| `base_integrada_estado_data_pib.csv` | Base de 2024 integrada com PIB e população |
| `base_integrada_multi_ano.csv` | Pool 2023+2024 integrado (n=50 observações) |
| `grafico1_pib_por_estado.png` | Contexto: PIB per capita por estado |
| `grafico2_pib_x_salario.png` | Evidência central: PIB x salário médio |
| `grafico3_pib_x_oportunidades.png` | PIB x nº de respondentes (proxy de oportunidades) |
| `grafico4_top5_vs_bottom5.png` | Contraste: 5 estados mais ricos vs. 5 mais pobres |
| `grafico5_evolucao_2023_2024.png` | Evolução do salário médio 2023→2024 |
| `grafico6_densidade_profissionais.png` | Densidade de respondentes por 100 mil hab. |
| `grafico7_salario_relativo_pib.png` | Salário relativo ao PIB per capita |
| `relatorio_estados_ricos_dados.pdf` | Relatório completo em PDF (capa + gráficos + conclusão) |

**Integrantes:**

| Nome | Matrícula | E-mail institucional | Usuário GitHub |
|------|-----------|----------------------|----------------|
|Vitor reis rodrigues de Souza|22308730|vitor.rsouza@sempreceub.com|vitorr0801
| Mateus Cavalcante Rodrigues|22303356|mateuscr2005@gmail.com|Mateus0516|
|      |           |                      |                |
|      |           |                      |                |
