import time
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

def factorize_sync(*numbers):
    # Синхронна версія функції factorize
    result = [factorize_single(num) for num in numbers]
    return result

def factorize_parallel(*numbers):
    # Вивести кількість робочих процесів
    num_workers = multiprocessing.cpu_count()
    print(f"Кількість робочих процесів: {num_workers}")
    
    # Паралельна версія функції factorize
    with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        futures = [executor.submit(factorize_single, num) for num in numbers]
        result = [future.result() for future in futures]
    return result  # Додано return для повернення результату

def factorize_single(num):
    # Функція для знаходження множників числа
    factors = [i for i in range(1, num + 1) if num % i == 0]
    return factors

if __name__ == '__main__':
    # Тестові дані для перевірки
    a, b, c, d = factorize_sync(10651060, 14565540, 56784010, 489400)
    assert a == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    assert b == [1, 2, 3, 4, 5, 6, 10, 11, 12, 15, 20, 22, 29, 30, 33, 44, 55, 58, 60, 66, 87, 110, 116, 132, 145, 165, 174, 220, 290, 319, 
330, 348, 435, 580, 638, 660, 761, 870, 957, 1276, 1522, 1595, 1740, 1914, 2283, 3044, 3190, 3805, 3828, 4566, 4785, 6380, 7610, 8371, 9132, 9570, 11415, 15220, 16742, 19140, 22069, 22830, 25113, 33484, 41855, 44138, 45660, 50226, 66207, 83710, 88276, 100452, 110345, 125565, 132414, 167420, 220690, 242759, 251130, 264828, 331035, 441380, 485518, 502260, 662070, 728277, 971036, 1213795, 1324140, 1456554, 2427590, 2913108, 3641385, 4855180, 7282770, 14565540]
    assert c == [1, 2, 5, 10, 23, 46, 115, 230, 239, 478, 1033, 1195, 2066, 2390, 5165, 5497, 10330, 10994, 23759, 27485, 47518, 54970, 118795, 237590, 246887, 493774, 1234435, 2468870, 5678401, 11356802, 28392005, 56784010]
    assert d == [1, 2, 4, 5, 8, 10, 20, 25, 40, 50, 100, 200, 2447, 4894, 9788, 12235, 19576, 24470, 48940, 61175, 97880, 122350, 244700, 489400]

    # Вимірюємо час виконання синхронної версії
    start_time_sync = time.time()
    result_sync = factorize_sync(10651060, 14565540, 56784010, 489400)
    end_time_sync = time.time()
    print("Результат синхронного виконання:", result_sync)
    print("Час виконання синхронного коду:", round(end_time_sync - start_time_sync, 3), "секунд")

    # Вимірюємо час виконання паралельної версії
    start_time_parallel = time.time()
    result_parallel = factorize_parallel(10651060, 14565540, 56784010, 489400)
    end_time_parallel = time.time()
    print("\nРезультат паралельного виконання:", result_parallel)
    print("Час виконання паралельного коду:", round(end_time_parallel - start_time_parallel, 3), "секунд")

