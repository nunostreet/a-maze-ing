# Define a fisica do nosso labirinto

# 0b significa que o número está escrito em binário
NORTH = 0b0001  # bit 0
EAST = 0b0010  # bit 1
SOUTH = 0b0100  # bit 2
WEST = 0b1000  # bit 3

# CADA BIT REPRESENTA SE UMA PAREDE ESTÁ FECHADA (1) OU ABERTA (0)

# Exemplo 1: 0b1111 -> todas as paredes fechadas
# Exemplo 2: 0b0000 -> não tem paredes
# Exemplo 3: 0b0101 -> Norte e Sul fechados.

ALL_WALLS = NORTH | EAST | SOUTH | WEST

# (
#   x movement,
#   y movement,
#   wall to remove from current cell,
#   wall to remove from neighbour
# )

DIRECTIONS = {
    "N": (0, -1, NORTH, SOUTH),
    "E": (1, 0, EAST, WEST),
    "S": (0, 1, SOUTH, NORTH),
    "W": (-1, 0, WEST, EAST),
}
