
import sys
from math import sqrt
from random import randint
import pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, K_RETURN, K_BACKSPACE,\
    K_LEFT, K_RIGHT, K_DOWN, K_SPACE, K_z, K_x
import time

BLOCK_DATA = (
    (
        (0, 0, 1,
         1, 1, 1,
         0, 0, 0),
        (0, 1, 0,
         0, 1, 0,
         0, 1, 1),
        (0, 0, 0,
         1, 1, 1,
         1, 0, 0),
        (1, 1, 0,
         0, 1, 0,
         0, 1, 0),
    ), (
        (2, 0, 0,
         2, 2, 2,
         0, 0, 0),
        (0, 2, 2,
         0, 2, 0,
         0, 2, 0),
        (0, 0, 0,
         2, 2, 2,
         0, 0, 2),
        (0, 2, 0,
         0, 2, 0,
         2, 2, 0)
    ), (
        (0, 3, 0,
         3, 3, 3,
         0, 0, 0),
        (0, 3, 0,
         0, 3, 3,
         0, 3, 0),
        (0, 0, 0,
         3, 3, 3,
         0, 3, 0),
        (0, 3, 0,
         3, 3, 0,
         0, 3, 0)
    ), (
        (4, 4, 0,
         0, 4, 4,
         0, 0, 0),
        (0, 0, 4,
         0, 4, 4,
         0, 4, 0),
        (0, 0, 0,
         4, 4, 0,
         0, 4, 4),
        (0, 4, 0,
         4, 4, 0,
         4, 0, 0)
    ), (
        (0, 5, 5,
         5, 5, 0,
         0, 0, 0),
        (0, 5, 0,
         0, 5, 5,
         0, 0, 5),
        (0, 0, 0,
         0, 5, 5,
         5, 5, 0),
        (5, 0, 0,
         5, 5, 0,
         0, 5, 0)
    ), (
        (6, 6, 6, 6),
        (6, 6, 6, 6),
        (6, 6, 6, 6),
        (6, 6, 6, 6)
    ), (
        (0, 7, 0, 0,
         0, 7, 0, 0,
         0, 7, 0, 0,
         0, 7, 0, 0),
        (0, 0, 0, 0,
         7, 7, 7, 7,
         0, 0, 0, 0,
         0, 0, 0, 0),
        (0, 0, 7, 0,
         0, 0, 7, 0,
         0, 0, 7, 0,
         0, 0, 7, 0),
        (0, 0, 0, 0,
         0, 0, 0, 0,
         7, 7, 7, 7,
         0, 0, 0, 0)
    )
)


class Block:

    def __init__(self, count):
        self.turn = randint(0, 3)      # 블록의 방향(0~3)
        self.type = BLOCK_DATA[randint(0, 6)]  # 블럭(0~6), 2차원 데이터
        self.data = self.type[self.turn]      # 블럭의 한방향 모양, 1차원 데이터
        self.size = int(sqrt(len(self.data)))  # 2~4
        self.xpos = randint(2, 8 - self.size)  # 블럭의 x좌표 / 블럭의 생성위치
        self.ypos = 1 - self.size  # 블럭의 y좌표 (블럭의 맨 밑의 줄부터 보이기 시작)
        self.fire = count + INTERVAL  # 블럭이떨어지는 시간 설정

    def update(self, count):
        '''블록 상태 갱신'''

        erased = 0
        #bomb = 0
        if is_overlapped(self.xpos, self.ypos + 1, self.turn):
            # is_overlapped()함수를 먼저 실행하여 True가 나오면 밑에 식을 실행 => 셀에 블럭을 저장
            # 현재블럭을 y좌표에 1을 더해 한칸 더 밑으로 갔을 때 충돌이 일어나는 지 본다.
            for y_offset in range(BLOCK.size):
                # 이 이중 for반복문은 하나의 블럭 1차원데이터를 셀하나하나 보는 것
                for x_offset in range(BLOCK.size):
                    if 0 <= self.xpos+x_offset < WIDTH and \
                            0 <= self.ypos+y_offset < HEIGHT:
                        val = BLOCK.data[y_offset*BLOCK.size
                                         + x_offset]
                        if val != 0:
                            FIELD[self.ypos+y_offset][self.xpos+x_offset] = val

            erased = erase_line()  # 밑의 erase_line()함수 실행
            go_next_block(count)  # 다음 블럭으로 전환
            #Bomb = Bomb_line

            '''
            if erased % 2 ==0:
                bomb+=1'''

        # 블럭 낙하 (시간이 지날수록 빨라짐)  # self.fire = 40+40 =80 # count는 계속 5씩 증가
        if self.fire < count:
            self.fire = count + INTERVAL
            self.ypos += 1
        return erased

    def draw(self):
        # 블럭을 그리는 메서드
        for index in range(len(self.data)):
            xpos = index % self.size
            ypos = index // self.size
            val = self.data[index]
            if 0 <= ypos + self.ypos < HEIGHT and \
               0 <= xpos + self.xpos < WIDTH and val != 0:
                x_pos = 25 + (xpos + self.xpos) * 25
                # 한 셀의 크기가 25이므로 벽을 먼저 두고 다음에 ( xpos(블럭의 한셀 x위치) + 블럭의 x위치)*25를 하여 블럭을 그릴 좌표를 구함
                y_pos = 25 + (ypos + self.ypos) * 25
                pygame.draw.rect(SURFACE, COLORS[val],
                                 (x_pos, y_pos, 24, 24))  # 24,24로 그리는 이유는 블럭 사이사이 검정선을 표현


