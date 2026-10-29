from dataclasses import dataclass
from datetime import datetime
from estrutura.LinkedList import LinkedList


@dataclass
class ItemPeca:
    codigo: str
    nome: str
    quantidade: int
    preco_unitario: float

    def valor(self):
        return self.quantidade * self.preco_unitario


@dataclass
class Servico:
    descricao: str
    valor: float


class OrdemServico:
    def __init__(self, numero, placa, cliente, mecanico, abertura=None):
        self.numero = numero
        self.placa = placa
        self.cliente = cliente
        self.mecanico = mecanico
        self.abertura = abertura or datetime.now()
        self.pecas = LinkedList()
        self.servicos = LinkedList()
        self.remontagem_concluida = False
        self.fechada = False

    def _validar_aberta(self):
        if self.fechada:
            raise ValueError(f"OS {self.numero} já está fechada")

    def adicionar_peca(self, codigo, nome, quantidade, preco_unitario):
        self._validar_aberta()
        item = self.pecas.search(lambda p: p.codigo == codigo)
        if item is not None:
            item.quantidade += quantidade  # mesma peça de novo: soma a quantidade
        else:
            self.pecas.add_list(ItemPeca(codigo, nome, quantidade, preco_unitario))

    def remover_peca(self, codigo):
        self._validar_aberta()
        return self.pecas.remove(lambda p: p.codigo == codigo)

    def adicionar_servico(self, descricao, valor):
        self._validar_aberta()
        self.servicos.add_list(Servico(descricao, valor))

    def remover_servico(self, descricao):
        self._validar_aberta()
        return self.servicos.remove(lambda s: s.descricao == descricao)

    def concluir_remontagem(self):
        self.remontagem_concluida = True

    def valor_pecas(self):
        total = 0
        for peca in self.pecas:
            total += peca.valor()
        return total

    def valor_mao_de_obra(self):
        total = 0
        for servico in self.servicos:
            total += servico.valor
        return total

    def total(self):
        return self.valor_pecas() + self.valor_mao_de_obra()

    def pode_fechar(self):
        return self.remontagem_concluida and not self.fechada


class OrdensServico:
    def __init__(self):
        self.abertas = LinkedList()
        self.fechadas = LinkedList()
        self._proximo_numero = 1

    def abrir(self, placa, cliente, mecanico, abertura=None):
        os_ = OrdemServico(self._proximo_numero, placa, cliente, mecanico, abertura)
        self._proximo_numero += 1
        self.abertas.add_list(os_)
        return os_

    def buscar(self, numero):
        return self.abertas.search(lambda o: o.numero == numero)

    def marcar_fechada(self, numero):
        os_ = self.abertas.remove(lambda o: o.numero == numero)
        if os_ is not None:
            os_.fechada = True
            self.fechadas.add_list(os_)
        return os_
