def test(schedule, last_interchange):
    n = len(schedule)

    neighbors = []

    for i in range(len(schedule)):
        if schedule[i] == last_interchange[1]:
            start_index = i
            break
    
    for offset in range(n - 1):  # There are n-1 adjacent pairs
        i = (start_index + offset) % (n - 1)  # Wrap around to ensure cyclic iteration
        job1, job2 = schedule[i], schedule[i + 1]

        neighbors.append((job1, job2))
    
    return neighbors

print(test([1, 2, 3, 4, 5], [4,5]))