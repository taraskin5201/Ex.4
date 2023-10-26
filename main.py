import threading
import itertools

# Глобальна змінна для зберігання сумарної кількості кроків
total_steps = 0

def collatz_steps(n):
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps

def calculate_steps_range(start, end):
    local_steps = 0
    for num in range(start, end + 1):
        steps = collatz_steps(num)
        local_steps += steps
    # Використання атомарної операції для збільшення загальної кількості кроків
    global total_steps
    total_steps += local_steps

def worker(task_range):
    calculate_steps_range(*task_range)

if __name__ == "__main__":
    N = 1000
    num_threads = 4

    # Розподіл завдань між потоками за допомогою itertools
    step = N // num_threads
    ranges = [(i * step + 1, (i + 1) * step if i != num_threads - 1 else N) for i in range(num_threads)]

    # Створення та запуск потоків
    threads = []
    for task_range in ranges:
        thread = threading.Thread(target=worker, args=(task_range,))
        thread.start()
        threads.append(thread)

    # Чекаємо завершення потоків
    for thread in threads:
        thread.join()

    # Розрахунок середньої кількості кроків
    average_steps = total_steps / N
    print(f"Середня кількість кроків для чисел від 1 до {N}: {average_steps}")