'''
score_str = None
class Score:
    score_list = []
    def __init__(self,name):
        global score_str
        self.score = score_str
        self.name = name
        self.score_list.append([name,score_str])
'''


def erase_line():
    # 행이 모두 채워진 줄을 지움
    erased = 0
    ypos = 20   # Field의 Height은 22지만 index로는 0~21이라서 맨아래 바닥을 제외한 20부터 시작
    while ypos >= 0:
        if all(FIELD[ypos]):  # all함수는 인수의 배열요소가 모두 True면 True반환, 모든 숫자가 0이 아니면
            erased += 1
            del FIELD[ypos]
            # 다 채워진 맨 아래줄은지우고 맨 위에 새로운 줄을 생성
            FIELD.insert(0, [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8])
            sounderased = pygame.mixer.Sound(
                'D:\pygame\부산대_빅데이터_김민수/erased.wav')
            sounderased.play()
            '''
            >>> a=[[1],[2]]
            >>> a.insert(0,[0])
            >>> a
            [[0], [1], [2]]
            >>> a.insert(1,[100])
            >>> a
            [[0], [100], [1], [2]]
            '''
        else:
            ypos -= 1
    return erased


def is_game_over():

    filled = 0
    for cell in FIELD[0]:  # 가장 윗줄
        if cell != 0:
            filled += 1
    return filled > 2  # 2는 양쪽 벽의 셀에 8이 들어가서 2초과로 잡음


def go_next_block(count):       # 블록 객체를 생성, 객체(BLOCK, NEXT_BLOCK)는 모두 대문자, 클래스는 Block 맨 앞만 대문자
    # 다음블럭으로 전환
    global BLOCK, NEXT_BLOCK
    BLOCK = NEXT_BLOCK if NEXT_BLOCK != None else Block(count)
    '''
    if NEXT_BLOCK != None:
        BLOCK = NEXT_BLOCK
    else:
        BLOCK = Block(count)
    '''
    NEXT_BLOCK = Block(count)


def is_overlapped(xpos, ypos, turn):
    # 블록이 다른 블럭이나 바닥의 블럭과 충돌을 하는지를 보는 함
    data = BLOCK.type[turn]
    for y_offset in range(BLOCK.size):
        for x_offset in range(BLOCK.size):
            if 0 <= xpos+x_offset < WIDTH and \
                    0 <= ypos+y_offset < HEIGHT:
                if data[y_offset*BLOCK.size + x_offset] != 0 and \
                        FIELD[ypos+y_offset][xpos+x_offset] != 0:  # 충돌이 일어난다면 True를 반환
                    return True
    return False

# 하드드랍 함수


