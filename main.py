import functions
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
        tasks = read_file(filename)
        
        matrix, total_vertices = build_graph(tasks)

if __name__ == "__main__":
    main()