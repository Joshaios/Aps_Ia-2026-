import pandas as pd
from newspaper import Article


def construir_dataset(lista_urls, label_classificacao):
    """
    Processa uma lista de URLs, extrai a semântica e estrutura em um DataFrame.
    label_classificacao: inteiro (ex: 1 para Verdadeira, 0 para Falsa)
    """
    dados_extraidos = []

    for url in lista_urls:
        try:
            artigo = Article(url, language='pt')
            artigo.download()
            artigo.parse()

            # Higienização básica: remove quebras de linha brutas do HTML
            texto_limpo = artigo.text.replace('\n', ' ').strip()

            if texto_limpo:
                dados_extraidos.append({
                    "texto": texto_limpo,
                    "label": label_classificacao
                })

        except Exception as e:
            print(f"Erro de rede ou parsing na URL {url}: {e}")

    # Retorna uma estrutura tabular serializável
    return pd.DataFrame(dados_extraidos)


# --- Exemplo de Uso ---
links_noticias_reais = ["https://g1.globo.com/meio-ambiente/noticia/2026/08/12/novo-veranico-comeca-hoje.ghtml", "https://g1.globo.com/meio-ambiente/noticia/2026/08/12/novo-veranico-comeca-hoje.ghtml"]
df_reais = construir_dataset(links_noticias_reais, 1)

# Exporta para CSV para treinar o modelo depois
df_reais.to_csv("dataset_noticias.csv", index=False)
