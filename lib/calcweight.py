import lib.board as board
#from threading import Thread
from multiprocessing import Process, Queue
import time

def _nextMove(gameboard, player, depth, maxdepth):
    if depth == maxdepth or gameboard.winner > -1:
        return gameboard.getScore(1) - gameboard.getScore(0)
    else:
        results = []
        for i in range(1, 7):
            if gameboard.cells[i + player * 7] > 0:
                nextBoard = board.Board(gameboard.cells.copy(), player)
                nextBoard.play(player, i)
                results.append(_nextMove(nextBoard, nextBoard.current_player, depth + 1, maxdepth))
        results.sort(reverse = (player == 1))
        if len(results) >= 3:
            return 0.5 * results[0] + 0.3 * results[1] + 0.2 * results[2]
        elif len(results) == 2:
            return 0.7 * results[0] + 0.3 * results[1]
        elif len(results) == 1:
            return results[0]

def calcMove(gameboard, aiplayer, maxdepth):
    start = time.time()
    # results = [-99999] * 7
    # currentmax = 0
    threads = []
    queue = Queue()
    maxmove = 0
    maxscore = -99999
    for i in range(1, 7):

        if gameboard.cells[i + gameboard.current_player * 7] > 0:
            nextBoard = board.Board(gameboard.cells.copy(), gameboard.current_player)
            nextBoard.play(gameboard.current_player, i)
            # results[i] = _nextMove(nextBoard, gameboard.current_player, 0, maxdepth)
            threads.append(MancThread(queue, nextBoard, gameboard.current_player, maxdepth, i)) 
            threads[-1].start()
            # if aiplayer == 0:
            #     results[i] *= -1
            # if results[i] > results[currentmax]:
            #     currentmax = i
            #     #print(result)
    for thread in threads:
        thread.join()

    while not queue.empty():
        score, move = queue.get()
        if aiplayer == 0:
            score *= -1
        if score > maxscore:
            maxscore = score
            maxmove = move
    print(f"Threaded: elapsed time = {time.time() - start} seconds")
    #print(f"suggested move: {maxmove}")
    return maxmove

    start = time.time()
    results = [-99999] * 7
    currentmax = 0
    for i in range(1, 7):

        if gameboard.cells[i + gameboard.current_player * 7] > 0:
            nextBoard = board.Board(gameboard.cells.copy(), gameboard.current_player)
            nextBoard.play(gameboard.current_player, i)
            results[i] = _nextMove(nextBoard, gameboard.current_player, 0, maxdepth)
            if aiplayer == 0:
                results[i] *= -1
            if results[i] > results[currentmax]:
                currentmax = i
                #print(result)
    print(f"Nonethreaded: elapsed time = {time.time() - start} seconds")
    return currentmax

class MancThread(Process):
    def __init__(self, queue, gameboard, aiplayer, maxdepth, move):
        super().__init__()
        self.queue = queue
        self.gameboard = gameboard
        self.player = aiplayer
        self.maxdepth = maxdepth
        self.move = move
        self.score = -99999
    def run(self) -> None:
        self.queue.put((_nextMove(self.gameboard, self.player, 0, self.maxdepth), self.move))