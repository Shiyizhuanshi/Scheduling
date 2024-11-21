# Import of libraries
import random

def total_tardiness(jobs, schedule):
    tardiness = 0
    cur_time = 0
    for job in schedule:
        cur_time += jobs[job][0]
        tardiness += max(0, cur_time - jobs[job][1])
    return tardiness


def neighbors(x, T, workflow):
    n = len(x)
    # Create a dictionary to represent workflow dependencies for fast checks
    dependency_map = {job: [] for job in x}
    for before, after in workflow:
        dependency_map[after].append(before)
    
    for _ in range(1000):  # Limit iterations to avoid infinite loops
        # Randomly select two distinct jobs to swap
        i, j = random.sample(range(n), 2)
        job1, job2 = x[i], x[j]
        
        # Ensure the swap is not tabu
        if (job1, job2) not in T and (job2, job1) not in T:
            # Check if swapping jobs violates workflow constraints
            new_x = x.copy()
            new_x[i], new_x[j] = new_x[j], new_x[i]
            if not violates_workflow(new_x, dependency_map):
                return new_x, job1, job2

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

# processing times and due dates
JOBS_P = [3, 10, 2, 2, 5, 2, 14, 5, 6, 5, 5, 2, 3, 3, 5, 6, 6, 6, 2, 3, 2, 3, 14, 5, 18, 10, 2, 3, 6, 2, 10]
JOBS_D = [172, 82, 18, 61, 93, 71, 217, 295, 290, 287, 253, 307, 279, 73, 355, 34,
233, 77, 88, 122, 71, 181, 340, 141, 209, 217, 256, 144, 307, 329, 269]

# Jobs as tuples of (processing time, due date)
JOBS = list(zip(JOBS_P, JOBS_D))
# Workflow of jobs
WORKFLOW = [
    (0, 30), (1, 0), (2, 7), (3, 2), (4, 1), (5, 15), (6, 5), (7, 6), (8, 7), (9, 8),
    (10, 0), (11, 4), (12, 11), (13, 12), (16, 14), (14, 10), (15, 4), (16, 15),
    (17, 16), (18, 17), (19, 18), (20, 17), (21, 20), (22, 21), (23, 4), (24, 23),
    (25, 24), (26, 25), (27, 25), (28, 26), (28, 27), (29, 3), (29, 9), (29, 13),
    (29, 19), (29, 22), (29, 28), 
]

X_0 = [30,29,23,10,9,14,13,12,4,20,22,3,27,28,8,7,19,21,26,18,25,17,15,6,24,16,5,11,2,1,31]
for i in range(len(X_0)):
    X_0[i] -= 1

K = 1000
L = 20
GAMMA = 5

# Run tabu search
xbest = tabu_search(X_0, L, GAMMA, K, total_tardiness, neighbors, JOBS, WORKFLOW)
xbest = [job + 1 for job in xbest]  # Convert back to 1-indexed jobs
print(f'Best schedule: {xbest}')