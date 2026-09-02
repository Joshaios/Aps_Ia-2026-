import tkinter as tk
from tkinter.constants import DISABLED
from newspaper import Article

PLACEHOLDER = "Digite o link da notícia:" # 10/08/2026 Variável global


def analisar(event=None):
    link = entrada.get()

    if link == PLACEHOLDER or not link.strip():
        return

    # --- ATUALIZAÇÃO DA INTERFACE (MENSAGEM DO USUÁRIO) --- 12/08/2026
    chat.config(state=tk.NORMAL)
    chat.insert(tk.END, "Você: ", "tag_voce")
    chat.insert(tk.END, f"{link}\n\n")
    chat.see(tk.END)
    chat.update()  # Força a interface a atualizar antes de congelar no download

    # --- DECLARAÇÃO DA FUNÇÃO DE EXTRAÇÃO --- 12/08/2026
    def extrair_texto_noticia(url_alvo):
        try:
            if not url_alvo.startswith("http"):
                url_alvo = "https://" + url_alvo

            artigo = Article(url_alvo, language='pt')
            artigo.download()
            artigo.parse()

            return artigo.title
        except Exception as erro:
            return f"Erro na extração: {erro}"

    # --- EXECUÇÃO E RETORNO PARA A INTERFACE --- 12/08/2026
    # Invocamos a função e guardamos o título extraído
    titulo_extraido = extrair_texto_noticia(link)

    # Injetamos a resposta do "Bot" no histórico
    chat.insert(tk.END, "Bot: ", "tag_bot")
    chat.insert(tk.END, f"Título lido: {titulo_extraido}\n\n")

    chat.see(tk.END)
    chat.config(state=tk.DISABLED)

    entrada.delete(0, tk.END)
    janela.focus_set()


def apagar_texto(event): #10/08/2026 função responsável por apagar o texto caso seja igual à variável PlaceHolder lá na linha 4
    if entrada.get() == PLACEHOLDER:
        entrada.delete(0, tk.END) #10/08/2026 Deleta o que está na caixa de texto


def colocar_texto(event): #10/08/2026 função responsável por colocar o texto na variável caso a caixa de texto esteja vazia
    if entrada.get() == "":
        entrada.insert(0, PLACEHOLDER)


# Inicialização do loop de interface
janela = tk.Tk()
janela.title("")
largura = 400
altura = 600

# Cálculo de geometria vetorial para centralização de janela
largura_tela = janela.winfo_screenwidth() #Pega a largura da tela
altura_tela = janela.winfo_screenheight() # Pega a altura da tela
x = (largura_tela - largura) // 2 # Responsável por pegar a largura da tela subtrair com a largura da janela e dividir por 2 para centralizar o eixo X
y = (altura_tela - altura) // 2 # Responsável por pegar a altura da tela subtrair com a altura da janela e dividir por 2 para centralizar o eixo Y

janela.geometry(f"{largura}x{altura}+{x}+{y}") # Responsável pela largura e altura da janela e também responsável pelo eixo x e y da posição do mesmo
janela.config(bg="#45484A") #Responsável pela cor de fundo

# Área de exibição (agora com texto alinhado no topo esquerdo)
chat = tk.Text(janela, font=("Arial", 10), fg="#ffffff", cursor="arrow")
chat.place(width=370, height=530, x=15, y=15)
chat.tag_config("tag_voce", foreground="#000080")
chat.tag_config("tag_bot", foreground="#D75413")
chat.config(bg="#7a7a7a", state=DISABLED)

# Área de inserção
entrada = tk.Entry(janela)
entrada.insert(0, PLACEHOLDER)
entrada.place(width=310, height=30, x=15, y=555)
entrada.config(bg="#7a7a7a", fg="#CCFF00")

# Botão de disparo de evento
botao = tk.Button(janela, text="Analisar", command=lambda:[analisar()])
botao.place(width=50, height=30, x=335, y=555)
botao.config(bg="#7a7a7a")

# Bindings de controle de estado (foco)
entrada.bind("<FocusIn>", apagar_texto) #10/08/2026 Quando o focar na caixa de texto "entrada" vai chamar a def "apagar_texto" da linha 28
entrada.bind("<FocusOut>", colocar_texto) #10/08/2026 Quando o foco sair da caixa de texto "entrada" vai chamar a def "colocar_texto" da linha 33
entrada.bind("<Return>", lambda event: analisar()) # 11/08/2026 Faz o botão Enter quando apertado ter a funcionalidade da DEF "Analisar" na linha 6

janela.bind("<Button-1>", lambda event: event.widget.focus_set()) # 10/08/2026 Faz com que o clique esquerdo do mouse transfira o foco dele para o local de onde o cursor está em cima

janela.mainloop()
