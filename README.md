# A-Maze-ing

Projeto de geração e resolução de labirintos em Python.

## Setup rápido (para correção)

```bash
python3 -m venv .venv
source .venv/bin/activate
make install
make lint
make run
```

Notas:
- O ambiente virtual `.venv` não é versionado (está no `.gitignore`).
- As dependências para lint estão em `requirements.txt`.
- Para debug interativo: `make debug`.

## Como funciona (resumo)

1. O `MazeGenerator` cria uma grelha com todas as paredes fechadas.
2. Gera a topologia do labirinto com um algoritmo de geração:
   - DFS (recursive backtracker), ou
   - Prim randomizado.
3. Se `PERFECT=False`, adiciona ciclos extra.
4. Aplica o padrão `42` quando o tamanho do maze permite.
5. Valida regras estruturais (células bloqueadas, isolamento e áreas abertas).
6. Calcula o caminho mais curto com BFS.

## Algoritmos

### DFS (Depth-First Search) - Geração

Implementado em `maze/algorithms/dfs.py`.

- Começa numa célula inicial.
- Marca a célula como visitada.
- Escolhe um vizinho não visitado aleatório e abre a parede entre os dois.
- Continua em profundidade (stack/backtracking) até não haver mais vizinhos.
- Quando bloqueia, recua (pop) até encontrar uma célula com vizinhos disponíveis.

Resultado: um maze "perfect" (sem ciclos) antes de qualquer pós-processamento.

### Prim Randomizado - Geração

Implementado em `maze/algorithms/prim.py`.

- Começa com uma célula visitada.
- Adiciona as paredes fronteira dessa célula a uma lista de candidatos.
- Escolhe uma parede aleatória.
- Se a parede liga uma célula visitada a outra não visitada, abre essa ligação.
- Marca a nova célula como visitada e adiciona as suas paredes fronteira.
- Repete até esgotar candidatos.

Resultado: também gera um maze "perfect" inicial, com estilo visual diferente do DFS.

### BFS (Breadth-First Search) - Resolução

Implementado em `maze/solver.py`.

- Parte da célula de entrada (`ENTRY`).
- Explora por camadas usando uma fila.
- Só avança para vizinhos com passagem aberta em ambos os lados.
- Guarda `parent` para reconstruir o caminho ao chegar ao `EXIT`.
- O caminho devolvido é o mais curto em número de passos.

### Configuração e Parsing

Implementado em `config/parser.py`.

- Responsável pela gestão de inputs e estabilidade do programa:
- Leitura: Processamento do ficheiro config.txt.
- Validação: Verificação rigorosa de todos os parâmetros de entrada.
- Robustez: Tratamento de exceções para garantir que o programa nunca encerra inesperadamente por erros de configuração.

### Output e Persistência

Implementado em `io/writer.py`.

Garante que o resultado final é guardado conforme as especificações:

- Conversão Hex: Transfere a grelha lógica para representação hexadecimal.
- Escrita: Geração do ficheiro final com metadados estruturados.
- Dados: Inserção precisa dos pontos de entrada (entry), saída (exit) e do caminho resolvido (path).
- Format Check: Garantia total de que o formato do ficheiro segue o padrão exigido pelo "subject".

 ### Interface Visual

Implementado em `render/ascii.py`.

Motor de renderização em terminal para visualização em tempo real:

- Desenho: Renderização de paredes e caminhos usando caracteres ASCII.
- Destaque: Identificação visual clara dos pontos de entrada e saída.

Interatividade:
- Opção para regenerar o labirinto.
- Funcionalidade de ligar/desligar (show/hide) a visualização do caminho.
- Suporte para mudança de cores via ANSI escape codes.

## Links úteis

- https://medium.com/@nacerkroudir
- randomized-depth-first-search-algorithm-for-maze-generation-fb2d83702742
- https://www.kaggle.com/code/mexwell/maze-runner-shortest-path-algorithms
- https://en.wikipedia.org/wiki/ANSI_escape_code
