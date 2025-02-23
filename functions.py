import sys

def read_file(filename):
    tasks = {}
    # Handle error
    try:
        with open(filename, 'r') as f:
            # loop over each lines
            for line in f:
                # Remove unnecessary ' ', '\t' or '\n' at the start or end of a line
                line = line.strip()
                if not line:
                    continue  # ignore empty line
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