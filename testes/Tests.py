from estrutura.No import No


def teste_no_guarda_conteudo():
    no = No("Peça A")
    assert no.content == "Peça A"


def teste_no_novo_nao_tem_proximo():
    no = No("Peça A")
    assert no.next is None


def teste_ligar_dois_nos():
    a = No("Peça A")
    b = No("Peça B")
    a.next = b
    assert a.next.content == "Peça B"


teste_no_guarda_conteudo()
teste_no_novo_nao_tem_proximo()
teste_ligar_dois_nos()
print("Tudo certo! ✅")
