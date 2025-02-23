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

if __name__ == "__main__":
    main()