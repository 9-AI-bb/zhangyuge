import time
import multiprocessing


# 定义一个简单的任务函数
def worker_func(num):
    print(f"Worker {num} is running")
    time.sleep(2)  # 模拟耗时任务
    print(f"Worker {num} is done")


def test_process_pool_runtime(processes):
    # 创建进程池
    with multiprocessing.Pool(processes=processes) as pool:
        # 提交任务到进程池
        start_time = time.time()
        pool.map(worker_func, range(10))  # 提交10个任务到进程池
        end_time = time.time()
        print(f"Process pool with {processes} processes took {end_time - start_time} seconds")


if __name__ == "__main__":
    # 测试不同进程数量下的运行时长
    for processes in [1, 2, 4, 8, 10]:
        test_process_pool_runtime(processes)
