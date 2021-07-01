from random import sample

#LEVEL
DEFAULT, EASY, NORMAL, HARD, EXIT = 1, 1, 2, 3, 4
#FLAG
CLOSE, OPEN, FLAG = 0, 1, 2
PROGRESS,WIN,LOSE = 0,1,2
GAME_START = False

MINE = 99 # 보드에서 지뢰일때 99로 저장
NUM_MINES = {1: 10, 2: 33, 3: 99} # 레벨별 마인 갯수
BOARD_SIZE = {1: 5, 2: 10, 3: 15} # 레벨별 보드 크기

GAME_INFO = { # 게임 정보, 크기와 지뢰 갯수, 지뢰찾기 보드를 저장한다.
    'size': 10,
    'num_mines': 10,
    'result' : PROGRESS,
    'mine_pos' : [],
    'flag_pos' : [],
    'board': []
    # board : [ { 'mine' : 0~7/MINE,'flag' : CLOSED/OPENED/FLAGED } ]
}


# level (int type) 은 사용자 입력으로 받는다.
def init_game(level : int):
    global GAME_INFO  # 전역변수로 있는 게임정보를 가져온다.
    # 난이도별로 지뢰갯수,크기를 설정한다.
    if level == EASY:
        GAME_INFO['num_mines'] = NUM_MINES[EASY]
        GAME_INFO['size'] = BOARD_SIZE[EASY]
    elif level == NORMAL:
        GAME_INFO['num_mines'] = NUM_MINES[NORMAL]
        GAME_INFO['size'] = BOARD_SIZE[NORMAL]
    elif level == HARD:
        GAME_INFO['num_mines'] = NUM_MINES[HARD]
        GAME_INFO['size'] = BOARD_SIZE[HARD]
    else :
        GAME_INFO['num_mines'] = NUM_MINES[DEFAULT]
        GAME_INFO['size'] = BOARD_SIZE[DEFAULT]

    # 지뢰찾기 보드는 초기값으로 0 전부 채워둔다.
    GAME_INFO['board'] = []
    for height in range(GAME_INFO['size']):
        GAME_INFO['board'].append([{'mine': 0, 'flag': CLOSE} for _ in range(GAME_INFO['size'])])


def set_mines():
    global GAME_INFO # 전역변수로 있는 게임정보를 가져온다.
    size = GAME_INFO['size']
    num_mines = GAME_INFO['num_mines']
    cand_mines = []  # 마인이 될 수 있는 위치
    for r in range(size):
        for c in range(size):
            cand_mines.append((r, c))

    GAME_INFO['mine_pos'] = sample(cand_mines, num_mines) # 마인의 위치를 랜덤하게 뽑는다.
    # 8 방향
    for row, col in GAME_INFO['mine_pos']:
        r1, r2 = max(row-1,0), min(row+1, size-1)
        c1, c2 = max(col-1,0), min(col+1, size-1)
        # 인접(8방향)한 칸에 지뢰 갯수 추가하기
        for r in range(r1, r2+1):
            for c in range(c1, c2+1):
                cell = GAME_INFO['board'][r][c]
                if r == row and c == col:  # 현재 위치는 지뢰
                    cell['mine'] = MINE
                else:
                    if cell['mine'] != MINE:  # 만약 인접한 곳이 지뢰가 아니라면
                        cell['mine'] += 1  # 1을 더해준다.


def open_cell(row,col) :
    board = GAME_INFO['board']
    if (row,col) in GAME_INFO['mine_pos']:  # 만약 입력된 좌표에 지뢰가 있다면
        GAME_INFO['result'] = LOSE
        for (r,c) in GAME_INFO['mine_pos']:  # 지뢰를 전부 열고 종료합니다.
            board[r][c]['flag'] = OPEN
        return
    cell = board[row][col]
    if cell['flag'] == OPEN or cell['flag'] == FLAG:  # 이미 열려있거나 깃발을 세웠으면 넘어간다.
        return

    cell['flag'] = OPEN
    size = GAME_INFO['size']
    if cell['mine'] == 0 :  # 주변에 지뢰가 없다면 전부 연다.
        r1,r2 = max(row-1,0), min(row+1, size-1)
        c1,c2 = max(col-1,0), min(col+1, size-1)
        for r in range(r1, r2+1) :
            for c in range(c1, c2+1) :
                open_cell(r,c)


# 깃발은 설치,취소 가능
def flag_cell(row,col) :
    flag_pos = GAME_INFO['flag_pos']
    board = GAME_INFO['board']
    cell = board[row][col]
    if cell['flag'] == OPEN: # 만약 열려있는 곳이면 넘어간다.
        return
    elif cell['flag'] == CLOSE: # 만약 닫혀있는 곳이면 깃발을 세운다.
        cell['flag'] = FLAG
        flag_pos.append((row,col))
        GAME_INFO['num_mines'] -= 1
    elif cell['flag'] == FLAG: # 만약 깃발이 세워진 곳이면 닫혀있는 상태로 돌린다.
        cell['flag'] = CLOSE
        flag_pos.remove((row,col))
        GAME_INFO['num_mines'] += 1
    # 만약 지뢰 갯수만큼만 깃발을 세웠고, 그 깃발들이 모두 정확한 위치에 깃발을 세웠다면 승리.
    if GAME_INFO['num_mines'] == 0 and is_victory():
        GAME_INFO['result'] = WIN

def is_victory() :
    for flag in GAME_INFO['flag_pos'] :
        if flag not in GAME_INFO['mine_pos'] :
            return False
    return True


def select_cell() :
    row, col = map(int, input('SELECT CELL(row,col) : ').split())
    return row, col


def select_click() :
    print("==================================================================")
    print('SELECT MODE | OPEN : 1\tFLAG : 2 | ', end='')
    click = int(input())
    return click


def print_board() :
    print(f'Mines\t:\t{GAME_INFO["num_mines"]}\t | Size : {GAME_INFO["size"]}')
    print("==================================================================")
    for board in GAME_INFO['board']:
        for col in range(GAME_INFO['size']):
            cell = board[col]
            if cell['flag'] == CLOSE:
                print('#', end=' ')
            elif cell['flag'] == OPEN:
                if cell['mine'] == MINE :
                    print('x', end=' ')
                else:
                    print(cell['mine'], end=' ')
            elif cell['flag'] == FLAG:
                print('?', end=' ')
        print()


if __name__ == '__main__':
    print('============= Enter the level of difficulty you want =============')
    print(' LEVEL(Num of Mines) | 1. EASY(10) | 2. NORMAL(20) | 3. HARD(30)')
    print("============================ EXIT : 4 ============================")
    level = int(input('LEVEL\t:\t'))
    init_game(level)
    set_mines()
    while True:
        print_board()
        if GAME_INFO['result'] == LOSE :
            print("GAME OVER")
            break
        elif GAME_INFO['result'] == WIN :
            print("WIN")
            break
        click = select_click()
        row, col = select_cell()
        if click == OPEN:
            open_cell(row, col)
        elif click == FLAG:
            flag_cell(row, col)