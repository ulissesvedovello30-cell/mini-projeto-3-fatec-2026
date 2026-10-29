from dataclasses import dataclass
from estrutura.LinkedList import LinkedList


@dataclass
class Veiculo:
    placa: str
    modelo: str
    marca: str
    ano: int


class Cliente:
    def __init__(self, nome, cpf, telefone):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.veiculos = LinkedList() # COMBINAÇÃO: cada cliente carrega a sua própria lista de veículos


class CadastroClientes:
    def __init__(self):
        self.clientes = LinkedList() # lista de clientes (cada um com uma lista de veículos dentro)

    def cadastrar_cliente(self, nome, cpf, telefone):
        if self.buscar_por_cpf(cpf) is not None:
            raise ValueError(f"Já existe cliente com o CPF {cpf}")
        cliente = Cliente(nome, cpf, telefone)
        self.clientes.add_list(cliente)
        return cliente

    def buscar_por_cpf(self, cpf):
        return self.clientes.search(lambda c: c.cpf == cpf)

    def buscar_por_placa(self, placa):
        # Percorre as DUAS listas: para cada cliente, procura a placa na lista dele.
        # Devolve (cliente, veiculo) ou None.
        for cliente in self.clientes:
            veiculo = cliente.veiculos.search(lambda v: v.placa == placa)
            if veiculo is not None:
                return cliente, veiculo
        return None

    def remover_cliente(self, cpf):
        return self.clientes.remove(lambda c: c.cpf == cpf)

    def cadastrar_veiculo(self, cpf, placa, modelo, marca, ano):
        cliente = self.buscar_por_cpf(cpf)
        if cliente is None:
            raise ValueError(f"Cliente com CPF {cpf} não encontrado")
        if self.buscar_por_placa(placa) is not None:
            raise ValueError(f"A placa {placa} já está cadastrada")
        veiculo = Veiculo(placa, modelo, marca, ano)
        cliente.veiculos.add_list(veiculo) # sem limite de veículos por cliente
        return veiculo

    def remover_veiculo(self, placa):
        achado = self.buscar_por_placa(placa)
        if achado is None:
            return None
        cliente, _ = achado
        return cliente.veiculos.remove(lambda v: v.placa == placa)
