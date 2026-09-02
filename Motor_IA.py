import joblib
from newspaper import Article


# Carrega o modelo treinado
modelo = joblib.load("modelo_noticias.pkl")


def analisar_noticia(texto):

    # O Pipeline já transforma o texto com TF-IDF
    # e depois faz a classificação
    classificacao = modelo.predict(
        [texto]
    )[0]

    return classificacao


def analisar_link(url):

    try:

        # Caso o usuário digite o link sem https://
        if not url.startswith("http"):
            url = "https://" + url


        # Baixa a notícia
        artigo = Article(
            url,
            language="pt"
        )

        artigo.download()
        artigo.parse()


        # Obtém título e texto
        titulo = artigo.title

        texto = artigo.text.replace(
            "\n",
            " "
        ).strip()


        # Verifica se conseguiu extrair o texto
        if not texto:

            return (
                "Não foi possível extrair "
                "o texto da notícia."
            )


        # Envia o texto para a IA
        classificacao = analisar_noticia(
            texto
        )


        # Retorna o resultado para a Tela.py
        return (
            f"Título: {titulo}\n\n"
            f"Classificação: Notícia {classificacao}"
        )


    except Exception as erro:

        return (
            f"Erro ao analisar notícia: {erro}"
        )
