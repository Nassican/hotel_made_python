class SemanticNetwork:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node, relationships):
        self.nodes[node] = relationships

    def find_activation(self, start_node, target_node, visited=None):
        if visited is None:
            visited = set()

        if start_node in visited:
            return None

        visited.add(start_node)

        if start_node == target_node:
            return [start_node]

        if start_node not in self.nodes:
            return None

        for related_node in self.nodes[start_node]:
            path = self.find_activation(related_node, target_node, visited.copy())
            if path:
                return [start_node] + path

        return None


# Crear la red semántica
network = SemanticNetwork()

# Agregar nodos y relaciones
network.add_node("Ser Vivo", [])
network.add_node("Persona", ["Ser Vivo"])
network.add_node("Derecha", [])
network.add_node("Derecha", ["Persona"])
network.add_node("Juan", ["Persona"])
network.add_node("Pasto", [])
network.add_node("Ingeniero", ["Persona"])

# Realizar búsquedas por intersección
activation_path_1 = network.find_activation("Pasto", "Ingeniero")
activation_path_2 = network.find_activation("Juan", "Persona")

# Imprimir resultados
print("Activación entre Pasto e Ingeniero:", activation_path_1)
print("Activación entre Pasto y Persona:", activation_path_2)
