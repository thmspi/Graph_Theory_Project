import functions as f
import os

def main():
    while True:
        print("Entrez le chemin du fichier de contraintes (.txt) ou 'q' pour quitter :")
        filename = input().strip()
        if filename.lower() == 'q':
            break
        if not os.path.exists(filename):
            print("Fichier non trouvé. Réessayez.")
            continue
        tasks = f.read_file(filename)
        
        matrix, total_vertices = f.build_graph(tasks)

        f.display_matrix(matrix, total_vertices)
        
        if not f.check_negative_arcs(matrix, total_vertices):
            print("Le graphe contient des arcs négatifs. Veuillez utiliser un autre tableau de contraintes.")
            continue
        
        has_cycle = f.detect_cycles(matrix, total_vertices)
        if not has_cycle:
            print("Le graphe n'est pas un graphe d'ordonnancement (circuit détecté). Veuillez utiliser un autre tableau de contraintes.")
            continue

if __name__ == "__main__":
    main()