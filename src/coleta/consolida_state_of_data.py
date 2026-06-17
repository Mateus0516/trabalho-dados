"""
Consolida as edições do State of Data Brazil (2021–2025) num único .parquet.

ENTRADA  : data/raw/State_of_Data_*.csv
SAÍDA    : data/processed/dados_state_of_data_consolidados.parquet

Rode com: python3 src/coleta/consolida_state_of_data.py
"""

from pathlib import Path
import pandas as pd

PASTA_RAW = Path("data/raw")
PASTA_OUT = Path("data/processed")
ARQUIVO_SAIDA = PASTA_OUT / "dados_state_of_data_consolidados.parquet"


def carregar_edicoes(pasta: Path) -> pd.DataFrame:
    """Lê todos os CSVs State_of_Data_* e empilha num só DataFrame."""
    arquivos = sorted(pasta.glob("State_of_Data_*.csv"))

    if not arquivos:
        raise FileNotFoundError(
            f"Nenhum CSV encontrado em {pasta}. "
            "Coloque os arquivos State_of_Data_AAAA.csv lá."
        )

    quadros = []

    for arq in arquivos:
        print(f"  lendo {arq.name} ...")
        df = pd.read_csv(arq, low_memory=False)
        df["arquivo_origem"] = arq.name
        quadros.append(df)

    consolidado = pd.concat(quadros, ignore_index=True)
    print(f"  total consolidado: {len(consolidado):,} linhas")
    return consolidado


def main():
    PASTA_OUT.mkdir(parents=True, exist_ok=True)

    print("Consolidando edições do State of Data...")
    df = carregar_edicoes(PASTA_RAW)

    df["ano_pesquisa"] = (
        df["arquivo_origem"].str.extract(r"(\d{4})").astype("Int64")
    )

    antes = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    print(f"  duplicatas removidas: {antes - len(df)}")

    # Corrige colunas com tipos misturados para salvar em parquet
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str)

    df.to_parquet(ARQUIVO_SAIDA, index=False)

    print(f"Arquivo gerado: {ARQUIVO_SAIDA}")
    print(f"Dimensões finais: {df.shape[0]:,} linhas x {df.shape[1]:,} colunas")


if __name__ == "__main__":
    main()