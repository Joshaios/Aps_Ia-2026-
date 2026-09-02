import pandas as pd
import joblib

from newspaper import Article

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report


# ============================================================
# LINKS UTILIZADOS PARA TREINAR A IA
# ============================================================

noticias = [

    # -------------------------
    # NOTÍCIAS BOAS
    # -------------------------

    {
        "url": "https://g1.globo.com/df/distrito-federal/noticia/2026/08/30/projeto-de-restauracao-do-cerrado-e-reconhecido-como-referencia-mundial-pela-onu-conheca.ghtml",
        "classificacao": "boa"
    },

    {
        "url": "https://g1.globo.com/to/tocantins/noticia/2026/04/19/acordo-preve-recuperacao-de-33-mil-hectares-de-area-degradada-no-cerrado-segundo-mpto.ghtml",
        "classificacao": "boa"
    },

    {
        "url": "https://g1.globo.com/to/tocantins/noticia/2026/04/19/acordo-preve-recuperacao-de-33-mil-hectares-de-area-degradada-no-cerrado-segundo-mpto.ghtml",
        "classificacao": "boa"
    },



    # -------------------------
    # NOTÍCIAS RUINS
    # -------------------------

    {
        "url": "https://g1.globo.com/meio-ambiente/noticia/2025/10/01/cerrado-perdeu-40-milhoes-de-hectares-de-vegetacao-em-40-anos-aponta-estudo.ghtml",
        "classificacao": "ruim"
    },

    {
        "url": "https://g1.globo.com/meio-ambiente/noticia/2025/05/15/desmatamento-no-brasil-recua-mas-cerrado-concentra-maior-devastacao-e-mais-de-50percent-das-perdas-aponta-mapbiomas.ghtml",
        "classificacao": "ruim"
    },
    {
        "url": "https://g1.globo.com/meio-ambiente/noticia/2025/05/15/desmatamento-no-brasil-recua-mas-cerrado-concentra-maior-devastacao-e-mais-de-50percent-das-perdas-aponta-mapbiomas.ghtml",
        "classificacao": "ruim"
    }
]


# ============================================================
# FUNÇÃO PARA EXTRAIR O TEXTO DAS NOTÍCIAS
# ============================================================

def coletar_noticias(lista_noticias):

    dados = []

    for noticia in lista_noticias:

        url = noticia["url"]
        classificacao = noticia["classificacao"]

        try:

            print(f"\nProcessando: {url}")

            artigo = Article(
                url,
                language="pt"
            )

            artigo.download()
            artigo.parse()

            titulo = artigo.title

            texto = artigo.text.replace(
                "\n",
                " "
            ).strip()

            if texto:

                dados.append({
                    "url": url,
                    "titulo": titulo,
                    "texto": texto,
                    "classificacao": classificacao
                })

                print(
                    f"Adicionada como: {classificacao}"
                )

            else:

                print(
                    "Não foi possível extrair o texto."
                )

        except Exception as erro:

            print(
                f"Erro ao acessar a notícia: {erro}"
            )

    return pd.DataFrame(dados)


# ============================================================
# CRIA O DATASET
# ============================================================

df = coletar_noticias(noticias)


df.to_csv(
    "dataset_noticias.csv",
    index=False,
    encoding="utf-8-sig"
)


print("\nDataset criado!")
print(df[["titulo", "classificacao"]])


# ============================================================
# VERIFICAÇÃO
# ============================================================

if len(df) < 4:
    print("\nPoucas notícias foram coletadas.")
    exit()


print("\nQuantidade por classificação:")

print(
    df["classificacao"].value_counts()
)


# ============================================================
# DEFINE ENTRADA E RESPOSTA
# ============================================================

X = df["texto"]

y = df["classificacao"]


# ============================================================
# SEPARA TREINAMENTO E TESTE
# ============================================================

X_treino, X_teste, y_treino, y_teste = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ============================================================
# CRIA O MODELO
# ============================================================

modelo = Pipeline([

    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            max_features=5000
        )
    ),

    (
        "classificador",
        LogisticRegression(
            max_iter=1000
        )
    )

])


# ============================================================
# TREINAMENTO
# ============================================================

print("\nTreinando modelo...")


modelo.fit(
    X_treino,
    y_treino
)


# ============================================================
# TESTE
# ============================================================

previsoes = modelo.predict(
    X_teste
)


acuracia = accuracy_score(
    y_teste,
    previsoes
)


print("\nAcurácia:")

print(
    f"{acuracia * 100:.2f}%"
)


print("\nRelatório de classificação:")

print(
    classification_report(
        y_teste,
        previsoes
    )
)


# ============================================================
# SALVA O MODELO
# ============================================================

joblib.dump(
    modelo,
    "modelo_noticias.pkl"
)


print(
    "\nModelo salvo como modelo_noticias.pkl"
)
