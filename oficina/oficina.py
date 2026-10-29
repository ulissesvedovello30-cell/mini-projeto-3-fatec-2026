from datetime import date
from oficina.clientes import CadastroClientes
from oficina.atendimento import Atendimento
from oficina.diagnostico import Diagnostico
from oficina.estoque import Estoque
from oficina.ordem_servico import OrdensServico
from oficina.pagamento import Pagamentos
from oficina.consumo import ControleConsumo


class Oficina:
    # Junta todos os módulos. As regras ficam aqui; as estruturas genéricas ficam em estrutura/.
    def __init__(self, boxes=2):
        self.cadastro = CadastroClientes()
        self.atendimento = Atendimento(boxes)
        self.estoque = Estoque()
        self.ordens = OrdensServico()
        self.pagamentos = Pagamentos()
        self.consumo = ControleConsumo(self.cadastro, self.estoque, self.ordens, self.pagamentos)
        self.diagnostico = Diagnostico.padrao()

    def carregar_dados_exemplo(self):
        c = self.cadastro
        c.cadastrar_cliente("Ana Souza", "111.111.111-11", "(19) 99999-0001")
        c.cadastrar_veiculo("111.111.111-11", "ABC1D23", "Gol", "Volkswagen", 2018)
        c.cadastrar_veiculo("111.111.111-11", "BRA2E19", "Onix", "Chevrolet", 2021)
        c.cadastrar_cliente("Bruno Lima", "222.222.222-22", "(19) 99999-0002")
        c.cadastrar_veiculo("222.222.222-22", "XYZ9K88", "Civic", "Honda", 2015)
        c.cadastrar_cliente("Carla Dias", "333.333.333-33", "(19) 99999-0003")
        c.cadastrar_veiculo("333.333.333-33", "QWE4R56", "Uno", "Fiat", 2012)

        e = self.estoque
        e.cadastrar_produto("Vela de ignição", "VELA-001", 40.0, estoque_minimo=4)
        e.cadastrar_produto("Bobina", "BOB-001", 180.0, estoque_minimo=1)
        e.cadastrar_produto("Correia dentada", "COR-001", 150.0, estoque_minimo=1)
        e.cadastrar_produto("Pastilha dianteira", "PAST-001", 120.0, estoque_minimo=2)
        e.cadastrar_produto("Disco dianteiro", "DISC-001", 260.0, estoque_minimo=1)
        e.cadastrar_produto("Amortecedor", "AMORT-001", 300.0, estoque_minimo=1)
        e.cadastrar_produto("Bandeja", "BAND-001", 220.0, estoque_minimo=1)
        e.cadastrar_produto("Óleo 5W30", "OLEO-001", 55.0, estoque_minimo=5)
        e.comprar_lote("VELA-001", "AutoPeças Rio Claro", 22.0, date(2026, 8, 1), 4)
        e.comprar_lote("VELA-001", "AutoPeças Rio Claro", 25.0, date(2026, 9, 15), 4)
        e.comprar_lote("BOB-001", "Distribuidora Sul", 110.0, date(2026, 8, 10), 2)
        e.comprar_lote("COR-001", "Distribuidora Sul", 90.0, date(2026, 8, 10), 2)
        e.comprar_lote("PAST-001", "Freios Brasil", 70.0, date(2026, 8, 20), 4)
        e.comprar_lote("DISC-001", "Freios Brasil", 160.0, date(2026, 8, 20), 2)
        e.comprar_lote("AMORT-001", "Suspensão Total", 190.0, date(2026, 9, 1), 2)
        e.comprar_lote("BAND-001", "Suspensão Total", 130.0, date(2026, 9, 1), 2)
        e.comprar_lote("OLEO-001", "Lubrificantes SP", 30.0, date(2026, 1, 10), 6, validade=date(2026, 6, 30))  # vencido
        e.comprar_lote("OLEO-001", "Lubrificantes SP", 33.0, date(2026, 9, 1), 8, validade=date(2028, 9, 1))
