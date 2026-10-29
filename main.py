from datetime import date, datetime
from oficina.oficina import Oficina
from oficina.estoque import EstoqueInsuficiente
from oficina import simulacao


# ---------- entrada de dados ----------
def ler(texto, obrigatorio=True):
    while True:
        valor = input(f"{texto}: ").strip()
        if valor or not obrigatorio:
            return valor
        print("  (campo obrigatório)")


def ler_int(texto, minimo=0):
    while True:
        try:
            valor = int(ler(texto))
            if valor >= minimo:
                return valor
            print(f"  (precisa ser >= {minimo})")
        except ValueError:
            print("  (digite um número inteiro)")


def ler_float(texto):
    while True:
        try:
            return float(ler(texto).replace(",", "."))
        except ValueError:
            print("  (digite um valor, ex.: 150,50)")


def ler_data(texto, obrigatorio=True):
    while True:
        valor = ler(texto + " (dd/mm/aaaa)", obrigatorio)
        if not valor:
            return None
        try:
            return datetime.strptime(valor, "%d/%m/%Y").date()
        except ValueError:
            print("  (data inválida, use dd/mm/aaaa)")


def sim_nao(texto):
    return ler(texto + " (s/n)").lower().startswith("s")


def dinheiro(valor):
    return f"R$ {valor:.2f}".replace(".", ",")


def submenu(oficina, titulo, opcoes):
    # opcoes: lista de (texto, função). Repete até o usuário voltar (0).
    while True:
        print(f"\n--- {titulo} ---")
        for numero, (texto, _) in enumerate(opcoes, start=1):
            print(f"{numero}  {texto}")
        print("0  Voltar")
        escolha = input("Opção: ").strip()
        if escolha == "0":
            return
        if not escolha.isdigit() or not 1 <= int(escolha) <= len(opcoes):
            print("Opção inválida.")
            continue
        try:
            opcoes[int(escolha) - 1][1](oficina)
        except (ValueError, EstoqueInsuficiente) as erro:
            print(f"Erro: {erro}")


# ---------- clientes e veículos ----------
def cadastrar_cliente(o):
    cliente = o.cadastro.cadastrar_cliente(ler("Nome do cliente"), ler("CPF"), ler("Telefone"))
    print(f"Cliente {cliente.nome} cadastrado.")
    if sim_nao("Cadastrar um veículo dele agora?"):
        cadastrar_veiculo(o, cliente.cpf)


def cadastrar_veiculo(o, cpf=None):
    cpf = cpf or ler("CPF do dono")
    o.cadastro.cadastrar_veiculo(cpf, ler("Placa").upper(), ler("Modelo"), ler("Marca"), ler_int("Ano", 1900))
    print("Veículo cadastrado.")


def mostrar_cliente(cliente):
    print(f"{cliente.nome} | CPF {cliente.cpf} | Tel {cliente.telefone}")
    if len(cliente.veiculos) == 0:
        print("    (sem veículos)")
    for v in cliente.veiculos:
        print(f"    {v.placa} - {v.marca} {v.modelo} {v.ano}")


def buscar_cliente(o):
    chave = ler("CPF ou placa")
    cliente = o.cadastro.buscar_por_cpf(chave)
    if cliente is not None:
        mostrar_cliente(cliente)
        return
    achado = o.cadastro.buscar_por_placa(chave.upper())
    if achado is None:
        print("Não encontrado.")
    else:
        print(f"Veículo {achado[1].placa} - {achado[1].marca} {achado[1].modelo} {achado[1].ano}")
        mostrar_cliente(achado[0])


def listar_clientes(o):
    if len(o.cadastro.clientes) == 0:
        print("Nenhum cliente cadastrado.")
    for cliente in o.cadastro.clientes:
        mostrar_cliente(cliente)


def remover_cliente(o):
    print("Cliente removido." if o.cadastro.remover_cliente(ler("CPF")) else "Não encontrado.")


def remover_veiculo(o):
    print("Veículo removido." if o.cadastro.remover_veiculo(ler("Placa").upper()) else "Não encontrado.")


def menu_clientes(o):
    submenu(o, "CLIENTES E VEÍCULOS", [
        ("Cadastrar cliente", cadastrar_cliente),
        ("Cadastrar veículo para um cliente", cadastrar_veiculo),
        ("Buscar por CPF ou placa", buscar_cliente),
        ("Listar todos", listar_clientes),
        ("Remover cliente", remover_cliente),
        ("Remover veículo", remover_veiculo)])


