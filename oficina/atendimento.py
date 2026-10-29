from dataclasses import dataclass
from datetime import datetime
from estrutura.Queue import Queue
from estrutura.LinkedList import LinkedList


@dataclass
class Chegada:
    placa: str
    cliente: str
    data_hora: datetime
    queixa: str
    guincho: bool = False


class Box:
    def __init__(self, numero):
        self.numero = numero
        self.chegada = None # None = box livre

    def livre(self):
        return self.chegada is None


class Atendimento:
    def __init__(self, quantidade_boxes=2):
        self.fila_guincho = Queue() # prioridade, mas FIFO entre si
        self.fila_normal = Queue()  # ordem de chegada
        self.boxes = LinkedList()
        for numero in range(1, quantidade_boxes + 1):
            self.boxes.add_list(Box(numero))

    def chegar(self, placa, cliente, queixa, guincho=False, data_hora=None):
        chegada = Chegada(placa, cliente, data_hora or datetime.now(), queixa, guincho)
        if guincho:
            self.fila_guincho.add(chegada)
        else:
            self.fila_normal.add(chegada)
        return chegada

    def proximo(self):
        # COMBINAÇÃO Fila + Fila: guincho primeiro; se estiver vazia, a fila normal.
        # Só olha (peek), não tira.
        if not self.fila_guincho.is_empty():
            return self.fila_guincho.peek()
        return self.fila_normal.peek()

    def _retirar_proximo(self):
        if not self.fila_guincho.is_empty():
            return self.fila_guincho.remove().content
        removido = self.fila_normal.remove()
        return removido.content if removido is not None else None

    def chamar_proximo(self):
        # Coloca o próximo veículo no primeiro box livre. Devolve (box, chegada) ou None.
        box = self.boxes.search(lambda b: b.livre())
        if box is None:
            return None # todos os boxes ocupados
        chegada = self._retirar_proximo()
        if chegada is None:
            return None # ninguém esperando
        box.chegada = chegada
        return box, chegada

    def liberar_box(self, numero):
        # Libera o box e já chama automaticamente o próximo veículo para ele.
        box = self.boxes.search(lambda b: b.numero == numero)
        if box is None:
            raise ValueError(f"Box {numero} não existe")
        box.chegada = None
        return self.chamar_proximo()
