# Require Python 3
import json
from functools import reduce
import matplotlib.pyplot as plt


def generate_gnatt_chart(graph, time_span):
    if time_span > 30:
        time_span = 30
    
    fig, gnt = plt.subplots()
    task_names = [task[0] for task in graph]

    fig.suptitle("Gantt Chart using Earliest Deadline First Algorithm")
    gnt.set_ylim(0, 5 * (len(task_names)))
    gnt.set_xlim(0, time_span)
    gnt.set_xlabel('Time')
    gnt.set_xticks([i for i in range(time_span + 1)])
    gnt.set_ylabel('Tasks')
    # gnt.set_yticks([i + 2.5 for i in range(0, 5 * len(task_names), 5)])
    gnt.set_yticks([i for i in range(0, 5 * len(task_names), 5)])
    gnt.set_yticklabels(task_names)
    gnt.grid(True)

    for i, task in enumerate(graph):
        gnt.broken_barh(task[1], (5 * (i), 5), facecolors='tab:blue')

    plt.savefig("gantt_edf.png")
    plt.show()

    print("gantt_edf.png is generated based on the input tasks")


def get_gcd(first_number, second_number):
    if second_number == 0:
        return first_number

    return get_gcd(second_number, first_number % second_number)


def get_lcm(first_number, second_number):
    return first_number * second_number // get_gcd(first_number, second_number)


def get_graph(jobs):
    graph = {}

    if len(jobs) > 30:
        jobs = jobs[:30]

    for job in jobs:
        task_name, execution_time, task_start_time, task_end_time, _ = job
        node = (task_start_time, execution_time)

        if task_name not in graph:
            graph[task_name] = [node]
        else:
            graph[task_name].append(node)

    graph = sorted(graph.items())

    return graph


def get_deadline_table(jobs):
    table = {}
    for job in jobs:
        task_name = job[0]
        deadline_missed = job[-1]
        table[task_name] = table.get(task_name, 0) + int(deadline_missed)
    return table


qu2= []
def get_edf(tasks, time_span):
    queue = []
    output = []

    for task in tasks:
        task_name, execution_time, deadline, period = task

        for i in range(0, time_span + 1 - period, period):
            task_deadline = i + deadline
            queue.append((task_name, execution_time, i, task_deadline))

    # print('queue', queue)
    
    '''
    task_name, execution_time, deadline, period
    [('T1', 1, 0, 4), ('T1', 1, 4, 8), ('T1', 1, 8, 12), ('T1', 1, 12, 16), ('T1', 1, 16, 20), ('T1', 1, 20, 24),
    ('T2', 2, 0, 6), ('T2', 2, 6, 12), ('T2', 2, 12, 18), ('T2', 2, 18, 24),
    ('T3', 3, 0, 8), ('T3', 3, 8, 16), ('T3', 3, 16, 24)]
    '''
    
    queue = sorted(queue, key=lambda x: (x[3], x[2]))
    
    '''
    task_name, execution_time, deadline, period
    [('T1', 1, 0, 4), ('T2', 2, 0, 6), ('T3', 3, 0, 8), 
    ('T1', 1, 4, 8), ('T2', 2, 6, 12), 
    ('T1', 1, 8, 12), ('T3', 3, 8, 16), 
    ('T1', 1, 12, 16), ('T2', 2, 12, 18), 
    ('T1', 1, 16, 20), ('T3', 3, 16, 24), ('T2', 2, 18, 24), 
    ('T1', 1, 20, 24)]
    '''
    print('sorted queue', queue)

    cpu_current_time = 0

    for task in queue:
        task_name, execution_time, task_start_time, task_deadline = task
        task_start_time = max(task_start_time, cpu_current_time)
        task_end_time = task_start_time + execution_time
        deadline_missed = task_end_time > task_deadline

        job = (task_name,
               execution_time,
               task_start_time,
               task_end_time,
               deadline_missed)

        print('task_name, execution_time, task_start_time, task_end_time, deadline_missed', job)
        
        if not deadline_missed:
            cpu_current_time = task_end_time
            output.append(job)
        else:
            qu2.append(job)
        
    # print('output',output)
    
    '''
    [('T1', 1, 0, 1, False), ('T2', 2, 1, 3, False), ('T3', 3, 3, 6, False), 
    ('T1', 1, 6, 7, False), ('T2', 2, 7, 9, False), 
    ('T1', 1, 9, 10, False), ('T3', 3, 10, 13, False), 
    ('T1', 1, 13, 14, False), ('T2', 2, 14, 16, False), 
    ('T1', 1, 16, 17, False), ('T3', 3, 17, 20, False), ('T2', 2, 20, 22, False), 
    ('T1', 1, 22, 23, False)]
    '''

    return output

given_tasks = [
    ["T1", 1, 4, 4],
    ["T2", 2, 6, 6],
    ["T3", 3, 8, 8],
]


# given_tasks = [
#     ["T1", 3, 7, 20],
#     ["T2", 2, 8, 10],
#     ["T3", 2, 4, 5],
# ]

given_tasks = [
    ["T1", 2, 5, 5],
    ["T2", 2, 6, 6],
    ["T3", 2, 7, 7],
    ["T4", 2, 8, 8],
]

given_tasks = [
    ["T1", 2, 5, 5],
    ["T2", 2, 4, 6],
    ["T3", 2, 4, 7],
    ["T4", 2, 3, 6],
]

if __name__ == "__main__":
    # [[task_name, execution_time, deadline, period]]
    # given_tasks = []
    # total_number_of_tasks = int(input("How many tasks to schedule: "))

    # for i in range(1, total_number_of_tasks + 1):
    #     task_name = f"T{i}"

    #     execution_time, deadline, period = map(
    #         int,
    #         input(f"Enter the execution time, deadline and period of task {i}: ").split()
    #     )

    #     given_tasks.append([task_name, execution_time, deadline, period])

    span = reduce(get_lcm, [task[2] for task in given_tasks])
    edf_jobs = get_edf(given_tasks, span)
    graph_data = get_graph(edf_jobs)

    print("Deadline missed for each task: ", end="")
    # print(get_deadline_table(edf_jobs))
    print(qu2)
    
    
    generate_gnatt_chart(graph_data, span)
    # generate_gnatt_chart(graph_data, 30)