# ---------- atendimento ----------
def chegada(o):
    placa = ler("Placa").upper()
    achado = o.cadastro.buscar_por_placa(placa)
    if achado is not None:
        nome = achado[0].nome
        print(f"Veículo cadastrado: {achado[1].marca} {achado[1].modelo} de {nome}")
    else:
        print("Placa não cadastrada.")
        nome = ler("Nome do cliente")
    queixa = ler("Queixa / problema do carro")
    guincho = sim_nao("Veio de guincho?")
    o.atendimento.chegar(placa, nome, queixa, guincho)
    print(f"{placa} entrou na fila {'de GUINCHO (prioridade)' if guincho else 'normal'}.")


def mostrar_chamada(resultado):
    if resultado is None:
        print("Nenhum box livre ou ninguém esperando.")
    else:
        box, c = resultado
        print(f"Box {box.numero} <- {c.placa} ({c.cliente}): {c.queixa}")


def chamar_proximo(o):
    mostrar_chamada(o.atendimento.chamar_proximo())


def liberar_box(o):
    mostrar_chamada(o.atendimento.liberar_box(ler_int("Número do box a liberar", 1)))


def ver_filas(o):
    a = o.atendimento
    print(f"Guincho ({len(a.fila_guincho)}):")
    for c in a.fila_guincho:
        print(f"    {c.placa} - {c.cliente} - {c.queixa} ({c.data_hora:%d/%m %H:%M})")
    print(f"Normal ({len(a.fila_normal)}):")
    for c in a.fila_normal:
        print(f"    {c.placa} - {c.cliente} - {c.queixa} ({c.data_hora:%d/%m %H:%M})")
    for box in a.boxes:
        ocupante = box.chegada.placa if box.chegada else "livre"
        print(f"Box {box.numero}: {ocupante}")
    proximo = a.proximo()
    print(f"Próximo da vez: {proximo.placa if proximo else '-'}")


def menu_atendimento(o):
    submenu(o, "ATENDIMENTO", [
        ("Chegada de veículo", chegada),
        ("Chamar próximo para um box livre", chamar_proximo),
        ("Liberar box (e chamar o próximo)", liberar_box),
        ("Ver filas e boxes", ver_filas)])


# ---------- diagnóstico ----------
def ver_arvore(o):
    print(o.diagnostico.exibir())


def marcar_defeito(o):
    ver_arvore(o)
    c = o.diagnostico.marcar_defeito(ler("Nome do componente com defeito"))
    print(f"{c.nome} marcado como '{c.estado}'.")


def pecas_defeito(o):
    if len(o.diagnostico.pecas_com_defeito()) == 0:
        print("Nenhuma peça com defeito.")
    for p in o.diagnostico.pecas_com_defeito():
        print(f"{p.nome} [{p.codigo}]")


def menu_diagnostico(o):
    submenu(o, "DIAGNÓSTICO", [
        ("Ver árvore de componentes", ver_arvore),
        ("Marcar componente com defeito", marcar_defeito),
        ("Listar peças com defeito", pecas_defeito)])


# ---------- estoque ----------
def listar_estoque(o):
    if len(o.estoque.produtos) == 0:
        print("Estoque vazio.")
    for p in o.estoque.produtos:
        print(f"{p.codigo} | {p.nome} | venda {dinheiro(p.preco_venda)} | "
              f"total {p.quantidade_total()} (mín. {p.estoque_minimo})")
        for l in p.lotes:
            validade = f"{l.validade:%d/%m/%Y}" if l.validade else "sem validade"
            print(f"      lote {l.numero}: {l.quantidade} un. | compra {dinheiro(l.preco_compra)} "
                  f"em {l.data_compra:%d/%m/%Y} | {l.fornecedor} | {validade}")
    for p in o.estoque.alertas():
        print(f"ALERTA: {p.nome} abaixo do mínimo ({p.quantidade_total()} < {p.estoque_minimo})")


def cadastrar_produto(o):
    o.estoque.cadastrar_produto(ler("Nome do produto"), ler("Código"), ler_float("Preço de venda"),
                                ler_int("Estoque mínimo"))
    print("Produto cadastrado.")


