#라이브러리
import pygame
import sys 
import random
import timeit
import math
from time import sleep 
from time import time


padWidth = 1200 # 게임화면의 가로크기
padHeight = 800 # 게임화면의 세로크기


pygame.init() # 초기화

gamePad = pygame.display.set_mode((padWidth, padHeight)) # 해상도 설정


### 컬러 지정( 필요할 경우 사용 )
# black    = (   0,   0,   0 )
# white    = ( 255, 255, 255 )
# green    = (   0, 255,   0 )
# red      = ( 255,   0,   0 )


frame_count = 0 # 초당 프레임 분자 초기값
frame_rate = 60 # 초당 프레임 분모 초기값
key = [0,0,0,0] # 키 조작 배열 초기값
rock_list = [] # 바위 배열 초기값
explosion_list = [] # 폭발 배열 초기값
onGame = False

clock = pygame.time.Clock() # 시간 설정

rockImage = ['rock01.png', 'rock02.png', 'rock03.png', 'rock04.png','rock05.png']
explosionSound = ['explosion01.wav', 'explosion02.wav', 'explosion03.wav', 'explosion04.wav' ]


# 운석 맞춘 개수 계산
def writeScore(count):
    
    global gamePad
    
    font = pygame.font.Font('BMDOHYEON.ttf', 20)
    text = font.render('파괴한 운석 수:' + str(count), True, (255, 255, 255))
    gamePad.blit(text,(10,10)) # blit(블록전송)은 'bit block image transfer'의 약어 / a메모리-> b메모리로 '그래픽'과 관련된 데이터 블록 전송
    

# 운석이 화면 아래로 통과한 개수
def writePassed(count):
    
    global gamepad
    
    font = pygame.font.Font('BMDOHYEON.ttf', 20)
    text = font.render('놓친 운석 :' + str(count), True, ( 255, 255, 255 ))
    gamePad.blit(text,(10, 35))


# 타이머
def timer():
    
    global gamePad
    global rock_list
    global key
    global gameClearSound
    global frame_count

    # 시간 출력 계산
    total_seconds = frame_count // frame_rate
    
    minutes = total_seconds // 60
    
    seconds = total_seconds % 60

    
    output_string = "Time: {0:02}:{1:02}".format(minutes, seconds) # 경과된 시간 출력      
    font = pygame.font.Font('BMDOHYEON.ttf', 20) # 폰트 크기
    text = font.render(output_string, True, ( 255, 255, 255 ) ) # 글자 색(흰색)
    gamePad.blit(text,(1065,10)) # 생성 위치
    frame_count = frame_count + 1 # 카운트 증가

    # 클리어
    if frame_count == 3600: # 1분 경과 시 클리어
        key = [0,0,0,0]
        rock_list = []
        frame_count = 0 # 시간 초기화
        
        writeMessage('Game Clear!!', (255, 255, 255), gameClearSound , 5 )

    # 낙하 운석 추가
    if frame_count % 300 == 0:
        if len(rock_list) < 3: # 화면 상 최대 3개까지 생성으로 제한
            rock_create()


# 메시지 출력
def writeMessage(text, color, sound, time): # ('출력할 메시지', 색상, 사운드, 메시지 지속시간)
    
    global gamePad, gameOverSound, destroySound, onGame
    
    drawObject(background, 0, 0)
    
    textfont = pygame.font.Font('BMDOHYEON.ttf', 100)
    text = textfont.render(text, True, color)
    textpos = text.get_rect() # 텍스트 위치
    textpos.center = (padWidth/2, padHeight/2) # 정중앙에 출력
    gamePad.blit(text, textpos) # 텍스트 출력
    
    pygame.display.update() # 화면 업데이트
    pygame.mixer.music.stop() # 배경 음악 정지
    sound.play() # 게임 오버 사운드 재생
    
    onGame = False
    
    sleep(time) # 2초 쉬고
    runGame() # 게임 재실행


# 충돌
def crash():
    
    global gamePad
    global frame_count
    global rock_list
    global key
    global gameOverSound
    
    key = [0,0,0,0]
    rock_list = []
    frame_count = 0
    
    writeMessage('전투기 파괴', (150, 0, 0), gameOverSound, 3 )


# 운석 일정 개수 낙하 시 게임종료
def gameOver():
    
    global gamePad
    global frame_count
    global rock_list
    global key
    global gameOverSound
    
    key = [0,0,0,0]   
    rock_list = []
    frame_count = 0
    
    writeMessage('Game Over', (255, 0, 0), gameOverSound, 3)


# 배경 그리기
def drawObject(obj, x, y):
    
    global gamePad
    
    gamePad.blit(obj, (x, y)) # 비트 연산, 게임 화면 그리기 / 해당하는 오브젝트를 x,y 좌표(그 위치)로부터 그리기


