from estrutura.No import No

class LinkedList:
    def __init__(self):
        self.first = None

    def add_list(self, content):
        new_node = No(content)
        if self.first is None:
            self.first = new_node # Se a lista for vazia o novo nó vira first
        else:
            actual = self.first
            while actual.next is not None: # anda até parar no último nó (o que não tem próximo)
                actual = actual.next
            actual.next = new_node # o último nó antigo passa a apontar para o novo

