import unittest  # Biblioteca para testes unitários
from estrutura.Queue import Queue


# Cada método que começa com "test" é um teste: o unittest acha e roda sozinho
class QueueTest(unittest.TestCase):
    def test_empty_queue(self):  # teste para caso de fila vazia
        fila = Queue()  # 1) cria uma fila vazia
        fila.add("Ana")  # 2) A Ana é a primeira pessoa que entra
        # 3) com uma pessoa só, ela é o primeiro E o último da fila
        self.assertEqual(fila.first.content, "Ana")
        self.assertEqual(fila.last.content, "Ana")
        # O assertEqual confere se dois valores são iguais. Se não forem, o teste falha e mostra o resultado esperado

    def test_queue_with_people(self):  # teste para fila com pessoas
        fila = Queue()
        fila.add("Ana")  # 2) Ana entra primeiro...
        fila.add("Bia")  # e a Bia entra depois dela
        # a Ana continua no começo e a Bia ficou no fim
        self.assertEqual(fila.first.content, "Ana")
        # o "next" da Ana tem que apontar para Bia (é isso que liga a fila)
        self.assertEqual(fila.first.next.content, "Bia")
        self.assertEqual(fila.last.content, "Bia")

    def test_remove_empty_queue(self):  # teste do remove com a fila vazia
        fila = Queue()  # 1) cria uma fila vazia
        resultado = fila.remove()  # 2) tenta tirar alguém e guarda o que voltou
        # 3) não tinha ninguém, então o remove tem que devolver None (nada)
        self.assertIsNone(resultado)

    def test_remove_queue_with_people(self):  # teste do remove com gente na fila
        fila = Queue()  # 1) monta a fila: Ana -> Bia
        fila.add("Ana")
        fila.add("Bia")
        removido = fila.remove()  # 2) a Ana é atendida e sai
        # 3) o remove devolve quem saiu (a Ana)...
        self.assertEqual(removido.content, "Ana")
        # ...e a Bia passa a ser a primeira da fila
        self.assertEqual(fila.first.content, "Bia")
        # o last não muda: a Bia continua sendo a última
        self.assertEqual(fila.last.content, "Bia")

    def test_remove_last_person(self):  # teste do remove que esvazia a fila
        fila = Queue()  # 1) fila com uma pessoa só
        fila.add("Ana")
        fila.remove()  # 2) a única pessoa sai
        # 3) fila vazia: o first E o last têm que ser None
        # (esse teste protege o bug do last "fantasma")
        self.assertIsNone(fila.first)
        self.assertIsNone(fila.last)


# Permite rodar o arquivo direto (python test_queue.py)
if __name__ == "__main__":
    unittest.main()
