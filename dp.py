def minimize_total_tardiness(jobs):
    """
    Solve the 1||sum T_j problem using Dynamic Programming.

    Parameters:
        jobs: List of tuples [(p1, d1), (p2, d2), ...] where
              - pi is the processing time of job i
              - di is the due date of job i.

    Returns:
        min_tardiness: Minimum total tardiness.
        optimal_schedule: Job order that achieves the minimum tardiness.
    """
    n = len(jobs)
    # Processing times and due dates
    p = [job[0] for job in jobs]
    d = [job[1] for job in jobs]

    # Maximum possible time is the sum of all processing times
    max_time = sum(p)
    
    # Initialize DP table
    dp = [[float('inf')] * (max_time + 1) for _ in range(1 << n)]
    dp[0][0] = 0  # Base case: no jobs, no tardiness
    
    # Backtracking table to reconstruct the schedule
    parent = [[None] * (max_time + 1) for _ in range(1 << n)]
    
    # Iterate over all subsets of jobs
    for S in range(1 << n):  # 2^n subsets
        for t in range(max_time + 1):  # Time from 0 to max_time
            if dp[S][t] == float('inf'):
                continue  # Skip invalid states
            for j in range(n):  # Try scheduling each job j
                if S & (1 << j):  # Job j is already scheduled
                    continue
                next_S = S | (1 << j)  # Add job j to subset
                next_t = t + p[j]  # Next time is current time + p[j]
                tardiness = max(0, next_t - d[j])
                if dp[next_S][next_t] > dp[S][t] + tardiness:
                    dp[next_S][next_t] = dp[S][t] + tardiness
                    parent[next_S][next_t] = (S, t, j)  # Track the parent state

    # Find the minimum tardiness in the last row
    all_jobs = (1 << n) - 1  # All jobs scheduled
    min_tardiness = float('inf')
    end_time = -1
    for t in range(max_time + 1):
        if dp[all_jobs][t] < min_tardiness:
            min_tardiness = dp[all_jobs][t]
            end_time = t

    # Reconstruct the optimal schedule
    schedule = []
    current_state = (all_jobs, end_time)
    while current_state[0] != 0:  # Until no jobs are scheduled
        S, t = current_state
        prev_S, prev_t, job = parent[S][t]
        schedule.append(job)
        current_state = (prev_S, prev_t)
    
    schedule.reverse()  # Reverse to get the correct order

    return min_tardiness, schedule

# Example usage
jobs = [(1, 4), (3, 3), (5, 6)]  # (processing time, due date)
min_tardiness, schedule = minimize_total_tardiness(jobs)
print(f"Minimum Total Tardiness: {min_tardiness}")
print(f"Optimal Schedule (job indices): {schedule}")
