import sys

# The function works only if there is task id start is continuous and start from 1
def read_file(filename):
    tasks = {}
    try:
        with open(filename, 'r') as f:
            for line in f:
                # Remove unnecessary ' ', '\t' or '\n' at the start or end of a line
                line = line.strip()
                if not line:
                    continue
                # Create a list with every element on the line
                parts = line.split()
                # Convert to int
                numbers = list(map(int, parts))
                # Element 0 is the task id
                task_id = numbers[0]
                # Element 1 is the task duration
                duration = numbers[1]
                # Other elements are predecessor of the task (if they exists)
                if len(numbers) > 2:
                    predecessors = numbers[2:]
                else:
                    predecessors = []
                # create a task element
                tasks[task_id] = {'duration': duration, 'predecessors': predecessors}
    except Exception as e:
        print("Erreur lors de la lecture du fichier :", e)
        sys.exit(1)
    return tasks


def build_graph(tasks):
    # Number of task (max id as we count 0)
    N = max(tasks.keys())
    # We add initial and terminal task
    total_vertices = N + 2
    matrix = [[None for i in range(total_vertices)] for j in range(total_vertices)]
    
    # Iterate from task 1 to last 0 being the initial task (to attribute links with alpha elements)
    for i in range(1, N+1):
        #  if a task as no predecessor, then we set alpha as a predecessor of the task in the matrix
        if len(tasks[i]['predecessors']) == 0:
            matrix[0][i] = 0
        
    
    
    # Iterate over all task (to set the insides links between tasks)
    for i in range(1, N+1):
        for p in tasks[i]['predecessors']:
            # Error handler if a predecessor don't exist
            if p not in tasks:
                print(f"Avertissement : La tâche prédécesseur {p} pour la tâche {i} n'existe pas.")
                continue
            # Set the duration of task p (predecessor of i) in the matrix 
            matrix[p][i] = tasks[p]['duration']
    
    # Create a set to ensure no duplicate element
    used_as_pred = set()

    # Iterate over all elements (to check for elements used as a predecessor)
    for i in range(1, N+1):
        # For each element, add all predecessor of it
        for p in tasks[i]['predecessors']:
            used_as_pred.add(p)

    # Iterate over each element (for omega element)
    for i in range(1, N+1):
        # If an element asn't been used as a predecessor (final task), then we link the final task N+1 to it with the correct duration
        if i not in used_as_pred:
            matrix[i][N+1] = tasks[i]['duration']
    
    return matrix, total_vertices



def display_graph_arcs(arcs, total_vertices):

    # Print the header for graph creation
    print("* Création du graphe d’ordonnancement :")
    
    # Print the total number of vertices
    print(f"{total_vertices} sommets")
    
    # Print the total number of arcs
    print(f"{len(arcs)} arcs")
    
    # Print each arc in the format "source -> destination = weight"
    for arc in arcs:
        print(f"{arc[0]} -> {arc[1]} = {arc[2]}")



def display_matrix(matrix, total_vertices):
    cell_width = 5  # Width of each cell
    # Build horizontal border as : +-----+-----+ 
    h_border = '+' + '+'.join(['-' * cell_width] * (total_vertices + 1)) + '+'

    # Join empty cell to task list
    header_cells = [''] + [str(j) for j in range(total_vertices)]
    # Build label layer as : |     |  0  |  1  |  2  |  ... |
    header_row = "|" + "|".join(cell.center(cell_width) for cell in header_cells) + "|"

    print("\nMatrice des valeurs")
    print(h_border)
    print(header_row)
    print(h_border)

    # Iterate for each vertices 
    for i in range(total_vertices):
        # Set first cell (name) as the task we iterate over
        row_cells = [str(i)]
        for j in range(total_vertices):
            # Use * is value is None, else we append the duration of the task
            cell = "*" if matrix[i][j] is None else str(matrix[i][j])
            row_cells.append(cell)
        # Build |  i  |  *  |  *  |  *  |  3  |  ... |
        row_str = "|" + "|".join(cell.center(cell_width) for cell in row_cells) + "|"
        print(row_str)
        print(h_border)


def check_negative_arcs(matrix, total_vertices):
    
    print("\nVérification des arcs négatifs")
    
    # Iterate for each vertices
    for i in range(total_vertices):
        for j in range(total_vertices):
            # Check if there is an arc and its weight is negative
            if matrix[i][j] is not None and matrix[i][j] < 0:
                print(f"Arc négatif détecté : {i} -> {j} = {matrix[i][j]}")
                return False # Return False if a negative arc is found and print its details
    
    print("Aucun arc négatif trouvé")
    return True # Return True if all arcs have positive weights

