import networkx as nx
import matplotlib.pyplot as plt

# Remplace "graphe.txt" par le nom de ton fichier si besoin
filename = "table 3.txt"

G = nx.DiGraph()

with open(filename, "r") as file:
    for line in file:
        parts = list(map(int, line.strip().split()))
        if len(parts) < 2:
            continue
        node = parts[0]
        weight = parts[1]
        predecessors = parts[2:]

        # Ajoute le nœud avec son poids d'arcs sortants (attribut personnalisé)
        G.add_node(node, weight=weight)

        # Ajoute des arêtes des prédécesseurs vers ce nœud
        for pred in predecessors:
            G.add_edge(pred, node)

# Affichage
pos = nx.spring_layout(G)  # tu peux aussi essayer nx.kamada_kawai_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=800, font_weight='bold')
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.title("Graphe dirigé à partir du fichier")
plt.show()
