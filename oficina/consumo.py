from dataclasses import dataclass
from datetime import datetime
from estrutura.LinkedList import LinkedList


@dataclass
class RegistroConsumo:
    cpf: str
    cliente: str
    placa: str
    codigo_peca: str
    nome_peca: str
    quantidade: int
    valor: float
    numero_os: int
    data_hora: datetime


class ControleConsumo:
    # Une as outras partes no fechamento da OS: baixa o estoque, registra o pagamento
    # e anota qual cliente/veículo consumiu quais peças.
    def __init__(self, cadastro, estoque, ordens, pagamentos):
        self.cadastro = cadastro
        self.estoque = estoque
        self.ordens = ordens
        self.pagamentos = pagamentos
        self.registros = LinkedList()

    def fechar_os(self, numero, forma, parcelas=1, pagador=None, data_hora=None):
        os_ = self.ordens.buscar(numero)
        if os_ is None:
            raise ValueError(f"OS {numero} não encontrada entre as abertas")
        if not os_.pode_fechar():
            raise ValueError("A OS só pode ser fechada depois da remontagem concluída")

        # 1) confere TODO o estoque antes de baixar qualquer coisa (nada de baixa pela metade)
        for item in os_.pecas:
            disponivel = self.estoque.quantidade_total(item.codigo)
            if disponivel < item.quantidade:
                raise ValueError(f"Estoque insuficiente de {item.nome}: "
                                 f"precisa {item.quantidade}, tem {disponivel}")

        # 2) registra o pagamento primeiro (se a forma for inválida, o estoque não é tocado)
        pagamento = self.pagamentos.registrar(pagador or os_.cliente, os_, forma, parcelas, data_hora)

        # 3) baixa o estoque (lote mais antigo primeiro) e anota o consumo
        achado = self.cadastro.buscar_por_placa(os_.placa)
        cpf = achado[0].cpf if achado else ""
        for item in os_.pecas:
            self.estoque.baixar(item.codigo, item.quantidade)
            self.registros.add_list(RegistroConsumo(
                cpf, os_.cliente, os_.placa, item.codigo, item.nome,
                item.quantidade, item.valor(), os_.numero, data_hora or datetime.now()))

        self.ordens.marcar_fechada(numero)
        return pagamento

    def consumo_por_cliente(self, cpf):
        resultado = LinkedList()
        for r in self.registros:
            if r.cpf == cpf:
                resultado.add_list(r)
        return resultado

    def consumo_por_placa(self, placa):
        resultado = LinkedList()
        for r in self.registros:
            if r.placa == placa:
                resultado.add_list(r)
        return resultado
