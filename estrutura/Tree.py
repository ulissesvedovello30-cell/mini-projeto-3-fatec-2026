from estrutura.LinkedList import LinkedList

class TreeNode:
    # Nó de árvore GENÉRICA: não é binária, cada nó tem de zero a N filhos.
    def __init__(self, content):
        self.content = content
        self.children = LinkedList() # os filhos ficam numa lista encadeada nossa

    def add_child(self, content):
        child = TreeNode(content)
        self.children.add_list(child)
        return child


class Tree:
    def __init__(self, root_content):
        self.root = TreeNode(root_content)

    def preorder(self):
        # Percurso em profundidade (pré-ordem): visita o nó, depois cada filho inteiro.
        # Devolve pares (nó, profundidade) - a profundidade serve para indentar.
        yield from self._preorder(self.root, 0)

    def _preorder(self, node, depth):
        yield node, depth
        for child in node.children: # cada filho é visitado com tudo que há embaixo dele
            yield from self._preorder(child, depth + 1)

    def find(self, criterion):
        for node, _ in self.preorder():
            if criterion(node.content):
                return node
        return None
