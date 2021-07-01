# 지뢰찾기

### 2021.07.01

## 지뢰찾기 셀 선택/클릭하기 (추가)

``` python
def select_cell() :
    row, col = map(int, input('SELECT CELL(row,col) : ').split())
    return row, col


def select_click() :
    print("==================================================================")
    print('SELECT MODE | OPEN : 1\tFLAG : 2 | ', end='')
    click = int(input())
    return click
```

## 지뢰찾기 셀 열기 (추가)

``` python
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
```

- 받은 좌표에 지뢰가 있다면 게임 결과는 패배. 게임이 종료된다.
- 받은 좌표에 깃발이 있다면 넘어간다
- 받은 좌표 주변에 지뢰가 주변에 지뢰가 1개 이상 있는 셀을 찾아 모두 연다(재귀)

## 지뢰찾기 셀 깃발 세우기 (추가)

``` python
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
```

- 깃발은 설치, 취소가 가능하다.
- 깃발을 세우면 `GAME_INFO`의 `num_mines` 값을 줄인다.
- 깃발은 세운 후, `GAME_INFO`의 `num_mines`값이 0이 된다면(지뢰 갯수만큼 깃발을 세웠다면) 승리 여부를 판단한다.

## 지뢰찾기 승리여부 판단하기 (추가)

``` python
def is_victory() :
    for flag in GAME_INFO['flag_pos'] :
        if flag not in GAME_INFO['mine_pos'] :
            return False
    return True
```

- 깃발을 세운 좌표가 지뢰가 설치된 좌표와 하나라도 다르다면 승리하지 못한다.

## 지뢰찾기 게임에 사용될 상수 (추가)

``` python
#FLAG
CLOSE, OPEN, FLAG = 0, 1, 2
PROGRESS,WIN,LOSE = 0,1,2
GAME_START = False
```

- 셀의 상태 플래그
- 게임 진행 상태 플래그

## 지뢰찾기 게임 정보 추가(수정) 

``` python
GAME_INFO = { # 게임 정보, 크기와 지뢰 갯수, 지뢰찾기 보드를 저장한다.
    'size': 10,
    'num_mines': 10,
    'result' : PROGRESS,
    'mine_pos' : [],
    'flag_pos' : [],
    'board': []
    # board : [ { 'mine' : 0~7/MINE,'flag' : CLOSED/OPENED/FLAGED } ]
}
```

- `num_mines` 지뢰의 갯수, 깃발이 세워지면 1씩 감소한다.
- `result` 게임 진행 상태, `PROGRESS` 진행중/`WIN` 승리/`LOSE` 패배
- `mine_pos` `set_mines()`로 생성된 지뢰의 위치 저장
- `flag_pos` 깃발을 세운 위치 저장
- `board` 의 내용에 주변 지뢰 갯수`mine` 과 현재 셀 상태`flag` 를 저장. 

## 지뢰를 모두 찾았을 경우

![](D:\Code\Python\MineSweeper\image-20210701234148630.png지뢰찾기 셀 선택/클릭하기 (추가)

``` python
def select_cell() :
    row, col = map(int, input('SELECT CELL(row,col) : ').split())
    return row, col


def select_click() :
    print("==================================================================")
    print('SELECT MODE | OPEN : 1\tFLAG : 2 | ', end='')
    click = int(input())
    return click
```

## 지뢰찾기 셀 열기 (추가)

``` python
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
```

- 받은 좌표에 지뢰가 있다면 게임 결과는 패배. 게임이 종료된다.
- 받은 좌표에 깃발이 있다면 넘어간다
- 받은 좌표 주변에 지뢰가 주변에 지뢰가 1개 이상 있는 셀을 찾아 모두 연다(재귀)

## 지뢰찾기 셀 깃발 세우기 (추가)

``` python
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
```

- 깃발은 설치, 취소가 가능하다.
- 깃발을 세우면 `GAME_INFO`의 `num_mines` 값을 줄인다.
- 깃발은 세운 후, `GAME_INFO`의 `num_mines`값이 0이 된다면(지뢰 갯수만큼 깃발을 세웠다면) 승리 여부를 판단한다.

## 지뢰찾기 승리여부 판단하기 (추가)

``` python
def is_victory() :
    for flag in GAME_INFO['flag_pos'] :
        if flag not in GAME_INFO['mine_pos'] :
            return False
    return True
```

- 깃발을 세운 좌표가 지뢰가 설치된 좌표와 하나라도 다르다면 승리하지 못한다.

## 지뢰찾기 게임에 사용될 상수 (추가)

``` python
#FLAG
CLOSE, OPEN, FLAG = 0, 1, 2
PROGRESS,WIN,LOSE = 0,1,2
GAME_START = False
```

- 셀의 상태 플래그
- 게임 진행 상태 플래그

## 지뢰찾기 게임 정보 추가(수정) 

``` python
GAME_INFO = { # 게임 정보, 크기와 지뢰 갯수, 지뢰찾기 보드를 저장한다.
    'size': 10,
    'num_mines': 10,
    'result' : PROGRESS,
    'mine_pos' : [],
    'flag_pos' : [],
    'board': []
    # board : [ { 'mine' : 0~7/MINE,'flag' : CLOSED/OPENED/FLAGED } ]
}
```

- `num_mines` 지뢰의 갯수, 깃발이 세워지면 1씩 감소한다.
- `result` 게임 진행 상태, `PROGRESS` 진행중/`WIN` 승리/`LOSE` 패배
- `mine_pos` `set_mines()`로 생성된 지뢰의 위치 저장
- `flag_pos` 깃발을 세운 위치 저장
- `board` 의 내용에 주변 지뢰 갯수`mine` 과 현재 셀 상태`flag` 를 저장. 

## 지뢰를 모두 찾았을 경우

![image-20210701234148630](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FWHYrK%2Fbtq8zywjL1h%2FkUrhzCBtdUGeIqCTniQS1k%2Fimg.png)

## 지뢰를 밟았을 경우

![image-20210702001745449](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FqXO4Z%2Fbtq8BmVX5WR%2FBTzMK2ZfoORVyka6OZHf0k%2Fimg.png)

---

### 2021.06.24 

## 지뢰찾기 보드 만들기

게임에 사용할 상수 (추가)

```python
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
```

게임 초기화 (추가)

```python
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
```

- level은 사용자 입력 `int(input())` 으로 받은 값

지뢰 생성하기

```python
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
```

- `random` 모듈의 `sample` 을 이용하여 무작위한 위치에 지뢰 생성
- `r1, r2, c1, c2`는 각 좌상,우상,좌하,우하 의 좌표값이다.
- 지뢰를 감싸고 있는 8방향의 cell 에 값을 1 더해준다.