# 게임 초기화
def initGame():
    
    global gamePad, clock, background, fighter, missile, explosion, explosion2, missileSound, gameOverSound,gameClearSound, start # 전역변수 , fighter는 전투기

    pygame.init() # 초기화
    
    gamePad = pygame.display.set_mode((padWidth, padHeight))

    pygame.display.set_caption('PyShooting') # 게임 창 이름

    background = pygame.image.load('background.png') # 배경 그림

    start = pygame.image.load('start.png') # 로딩 그림

    fighter = pygame.image.load('fighter.png') # 전투기 그림

    missile = pygame.image.load('missile.png') # 미사일 그림

    explosion = pygame.image.load('explosion.png') # 폭발 그림

    explosion2 = pygame.image.load('explosion2.png') # 타격 그림

    pygame.mixer.music.load('music.wav') # 배경 음악    

    missileSound = pygame.mixer.Sound('missile.wav') # 미사일 사운드

    gameOverSound = pygame.mixer.Sound('gameover.wav') # 게임 오버 사운드

    gameClearSound = pygame.mixer.Sound('clear.wav') # 게임 클리어 사운드

    clock = pygame.time.Clock()


# 운석 생성
def rock_create():
    
    global rock_list
    
    # 운석 랜덤 생성
    image = random.choice(rockImage)
    hp = 1
    rock = pygame.image.load(image)
    if  image == "rock01.png" :
        hp = 1
    elif image == "rock02.png" :
        hp = 2
    elif image == "rock03.png" :
        hp = 3
    elif image == "rock04.png" :
        hp = 4
    elif image == "rock05.png" :
        hp = 5
         
    rockSize = rock.get_rect().size # 운석 크기
    rockWidth = rockSize[0] # 운석 가로 초기값
    rockHeight = rockSize[1] # 운석 세로 초기값

    # 운석 초기 위치 설정
    rockX = random.randrange(0, padWidth - rockWidth) # x축 상에서 게임 화면 범위 내 랜덤으로 생성
    rockY = 0 # y축 최상단(0)에서 생성
    rock_list.append( [ rock, rockWidth, rockHeight, rockX, rockY, hp ] )

   
