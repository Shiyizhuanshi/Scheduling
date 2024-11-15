# pip3 install networkx matplotlib
# import networkx as nx
# import matplotlib.pyplot as plt

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

def get_jobs_with_successor(edges):
    jobs = []
    for edge in edges:
        jobs.append(edge[0])
    return list(set(jobs))
        
def get_jobs_without_successor(edges, schedule_jobs_count):
    jobs = []
    jobs_with_successor = get_jobs_with_successor(edges)
    for i in range(31 - schedule_jobs_count):
        if i not in jobs_with_successor:
            jobs.append(i)
    return jobs

# when scheduling a job, remove the edge that points to the job
def schedule_job(index, edges):
    for i in range(len(edges)):
        if edges[i][1] == index:
            edges.pop(i)
            break

def get_cur_time(un_schedule_jobs):
    cur_time = 0
    for job in un_schedule_jobs:
        cur_time += p[job]
    return cur_time


# schedule_jobs = []
# jobs = get_jobs_without_successor(edges, len(schedule_jobs))

# for job in jobs:
#     print(p[job])
#     schedule_job(job, edges)
#     schedule_jobs.append(job)
#     print(get_jobs_without_successor(edges, len(schedule_jobs)))





# # Create a directed graph
# G = nx.DiGraph()
# G.add_edges_from(edges)

# # Plot the DAG
# plt.figure(figsize=(12, 8))
# pos = nx.spring_layout(G)  # Position the nodes

# # Draw nodes and edges
# nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_weight="bold", arrows=True)
# nx.draw_networkx_edges(G, pos, edgelist=edges, arrowstyle='->', arrowsize=15)

# # Display the plot
# plt.title("Directed Acyclic Graph (DAG)")
# plt.show()
