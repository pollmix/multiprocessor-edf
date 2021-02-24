# Require Python 3
import json
from functools import reduce
import matplotlib.pyplot as plt
from collections import Counter


def generate_gnatt_chart(graph, time_span, name='figure'):
    # if time_span > 30:
    #     time_span = 30

    fig, gnt = plt.subplots()
    task_names = [task[0] for task in graph]

    fig.suptitle(name)
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

    plt.savefig(name + '.png')
    plt.show()

    print(name + ".png is generated based on the input tasks")


def get_gcd(first_number, second_number):
    if second_number == 0:
        return first_number

    return get_gcd(second_number, first_number % second_number)


def get_lcm(first_number, second_number):
    return first_number * second_number // get_gcd(first_number, second_number)


def get_graph(jobs):
    graph = {}

    # if len(jobs) > 30:
    #     jobs = jobs[:30]

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


def task_period(tasks):
    tasks_period_map = {}

    for task in tasks:
        tasks_period_map[task[0]] = task[3]

    return tasks_period_map


def create_queue(tasks, time_span):
    queue = []

    for task in tasks:
        task_name, execution_time, deadline, period = task

        for i in range(0, time_span + 1 - period, period):
            task_deadline = i + deadline
            queue.append((task_name, execution_time, i, task_deadline))

    queue = sorted(queue, key=lambda x: (x[3], x[2]))

    print('sorted queue', queue)

    return queue


def preemptive(queue, tasks_period_map):
    output = []
    leftover = []
    task_counter = []
    job_response_time = []
    cpu_current_time = 0

    for task in queue:
        task_name, execution_time, task_start_time, task_deadline = task
        task_start_time = max(task_start_time, cpu_current_time)
        task_end_time = task_start_time + execution_time
        deadline_missed = task_end_time > task_deadline
        task_counter.append(task_name)

        job = (task_name,
               execution_time,
               task_start_time,
               task_end_time,
               deadline_missed)

        print('task_name, execution_time, task_start_time, task_end_time, deadline_missed', job)

        if not deadline_missed:
            task_count = task_counter.count(task_name)
            job_response_time.append(
                f'{task_name} Job{task_count}: {task_start_time - (task_count - 1) * tasks_period_map[task_name]}')
            cpu_current_time = task_end_time
            output.append(job)
        else:
            leftover.append(job[:-1])

    print('leftover', leftover)

    return output, leftover, job_response_time


def non_preemptive(queue, tasks_period_map):
    task_counter = []
    job_response_time = []
    leftover = []
    output = []
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

        task_count = task_counter.count(task_name)
        job_response_time.append(
            f'{task_name} Job{task_count}: {task_start_time - (task_count - 1) * tasks_period_map[task_name]}')

        cpu_current_time = task_end_time

        output.append(job)

    print('leftover', leftover)

    return output, job_response_time


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

# given_tasks = [
#     ["T1", 2, 5, 5],
#     ["T2", 2, 6, 6],
#     ["T3", 2, 7, 7],
#     ["T4", 2, 8, 8],
# ]

given_tasks = [
    ["T1", 2, 5, 5],
    ["T2", 2, 4, 6],
    ["T3", 2, 4, 7],
    ["T4", 2, 3, 6],
]

# given_tasks = [
#     ["T1", 2, 5, 5],
#     ["T2", 2, 4, 6],
#     ["T3", 3, 3, 4],
#     ["T4", 2, 3, 4],
#     ["T5", 2, 3, 4],
# ]


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
    tasks_period_map = task_period(given_tasks)
    queue = create_queue(given_tasks, span)

    primary_cpu_jobs, offloadable, primary_job_response_time = preemptive(queue, tasks_period_map)
    primary_graph_data = get_graph(primary_cpu_jobs)

    # print("Deadline missed for each task: ")
    # print(get_deadline_table(edf_jobs))
    # print(offloadable)

    # generate_gnatt_chart(primary_graph_data, 30)

    network_cpu_jobs, network_job_response_time = non_preemptive(offloadable, tasks_period_map)
    network_graph_data = get_graph(network_cpu_jobs)

    print('Primary CPU Job response time')
    for job in sorted(primary_job_response_time):
        print(job)

    if len(offloadable):
        # print('Network CPU Job response time')
        # for job in sorted(network_job_response_time):
        #     print(job)

        print('Missed job count for each task')
        for key, value in Counter([job[0] for job in offloadable]).items():
            print(key, value)

    generate_gnatt_chart(primary_graph_data, span, 'Primary CPU EDF')
    generate_gnatt_chart(network_graph_data, span, 'Network CPU EDF')