def comprar_lote(o):
    codigo = ler("Código do produto")
    o.estoque.comprar_lote(codigo, ler("Fornecedor"), ler_float("Preço de compra (unidade)"),
                           ler_data("Data da compra", False) or date.today(), ler_int("Quantidade", 1),
                           ler_data("Validade, Enter se não vence", False))
    print("Lote registrado.")


def ajustar_estoque(o):
    o.estoque.ajustar_quantidade(ler("Código do produto"), ler_int("Número do lote", 1),
                                 ler_int("Nova quantidade (0 remove o lote)"))
    print("Quantidade ajustada.")


def descartar_vencidos(o):
    perdas = o.estoque.descartar_vencidos(date.today())
    if len(perdas) == 0:
        print("Nenhum lote vencido.")
    for perda in perdas:
        print(f"Perda registrada: lote {perda.lote.numero} de {perda.codigo} ({perda.lote.quantidade} un.)")


def ver_perdas(o):
    if len(o.estoque.perdas) == 0:
        print("Nenhuma perda registrada.")
    for perda in o.estoque.perdas:
        valor = perda.lote.quantidade * perda.lote.preco_compra
        print(f"{perda.codigo} lote {perda.lote.numero}: {perda.lote.quantidade} un. "
              f"({dinheiro(valor)}) em {perda.data:%d/%m/%Y}")


def menu_estoque(o):
    submenu(o, "ESTOQUE", [
        ("Listar estoque e alertas", listar_estoque),
        ("Cadastrar produto", cadastrar_produto),
        ("Registrar compra de lote", comprar_lote),
        ("Ajuste de inventário", ajustar_estoque),
        ("Descartar lotes vencidos", descartar_vencidos),
        ("Ver perdas", ver_perdas)])


# ---------- ordens de serviço ----------
def pedir_os(o):
    os_ = o.ordens.buscar(ler_int("Número da OS", 1))
    if os_ is None:
        raise ValueError("OS aberta não encontrada")
    return os_


def abrir_os(o):
    placa = ler("Placa").upper()
    achado = o.cadastro.buscar_por_placa(placa)
    cliente = achado[0].nome if achado else ler("Nome do cliente")
    os_ = o.ordens.abrir(placa, cliente, ler("Mecânico responsável"))
    print(f"OS {os_.numero} aberta para {placa} ({cliente}).")


def mostrar_os(os_):
    print(f"OS {os_.numero} | {os_.placa} | {os_.cliente} | mecânico {os_.mecanico} | "
          f"aberta {os_.abertura:%d/%m/%Y %H:%M} | remontagem: {'concluída' if os_.remontagem_concluida else 'pendente'}")
    for p in os_.pecas:
        print(f"    peça {p.codigo} {p.nome}: {p.quantidade} x {dinheiro(p.preco_unitario)} = {dinheiro(p.valor())}")
    for s in os_.servicos:
        print(f"    serviço {s.descricao}: {dinheiro(s.valor)}")
    print(f"    Peças {dinheiro(os_.valor_pecas())} + mão de obra {dinheiro(os_.valor_mao_de_obra())} "
          f"= TOTAL {dinheiro(os_.total())}")


def listar_os(o):
    if len(o.ordens.abertas) == 0:
        print("Nenhuma OS aberta.")
    for os_ in o.ordens.abertas:
        mostrar_os(os_)


def adicionar_peca(o):
    os_ = pedir_os(o)
    pecas = o.diagnostico.pecas_com_defeito()
    if len(pecas) > 0:
        print("Peças com defeito no diagnóstico: " + ", ".join(f"{p.nome} [{p.codigo}]" for p in pecas))
    codigo = ler("Código da peça/fluido")
    produto = o.estoque.buscar(codigo)
    if produto is None:
        raise ValueError(f"Produto {codigo} não existe no estoque")
    quantidade = ler_int("Quantidade", 1)
    if quantidade > produto.quantidade_total():
        raise EstoqueInsuficiente(f"{produto.nome}: só há {produto.quantidade_total()} em estoque")
    os_.adicionar_peca(codigo, produto.nome, quantidade, produto.preco_venda)
    print(f"{quantidade}x {produto.nome} adicionado(s) à OS (baixa no estoque ocorre no fechamento).")


def adicionar_servico(o):
    os_ = pedir_os(o)
    os_.adicionar_servico(ler("Serviço (ex.: troca de pastilhas)"), ler_float("Valor da mão de obra"))
    print("Serviço adicionado.")


