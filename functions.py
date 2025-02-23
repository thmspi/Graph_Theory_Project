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
    print(matrix)
    
    # Iterate from task 1 to last 0 being the initial task (to attribute links with alpha elements)
    for i in range(1, N+1):
        #  if a task as no predecessor, then we set alpha as a predecessor of the task in the matrix
        if len(tasks[i]['predecessors']) == 0:
            matrix[0][i] = 0
    print(matrix)
        
    
    
    # Iterate over all task (to set the insides links between tasks)
    for i in range(1, N+1):
        for p in tasks[i]['predecessors']:
            # Error handler if a predecessor don't exist
            if p not in tasks:
                print(f"Avertissement : La tâche prédécesseur {p} pour la tâche {i} n'existe pas.")
                continue
            # Set the duration of task p (predecessor of i) in the matrix 
            matrix[p][i] = tasks[p]['duration']
    print(matrix)
    
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