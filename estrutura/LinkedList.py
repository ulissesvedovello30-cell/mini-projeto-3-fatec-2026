from estrutura.No import No

class LinkedList:
    def __init__(self):
        self.first = None
        self.size = 0

    def add_list(self, content):
        new_node = No(content)
        if self.first is None:
            self.first = new_node # Se a lista for vazia o novo nó vira first
        else:
            actual = self.first
            while actual.next is not None: # anda até parar no último nó (o que não tem próximo)
                actual = actual.next
            actual.next = new_node # o último nó antigo passa a apontar para o novo
        self.size += 1

    def search(self, criterion):
        # criterion é uma função que recebe o content e diz True/False (ex.: lambda c: c.cpf == "123")
        actual = self.first
        while actual is not None: # anda nó por nó, do primeiro ao último
            if criterion(actual.content):
                return actual.content # achou: devolve o conteúdo
            actual = actual.next
        return None # chegou ao fim sem achar

    def remove(self, criterion):
        previous = None # guarda o nó de trás, pois ele precisa "pular" o nó removido
        actual = self.first
        while actual is not None:
            if criterion(actual.content):
                if previous is None:
                    self.first = actual.next # removendo o primeiro: first passa para o segundo
                else:
                    previous.next = actual.next # o anterior pula o nó removido
                self.size -= 1
                return actual.content
            previous = actual
            actual = actual.next
        return None # não achou ninguém para remover

    def __iter__(self): # permite usar "for item in lista"
        actual = self.first
        while actual is not None:
            yield actual.content
            actual = actual.next

    def __len__(self):
        return self.size