def Hard(xpos, ypos, turn):

    while not is_overlapped(xpos, ypos, turn):
        ypos += 1
        if is_overlapped(xpos, ypos, turn) == True:
            BLOCK_drop = ypos - 1
            break
    return BLOCK_drop


'''
# 폭탄 아이템 함수
def Bomb_line():
    global bomb
    for ypos in range(18,21):
        del FIELD[ypos]
        FIELD.insert(0, [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8])
    bomb-=1
    return bomb
'''


pygame.init()  # 초기화
pygame.display.set_caption("Tetris")  # 창 제목 설정
#pygame.key.set_repeat(30, 30)
SURFACE = pygame.display.set_mode([600, 600])  # 전체 창 설정
FPSCLOCK = pygame.time.Clock()
WIDTH = 12  # 게임이 실행되는 영역의 가로칸(x축)의 개수(양쪽의 벽을 포함한 개수)
HEIGHT = 22  # 게임이 실행되는 영역의 세로칸(y축)의 개수(아래의 벽을 포함한 개수)
INTERVAL = 40  # 낙하시간 40 설정
FIELD = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
COLORS = ((0, 0, 0), (255, 165, 0), (0, 0, 255), (0, 255, 255),
          (0, 255, 0), (255, 0, 255), (255, 255, 0), (255, 0, 0), (128, 128, 128))
BLOCK = None
NEXT_BLOCK = None
ToRestart = False
Drop = True


# 초기화
def init():
    global SURFACE, FPSCLOCK, WIDTH, HEIGHT, INTERVAL, FIELD, COLORS, BLOCK, NEXT_BLOCK, ToRestart

    pygame.init()
    #pygame.key.set_repeat(30, 30)
    SURFACE = pygame.display.set_mode([600, 600])
    FPSCLOCK = pygame.time.Clock()
    WIDTH = 12  # 게임이 실행되는 영역의 가로칸(x축)의 개수(양쪽의 벽을 포함한 개수)
    HEIGHT = 22  # 게임이 실행되는 영역의 세로칸(y축)의 개수(아래의 벽을 포함한 개수)
    INTERVAL = 40  # 낙하시간 40 설정
    FIELD = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    COLORS = ((0, 0, 0), (255, 165, 0), (0, 0, 255), (0, 255, 255),
              (0, 255, 0), (255, 0, 255), (255, 255, 0), (255, 0, 0), (128, 128, 128))
    BLOCK = None
    NEXT_BLOCK = None
    ToRestart = False
    Drop = True


