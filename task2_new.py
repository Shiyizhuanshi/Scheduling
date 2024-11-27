import random

def calculate_total_cost(schedule_jobs, p, d):
    total_cost = 0
    cur_time = 0
    for job in schedule_jobs:
        cur_time += p[job]
        total_cost += max(0, cur_time - d[job])
    return total_cost

def find_available_jobs(edges, scheduled_jobs):
    # This function returns the jobs that can be scheduled
    # Available jobs are the jobs that have no successor or have successors that have been scheduled
    jobs = []
    jobs_with_successor = []

    # Find all the jobs that have successors
    for edge in edges:
        jobs_with_successor.append(edge[0])
    jobs_with_successor = list(set(jobs_with_successor))

    # iterate through all the jobs
    for i in range(31):
        # if job is not scheduled
        if i not in scheduled_jobs:
            # if job has no successor
            if i not in jobs_with_successor:
                jobs.append(i)
            # if the job has successor, check if all the successors have been scheduled
            else:
                successors_count = 0
                edges_from_job = []
                # Find out all the edges that starts from the job
                for edge in edges:
                    if edge[0] == i:
                        edges_from_job.append(edge)
                # Check if all the successors of the job have been scheduled
                for edge in edges_from_job:
                    if edge[1] in scheduled_jobs:
                        successors_count += 1
                # If all the successors have been scheduled, add the job to jobs_to_choose
                if successors_count == len(edges_from_job):
                    jobs.append(i)
    return jobs

def get_initial_solution(edges):
    # This function returns the random initial solution that takes precedence into account
    schedule = []
    while (len(schedule) < 31):
        # Find the available jobs
        available_jobs = find_available_jobs(edges, schedule)
        # Randomly choose the job to schedule
        job = random.choice(available_jobs)
        schedule.append(job)
    return schedule


def validate_schedule(schedule, edges):
    # This function validates the schedule based on the workflow constraints

    # Create a mapping from task to its position in the schedule
    position = {task: idx for idx, task in enumerate(schedule)}

    # Check each dependency
    for u, v in edges:
        if u not in position or v not in position:
            raise ValueError(f"Task '{u}' or '{v}' not found in the schedule.")
        
        # Validate that u comes before v in the schedule
        if position[u] >= position[v]:
            return False
        
    return True


def get_neighbors(schedule, tabu_list, edges, p, d):
    # This function returns the neighbors of the current schedule

    n = len(schedule)
    # Return None if there are no jobs to swap
    if n < 2 and len(tabu_list):
        return None, None, None  # No adjacent pairs to swap
    

    if len(tabu_list) == 0:
        start_index = 0
    else:
        last_interchange = list(tabu_list)[-1]  # Get the last interchange
        # Get the start index from the last interchange
        for i in range(len(schedule)):
            if schedule[i] == last_interchange[1]:
                start_index = i
                break
    neighbors = []
    swapped_jobs = []
    new_schedules = []
    
    # Iterate cyclically over adjacent pairs
    for offset in range(len - 1):  # There are n-1 adjacent pairs
        i = (start_index + offset) % (len - 1)  # Wrap around to ensure cyclic iteration
        j = i + 1
        job1, job2 = schedule[i], schedule[i + 1]

        # Ensure the swap is not tabu
        if (job1, job2) not in tabu_list and (job2, job1) not in tabu_list:
            # Check if swapping jobs violates workflow constraints
            new_schedule = schedule.copy()
            new_schedule[i], new_schedule[j] = new_schedule[j], new_schedule[i]
            if validate_schedule(new_schedule, edges):
                return new_schedule, job1, job2

    # If no valid neighbor found, return None
    return None, None, None


def violates_workflow(schedule, dependency_map):
    # Map job indices to positions in the schedule
    position_map = {job: pos for pos, job in enumerate(schedule)}
    
    for job, dependencies in dependency_map.items():
        for dependency in dependencies:
            if position_map[dependency] > position_map[job]:
                return True  # Dependency violated
    return False


def tabu_search(L, gamma, K, goal_func, neighbors_func, edges, p, d):
    iteration = 0
    tabu_list = set()  # Set to track pairs of jobs
    local_schedule = get_initial_solution(edges)
    gbest = goal_func(local_schedule, p, d)  # Best value of g found so far
    best_schedule = local_schedule     # Best schedule corresponding to gbest
    
    while iteration <= K:
        print("--------------------")
        print(f'Iteration {iteration}: best_g={gbest}')
        print(f'Local schedule: {local_schedule}')
        print(f'Tabu list: {tabu_list}')
        while True:
            neighbor_schedule, i, j = neighbors_func(local_schedule, tabu_list, edges, p, d)  # Select next neighbor and jobs swapped
            if neighbor_schedule is None:  # Run out of neighbors
                return best_schedule      # Then stop the search
            
            delta = goal_func(local_schedule, p, d) - goal_func(neighbor_schedule, p, d)
            if (delta > -gamma and (i, j) not in tabu_list) or goal_func(neighbor_schedule, p, d) < gbest:
                break
        
        # Update the current schedule
        local_schedule = neighbor_schedule
        # Add the swapped jobs to the tabu list
        tabu_list.add((i, j))
        
        # Remove pairs older than L iterations
        if len(tabu_list) > L:
            tabu_list = set(list(tabu_list)[-L:])
        
        g_neighbor = goal_func(neighbor_schedule, p, d)
        if g_neighbor < gbest:
            gbest = g_neighbor
            best_schedule = neighbor_schedule
        
        iteration += 1
    
    return best_schedule

# Define the directed edges
edges = [
    (0, 30), (1, 0), (2, 7), (3, 2), (4, 1), (5, 15), (6, 5), (7, 6), (8, 7), (9, 8),
    (10, 0), (11, 4), (12, 11), (13, 12), (16, 14), (14, 10), (15, 4), (16, 15),
    (17, 16), (18, 17), (19, 18), (20, 17), (21, 20), (22, 21), (23, 4), (24, 23),
    (25, 24), (26, 25), (27, 25), (28, 26), (28, 27), (29, 3), (29, 9), (29, 13),
    (29, 19), (29, 22), (29, 28), 
]

# Processing time for each job
p = [3, 10, 2, 2, 5, 2, 14, 5, 6, 5, 5, 2, 3, 3, 5, 6, 6, 6, 2, 3, 2, 3, 14, 5, 18, 10, 2, 3, 6, 2, 10]
# Due date for each job
d = [172, 82, 18, 61, 93, 71, 217, 295, 290, 287, 253, 307, 279, 73, 355, 34,
233, 77, 88, 122, 71, 181, 340, 141, 209, 217, 256, 144, 307, 329, 269]

print(get_initial_solution(edges))