def remover_peca_os(o):
    os_ = pedir_os(o)
    print("Peça removida." if os_.remover_peca(ler("Código da peça")) else "Peça não está na OS.")


def remover_servico_os(o):
    os_ = pedir_os(o)
    print("Serviço removido." if os_.remover_servico(ler("Descrição do serviço")) else "Serviço não está na OS.")


def concluir_remontagem(o):
    pedir_os(o).concluir_remontagem()
    print("Remontagem concluída. A OS já pode ser fechada.")


def fechar_os(o):
    os_ = pedir_os(o)
    mostrar_os(os_)
    forma = ler("Forma de pagamento (PIX, CARTAO ou DINHEIRO)").upper()
    parcelas = ler_int("Número de parcelas", 1) if forma == "CARTAO" else 1
    pagador = ler("Nome de quem pagou, Enter = " + os_.cliente, False) or None
    pag = o.consumo.fechar_os(os_.numero, forma, parcelas, pagador)
    print(f"OS {pag.numero_os} fechada. {pag.pagador} pagou {dinheiro(pag.valor_total)} "
          f"({pag.forma}{f' em {pag.parcelas}x' if pag.forma == 'CARTAO' else ''}). Estoque atualizado.")
    for produto in o.estoque.alertas():
        print(f"ALERTA: {produto.nome} abaixo do mínimo ({produto.quantidade_total()} < {produto.estoque_minimo})")


def menu_os(o):
    submenu(o, "ORDENS DE SERVIÇO", [
        ("Abrir OS", abrir_os),
        ("Listar OS abertas", listar_os),
        ("Adicionar peça/fluido", adicionar_peca),
        ("Adicionar serviço de mão de obra", adicionar_servico),
        ("Remover peça", remover_peca_os),
        ("Remover serviço", remover_servico_os),
        ("Concluir remontagem", concluir_remontagem),
        ("Fechar OS e pagar", fechar_os)])


# ---------- pagamentos e consumo ----------
def listar_pagamentos(o):
    if len(o.pagamentos.registros) == 0:
        print("Nenhum pagamento registrado.")
    for p in o.pagamentos.registros:
        print(f"OS {p.numero_os} | {p.pagador} | {p.forma} {p.parcelas}x | peças {dinheiro(p.valor_pecas)} + "
              f"mão de obra {dinheiro(p.valor_mao_de_obra)} = {dinheiro(p.valor_total)} | {p.data_hora:%d/%m/%Y %H:%M}")


def mostrar_consumo(registros):
    if len(registros) == 0:
        print("Nenhum consumo registrado.")
    for r in registros:
        print(f"{r.cliente} / {r.placa}: {r.quantidade}x {r.nome_peca} = {dinheiro(r.valor)} (OS {r.numero_os})")


def consumo_cliente(o):
    mostrar_consumo(o.consumo.consumo_por_cliente(ler("CPF do cliente")))


def consumo_placa(o):
    mostrar_consumo(o.consumo.consumo_por_placa(ler("Placa").upper()))


def menu_pagamentos(o):
    submenu(o, "PAGAMENTOS E CONSUMO", [
        ("Listar pagamentos", listar_pagamentos),
        ("Peças consumidas por cliente (CPF)", consumo_cliente),
        ("Peças consumidas por veículo (placa)", consumo_placa)])


# ---------- principal ----------
def main():
    oficina = Oficina(boxes=ler_int("Quantos boxes (elevadores) a oficina tem?", 1))
    if sim_nao("Carregar dados de exemplo (clientes e estoque prontos)?"):
        oficina.carregar_dados_exemplo()
        print("Dados de exemplo carregados.")
    principal = [
        ("Clientes e veículos", menu_clientes),
        ("Atendimento (fila e boxes)", menu_atendimento),
        ("Diagnóstico (árvore de componentes)", menu_diagnostico),
        ("Estoque", menu_estoque),
        ("Ordens de serviço", menu_os),
        ("Pagamentos e consumo", menu_pagamentos),
        ("Rodar a simulação automática (demonstração)", lambda o: simulacao.rodar())]
    while True:
        print("\n===== OFICINA MECÂNICA =====")
        for numero, (texto, _) in enumerate(principal, start=1):
            print(f"{numero}  {texto}")
        print("0  Sair")
        escolha = input("Opção: ").strip()
        if escolha == "0":
            break
        if escolha.isdigit() and 1 <= int(escolha) <= len(principal):
            principal[int(escolha) - 1][1](oficina)
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
