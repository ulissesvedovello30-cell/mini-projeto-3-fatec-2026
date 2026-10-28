from estrutura.No import No
class Queue:
    def __init__(self):
        self.first = None
        self.last = None

    def add (self, content):
     new_content = No(content)
     # É melhor usar um is None, pois ele testa se a variável aponta exatamente
     # para a mesma instância de memória que o singleton None.
     # Enquanto o == none é usado como comparador e nesse caso eu não quero comparar a lista com nada
     if self.first is None:
        self.first = new_content
        self.last = new_content
     else:
        self.last.next = new_content
        self.last = new_content

    def remove(self):
        if self.first is None: # caso não tenha ninguém para remover ele retorna None(nada)
            return None
        else:
            removed = self.first # Aqui o first se torna o elemento que vai ser removido
            self.first = removed.next # Então ele aponta para o proximo elemento
            if self.first is None:
                self.last = None
                return removed
            else:
                return removed
