from multiprocessing import Process, Pool

def element(index, m1, m2):
    i, j = index
    res = 0
    N = len(m1[0]) or len(m2)
    for k in range(N):
        res += m1[i][k] * m2[k][j]
    with open('result.txt', 'a', encoding='utf-8') as file:
        if i == 0 and j == 0:
            file.write(str(res) + " ")
        elif j == 0:
            file.write("\n" + str(res) + " ")
        else:
            file.write(str(res) + " ")
    return res

if __name__ == '__main__':

    with open('matrix1.txt') as f:
        matrix1 = [list(map(int, row.split())) for row in f.readlines()]

    with open('matrix2.txt') as f:
        matrix2 = [list(map(int, row.split())) for row in f.readlines()]

    number_of_processes = len(matrix1) * len(matrix2[0])

    positions = []
    for i in range(len(matrix1)):
        for j in range(len(matrix2[0])):
            positions.append((i, j))

    pool = Pool(processes=number_of_processes)
    for position in positions:
        result = pool.apply(element, (position, matrix1, matrix2))

    # for position in positions:
    #     p = Process(target=element, args=[position, matrix1, matrix2])
    #     p.start()
    #     print("PID запущенного процесса:", p.pid)
    #     p.join()