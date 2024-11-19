# pip3 install networkx matplotlib
# import networkx as nx
# import matplotlib.pyplot as plt

import time
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

def get_cur_time(scheduled_jobs):
    cur_time = 0
    un_scheduled_jobs = []
    for i in range(31):
        if i not in scheduled_jobs:
            un_scheduled_jobs.append(i)
    for job in un_scheduled_jobs:
        cur_time += p[job]
    return cur_time

def get_jobs_with_successor(edges):
    jobs = []
    for edge in edges:
        jobs.append(edge[0])
    return list(set(jobs))

# get jobs without successor and not in schedule_jobs
def get_jobs_without_successor(edges, schedule_jobs):
    jobs = []
    jobs_with_successor = get_jobs_with_successor(edges)
    for i in range(31):
        if i not in jobs_with_successor and i not in schedule_jobs:
            jobs.append(i)
    return jobs

# when scheduling a job, remove the edge that points to the job
def schedule_job(index, edges):
    for edge in edges:
        if edge[1] == index:
            edges.remove(edge)

def cost_function(job, scheduled_jobs):
    completion_time = get_cur_time(scheduled_jobs) + p[job]
    return max(0, completion_time - d[job])

def choose_job_to_schedule(jobs_to_choose, scheduled_jobs):
    min_cost = 999999
    job_to_schedule = -1
    for job in jobs_to_choose:
        cost = cost_function(job, scheduled_jobs)
        print("job:" + str(job) + " cost:" + str(cost))
        if cost <= min_cost:
            min_cost = cost
            job_to_schedule = job
    return job_to_schedule

def schedule_last_jobs(edges, scheduled_jobs):
    last_jobs = []
    for edge in edges:
        last_jobs.append(edge[0])
    if len(last_jobs) == 0:
        print("All jobs have been scheduled")
    else:
        while (len(last_jobs) > 0):
            jobs_to_choose =[]
            job = -1
            print("************************")
            print("last_jobs:" + str(last_jobs))
            print("edges" + str(edges))
            for job in last_jobs:
                edges_about_job = []
                successors_count = 0
                # Find out all the edges that starts from the job
                for edge in edges:
                    if edge[0] == job:
                        edges_about_job.append(edge)
                # Check if all the successors of the job have been scheduled
                for edge in edges_about_job:
                    if edge[1] in scheduled_jobs:
                        successors_count += 1
                # If all the successors have been scheduled, add the job to jobs_to_choose
                if successors_count == len(edges_about_job):
                    jobs_to_choose.append(job)
            print("jobs_to_choose:" + str(jobs_to_choose))
            job = choose_job_to_schedule(jobs_to_choose, scheduled_jobs)
            print("job to schedule:" + str(job))
            last_jobs.remove(job)
            scheduled_jobs.insert(0, job)
            for edge in edges:
                if edge[0] == job:
                    edges.remove(edge)

def calculate_total_cost(schedule_jobs):
    total_cost = 0
    cur_time = 0
    for job in schedule_jobs:
        cur_time += p[job]
        total_cost += max(0, cur_time - d[job])
        print("current total cost:" + str(total_cost))
    return total_cost

def calculate_max_cost(schedule_jobs):
    max_cost = -999999
    cur_time = 0
    for job in schedule_jobs:
        cur_time += p[job]
        cur_cost = max(0, cur_time - d[job])
        if cur_cost > max_cost:
            max_cost = cur_cost
    return max_cost

def calculate_best_schedule(egdes_of_jobs):
    scheduled_jobs = []
    while(len(scheduled_jobs) != 31):
        print("====================================")
        print("lengt of scheduled_jobs:" + str(len(scheduled_jobs)))
        jobs = get_jobs_without_successor(egdes_of_jobs, scheduled_jobs)
        print("jobs without successor:" + str(jobs))
        if (len(jobs) == 0):
            schedule_last_jobs(egdes_of_jobs, scheduled_jobs)
        else:
            job = choose_job_to_schedule(jobs, scheduled_jobs)
            schedule_job(job, egdes_of_jobs)
            scheduled_jobs.insert(0, job)
            print("scheduled job:" + str(job))
        print("scheduled_jobs:" + str(scheduled_jobs))
        # print("edges" + str(egdes_of_jobs))
    return scheduled_jobs

scheduled_jobs = calculate_best_schedule(edges)
print("Max cost:" + str(calculate_max_cost(scheduled_jobs)))