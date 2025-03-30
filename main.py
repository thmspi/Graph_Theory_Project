import functions as f
import os
import re

def main():
    while True:
        print("Entrez le chemin du fichier de contraintes (.txt) ou 'q' pour quitter :")
        filename = input().strip()
        if filename.lower() == 'q':
            break
        if not os.path.exists(filename):
            print("Fichier non trouvé. Réessayez.")
            continue
        trace = []
        tasks = f.read_file(filename)
        
        matrix, total_vertices = f.build_graph(tasks)

        f.display_matrix(matrix, total_vertices, trace)
   
        if not f.check_negative_arcs(matrix, total_vertices, trace):
            trace.append("Le graphe contient des arcs négatifs. Veuillez utiliser un autre tableau de contraintes.")
            f.save_trace(filename, trace)
            continue
        
        has_cycle = f.detect_cycles(matrix, total_vertices, trace)
        if not has_cycle:
            trace.append("Le graphe n'est pas un graphe d'ordonnancement (circuit détecté). Veuillez utiliser un autre tableau de contraintes.")
            f.save_trace(filename, trace)
            continue

        rank = f.ranks(matrix, total_vertices, trace)

        earliest_dates = f.earliest_start_schedule(matrix, rank, total_vertices, trace)
        latest_dates = f.latest_start_schedule(matrix, earliest_dates, total_vertices, trace)
    
        margins = f.compute_margins(matrix, total_vertices, earliest_dates, latest_dates, trace)
        
        f.find_critical_paths(matrix, total_vertices, margins, trace)

        print("\nTraitement terminé pour ce tableau de contraintes.\n")

        f.save_trace(filename, trace)

        print("Voulez-vous traiter un autre tableau ? (o/n)")
        answer = input().strip().lower()
        if answer != 'o':
            break
        
  
if __name__ == "__main__":
    main()