def detect_cycles(matrix, total_vertices):
    print("\nDétection des circuits")
    
    # Initialize an array to store the in-degree for each vertex
    in_degree = [0] * total_vertices
    
    # Compute the in-degree for each vertex by counting incoming edges
    for j in range(total_vertices):
        for i in range(total_vertices):
            if matrix[i][j] is not None:
                in_degree[j] += 1
    
    # Create a list of vertices with zero in-degree 
    entry_points = [i for i in range(total_vertices) if in_degree[i] == 0]
    sorted_order = []
    
    while entry_points:
        print("Points d’entrée :", " ".join(map(str, entry_points)))
        
        # Remove the first entry point from the list and process it
        u = entry_points.pop(0)
        print(f"Suppression du point d’entrée : {u}")
        sorted_order.append(u)
        
        # Decrease the in-degree for each successor of the removed vertex
        for v in range(total_vertices):
            if matrix[u][v] is not None:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    entry_points.append(v)
        
        # Identify remaining vertices that still have incoming edges
        remaining = [i for i in range(total_vertices) if i not in sorted_order and in_degree[i] > 0]
        print("Sommets restants :", " ".join(map(str, remaining)) if remaining else "Aucun")
    
    # If not all vertices have been processed, there is a cycle in the graph
    if len(sorted_order) != total_vertices:
        print("Il y a un circuit dans le graphe.")
        return False  # A cycle exists
    
    print("Il n’y a pas de circuit.")
    return True  # No cycles detected

def ranks(matrix, total_vertices):
    print("\nCalcul des rangs")
    # Number of predecessors for each vertex
    in_degree = [0] * total_vertices

    # Compute the in-degree for each vertex by counting incoming edges
    for i in range(total_vertices):
        for j in range(total_vertices):
            if matrix[i][j] is not None:
                in_degree[j] += 1

    # Create a list of vertices with zero in-degree (no predecessor)
    entry_points = [i for i in range(total_vertices) if in_degree[i] == 0]

    # Create a list of ranks for each vertex
    rank = [-1] * total_vertices

    # Initialisation
    k = 0

    while entry_points:
        # Create a list of new vertices with the rank k+1
        sorted_order = []

        for u in entry_points:
            rank[u] = k
            for v in range(total_vertices):
                if matrix[u][v] is not None:
                    in_degree[v] -= 1 # We make the vertex u disappear, so v losse one predecessor
                    if in_degree[v] == 0:
                        sorted_order.append(v) # New vertex without predecessors

        entry_points = sorted_order
        k += 1

    # Display each rank
    print("Pour chaque sommet : ")
    for i in range(total_vertices):
        print(f"Sommet {i} : Rang {rank[i]}")

    return rank


def earliest_start_schedule (matrix, rank, total_vertices):
    print("\nCalendrier au plus tôt")

    earliest_dates = {task_id: 0 for task_id in range(total_vertices)}
    chosen_pred = {task_id: None for task_id in range(total_vertices)} # The optimal predecessor with the highest date

    # Sort tasks by rank
    sorted_tasks = sorted(range(total_vertices), key=lambda task_id: (rank[task_id], task_id))

    for task_id in sorted_tasks:
        preds = [p for p in range(total_vertices) if matrix[p][task_id] is not None]
        if preds:
            best_pre = None
            best_val = 0
            for p in preds: # We search the maximum
                val = earliest_dates[p] + matrix[p][task_id]
                if val > best_val:
                    best_val = val
                    best_pre = p
            earliest_dates[task_id] = best_val
            chosen_pred[task_id] = best_pre

    # Display
    for t in sorted_tasks:
        if chosen_pred[t] is not None:
            print(f"Sommet {t} : {earliest_dates[t]} à partir de {chosen_pred[t]}")
        else:
            print(f"Sommet {t} : {earliest_dates[t]}")


    # Return earliest_dates to compute critical paths
    return earliest_dates


def latest_start_schedule(matrix, earliest_dates, total_vertices):
    print("\nCalendrier au plus tard")
    
    # Initialize latest dates and chosen successors
    latest_dates = {task_id: float('inf') for task_id in range(total_vertices)}
    chosen_succ = {task_id: None for task_id in range(total_vertices)}  
    
    # Find the final task (omega) and set its latest date
    omega = max(earliest_dates, key=earliest_dates.get)
    latest_dates[omega] = earliest_dates[omega]  
    
    # Sort tasks in descending order of earliest dates
    sorted_tasks = sorted(range(total_vertices), key=lambda task_id: -earliest_dates[task_id])
    
    # Calculate latest start dates for each task
    for task_id in sorted_tasks:
        succs = [s for s in range(total_vertices) if matrix[task_id][s] is not None]
        if succs:
            best_succ = None
            best_val = float('inf')
            for s in succs:
                val = latest_dates[s] - matrix[task_id][s]
                if val < best_val:
                    best_val = val
                    best_succ = s
            latest_dates[task_id] = best_val
            chosen_succ[task_id] = best_succ
    
    # Set the latest start date of the first task (alpha) to 0
    alpha = 0  
    latest_dates[alpha] = 0
    chosen_succ[alpha] = 1  
    
    # Display
    for t in range(total_vertices):
        if chosen_succ[t] is not None:
            print(f"Sommet {t} : {latest_dates[t]} à partir de {chosen_succ[t]}")
        else:
            print(f"Sommet {t} : {latest_dates[t]}")
    
    return latest_dates





