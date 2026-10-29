from dataclasses import dataclass
from datetime import datetime
from estrutura.LinkedList import LinkedList

FORMAS = ("PIX", "CARTAO", "DINHEIRO")


@dataclass
class Pagamento:
    pagador: str
    numero_os: int
    forma: str
    parcelas: int
    valor_pecas: float
    valor_mao_de_obra: float
    valor_total: float
    data_hora: datetime


class Pagamentos:
    def __init__(self):
        self.registros = LinkedList()

    def registrar(self, pagador, os_, forma, parcelas=1, data_hora=None):
        forma = forma.upper()
        if forma not in FORMAS:
            raise ValueError(f"Forma de pagamento inválida: {forma}")
        if forma == "CARTAO":
            if parcelas < 1:
                raise ValueError("Cartão precisa de pelo menos 1 parcela")
        else:
            parcelas = 1  # parcelamento só existe no cartão
        pagamento = Pagamento(pagador, os_.numero, forma, parcelas,
                              os_.valor_pecas(), os_.valor_mao_de_obra(), os_.total(),
                              data_hora or datetime.now())
        self.registros.add_list(pagamento)
        return pagamento

    def buscar_por_os(self, numero_os):
        return self.registros.search(lambda p: p.numero_os == numero_os)
