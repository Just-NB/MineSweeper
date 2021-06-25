from random import sample
#LEVEL
DEFAULT,EASY,NORMAL,HARD,EXIT = 1,1,2,3,4

MINE = 99 # 보드에서 지뢰일때 99로 저장
NUM_MINES = {1: 10, 2: 33, 3: 99} # 레벨별 마인 갯수
BOARD_SIZE = {1: 5, 2: 10, 3: 15} # 레벨별 보드 크기

GAME_INFO = { # 게임 정보, 크기와 지뢰 갯수, 지뢰찾기 보드를 저장한다.
    'Size': 10,
    'NumMines': 10,
    'Board': []
}


# level (int type) 은 사용자 입력으로 받는다.
def init_game(level : int):
    global GAME_INFO # 전역변수로 있는 게임정보를 가져온다.
    # 난이도별로 지뢰갯수,크기를 설정한다.
    if level == EASY:
        GAME_INFO['NumMines'] = NUM_MINES[EASY]
        GAME_INFO['Size'] = BOARD_SIZE[EASY]
    elif level == NORMAL:
        GAME_INFO['NumMines'] = NUM_MINES[NORMAL]
        GAME_INFO['Size'] = BOARD_SIZE[NORMAL]
    elif level == HARD:
        GAME_INFO['NumMines'] = NUM_MINES[HARD]
        GAME_INFO['Size'] = BOARD_SIZE[HARD]
    else :
        GAME_INFO['NumMines'] = NUM_MINES[DEFAULT]
        GAME_INFO['Size'] = BOARD_SIZE[DEFAULT]

    # 지뢰찾기 보드는 초기값으로 0 전부 채워둔다.
    GAME_INFO['Board'] = []
    for height in range(GAME_INFO['Size']):
        GAME_INFO['Board'].append([0]*GAME_INFO['Size'])


def set_mines():
    global GAME_INFO # 전역변수로 있는 게임정보를 가져온다.
    size = GAME_INFO['Size']
    num_mines = GAME_INFO['NumMines']
    cand_mines = [] # 마인이 될 수 있는 위치
    for r in range(size):
        for c in range(size):
            cand_mines.append((r, c))

    pos_mines = sample(cand_mines, num_mines) # 마인의 위치를 랜덤하게 뽑는다.
    # 8 방향
    for row, col in pos_mines:
        r1, r2 = max(row-1,0), min(row+1, size-1)
        c1, c2 = max(col-1,0), min(col+1, size-1)
        # 인접(8방향)한 칸에 지뢰 갯수 추가하기
        for r in range(r1, r2+1):
            for c in range(c1, c2+1):
                if r == row and c == col: # 현재 위치는 지뢰
                    GAME_INFO['Board'][r][c] = MINE
                else:
                    if GAME_INFO['Board'][r][c] != MINE: # 만약 인접한 곳이 지뢰가 아니라면
                        GAME_INFO['Board'][r][c] += 1 # 1을 더해준다.


if __name__ == '__main__':
    while True :
        print('============= Enter the level of difficulty you want =============')
        print(' LEVEL(Num of Mines) | 1. EASY(10) | 2. NORMAL(20) | 3. HARD(30)')
        print("============================ EXIT : 4 ============================")
        level = int(input('LEVEL\t:\t'))
        if level == EXIT:
            break
        init_game(level)
        print(f'Mines\t:\t{GAME_INFO["NumMines"]}\t | Size : {GAME_INFO["Size"]}')
        print("==================================================================")
        set_mines()
        for b in GAME_INFO['Board']:
            for t in b:
                if t == 99:
                    print('#', end=' ')
                else :
                    print(t, end=' ')
            print()
        print()



