import lib.game as game
import lib.calcweight as calcweight
import time

if __name__ == "__main__":
    depthstr = input("Bot AI depth (default 8): ")
    if depthstr.isnumeric():
        if 10 > int(depthstr) > 0:
            maxdepth = int(depthstr)
        else:
            maxdepth = 8
    else:
        maxdepth = 8
    testgame = game.Game(player = 1)
    print(testgame.draw())
    while testgame.winner < 0:
        while testgame.current_player == 0:      # human player
            move = ''
            while not move.isnumeric():
                move = input("Your move: ")
            if move == '0':
                break
            testgame.play(testgame.current_player, int(move))
            print(testgame.draw())
            if testgame.winner > -1:
                break
        while testgame.current_player == 1:              # bot
            aiMove = calcweight.calcMove(testgame, 1, maxdepth)
            if aiMove > 0:
                print(f'AI moves {aiMove}')
                testgame.play(testgame.current_player, aiMove, True)
                print(testgame.draw())
                time.sleep(1)
                if testgame.winner > -1:
                    break
            else:
                break
    else:
        print("Game over! The winner is " + ("you", "bot")[testgame.winner] + "!")