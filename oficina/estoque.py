from dataclasses import dataclass
from datetime import date
from estrutura.LinkedList import LinkedList
from estrutura.Queue import Queue


class EstoqueInsuficiente(Exception):
    pass


@dataclass
class Lote:
    numero: int
    fornecedor: str
    preco_compra: float
    data_compra: date
    validade: date  # None quando o produto não vence
    quantidade: int


@dataclass
class Perda:
    codigo: str
    lote: Lote
    data: date


class Produto:
    def __init__(self, nome, codigo, preco_venda, estoque_minimo=0):
        self.nome = nome
        self.codigo = codigo
        self.preco_venda = preco_venda
        self.estoque_minimo = estoque_minimo
        self.lotes = Queue()  # COMBINAÇÃO: fila de lotes, o mais antigo fica na frente (FIFO)

    def quantidade_total(self):
        total = 0
        for lote in self.lotes:
            total += lote.quantidade
        return total

    def abaixo_do_minimo(self):
        return self.quantidade_total() < self.estoque_minimo

    def consumir(self, quantidade):
        # Baixa pelo lote mais antigo; se ele acabar, sai da fila e usa o próximo.
        if quantidade > self.quantidade_total():
            raise EstoqueInsuficiente(
                f"{self.nome}: pedido {quantidade}, disponível {self.quantidade_total()}")
        usados = LinkedList()  # registra de quais lotes saiu cada quantidade
        restante = quantidade
        while restante > 0:
            lote = self.lotes.peek()
            retirado = min(lote.quantidade, restante)
            lote.quantidade -= retirado
            restante -= retirado
            usados.add_list((lote.numero, retirado, lote.preco_compra))
            if lote.quantidade == 0:
                self.lotes.remove()  # lote esgotado sai da frente da fila
        return usados

    def filtrar_lotes(self, manter):
        # Refaz a fila mantendo só os lotes que passam em "manter" e preservando a ordem.
        # Devolve os lotes que saíram.
        nova = Queue()
        saidos = LinkedList()
        while not self.lotes.is_empty():
            lote = self.lotes.remove().content
            if manter(lote):
                nova.add(lote)
            else:
                saidos.add_list(lote)
        self.lotes = nova
        return saidos


class Estoque:
    def __init__(self):
        self.produtos = LinkedList()  # COMBINAÇÃO: lista de produtos, cada um com uma fila de lotes
        self.perdas = LinkedList()
        self._proximo_lote = 1

    def cadastrar_produto(self, nome, codigo, preco_venda, estoque_minimo=0):
        if self.buscar(codigo) is not None:
            raise ValueError(f"Produto {codigo} já cadastrado")
        produto = Produto(nome, codigo, preco_venda, estoque_minimo)
        self.produtos.add_list(produto)
        return produto

    def buscar(self, codigo):
        return self.produtos.search(lambda p: p.codigo == codigo)

    def _obter(self, codigo):
        produto = self.buscar(codigo)
        if produto is None:
            raise ValueError(f"Produto {codigo} não encontrado")
        return produto

    def comprar_lote(self, codigo, fornecedor, preco_compra, data_compra, quantidade, validade=None):
        produto = self._obter(codigo)
        lote = Lote(self._proximo_lote, fornecedor, preco_compra, data_compra, validade, quantidade)
        self._proximo_lote += 1
        produto.lotes.add(lote)  # compras entram em ordem cronológica: o mais antigo fica na frente
        return lote

    def baixar(self, codigo, quantidade):
        # A baixa percorre a lista até o produto e consome o lote mais antigo da fila dele.
        return self._obter(codigo).consumir(quantidade)

    def quantidade_total(self, codigo):
        return self._obter(codigo).quantidade_total()

    def descartar_vencidos(self, hoje):
        # Lotes com validade anterior a hoje saem do estoque e viram perda.
        descartados = LinkedList()
        for produto in self.produtos:
            vencidos = produto.filtrar_lotes(lambda l: l.validade is None or l.validade >= hoje)
            for lote in vencidos:
                perda = Perda(produto.codigo, lote, hoje)
                self.perdas.add_list(perda)
                descartados.add_list(perda)
        return descartados

    def ajustar_quantidade(self, codigo, numero_lote, nova_quantidade):
        # Ajuste de inventário: corrige a quantidade de um lote (0 = remove o lote).
        if nova_quantidade < 0:
            raise ValueError("Quantidade não pode ser negativa")
        produto = self._obter(codigo)
        lote = None
        for candidato in produto.lotes:
            if candidato.numero == numero_lote:
                lote = candidato
        if lote is None:
            raise ValueError(f"Lote {numero_lote} não encontrado em {codigo}")
        lote.quantidade = nova_quantidade
        if nova_quantidade == 0:
            produto.filtrar_lotes(lambda l: l.numero != numero_lote)
        return lote

    def alertas(self):
        # Produtos cuja quantidade total está abaixo do mínimo
        baixos = LinkedList()
        for produto in self.produtos:
            if produto.abaixo_do_minimo():
                baixos.add_list(produto)
        return baixos
