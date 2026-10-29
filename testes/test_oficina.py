import unittest
from datetime import date
from estrutura.LinkedList import LinkedList
from estrutura.Tree import Tree
from oficina.clientes import CadastroClientes
from oficina.atendimento import Atendimento
from oficina.diagnostico import Diagnostico
from oficina.estoque import Estoque, EstoqueInsuficiente
from oficina.oficina import Oficina


class LinkedListTest(unittest.TestCase):
    def lista(self):
        lista = LinkedList()
        for nome in ("Ana", "Bia", "Caio"):
            lista.add_list(nome)
        return lista

    def test_search_acha_e_nao_acha(self):
        lista = self.lista()
        self.assertEqual(lista.search(lambda c: c == "Bia"), "Bia")
        self.assertIsNone(lista.search(lambda c: c == "Zeca"))

    def test_remove_primeiro_meio_ultimo(self):
        lista = self.lista()
        lista.remove(lambda c: c == "Bia")  # meio
        self.assertEqual(list(lista), ["Ana", "Caio"])
        lista.remove(lambda c: c == "Ana")  # primeiro
        self.assertEqual(list(lista), ["Caio"])
        lista.remove(lambda c: c == "Caio")  # último / único
        self.assertEqual(len(lista), 0)
        self.assertIsNone(lista.first)

    def test_remove_inexistente(self):
        self.assertIsNone(self.lista().remove(lambda c: c == "Zeca"))


class TreeTest(unittest.TestCase):
    def test_preordem_e_profundidade(self):
        arvore = Tree("A")
        b = arvore.root.add_child("B")
        b.add_child("C")
        arvore.root.add_child("D")
        resultado = [(n.content, d) for n, d in arvore.preorder()]
        self.assertEqual(resultado, [("A", 0), ("B", 1), ("C", 2), ("D", 1)])


class ClientesTest(unittest.TestCase):
    def setUp(self):
        self.c = CadastroClientes()
        self.c.cadastrar_cliente("Ana", "1", "99")
        self.c.cadastrar_cliente("Bia", "2", "98")
        self.c.cadastrar_veiculo("1", "AAA1111", "Gol", "VW", 2010)
        self.c.cadastrar_veiculo("2", "BBB2222", "Uno", "Fiat", 2012)
        self.c.cadastrar_veiculo("2", "CCC3333", "Palio", "Fiat", 2014)

    def test_buscar_por_cpf_e_placa(self):
        self.assertEqual(self.c.buscar_por_cpf("2").nome, "Bia")
        cliente, veiculo = self.c.buscar_por_placa("CCC3333")
        self.assertEqual((cliente.nome, veiculo.modelo), ("Bia", "Palio"))
        self.assertIsNone(self.c.buscar_por_placa("ZZZ0000"))

    def test_cpf_e_placa_duplicados(self):
        with self.assertRaises(ValueError):
            self.c.cadastrar_cliente("Outro", "1", "0")
        with self.assertRaises(ValueError):
            self.c.cadastrar_veiculo("1", "BBB2222", "X", "Y", 2000)

    def test_remover(self):
        self.c.remover_veiculo("BBB2222")
        self.assertIsNone(self.c.buscar_por_placa("BBB2222"))
        self.assertIsNotNone(self.c.buscar_por_placa("CCC3333"))
        self.c.remover_cliente("1")
        self.assertIsNone(self.c.buscar_por_cpf("1"))


class AtendimentoTest(unittest.TestCase):
    def test_guincho_tem_prioridade_e_respeita_ordem(self):
        a = Atendimento(quantidade_boxes=1)
        a.chegar("N1", "x", "q")
        a.chegar("G1", "x", "q", guincho=True)
        a.chegar("N2", "x", "q")
        a.chegar("G2", "x", "q", guincho=True)
        ordem = []
        box, chegada = a.chamar_proximo()
        ordem.append(chegada.placa)
        for _ in range(3):
            ordem.append(a.liberar_box(box.numero)[1].placa)
        self.assertEqual(ordem, ["G1", "G2", "N1", "N2"])

    def test_sem_box_livre_ou_sem_fila(self):
        a = Atendimento(quantidade_boxes=1)
        self.assertIsNone(a.chamar_proximo())  # fila vazia
        a.chegar("N1", "x", "q")
        a.chegar("N2", "x", "q")
        a.chamar_proximo()
        self.assertIsNone(a.chamar_proximo())  # box ocupado


class DiagnosticoTest(unittest.TestCase):
    def test_exibir_indentado_e_defeito(self):
        d = Diagnostico.padrao()
        d.marcar_defeito("Vela")
        linhas = d.exibir().split("\n")
        self.assertEqual(linhas[0], "- Veículo")
        self.assertEqual(linhas[1], "    - Motor")
        self.assertIn("            - Vela [VELA-001] (Com defeito)", linhas)
        self.assertEqual([p.nome for p in d.pecas_com_defeito()], ["Vela"])

    def test_componente_inexistente(self):
        with self.assertRaises(ValueError):
            Diagnostico.padrao().marcar_defeito("Turbina")


