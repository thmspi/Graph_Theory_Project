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

        rank = f.ranks(matrix, total_vertices)

        earliest_dates = f.earliest_start_schedule(matrix, rank, total_vertices)
        latest_dates = f.latest_start_schedule(matrix, earliest_dates, total_vertices)
    
        margins = f.compute_margins(matrix, total_vertices, earliest_dates, latest_dates)
        
        f.find_critical_paths(matrix, total_vertices, margins)

        print("\nTraitement terminé pour ce tableau de contraintes.\n")
        print("Voulez-vous traiter un autre tableau ? (o/n)")
        answer = input().strip().lower()
        if answer != 'o':
            break
        
  
if __name__ == "__main__":
    main()