# 게임 실행 함수
def runGame():
    
    global gamePad,clock, background, fighter, missile, explosion, explosion2, missileSound, frame_count , rock_list, onGame
  
    # 각종 이벤트 처리
    while not onGame:
        
        drawObject(start, 0, 0) # 시작 화면 그리기
        
        textfont = pygame.font.Font('BMDOHYEON.ttf', 140) # 폰트 종류 및 크기
        text = textfont.render("PyShooting", True, (255,255,255) )

        textpos = text.get_rect() # 텍스트 위치
        textpos.center = (padWidth/2, padHeight/2 - 30) # 정중앙에 출력
        gamePad.blit(text, textpos)

        textfont2 = pygame.font.Font('BMDOHYEON.ttf', 35) # 폰트 종류 및 크기
        text2 = textfont2.render("Press the 'S' button!!", True, (abs(math.sin(time())*255),abs(math.sin(time())*255),abs(math.sin(time())*255))) # sin함수 사용 ( 주기적 색상 변화 )

        textpos2 = text2.get_rect() # 텍스트 위치2
        textpos2.center = (padWidth/2, padHeight/2 + 100) # 정중앙에 출력
        gamePad.blit(text2, textpos2)
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit() #pygame 종료
                sys.exit() #시스템 종료
             
            if event.type in [pygame.KEYDOWN]: # 키 누를 시
              
                if event.key == 115: # 'S'키 누를 경우

                    onGame = True
        
    pygame.mixer.music.play(-1)
    frame_count = 0
    
    # 전투기 크기
    fighterSize = fighter.get_rect().size 
    fighterWidth = fighterSize[0] # 전투기 너비
    fighterHeight = fighterSize[1] # 전투기 폭

    # 전투기 초기 위치 ( 밑 부분의 중간 / (x,y) )    
    x = padWidth * 0.45
    y = padHeight * 0.9
    playerpos = [x,y] # 전투기의 x,y좌표 설정
    fighterX = 0
    fighterY = 0

    rock_create()
    
    missileXY = [] # 무기 좌표 리스트

    destroySound = pygame.mixer.Sound(random.choice(explosionSound))
    
    rockSpeed = 2

    # 미사일에 운석이 맞았을 경우 True
    shotCount = 0 # 갯수
    rockPassed = 0 # 운석 놓쳤을 때


    
    while onGame: # 각종 이벤트 처리
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit() # pygame 종료
                sys.exit() # 시스템 종료
             
            if event.type in [pygame.KEYDOWN]: # 키 누를 시
                
                if event.key == pygame.K_LEFT: # 왼쪽 방향키 누를 시

                    key[0] =  time()
                    
                elif event.key == pygame.K_RIGHT: # 오른쪽 방향키 누를 시
      
                    key[1] =  time()
                    
                elif event.key == pygame.K_UP: # 위 방향키 누를 시
   
                    key[2] =  time()

                elif event.key == pygame.K_DOWN: # 아래 방향키 누를 시

                    key[3] =  time()

                elif event.key == pygame.K_SPACE: # 미사일 발사 (중간에서 발사 되게끔)
                    missileSound.play()
                    missileX = playerpos[0] + fighterWidth/2 - 5
                    missileY = playerpos[1] - fighterHeight + 100
                    missileXY.append([missileX, missileY])
                    
            if event.type in [pygame.KEYUP]: # 키 뗐을 시
                
                if event.key == pygame.K_LEFT:

                    key[0] = 0
                    
                if event.key == pygame.K_RIGHT:
                    
                    key[1] = 0
                    
                if event.key == pygame.K_UP:
                
                    key[2] = 0
                    
                if event.key == pygame.K_DOWN:
                
                    key[3] = 0

                    
        if key[0] > key[1]:
           
            playerpos[0] = playerpos[0] - 20
            
        elif key[0] < key[1]  :
            
            playerpos[0] = playerpos[0] + 20

        if key[2] > key[3]:
            
            playerpos[1] = playerpos[1] - 20
            
        elif key[2] < key[3]:
            
            playerpos[1] = playerpos[1] + 20

              
        # gamePad.fill(BLACK) #게임 화면 색 채우기 / 게임 화면 블랙으로 안 칠해도 배경으로 꽉 채우기 때문에 필요x
        drawObject(background, 0, 0)

        
        # 게임 화면 왼쪽으로 끝까지 가는 경우
        if playerpos[0] < 0: # 게임 밖으로 비행기가 움직이면 안되기 때문에 음수가 될 경우 0 으로하여 최대 왼쪽으로 갈 수 있는 부분 조정
            playerpos[0] = 0
        elif playerpos[0] > padWidth - fighterWidth: 
            playerpos[0] = padWidth - fighterWidth

        if playerpos[1] <0:
            playerpos[1] = 0
        elif playerpos[1] > padHeight - fighterHeight:
            playerpos[1] = padHeight - fighterHeight
        
        # 전투기가 운석과 충돌했는지 체크
        for x in rock_list:
            if( (playerpos[1] < x[4] + x[2] and playerpos[1]+ fighterHeight >  x[4] ) or (playerpos[1] > x[4] + x[2] and playerpos[1] <  x[4] + x[2] ) ) and \
            ( (x[3] + x[1] > playerpos[0] and x[3] < playerpos[0] + fighterWidth )or (x[3] + x[1] < playerpos[0] and x[3] + x[1] > playerpos[0] ) ):
                crash()
        
        drawObject(fighter, playerpos[0], playerpos[1]) # 전투기를 게임 화면의 (x,y) 좌표에 그리기 

        if rockPassed == 2: #운석 2개 놓치면 게임오버
            gameOver()

        # 미사일 발사 화면에 그리기
        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY): # 미사일 요소에 대해 반복함
                bxy[1] -= 20 # 총알의 y좌표 -10 (위로 이동)
                missileXY[i][1] = bxy[1]
 
                # 미사일이 운석을 맞추었을 경우
                for x in rock_list:
                    if bxy[1] < x[4]:
                        if bxy[0] > x[3] and bxy[0] < x[3] + x[1]:
                            
                            x[5] = x[5] - 1
                            explosion_list.append( [ explosion2, bxy[0], bxy[1]+100, time() ]  )
                            missileXY.remove(bxy)
                        
                            destroySound.play() #운석 폭발 사운드 재생
      
                            break # 겹쳐있는 두 운석 동시 파괴 시 나타나는 오류 방지

                    if bxy[1] <= 0: # 미사일이 화면 밖을 벗어나면
                        try:
                            missileXY.remove(bxy) # 미사일 제거
                            break
                        except:
                            pass
                    
        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawObject(missile, bx, by)
    
        # 타임
        timer()

        # 운석 맞춘 점수 표시 
        writeScore(shotCount)

        for x in rock_list:
            x[4] += rockSpeed # 운석 아래로 움직임

            # 운석이 지구로 떨어진 경우
            if x[4] > padHeight:
                if len(rock_list) < 3:
                    rock_create()
                rockPassed += 1

        for x in rock_list:   
            drawObject(x[0], x[3] , x[4]) # 운석 그리기

             # 운석을 맞춘 경우
            if x[5] == 0: #x[5]는 바위의 체력(hp)
                
                # 운석 폭발
                explosion_list.append( [ explosion, x[3]-60, x[4], time() ]  )
                destroySound.play() #운석 폭발 사운드 재생
                shotCount += 1 # 운석 파괴 개수 증가
                
                # 새로운 운석 (랜덤)
                rock_list.remove(x)
                if len(rock_list) < 3:
                    rock_create()
                destroySound = pygame.mixer.Sound(random.choice(explosionSound))
                
                #운석 맞추면 속도 증가
                rockSpeed += 0.05
                if rockSpeed >= 5:
                    rockSpeed = 5
        
        for x in explosion_list:
            if time() - x[3] > 0.2 :
                explosion_list.remove(x)
            else:
                drawObject(x[0],x[1],x[2] )   
                  
                    
        # 놓친 운석 수 표시 
        writePassed(rockPassed)
        
        pygame.display.update() # 게임화면 다시 그리기

        clock.tick(60) #초당 프레임(FPS) 60

    pygame.quit()

initGame()
runGame()
