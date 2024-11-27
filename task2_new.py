# Import of libraries
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

def get_neighbors(schedule, tabu_list, edges):
    # This function returns the neighbors of the current schedule
    # return a list of neighbors, the jobs swapped and the new schedule

    n = len(schedule)
    neighbors = []
    swapped_jobs = []
    new_schedules = []

    # Create a dictionary to represent workflow dependencies for fast checks
    dependency_map = {job: [] for job in schedule}
    for before, after in edges:
        dependency_map[after].append(before)
    
    for _ in range(1000):  # Limit iterations to avoid infinite loops
        # Randomly select two distinct jobs to swap
        i, j = random.sample(range(n), 2)
        job1, job2 = schedule[i], schedule[j]
        
        # Ensure the swap is not tabu
        if (job1, job2) not in tabu_list and (job2, job1) not in tabu_list:
            # Check if swapping jobs violates workflow constraints
            new_schedule = schedule.copy()
            new_schedule[i], new_schedule[j] = new_schedule[j], new_schedule[i]
            if not violates_workflow(new_schedule, dependency_map):
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


def tabu_search(x0, L, gamma, K, g, neighbors_fn, jobs, workflow):
    k = 0
    T = set()  # Set to track pairs of jobs
    xk = x0
    gbest = g(jobs, x0)  # Best value of g found so far
    xbest = x0     # Best schedule corresponding to gbest
    
    while k <= K:
        print(f'Iteration {k}: g={gbest}')
        print(f'Schedule: {xk}')
        print(f'Tabu list: {T}')
        print("**********")
        while True:
            y, i, j = neighbors_fn(xk, T, workflow)  # Select next neighbor and jobs swapped
            if y is None:  # No new solution can be found
                return xbest
            
            delta = g(jobs, xk) - g(jobs, y)
            if (delta > -gamma and (i, j) not in T) or g(jobs, y) < gbest:
                break
        
        xk = y
        T.add((i, j))
        
        # Remove pairs older than L iterations
        if len(T) > L:
            T = set(list(T)[-L:])
        
        g_y = g(jobs, xk)
        if g_y < gbest:
            gbest = g_y
            xbest = xk
        
        k += 1
    
    return xbest

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