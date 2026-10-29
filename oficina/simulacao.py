import os
import sys

# Permite rodar este arquivo direto (botão play): coloca a raiz do projeto no caminho de busca
# e tira a pasta oficina/ dele, senão "oficina" apontaria para oficina/oficina.py.
if __name__ == "__main__":
    pasta = os.path.dirname(os.path.abspath(__file__))
    sys.path = [p for p in sys.path if os.path.abspath(p or ".") != pasta]
    sys.path.insert(0, os.path.dirname(pasta))

from datetime import date, datetime
from oficina.oficina import Oficina


def titulo(texto):
    print(f"\n=== {texto} ===")


def adicionar_peca_na_os(oficina, os_, codigo, quantidade):
    produto = oficina.estoque.buscar(codigo)
    os_.adicionar_peca(codigo, produto.nome, quantidade, produto.preco_venda)


def rodar():
    o = Oficina(boxes=2)
    o.carregar_dados_exemplo()

    titulo("0. Descarte de lotes vencidos")
    for perda in o.estoque.descartar_vencidos(date(2026, 10, 28)):
        print(f"Perda: {perda.codigo} lote {perda.lote.numero} ({perda.lote.quantidade} un.) venceu em {perda.lote.validade}")

    titulo("1. Chegada dos veículos")
    chegadas = [
        ("ABC1D23", "Ana Souza", "barulho no freio", False),
        ("XYZ9K88", "Bruno Lima", "motor falhando", False),
        ("QWE4R56", "Carla Dias", "carro quebrou na estrada", True),  # guincho
        ("BRA2E19", "Ana Souza", "suspensão batendo", False),
    ]
    for placa, nome, queixa, guincho in chegadas:
        o.atendimento.chegar(placa, nome, queixa, guincho)
        print(f"Chegou {placa} ({nome}) - {queixa}" + (" [GUINCHO]" if guincho else ""))

    titulo("2. Chamada do próximo e abertura da OS")
    box, chegada = o.atendimento.chamar_proximo()
    print(f"Box {box.numero} recebeu {chegada.placa} (guincho tem prioridade)")
    box2, chegada2 = o.atendimento.chamar_proximo()
    print(f"Box {box2.numero} recebeu {chegada2.placa}")
    os_ = o.ordens.abrir(chegada2.placa, chegada2.cliente, "Seu Zé")
    print(f"OS {os_.numero} aberta para {os_.placa} - mecânico {os_.mecanico}")
    print("Box 1 liberado ->", end=" ")
    proximo = o.atendimento.liberar_box(box.numero)
    print(f"próximo: {proximo[1].placa}")

    titulo("3. Diagnóstico na árvore (pré-ordem)")
    o.diagnostico.marcar_defeito("Pastilha dianteira")
    o.diagnostico.marcar_defeito("Vela")
    print(o.diagnostico.exibir())

    titulo("4. Peças e serviços na OS (baixa pelo lote mais antigo no fechamento)")
    for peca in o.diagnostico.pecas_com_defeito():
        adicionar_peca_na_os(o, os_, peca.codigo, 2 if peca.codigo == "PAST-001" else 4)
        print(f"+ peça {peca.nome} ({peca.codigo})")
    os_.adicionar_servico("Troca de pastilhas", 150.0)
    os_.adicionar_servico("Alinhamento", 90.0)
    os_.adicionar_servico("Balanceamento (cliente não autorizou)", 60.0)
    os_.remover_servico("Balanceamento (cliente não autorizou)")
    print(f"Total parcial: R$ {os_.total():.2f}")
    try:
        o.consumo.fechar_os(os_.numero, "PIX")
    except ValueError as erro:
        print(f"Tentativa de fechar antes da remontagem: {erro}")
    os_.concluir_remontagem()

    titulo("5. Fechamento e pagamento")
    antes = o.estoque.quantidade_total("VELA-001")
    pag = o.consumo.fechar_os(os_.numero, "CARTAO", parcelas=3, data_hora=datetime(2026, 10, 28, 17, 0))
    print(f"Pago por {pag.pagador}: peças R$ {pag.valor_pecas:.2f} + mão de obra R$ {pag.valor_mao_de_obra:.2f} "
          f"= R$ {pag.valor_total:.2f} em {pag.parcelas}x no {pag.forma}")
    print(f"Estoque de velas: {antes} -> {o.estoque.quantidade_total('VELA-001')}")
    for produto in o.estoque.alertas():
        print(f"ALERTA: {produto.nome} abaixo do mínimo ({produto.quantidade_total()} < {produto.estoque_minimo})")

    titulo("Consumo por veículo")
    for r in o.consumo.consumo_por_placa(os_.placa):
        print(f"{r.cliente} / {r.placa}: {r.quantidade}x {r.nome_peca} = R$ {r.valor:.2f} (OS {r.numero_os})")
    return o


if __name__ == "__main__":
    rodar()