def main():
    soundbgm = pygame.mixer.Sound('D:\pygame\부산대_빅데이터_김민수/bgm.ogg')  # bgm 실행
    soundbgm.play(-1)  # 무한반복

    global ToRestart
    global INTERVAL  # 40
    count = 0
    score = 0
    game_over = False
    # pygame.font.SysFont('글꼴',크기,굵기여부,기울기여부)
    smallfont = pygame.font.SysFont(None, 36)  # 점수를 나타낼 폰트
    largefont = pygame.font.SysFont(None, 72)  # game over를 나타낼 폰트
    restartfont = pygame.font.SysFont(None, 50)
    # font명.render('텍스트', antialias여부, 텍스트 색 지정, 텍스트 배경색 지정 )
    message_over = largefont.render("GAME OVER!!",
                                    True, (0, 255, 225))
    message_rect = message_over.get_rect()  # 사각형의 틀을 만든다
    message_rect.center = (300, 300)    # 사각형틀의 중심이 해당좌표에 위치하도록 한다.

    # 재시작 메세지 만들기
    message_restart = restartfont.render(
        'Replay (press r)', True, (0, 255, 225))
    message_rect2 = message_restart.get_rect()
    message_rect2.center = (300, 400)

    '''효과음 삽입 '''
    soundstart = pygame.mixer.Sound(
        'D:\pygame\부산대_빅데이터_김민수/start.ogg')   # 사운드 파일을 로딩
    soundend = pygame.mixer.Sound('D:\pygame\부산대_빅데이터_김민수/end.wav')
    sounderased = pygame.mixer.Sound('D:\pygame\부산대_빅데이터_김민수/erased.wav')
    soundbomb = pygame.mixer.Sound('D:\pygame\부산대_빅데이터_김민수/bomb.ogg')
    soundstart.play()

    '''점수 기록 '''
    '''
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(200, 500, 140, 32) # Rect (왼쪽, 위쪽, 너비, 높이)
    color_inactive = pygame.Color((255,255,255))
    color_active = pygame.Color((0,225,255))
    color = color_inactive
    active = False
    text = ''
    done = False
    '''

    go_next_block(INTERVAL)  # 함수실행 => 블럭 객체 생성

    for ypos in range(HEIGHT):    # 게임이 진행되는 FIeld영역의 셀에 0과 8을 채우는 작업
        for xpos in range(WIDTH):
            FIELD[ypos][xpos] = 8 if xpos == 0 or \
                xpos == WIDTH - 1 else 0
    for index in range(WIDTH):
        FIELD[HEIGHT-1][index] = 8

    while True:
        key = None
        for event in pygame.event.get():  # 사용자 입력을 처
            # pygame.event.get() 함수는 게임의 이벤트 큐에 있는 모든 이벤트를 순서열로 만들어 반환한다.
            if event.type == QUIT:  # 해당event의 type
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:  # 해당event의 type # Keydown은 눌렀다가 땠을 때
                key = event.key  # event.key는  K_LEFT, K_RIGHT, K_DOWN, K_SPACE 등,  key에 저장
            '''
            # 점수 기록 (점수판 ) 
            elif event.type == MOUSEBUTTONDOWN:
                # 이름 입력 칸 클릭 
                if input_box.collidepoint(event.pos):
                    
                    # collidepoint는 점이 자신에게 포함되는지 아닌지 여부 반환
                    # ex) collidepoint(x, y) : (x, y)라는 점이 자신에게 포함되는지 아닌지 여부 반환
                    
                    active = not active
                else:
                    active = False
                # 클릭시 바꾸기 
                color = color_active if active else color_inactive

            elif event.type == KEYDOWN:
                if active:
                    if event.key == K_RETURN:
                        userName = text
                        userName = Score(userName)
                        N = len(Score.score_list)
                        for i in range(N-1):
                            for j in range(i+1,N):
                                if Score.score_list[i][1] > Score.score_list[j][1]:
                                    Score.score_list[i],Score.score_list[j] = Score.score_list[j],Score.score_list[i]
                        print('User\tScore')
                        for i in Score.score_list[0:5]:
                            print(i[0],'\t',i[1])
                        text = ''
                        break
                    elif event.key == K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                '''

        game_over = is_game_over()  # 함수 실행
        if not game_over:
            count += 5  # count가 5초씩 증가
            if count % 1000 == 0:
                # count가 1000의 배수가 될때마다 interval이 2씩 줄어들고 1과 interval중 최댓값을 가져옴
                INTERVAL = max(1, INTERVAL - 2)
            erased = BLOCK.update(count)  # 블럭의 상태를 갱신

            if erased > 0:
                score += (2 ** erased) * 100  # 점수 # 한번에 삭제하는 줄이 많을수록 점수가 높아짐

            # 키 이벤트
            next_x, next_y, next_t = \
                BLOCK.xpos, BLOCK.ypos, BLOCK.turn  # BLOCK.turn에는 난수로 설정된 숫자가 들어가 있음
            if key == K_SPACE:
                # 키 반복을 비활성화  # 홀드 키 반복 방법 제어 pygame.key.set_repeat(delay,interval)
                pygame.key.set_repeat()
                next_t = (next_t + 1) % 4  # 블럭의 방향을 변경
            elif key == K_RIGHT:
                next_x += 1     # 오른쪽 이동
            elif key == K_LEFT:
                next_x -= 1     # 왼쪽 이동
            elif key == K_DOWN:
                next_y += 1     # 아래로 이동

            elif key == K_z:   # 하드드랍
                next_y = Hard(BLOCK.xpos, BLOCK.ypos,
                              BLOCK.turn)  # 충돌 전까지 내린 y좌표를 받음

            if not is_overlapped(next_x, next_y, next_t):
                # is_overlapped함수는 충돌할 때 True이므로 충돌이 일어나지 않을때 아래가 실행
                # 즉, 충돌이 일어나지 않으면 이동하거나 변경한 방향이 블럭객체의 속성에 저장
                BLOCK.xpos = next_x
                BLOCK.ypos = next_y
                BLOCK.turn = next_t
                BLOCK.data = BLOCK.type[BLOCK.turn]

            # elif key == K_x:
            #    Bomb_line()

        SURFACE.fill((0, 0, 0))  # 전체를 검정색으로 칠함
        for ypos in range(HEIGHT):
            for xpos in range(WIDTH):
                val = FIELD[ypos][xpos]
                pygame.draw.rect(SURFACE, COLORS[val],
                                 (xpos*25 + 25, ypos*25 + 25, 24, 24))  # 게임 필드의 기본적인 틀을 그림
        BLOCK.draw()  # 블럭객체를 그림

        # 다음 블럭 그리기 (점수판 밑에)
        for ypos in range(NEXT_BLOCK.size):
            for xpos in range(NEXT_BLOCK.size):
                val = NEXT_BLOCK.data[xpos + ypos*NEXT_BLOCK.size]
                pygame.draw.rect(SURFACE, COLORS[val],
                                 (xpos*25 + 460, ypos*25 + 100, 24, 24))

        '''
        # 폭탄 개수 나타내기 
        bomb_set = 'x'+str(bomb).zfill(3)
        bomb_count = smallfont.render(bomb_set,True,(255,255,255))
        SURFACE.blit(bomb_count,(500,400))'''

        # 점수 나타내기
        score_str = str(score).zfill(6)  # 000000 # str(score).rjust(6,'0')도 가능
        score_image = smallfont.render(score_str,
                                       True, (0, 255, 0))  # Surface에 텍스트 쓰기
        SURFACE.blit(score_image, (500, 30))  # blit을 이용하여 위치설정

        if game_over:
            soundbgm.stop()  # bgm 정지

            soundend.play()
            time.sleep(1)
            soundend.stop()
            SURFACE.blit(message_over, message_rect)  # game_over메세지 나타내기
            SURFACE.blit(message_restart, message_rect2)  # restart메세지 나타내기
            ToRestart = True

            '''입력창 '''
            '''
            #SURFACE.fill((30, 30, 30))
            txt_surface = font.render(text, True, color)
            # 입력창 크기조절 
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width #Rect 객체의 속성 ,width(너비)를 나타냄 
            # 입력칸을 배치 
            SURFACE.blit(txt_surface, (input_box.x+5, input_box.y+5))
            # pygame.draw.rect(Surface, color, Rect, Width=0) # Rect는 [x축, y축, 가로, 세로]의 형태로 삽입가능 
            pygame.draw.rect(SURFACE, color, input_box, 2)
            '''

        pygame.display.update()  # ()안에 아무 것도 넣지않으면 Surface전체를 업데이트
        '''
        pygame.display.flip()                           # 화면 전체를 업데이트
 
        화면의 일부만 업데이트할 경우
        pygame.display.update(rectangle)                # 업데이트할 rectangle을 지정
        pygame.display.update(rectangle_list)           # 업데이트할 rectangle을 여러개 지정

        '''
        FPSCLOCK.tick(15)  # FPS(초당 프레임)를 설정 # 초당 15번화면 출력

        # r키를 누르면 재시작 가능하도록 설정
        while ToRestart:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == pygame.K_r:
                    ToRestart = False
                    break
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    break
            if ToRestart == False:
                init()
                main()
                break


def start_screen():  # 시작화면 함수 설정

    SURFACE.fill((0, 0, 0))
    largefont = pygame.font.SysFont(None, 72)
    message_start = largefont.render(
        "Press any key to play", True, (255, 255, 255))
    message_rect3 = message_start.get_rect()
    message_rect3.center = (300, 300)
    SURFACE.blit(message_start, message_rect3)
    pygame.display.update()
    FPSCLOCK.tick(10)


if __name__ == '__main__':  # 시작화면 => 게임 화면
    waiting = True
    while waiting:
        start_screen()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                break
            if event.type == KEYUP:
                waiting = False
                break
        if waiting == False:
            main()
            break