class EstoqueTest(unittest.TestCase):
    def setUp(self):
        self.e = Estoque()
        self.e.cadastrar_produto("Vela", "V1", 40.0, estoque_minimo=5)
        self.e.comprar_lote("V1", "F", 20.0, date(2026, 1, 1), 3)
        self.e.comprar_lote("V1", "F", 25.0, date(2026, 2, 1), 4)

    def test_consome_lote_mais_antigo_primeiro(self):
        usados = list(self.e.baixar("V1", 5))
        self.assertEqual(usados, [(1, 3, 20.0), (2, 2, 25.0)])
        self.assertEqual(self.e.quantidade_total("V1"), 2)
        self.assertEqual(self.e.buscar("V1").lotes.peek().numero, 2)

    def test_estoque_insuficiente_nao_baixa_nada(self):
        with self.assertRaises(EstoqueInsuficiente):
            self.e.baixar("V1", 8)
        self.assertEqual(self.e.quantidade_total("V1"), 7)

    def test_descartar_vencidos(self):
        self.e.cadastrar_produto("Óleo", "O1", 50.0)
        self.e.comprar_lote("O1", "F", 10.0, date(2026, 1, 1), 5, validade=date(2026, 6, 1))
        self.e.comprar_lote("O1", "F", 12.0, date(2026, 5, 1), 5, validade=date(2027, 1, 1))
        perdas = self.e.descartar_vencidos(date(2026, 10, 28))
        self.assertEqual(len(perdas), 1)
        self.assertEqual(len(self.e.perdas), 1)
        self.assertEqual(self.e.quantidade_total("O1"), 5)

    def test_ajuste_e_alerta(self):
        self.assertEqual(len(self.e.alertas()), 0)  # 7 >= 5
        self.e.ajustar_quantidade("V1", 2, 1)
        self.assertEqual(self.e.quantidade_total("V1"), 4)
        self.assertEqual(len(self.e.alertas()), 1)  # 4 < 5
        self.e.ajustar_quantidade("V1", 1, 0)  # zerar remove o lote
        self.assertEqual(len(self.e.buscar("V1").lotes), 1)


class FechamentoTest(unittest.TestCase):
    def setUp(self):
        self.o = Oficina()
        self.o.carregar_dados_exemplo()
        self.os = self.o.ordens.abrir("ABC1D23", "Ana Souza", "Zé")
        self.os.adicionar_peca("PAST-001", "Pastilha", 2, 120.0)
        self.os.adicionar_servico("Troca de pastilhas", 150.0)

    def test_nao_fecha_sem_remontagem(self):
        with self.assertRaises(ValueError):
            self.o.consumo.fechar_os(self.os.numero, "PIX")
        self.assertEqual(self.o.estoque.quantidade_total("PAST-001"), 4)

    def test_fecha_baixa_estoque_registra_pagamento_e_consumo(self):
        self.os.concluir_remontagem()
        pag = self.o.consumo.fechar_os(self.os.numero, "cartao", parcelas=2)
        self.assertEqual((pag.valor_pecas, pag.valor_mao_de_obra, pag.valor_total), (240.0, 150.0, 390.0))
        self.assertEqual(pag.parcelas, 2)
        self.assertEqual(self.o.estoque.quantidade_total("PAST-001"), 2)
        registros = list(self.o.consumo.consumo_por_cliente("111.111.111-11"))
        self.assertEqual(len(registros), 1)
        self.assertIsNone(self.o.ordens.buscar(self.os.numero))  # saiu das abertas
        with self.assertRaises(ValueError):
            self.os.adicionar_servico("Extra", 10.0)  # OS fechada não aceita mudanças

    def test_forma_invalida_nao_mexe_no_estoque(self):
        self.os.concluir_remontagem()
        with self.assertRaises(ValueError):
            self.o.consumo.fechar_os(self.os.numero, "cheque")
        self.assertEqual(self.o.estoque.quantidade_total("PAST-001"), 4)

    def test_remover_peca_e_servico_antes_de_fechar(self):
        self.os.remover_peca("PAST-001")
        self.os.remover_servico("Troca de pastilhas")
        self.assertEqual(self.os.total(), 0)

    def test_pix_ignora_parcelas(self):
        self.os.concluir_remontagem()
        pag = self.o.consumo.fechar_os(self.os.numero, "PIX", parcelas=5)
        self.assertEqual(pag.parcelas, 1)


if __name__ == "__main__":
    unittest.main()
