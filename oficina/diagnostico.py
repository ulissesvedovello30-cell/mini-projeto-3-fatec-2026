from dataclasses import dataclass
from estrutura.Tree import Tree
from estrutura.LinkedList import LinkedList

OK = "OK"
COM_DEFEITO = "Com defeito"


@dataclass
class Componente:
    nome: str
    codigo: str = None # só as peças têm código
    estado: str = OK


class Diagnostico:
    def __init__(self):
        self.arvore = Tree(Componente("Veículo"))

    @classmethod
    def padrao(cls):
        # Árvore pré-definida do enunciado (não é editada depois)
        d = cls()
        raiz = d.arvore.root
        motor = raiz.add_child(Componente("Motor"))
        ignicao = motor.add_child(Componente("Sistema de ignição"))
        ignicao.add_child(Componente("Vela", "VELA-001"))
        ignicao.add_child(Componente("Bobina", "BOB-001"))
        motor.add_child(Componente("Correia dentada", "COR-001"))
        freios = raiz.add_child(Componente("Freios"))
        freios.add_child(Componente("Pastilha dianteira", "PAST-001"))
        freios.add_child(Componente("Disco dianteiro", "DISC-001"))
        suspensao = raiz.add_child(Componente("Suspensão"))
        suspensao.add_child(Componente("Amortecedor", "AMORT-001"))
        suspensao.add_child(Componente("Bandeja", "BAND-001"))
        return d

    def exibir(self):
        # Pré-ordem: cada linha é indentada pela profundidade do nó
        linhas = []
        for no, profundidade in self.arvore.preorder():
            c = no.content
            texto = "    " * profundidade + "- " + c.nome
            if c.codigo:
                texto += f" [{c.codigo}]"
            if c.estado != OK:
                texto += f" ({c.estado})"
            linhas.append(texto)
        return "\n".join(linhas)

    def marcar_defeito(self, nome):
        no = self.arvore.find(lambda c: c.nome == nome)
        if no is None:
            raise ValueError(f"Componente '{nome}' não encontrado")
        no.content.estado = COM_DEFEITO
        return no.content

    def pecas_com_defeito(self):
        defeituosas = LinkedList()
        for no, _ in self.arvore.preorder():
            c = no.content
            if c.codigo and c.estado == COM_DEFEITO:
                defeituosas.add_list(c)
        return defeituosas
