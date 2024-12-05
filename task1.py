import sys
def calculate_total_cost(schedule_jobs, p, d):
    total_cost = 0
    cur_time = 0
    for job in schedule_jobs:
        cur_time += p[job]
        total_cost += max(0, cur_time - d[job])
    return total_cost

def calculate_max_cost(schedule_jobs, p, d):
    max_cost = -999999
    cur_time = 0
    for job in schedule_jobs:
        cur_time += p[job]
        cur_cost = max(0, cur_time - d[job])
        if cur_cost > max_cost:
            max_cost = cur_cost
    return max_cost

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


def choose_job_with_lowest_cost(jobs, cur_time, d):
    # This function returns the job with the lowest cost
    # Cost is calculated as max(0, cur_time - due_date)
    min_cost = 999999
    job_to_schedule = -1
    for job in jobs:
        cost = max(0, cur_time - d[job])
        if cost <= min_cost:
            min_cost = cost
            job_to_schedule = job
    return job_to_schedule

def find_lcl_schedule(edges, p, d):
    scheduled_jobs = []
    iteraton = 0
    # As we start from the last job, the current time is the sum of all the processing times
    cur_time = sum(p)
    while (len(scheduled_jobs) != 31):
        print("Schedule in iteration " + str(iteraton) + ":" + str(scheduled_jobs))
        print("Max cost:" + str(calculate_max_cost(scheduled_jobs, p, d)))
        # Find the jobs that can be scheduled
        available_jobs = find_available_jobs(edges, scheduled_jobs)
        # Find the job with the lowest cost
        job = choose_job_with_lowest_cost(available_jobs, cur_time, d)
        # Schedule the job
        scheduled_jobs.insert(0,job)
        # Remove the edge that points to the job
        for edge in edges:
            if edge[1] == job:
                edges.remove(edge)
        iteraton += 1
    return scheduled_jobs

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

print("This will print to the console.")
schedule = find_lcl_schedule(edges, p, d)
print("Final optimal schedule: " + str(schedule))
print("Max cost:" + str(calculate_max_cost(schedule, p, d)))
print("Total cost:" + str(calculate_total_cost(schedule, p, d)))