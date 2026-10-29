# Oficina Mecânica — Estrutura de Dados (Fatec Rio Claro)

Sistema em Python que gerencia o ciclo de um serviço: chegada do veículo, diagnóstico, troca de peças, ordem de serviço (OS) e pagamento.
Nenhuma estrutura built-in (`list`, `dict`, `deque`...) é usada para guardar os dados do problema: tudo usa as classes próprias abaixo.

## Como rodar

```
python main.py                                    # menu (opção 1 = simulação completa)
python -m unittest testes.test_queue testes.test_oficina -v   # testes
```

## Organização

| Pasta | Responsabilidade |
|---|---|
| `estrutura/` | Estruturas **genéricas**, sem regra de oficina: `No`, `Queue` (fila), `LinkedList` (lista encadeada), `Tree`/`TreeNode` (árvore com N filhos) |
| `oficina/` | **Regras da oficina**, usando as estruturas acima |

| Módulo (`oficina/`) | O que faz | Estruturas |
|---|---|---|
| `clientes.py` | Clientes e veículos (cadastrar, buscar por CPF/placa, remover) | Lista de clientes + Lista de veículos |
| `atendimento.py` | Espera e boxes; guincho tem prioridade | Fila + Fila (+ Lista de boxes) |
| `diagnostico.py` | Árvore de componentes, pré-ordem indentada, marcar defeito | Árvore (filhos em Lista) |
| `estoque.py` | Produtos, lotes, baixa FIFO, vencidos, ajuste, alerta de mínimo | Lista de produtos + Fila de lotes |
| `ordem_servico.py` | OS com peças e serviços; só fecha após remontagem | Listas |
| `pagamento.py` | Registro de pagamentos (PIX, cartão à vista/parcelado, dinheiro) | Lista |
| `consumo.py` | Fechamento: baixa estoque, registra pagamento, consumo por cliente/veículo | Listas |
| `oficina.py` / `simulacao.py` | Junta os módulos e roda o atendimento completo | — |

## Combinações de estruturas

### 1. Atendimento com prioridade para guincho — Fila + Fila
- **Classe/métodos:** `Atendimento` (`atendimento.py`): `chegar`, `proximo`, `chamar_proximo`, `liberar_box`; `fila_guincho` e `fila_normal` são duas `Queue`.
- **Como funciona:** o próximo vem da fila de guincho; se estiver vazia, da normal. Cada fila é FIFO, então a ordem de chegada é respeitada dentro de cada grupo. `liberar_box` já chama o próximo automaticamente.
- **Por que é adequada:** duas filas simples resolvem a prioridade com `add`/`remove` em O(1).
- **Desvantagem de uma estrutura só:** numa fila única, o guincho precisaria ser inserido no meio (percorrer até achar onde entra, O(n)) ou a fila reordenada a cada chegada.

### 2. Estoque com vários lotes por produto — Lista de produtos + Fila de lotes
- **Classes/métodos:** `Estoque` (lista `produtos`) e `Produto` (fila `lotes`): `Estoque.baixar` → `Produto.consumir`, `comprar_lote`, `descartar_vencidos`, `ajustar_quantidade`, `alertas`.
- **Como funciona:** a baixa percorre a lista até o produto e consome o lote do início da fila (o mais antigo). Se o lote zera, sai da fila e o próximo passa a ser consumido.
- **Por que é adequada:** "primeiro que entra, primeiro que sai" é exatamente o comportamento da fila; a lista serve para achar o produto por código.
- **Desvantagem de uma estrutura só:** uma lista única de lotes misturados exigiria filtrar por produto e ordenar por data a cada baixa; uma fila única não permitiria achar o produto.

### 3. Clientes e veículos — Lista de clientes + Lista de veículos
- **Classes/métodos:** `CadastroClientes` (lista `clientes`) e `Cliente` (lista `veiculos`): `buscar_por_placa`, `cadastrar_veiculo`, `remover_veiculo`.
- **Como funciona:** buscar por placa percorre a lista de clientes e, em cada um, a lista de veículos. Não há limite de veículos por cliente.
- **Por que é adequada:** a relação é 1 cliente → N veículos, e a lista cresce sem tamanho pré-definido.
- **Desvantagem de uma estrutura só:** uma lista única de veículos repetiria os dados do dono em cada veículo e dificultaria remover o cliente com todos os seus veículos.

## Complexidade (n = elementos na estrutura)

| Operação | Custo |
|---|---|
| `Queue.add` / `remove` / `peek` | O(1) (guarda `first` e `last`) |
| `LinkedList.add_list` | O(n) (anda até o último nó) |
| `LinkedList.search` / `remove` | O(n) |
| Buscar por CPF | O(clientes) |
| Buscar por placa | O(clientes × veículos por cliente) |
| Próximo veículo / liberar box | O(1) na fila + O(boxes) para achar box livre |
| Baixa de estoque | O(produtos) para achar o produto + O(lotes consumidos) |
| Descartar vencidos / ajustar lote | O(produtos × lotes) (a fila é refeita preservando a ordem) |
| Árvore pré-ordem / achar componente | O(nós) |

Possível melhoria: guardar o `last` na `LinkedList` para tornar `add_list` O(1).

## Decisões

- A **baixa do estoque acontece no fechamento da OS** (módulo de consumo). Ao incluir a peça, o preço de venda é copiado do produto; antes de baixar, o sistema confere o estoque de **todos** os itens, assim nunca ocorre uma baixa pela metade.
- Se a forma de pagamento for inválida, o estoque não é alterado.
- Pagamento parcelado só vale para cartão (PIX/dinheiro ficam com 1 parcela).
- Compras de lotes devem ser registradas em ordem cronológica, pois a fila assume que o lote da frente é o mais antigo.
- A árvore de componentes é pré-definida (`Diagnostico.padrao()`); só o estado (OK / Com defeito) muda.
