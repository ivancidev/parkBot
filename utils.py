def state_to_index(state):
    """Convierte un arreglo de estado binario en un índice único."""
    return int("".join(map(str, state.astype(int))), 2)
