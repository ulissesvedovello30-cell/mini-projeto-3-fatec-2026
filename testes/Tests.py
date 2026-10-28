from estrutura.No import No
from estrutura.Queue import Queue

# Testes do No (a "caixinha" que guarda um conteúdo e aponta pro próximo)
def teste_no_guarda_conteudo():
    no = No("Peça A")
    assert no.content == "Peça A"  # o que eu coloquei dentro tem que estar lá


def teste_no_novo_nao_tem_proximo():
    no = No("Peça A")
    assert no.next is None  # nó recém-criado ainda não aponta pra ninguém


def teste_ligar_dois_nos():
    a = No("Peça A")
    b = No("Peça B")
    a.next = b  # liga A -> B
    assert a.next.content == "Peça B"  # seguindo o next da A, chego na B


# Aqui os testes são chamados na mão (os da fila ficam em test_queue.py)
teste_no_guarda_conteudo()
teste_no_novo_nao_tem_proximo()
teste_ligar_dois_nos()
print("Tudo certo! ✅")
