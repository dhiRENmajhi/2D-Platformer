import pygame
from pygame.locals import *
import sys
pygame.init()
import random
import math
import pickle

FPS=30
fpsclock=pygame.time.Clock()
screen=pygame.display.set_mode((1280,720))
pygame.display.set_caption('Chop_ping')
pygame.mouse.set_visible(False)

welcome=pygame.image.load('sprites/images/chop_ping.jpg')
timewelcome=pygame.time.get_ticks()
introsound=pygame.mixer.Sound('sprites/audio/introsound.wav')
introsound.play()
while pygame.time.get_ticks()<timewelcome+3000:#shows welcome screen for 5 seconds
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(welcome,(0,0))
    pygame.display.update()
    fpsclock.tick(FPS)

def points(playerpos,Life,goldcoin,collectlife,collectedcoins,movegold,heal,showpoint,timepoint,phi):
    terminate=None
    points=[1,5,10,50,100]
    for l in range(len(goldcoin)):
        if goldcoin[l]['y']-ph<playerpos['y']<goldcoin[l]['h']+goldcoin[l]['y'] and goldcoin[l]['x']-pw<playerpos['x']<goldcoin[l]['w']+goldcoin[l]['x'] :
            coincollectsound.play()
            addup=random.randint(0,4)
            collectedcoins+=points[addup]
            cx= (goldcoin[l]['x']-195)*25/math.sqrt( (goldcoin[l]['x']-195)**2 + (goldcoin[l]['y']-35)**2 )
            cy= (goldcoin[l]['y']-35)*25/math.sqrt( (goldcoin[l]['x']-195)**2 + (goldcoin[l]['y']-35)**2 )
            movegold.append({'x':goldcoin[l]['x'],'y':goldcoin[l]['y'],'cx':-cx,'cy':-cy,'gold':addup})
            terminate=l
            break
    if terminate!=None:
        goldcoin.pop(terminate)
    terminate=None
    for l in range(len(collectlife)):
        if collectlife[l]['y']-ph<playerpos['y']<collectlife[l]['h']+collectlife[l]['y'] and collectlife[l]['x']-pw<playerpos['x']<collectlife[l]['w']+collectlife[l]['x'] :
            if Life<4:
                healsound.play()
                Life+=1
                phi=0
                terminate=l
                heal=True
                showpoint=lifeadd1
                timepoint=pygame.time.get_ticks()
            else:
                terminate=None
            
            break
    if terminate!=None:
        collectlife.pop(terminate)
    
    return Life,collectlife,collectedcoins,goldcoin,movegold,heal,showpoint,timepoint,phi
    

def Star(starpoint,playerpos,playstarcollect,timestar,sx,sy,starno):#checks no of stars collected       

    terminate=None
    
    for l in range(len(starpoint)):
        if starpoint[l]['y']-ph<playerpos['y']<starpoint[l]['h']+starpoint[l]['y'] and starpoint[l]['x']-pw<playerpos['x']<starpoint[l]['w']+starpoint[l]['x'] :
            starno+=1
            starcollectsound.play()
            playstarcollect=True
            timestar=pygame.time.get_ticks()
            terminate=l
            print("star",starno)
            sx,sy=starpoint[l]['x']-25,starpoint[l]['y']-25
            print(starpoint)
            break
    if terminate!=None:
        starpoint.pop(terminate)

    return starpoint,sx,sy,playstarcollect,timestar,starno

def Playerattack(monster,playerpos,Attack_r,attack,collectlife,goldcoin,enemyx,enemyy,enemyexplode):
    terminate=None
    for l in range(len(monster)):
        if Attack_r:
            if monster[l]['y']-ph<playerpos['y']<monster[l]['h']+monster[l]['y']+25 and monster[l]['x']-100<playerpos['x']<monster[l]['w']+monster[l]['x']:
                enemyhurtsound.play()
                monster[l]['health']-=1
                attack=False
                monster[l]['x']+=25
                if monster[l]['increment']==-1:
                    monster[l]['times']-=5
                else:
                    monster[l]['times']-=5
                if monster[l]['health']==0:
                    terminate=l
                break
                    
        else:
            if monster[l]['y']-ph<playerpos['y']<monster[l]['h']+monster[l]['y']+25 and monster[l]['x']-pw<playerpos['x']<monster[l]['w']+monster[l]['x']+50:
                enemyhurtsound.play()
                monster[l]['health']-=1
                attack=False
                monster[l]['x']-=25
                if monster[l]['increment']==-1:
                    monster[l]['times']+=5
                else:
                    monster[l]['times']+=5
                if monster[l]['health']==0:
                    terminate=l
                break

    if terminate != None:
        enemyblastsound.play()
        enemyx,enemyy=monster[terminate]['x']-25,monster[terminate]['y']-25
        enemyexplode=True
        if Attack_r:
            if random.randint(0,2)==2:
                collectlife.append({'x':monster[l]['x']+10,'y':monster[l]['y']+20,'w':30,'h':30})
            else:
                goldcoin.append({'x':monster[l]['x']+10,'y':monster[l]['y']+20,'w':30,'h':30})
        else:
            if random.randint(0,2)==2:
                collectlife.append({'x':monster[l]['x']-10,'y':monster[l]['y']+20,'w':30,'h':30})
            else:
                goldcoin.append({'x':monster[l]['x']-10,'y':monster[l]['y']+20,'w':30,'h':30})    
        monster.pop(terminate)
    return(monster,attack,collectlife,goldcoin,enemyx,enemyy,enemyexplode)
            
                
    



def collide(playerpast,playerpos,box,down,onground,doublejump,landing,timedelay):#changes playerpos accorting to platforms
    check=0
    notair=onground
    for l in range(len(box)):
        if box[l]['y']-ph<=playerpos['y']<box[l]['h']+box[l]['y'] and box[l]['x']-pw<playerpos['x']<box[l]['w']+box[l]['x'] :
            if playerpast['y']<=box[l]['y']-ph:
                playerpos['y']=box[l]['y']-ph
                onground=True
                doublejump=True
                check=1
                down=0
            elif playerpast['y']>=box[l]['y']+box[l]['h']:
                playerpos['y']=box[l]['y']+box[l]['h']
                down=0
            elif playerpast['x']<=box[l]['x']-pw:
                playerpos['x']=box[l]['x']-pw
            elif playerpast['x']>=box[l]['x']+box[l]['w']:
                playerpos['x']=box[l]['x']+box[l]['w']

    if check==0:
        onground=False
    elif notair==False:
        landing=True
        timedelay=pygame.time.get_ticks()
    else:
        landing=False
    return playerpos,onground,down,doublejump,landing,timedelay



def _obstacle(playerpos,trap,timehurt,Life,Hurt,timeeffect,playheartbreak):#checks if player is hurt by obstacles

    for l in range(len(trap)):
        if trap[l]['y']-ph<playerpos['y']<trap[l]['h']+trap[l]['y'] and trap[l]['x']-pw<playerpos['x']<trap[l]['w']+trap[l]['x'] :
            hurtsound.play()
            Life-=1
            Hurt=True
            playheartbreak=True
            timeeffect=pygame.time.get_ticks()
            print(Life)
            timehurt=pygame.time.get_ticks()
            break

    return timehurt,Life,Hurt,timeeffect,playheartbreak


def Level1(data):
    surface=pygame.image.load('sprites/images/platform.png')
    obstacle=pygame.image.load('sprites/images/obstacle.png')
    spike200=pygame.image.load('sprites/images/spike200.png')
    spike250=pygame.image.load('sprites/images/spike250.png')
    spike400=pygame.image.load('sprites/images/spike400.png')
    dirt=pygame.image.load('sprites/images/dirt.png')
    dirtshadow=pygame.image.load('sprites/images/dirtshadow.png')
    mud=(
        {'image':pygame.transform.scale(dirtshadow,(300,30)),'x':400,'y':1000},#1
        {'image':pygame.transform.scale(dirtshadow,(400,30)),'x':1400,'y':1200},#2
        {'image':pygame.transform.scale(dirtshadow,(250,30)),'x':2650,'y':900},#3
        {'image':pygame.transform.scale(dirtshadow,(650,30)),'x':2250,'y':1450},#4
        {'image':pygame.transform.scale(dirtshadow,(300,30)),'x':3150,'y':1450},#5
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':3400,'y':1250},#6
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':4200,'y':900},#7
        {'image':pygame.transform.scale(dirtshadow,(100,30)),'x':4500,'y':1100},#8
        {'image':pygame.transform.scale(dirtshadow,(400,30)),'x':4600,'y':1100},#8
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':4650,'y':650},#9
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':5100,'y':900},#10
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':5300,'y':1100},#11
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':6100,'y':1100},#12
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':6300,'y':800},#13
        {'image':pygame.transform.scale(dirt,(300,220)),'x':400,'y':1030},#1
        {'image':pygame.transform.scale(dirt,(400,470)),'x':1400,'y':1230},#2
        {'image':pygame.transform.scale(dirt,(250,220)),'x':2650,'y':930},#3
        {'image':pygame.transform.scale(dirt,(650,220)),'x':2250,'y':1480},#4
        {'image':pygame.transform.scale(dirt,(300,220)),'x':3150,'y':1480},#5
        {'image':pygame.transform.scale(dirt,(200,420)),'x':3400,'y':1280},#6
        {'image':pygame.transform.scale(dirt,(200,370)),'x':4200,'y':930},#7
        {'image':pygame.transform.scale(dirt,(100,320)),'x':4500,'y':1130},#8
        {'image':pygame.transform.scale(dirt,(400,520)),'x':4600,'y':1130},#8
        {'image':pygame.transform.scale(dirt,(200,370)),'x':4650,'y':680},#9
        {'image':pygame.transform.scale(dirt,(200,420)),'x':5100,'y':930},#10
        {'image':pygame.transform.scale(dirt,(200,270)),'x':5300,'y':1130},#11
        {'image':pygame.transform.scale(dirt,(200,220)),'x':6100,'y':1130},#12
        {'image':pygame.transform.scale(dirt,(200,570)),'x':6300,'y':830}#13
        )

    platform=(
        pygame.transform.scale(surface,(900,500)),#1
        pygame.transform.scale(surface,(300,50)),#2
        pygame.transform.scale(surface,(500,250)),#3
        pygame.transform.scale(surface,(400,50)),#4
        pygame.transform.scale(surface,(400,50)),#5
        pygame.transform.scale(surface,(450,300)),#6
        pygame.transform.scale(surface,(850,300)),#7
        pygame.transform.scale(surface,(250,50)),#8
        pygame.transform.scale(surface,(1350,50)),#9
        pygame.transform.scale(surface,(250,300)),#10
        pygame.transform.scale(surface,(200,100)),#11
        pygame.transform.scale(surface,(600,300)),#12
        pygame.transform.scale(surface,(400,300)),#13
        pygame.transform.scale(surface,(200,50)),#14
        pygame.transform.scale(surface,(200,450)),#15
        pygame.transform.scale(surface,(200,300)),#16
        pygame.transform.scale(surface,(500,100)),#17
        pygame.transform.scale(surface,(500,50)),#18
        pygame.transform.scale(surface,(200,50)),#19
        pygame.transform.scale(surface,(200,400)),#20
        pygame.transform.scale(surface,(200,50)),#21
        pygame.transform.scale(surface,(200,50)),#22
        pygame.transform.scale(surface,(500,350)),#23
        pygame.transform.scale(surface,(500,400)),#24
        pygame.transform.scale(surface,(200,50)),#25
        pygame.transform.scale(surface,(200,350)),#26
        pygame.transform.scale(surface,(200,50)),#27
        pygame.transform.scale(surface,(200,400)),#28
        pygame.transform.scale(surface,(600,200))#29        
        )
    obstacles=(
        pygame.transform.flip(spike400,False,True),#1
        spike400,#2
        pygame.transform.rotate(spike250,-90),#3
        spike200,#4
        #spike200,#5
        spike200,#6
        pygame.transform.flip(spike200,False,True),#7
        pygame.transform.flip(spike200,False,True),#8
        spike200,#9
        pygame.transform.rotate(spike200,-90)#10
        )

    showpoint=None
    timepoint=pygame.time.get_ticks()


    
    Life=4 #player life
    starno=0 #no of stars collected
    collectedcoins=0
    nogold=collectedcoins
    glist=[]
    for j in range(len(str(nogold))):
        glist.insert(0,nogold%10)
        nogold=nogold//10 
    dead=False #True if player is dead
    Hurt=False #True if player is hurt by traps
    injuredtime=pygame.time.get_ticks()
    timehurt=pygame.time.get_ticks()

    goright=False #True if player is moving right
    goleft=False #True if player is moving left
    onground=False #True if player is on platform/surface/ground
    jump_=False
    face_r=True #True if player is facing right, False if facing left
    Attack_r=True
    attack=False
    attacking=False
    ai=0
    
    playerpos={'x':0,'y':1150}#initial player position

    #-----------------platforms
    box=[
        {'x':0,'y':1250,'w':900,'h':500},#1
        {'x':400,'y':950,'w':300,'h':50},#2
        {'x':900,'y':1500,'w':500,'h':250},#3
        {'x':1400,'y':1150,'w':400,'h':50},#4
        {'x':1400,'y':1700,'w':400,'h':50},#5
        {'x':1800,'y':1450,'w':450,'h':300},#6
        {'x':2050,'y':1150,'w':850,'h':300},#7
        {'x':2650,'y':850,'w':250,'h':50},#8
        {'x':2250,'y':1700,'w':1350,'h':50},#9
        {'x':3150,'y':1150,'w':250,'h':300},#10
        {'x':3400,'y':1150,'w':200,'h':100},#11
        {'x':3600,'y':1450,'w':600,'h':300},#12
        {'x':3800,'y':1150,'w':400,'h':300},#13
        {'x':4200,'y':850,'w':200,'h':50},#14
        {'x':4200,'y':1300,'w':200,'h':450},#15
        {'x':4400,'y':1450,'w':200,'h':300},#16
        {'x':4600,'y':1650,'w':500,'h':100},#17
        {'x':4500,'y':1050,'w':500,'h':50},#18
        {'x':4650,'y':600,'w':200,'h':50},#19
        {'x':5100,'y':1350,'w':200,'h':400},#20
        {'x':5100,'y':850,'w':200,'h':50},#21
        {'x':5300,'y':1050,'w':200,'h':50},#22
        {'x':5300,'y':1400,'w':500,'h':350},#23
        {'x':5800,'y':1350,'w':500,'h':400},#24
        {'x':6100,'y':1050,'w':200,'h':50},#25
        {'x':6300,'y':1400,'w':200,'h':350},#26
        {'x':6300,'y':750,'w':200,'h':50},#27
        {'x':6500,'y':1350,'w':200,'h':400},#28
        {'x':6700,'y':1550,'w':600,'h':200}#29
        ]
    
    #-----------------traps
    
    trap=[
        {'x':1400,'y':1200,'w':400,'h':50},#1
        {'x':1400,'y':1650,'w':400,'h':50},#2
        {'x':2250,'y':1450,'w':50,'h':250},#3
        {'x':4200,'y':1250,'w':200,'h':50},#4
        #{'x':4400,'y':1400,'w':200,'h':50},#5
        {'x':4600,'y':1600,'w':200,'h':50},#6
        {'x':5300,'y':1100,'w':200,'h':50},#7
        {'x':6100,'y':1100,'w':200,'h':50},#8
        {'x':6300,'y':1350,'w':200,'h':50},#9
        {'x':6700,'y':1350,'w':50,'h':200}#10
        ]
    

    #-----------------stars
    starpoint=[
        {'x':2350,'y':1550,'w':50,'h':50},
        {'x':5000,'y':1450,'w':50,'h':50},
        {'x':6375,'y':800,'w':50,'h':50}       
        ]
    goldcoin=[
        {'x':460,'y':920,'w':30,'h':30},
        {'x':510,'y':920,'w':30,'h':30},
        {'x':560,'y':920,'w':30,'h':30},
        {'x':610,'y':920,'w':30,'h':30},
        {'x':1870,'y':1420,'w':30,'h':30},
        {'x':1920,'y':1420,'w':30,'h':30},
        {'x':1970,'y':1420,'w':30,'h':30},
        {'x':2720,'y':820,'w':30,'h':30},
        {'x':2770,'y':820,'w':30,'h':30},
        {'x':2820,'y':820,'w':30,'h':30},
        {'x':2920,'y':1670,'w':30,'h':30},
        {'x':2970,'y':1670,'w':30,'h':30},
        {'x':3020,'y':1670,'w':30,'h':30},
        {'x':3070,'y':1670,'w':30,'h':30},
        {'x':3120,'y':1670,'w':30,'h':30},        
        {'x':3220,'y':1120,'w':30,'h':30},
        {'x':3270,'y':1120,'w':30,'h':30},
        {'x':3320,'y':1120,'w':30,'h':30},
        {'x':3370,'y':1120,'w':30,'h':30},
        {'x':3420,'y':1120,'w':30,'h':30},
        {'x':3470,'y':1120,'w':30,'h':30},
        {'x':3520,'y':1120,'w':30,'h':30},
        {'x':4285,'y':820,'w':30,'h':30},
        {'x':4735,'y':570,'w':30,'h':30},
        {'x':5185,'y':820,'w':30,'h':30},
        {'x':6345,'y':720,'w':30,'h':30},
        {'x':6395,'y':720,'w':30,'h':30},
        {'x':6445,'y':720,'w':30,'h':30}
        ]
    collectlife=[]
    movegold=[]

    monster=[
        {'x':1000,'y':1450,'w':50,'h':50,'move':5,'times':50,'increment':-1,'health':3},
        {'x':1700,'y':1100,'w':50,'h':50,'move':5,'times':1,'increment':1,'health':3},
        {'x':2200,'y':1100,'w':50,'h':50,'move':5,'times':50,'increment':-1,'health':3},
        {'x':2450,'y':1100,'w':50,'h':50,'move':5,'times':1,'increment':1,'health':3},
        {'x':2600,'y':1650,'w':50,'h':50,'move':5,'times':50,'increment':-1,'health':3},
        {'x':3400,'y':1650,'w':50,'h':50,'move':5,'times':1,'increment':1,'health':3},
        {'x':4600,'y':1000,'w':50,'h':50,'move':5,'times':50,'increment':-1,'health':3},
        {'x':4850,'y':1000,'w':50,'h':50,'move':5,'times':1,'increment':1,'health':3},
        {'x':5400,'y':1350,'w':50,'h':50,'move':5,'times':50,'increment':-1,'health':3},
        {'x':5650,'y':1350,'w':50,'h':50,'move':5,'times':1,'increment':1,'health':3},
        {'x':6800,'y':1500,'w':50,'h':50,'move':5,'times':50,'increment':-1,'health':3},
        {'x':7050,'y':1500,'w':50,'h':50,'move':5,'times':1,'increment':1,'health':3}
        ]
    messagebordpos=[
        {'x':0,'y':1100},
        {'x':7150,'y':1400}
        ]
    
    i=0 #player index
    player=standing_r
    timeindex=pygame.time.get_ticks()

    g=3 #gravity
    down=0 #down value

    timedelay=pygame.time.get_ticks()
    doublejump=True #True if player is onair and can be only used once, refills when player comes back to the ground
    landing=False #True when playe touches ground after jump
    freeze=False #True and makes player freeze for some time while landing

    changex=changey=0 #for camera movement
    timeeffect=timestar=pygame.time.get_ticks()
    hi=si=0
    playheartbreak=False
    playstarcollect=False
    sx=sy=0
    heal=False
    phi=0
    
    enemyx,enemyy,enemyexplode=0,0,False
    exi=0
    


    #-------------player margin on screen
    

    lmargin=400
    rmargin=880
    umargin=150
    bmargin=570
    levelX=levelY=0
    lwidth,lheight=7300,1750


    gamebgmusic.set_volume(0)
    gamebgmusic.play(-1)
    playrip=True
    runsoundplaying=False

    onRetry=False
    onMenu=False

    startwelcome=True
    timeintro=pygame.time.get_ticks()
    introsound.play()

    while True:
        
        mx,my=pygame.mouse.get_pos()#mouse position
        
        playerpast={'x':playerpos['x'],'y':playerpos['y']}#past position of player

        for event in pygame.event.get():#gets user interactions
            
            if event.type==QUIT:#checks if user clicked on quit
                pygame.quit()
                sys.exit()
            if not startwelcome:
                if event.type==KEYDOWN and event.key==K_ESCAPE:
                    gamebgmusic.stop()
                    runsound.stop()
                    runsoundplaying=False
                    Mode(data)
                
                if not dead:
                    if event.type==KEYDOWN and event.key==K_RIGHT:#right move
                        goright=True
                        goleft=False
                        face_r=True
                        player=walking_r
                    if event.type==KEYUP and event.key==K_RIGHT:
                        goright=False
                        if goleft:
                            player=walking_l
                        else:
                            player=standing_r
                            runsound.stop()

                    if event.type==KEYDOWN and event.key==K_LEFT:#left move
                        goright=False
                        goleft=True
                        face_r=False
                        player=walking_l
                    if event.type==KEYUP and event.key==K_LEFT:
                        goleft=False
                        if goright:
                            player=walking_r
                        else:
                            player=standing_l

                    if not freeze:
                        if onground and (event.type==KEYDOWN and event.key==K_UP):#jump move
                            jumpsound.play()
                            down=-30
                            onground=False
                        elif doublejump and (event.type==KEYDOWN and event.key==K_UP):
                            jumpsound.play()
                            down=-30
                            doublejump=False
                        if not attacking and (event.type==KEYDOWN and event.key==K_SPACE):
                            attacksound.play()
                            attack=attacking=True
                            if face_r:
                                Attack_r=True
                            else:
                                Attack_r=False
                            ai=0
                if dead and not Hurt:
                    if event.type==MOUSEBUTTONDOWN:
                        if onRetry:
                            buttonclickedsound.play()
                            screen.blit(afterdeathmessage[4],(265,210))
                            screen.blit(mouse,(mx,my))
                            pygame.display.update()
                            fpsclock.tick(FPS)
                            gamebgmusic.stop()
                            runsound.stop()
                            runsoundplaying=False
                            Level1(data)
                        if onMenu:
                            buttonclickedsound.play()
                            screen.blit(afterdeathmessage[2],(265,210))
                            screen.blit(mouse,(mx,my))
                            pygame.display.update()
                            fpsclock.tick(FPS)
                            gamebgmusic.stop()
                            runsound.stop()
                            runsoundplaying=False
                            Mode(data)

                                
        if not onground:#gravity pull/jump
            playerpos['y']+=down
            down+=g

        if not freeze:#right left motion
            if goright:
                playerpos['x']+=10
                                                    
            if goleft:
                playerpos['x']-=10

            if (onground and not runsoundplaying) and (goright or goleft):
                runsound.play(-1)
                runsoundplaying=True
            if (not goright and not goleft) or not onground:
                runsound.stop()
                runsoundplaying=False
                

        playerpos,onground,down,doublejump,landing,timedelay=collide(playerpast,playerpos,box,down,onground,doublejump,landing,timedelay)#changes playerpos accorting to platforms

        for j in range(len(monster)):            
            monster[j]['x']-=monster[j]['move']*monster[j]['increment']
            monster[j]['times']+=monster[j]['increment']
            if monster[j]['times']<=1:
                monster[j]['increment']=1
            elif monster[j]['times']>=50:
                monster[j]['increment']=-1

        Life,collectlife,collectedcoins,goldcoin,movegold,heal,showpoint,timepoint,phi=points(playerpos,Life,goldcoin,collectlife,collectedcoins,movegold,heal,showpoint,timepoint,phi)

        remove=None
        for j in range(len(movegold)):
            if 170<movegold[j]['x']<220 and 10<movegold[j]['y']<60:
                pointsound.play()
                remove=j
                showpoint=goldplus[movegold[j]['gold']]
                timepoint=pygame.time.get_ticks()
                glist=[]
                nogold=collectedcoins
                for k in range(len(str(nogold))):
                    glist.insert(0,nogold%10)
                    nogold=nogold//10 
                break
            else:
                movegold[j]['x']+=movegold[j]['cx']
                movegold[j]['y']+=movegold[j]['cy']
        if remove != None:
            movegold.pop(remove)
                
        starpoint,sx,sy,playstarcollect,timestar,starno=Star(starpoint,playerpos,playstarcollect,timestar,sx,sy,starno)#checks no of stars collected
        
        
        if not Hurt and not dead:
            timehurt,Life,Hurt,timeeffect,playheartbreak=_obstacle(playerpos,trap,timehurt,Life,Hurt,timeeffect,playheartbreak)#checks if player is hurt by obstacles
            if not Hurt:
                timehurt,Life,Hurt,timeeffect,playheartbreak=_obstacle(playerpos,monster,timehurt,Life,Hurt,timeeffect,playheartbreak)#checks if player is hurt by enemy
            if Life==0:
                dead=True
                goright=False
                goleft=False
                
                
        else:
            if pygame.time.get_ticks()>timehurt+1000:                
                Hurt=False
                
        if landing:
            landsound.play()
            freeze=True
        if pygame.time.get_ticks()>timedelay+100:
            freeze=False
            
        if attack:
            monster,attack,collectlife,goldcoin,enemyx,enemyy,enemyexplode=Playerattack(monster,playerpos,Attack_r,attack,collectlife,goldcoin,enemyx,enemyy,enemyexplode)

        #changes for camera movement

        if playerpos['x']<lmargin:
            if levelX>=0:
                changex=0-levelX
            else:                
                changex=lmargin-playerpos['x']
                if changex>-levelX:
                    changex=-levelX
        elif (playerpos['x']+pw)>rmargin:
            if levelX<=1280-lwidth:
                changex=1280-(levelX+lwidth)
            else:
                changex=rmargin-(playerpos['x']+pw)
                if changex<1280-(levelX+lwidth):
                    changex=1280-(levelX+lwidth)
        else:
            changex=0
        if playerpos['y']<umargin:
            if levelY>=0:
                changey=0-levelY
            else:
                changey=umargin-playerpos['y']
                if changey>-levelY:
                    changey=-levelY
        elif (playerpos['y']+ph)>bmargin:
            if levelY<=720-lheight:
                changey=720-(levelY+lheight)
            else:                
                changey=bmargin-(playerpos['y']+ph)
                if changey<720-(levelY+lheight):
                    changey=720-(levelY+lheight)
        else:
            changey=0

        if changex!=0:#changes x value for camera movement
            levelX+=changex
            playerpos['x']+=changex
            sx+=changex
            for k in range(len(box)):
                box[k]['x']+=changex
            for k in range(len(trap)):
                trap[k]['x']+=changex
            for k in range(len(starpoint)):
                starpoint[k]['x']+=changex
            for k in range(len(goldcoin)):
                goldcoin[k]['x']+=changex
            for k in range(len(collectlife)):
                collectlife[k]['x']+=changex
            for k in range(len(monster)):
                monster[k]['x']+=changex
            for k in range(len(mud)):
                mud[k]['x']+=changex
            for k in range(len(messagebordpos)):
                messagebordpos[k]['x']+=changex
                    
        if changey!=0:#changes y value for camera movement
            levelY+=changey
            playerpos['y']+=changey
            sy+=changey
            for k in range(len(box)):
                box[k]['y']+=changey
            for k in range(len(trap)):
                trap[k]['y']+=changey            
            for k in range(len(starpoint)):
                starpoint[k]['y']+=changey
            for k in range(len(goldcoin)):
                goldcoin[k]['y']+=changey
            for k in range(len(collectlife)):
                collectlife[k]['y']+=changey
            for k in range(len(monster)):
                monster[k]['y']+=changey
            for k in range(len(mud)):
                mud[k]['y']+=changey
            for k in range(len(messagebordpos)):
                messagebordpos[k]['y']+=changey

        if playerpos['x']+pw<0:
            gamebgmusic.stop()
            runsound.stop()
            runsoundplaying=False
            Mode(data)
        elif playerpos['x']>1280:
            #----------------------------------------------------------------------save progress
            gamebgmusic.stop()
            runsound.stop()
            runsoundplaying=False
            data[1]+=collectedcoins
            if data[0]['l1']<starno:
                data[0]['l1']=starno
            if data[0]['l2']==None:
                data[0]['l2']=0
            f=open('sprites/data/donotdelete.txt','wb')
            pickle.dump(data,f)
            f.close()
            Level2(data)


        

        #-----------------------------------------------------------blitting images
                
        screen.blit(background,(0,0))
        for j in range(len(messagebordpos)):
            screen.blit(messagebord[j],(messagebordpos[j]['x'],messagebordpos[j]['y']))
        for j in range(len(mud)):
            screen.blit(mud[j]['image'],(mud[j]['x'],mud[j]['y']))
        for j in range(len(box)):
            screen.blit(platform[j],(box[j]['x'],box[j]['y']))
        for j in range(len(trap)):
            screen.blit(obstacles[j],(trap[j]['x'],trap[j]['y']))
        for j in range(len(monster)):
            if monster[j]['increment']==-1:
                screen.blit(enemy1_l[i],(monster[j]['x'],monster[j]['y']))
            else:
                screen.blit(enemy1_r[i],(monster[j]['x'],monster[j]['y']))
            screen.blit(healthbar[monster[j]['health']-1],(monster[j]['x'],monster[j]['y']-15))
        for j in range(len(goldcoin)):
            screen.blit(dropgold,(goldcoin[j]['x'],goldcoin[j]['y']))
        for j in range(len(movegold)):
            screen.blit(dropgold,(movegold[j]['x'],movegold[j]['y']))
        for j in range(len(collectlife)):
            screen.blit(dropheart,(collectlife[j]['x'],collectlife[j]['y']))
        if enemyexplode:
            screen.blit(enemyblast[exi],(enemyx,enemyy))
            if exi==8:
                exi=0
                enemyexplode=False
            else:
                exi+=1

        for j in range(len(starpoint)):#star
            screen.blit(star_r[i],(starpoint[j]['x'],starpoint[j]['y']))

        #------------------------------------------------------------------player

        if Hurt and pygame.time.get_ticks()<injuredtime+100:
            if attacking:
                if face_r:
                    if onground:
                        screen.blit(p_hurt_r[2],(playerpos['x'],playerpos['y']-25))
                    elif not onground:
                        screen.blit(p_hurt_r[3],(playerpos['x'],playerpos['y']-25))
                elif not face_r:
                    if onground:
                        screen.blit(p_hurt_l[2],(playerpos['x']-50,playerpos['y']-25))
                    elif not onground:
                        screen.blit(p_hurt_l[3],(playerpos['x']-50,playerpos['y']-25))
            elif not attacking:            
                if face_r:
                    if onground:
                        screen.blit(p_hurt_r[0],(playerpos['x'],playerpos['y']))
                    elif not onground:
                        screen.blit(p_hurt_r[1],(playerpos['x'],playerpos['y']))
                elif not face_r:
                    if onground:
                        screen.blit(p_hurt_l[0],(playerpos['x'],playerpos['y']))
                    elif not onground:
                        screen.blit(p_hurt_l[1],(playerpos['x'],playerpos['y']))
        elif not Hurt and dead:
            if playrip:
                ripsound.play()
                playrip=False
            screen.blit(dead_p,(playerpos['x'],playerpos['y']))           

        else:
            if freeze:
                if face_r:
                    screen.blit(land_r,(playerpos['x'],playerpos['y']))
                elif not face_r:
                    screen.blit(land_l,(playerpos['x'],playerpos['y']))
            elif attacking:
                if face_r:
                    if onground:
                        screen.blit(attack_r[ai],(playerpos['x'],playerpos['y']-25))
                    elif not onground:
                        screen.blit(airattack_r[ai],(playerpos['x'],playerpos['y']-25))
                elif not face_r:
                    if onground:
                        screen.blit(attack_l[ai],(playerpos['x']-50,playerpos['y']-25))
                    elif not onground:
                        screen.blit(airattack_l[ai],(playerpos['x']-50,playerpos['y']-25))
            elif onground:
                screen.blit(player[i],(playerpos['x'],playerpos['y']))
            elif not onground:
                if face_r:
                    screen.blit(jump_r,(playerpos['x'],playerpos['y']))
                elif not face_r:
                    screen.blit(jump_l,(playerpos['x'],playerpos['y']))
        if pygame.time.get_ticks()>injuredtime+200:
            injuredtime=pygame.time.get_ticks()
        if heal:
            screen.blit(healtheffect[phi],(playerpos['x']-25,playerpos['y']-25))
            if phi==8:
                phi=0
                heal=False
            else:
                phi+=1
            
        #------------------------------------------------------------------player
    
            
        if playstarcollect:#starcollect
            screen.blit(starcollected[si],(sx,sy))
            if si==8:
                si=0
                playstarcollect=False
            elif pygame.time.get_ticks()>timestar+100:
                si+=1
                timestar=pygame.time.get_ticks()

        screen.blit(star_r[0],(25,25))#blits no of star collected
        screen.blit(_x,(75,35))
        screen.blit(_no[starno],(105,35))

        screen.blit(_gold,(185,25))
        screen.blit(_x,(235,35))
        gpx=265
        for j in glist:
            screen.blit(_no[j],(gpx,35))
            gpx+=30

            
        xheart=502
        for j in range(4):#heart
            if j<Life:
                screen.blit(heart[1],(xheart,25))
            else:
                screen.blit(heart[0],(xheart,25))
            xheart+=75
            
        if playheartbreak:#heartbreak
            screen.blit(heartbreak[hi],(477+(Life*75),0))
            if hi==8:
                hi=0
                playheartbreak=False
            elif pygame.time.get_ticks()>timeeffect+100:
                hi+=1
                timeeffect=pygame.time.get_ticks()
        screen.blit(esc_exit,(1105,25))
        
        if showpoint != None:
            screen.blit(showpoint,(565,100))
            if pygame.time.get_ticks()>timepoint+3000:
                showpoint=None
            

        #----------------------------------------------------------------------------index change
        

        if pygame.time.get_ticks()>timeindex+200:#change player index
            if i==3:
                i=0
            else:
                i+=1
            timeindex=pygame.time.get_ticks()
        if ai==3:
            ai=0
            attack=False
            attacking=False
        else:
            ai+=1
        if dead and not Hurt:
            screen.blit(blackscreen,(0,0))
            if 360<my<460:
                if 315<mx<615:
                    if not onRetry:
                        onbuttonsound.play()
                    onRetry=True
                else:
                    onRetry=False
                if 665<mx<965:
                    if not onMenu:
                        onbuttonsound.play()
                    onMenu=True
                else:
                    onMenu=False

            if onRetry:
                screen.blit(afterdeathmessage[3],(265,210))
            elif onMenu:
                screen.blit(afterdeathmessage[1],(265,210))
            else:
                screen.blit(afterdeathmessage[0],(265,210))
            screen.blit(mouse,(mx,my))
            pygame.display.update()
            fpsclock.tick(FPS)

        elif startwelcome:
            screen.blit(blackscreen,(0,0))
            screen.blit(levelbanner[0],(440,285))
            if pygame.time.get_ticks()>timeintro+4000:
                startwelcome=False
                gamebgmusic.set_volume(0.5)
            pygame.display.update()
            fpsclock.tick(FPS)            
            
        #screen.blit(mouse,(mx,my))#mouse
        else:       
            pygame.display.update()
            fpsclock.tick(FPS)

    

    
def Level2(data):
    surface=pygame.image.load('sprites/images/platform.png')
    obstacle=pygame.image.load('sprites/images/obstacle.png')
    spike200=pygame.image.load('sprites/images/spike200.png')
    spike250=pygame.image.load('sprites/images/spike250.png')
    spike400=pygame.image.load('sprites/images/spike400.png')
    dirt=pygame.image.load('sprites/images/dirt.png')
    dirtshadow=pygame.image.load('sprites/images/dirtshadow.png')
    mud=(
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':600,'y':900},#1
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':1200,'y':900},#2
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':1800,'y':900},#3
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':800,'y':1500},#4
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':1400,'y':1500},#5
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':2000,'y':1500},#6
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':2400,'y':1150},#7
        {'image':pygame.transform.scale(dirtshadow,(300,30)),'x':2600,'y':1150},#8
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':3500,'y':900},#9
        {'image':pygame.transform.scale(dirtshadow,(300,30)),'x':3800,'y':1150},#10
        {'image':pygame.transform.scale(dirtshadow,(650,30)),'x':4100,'y':1500},#11
        {'image':pygame.transform.scale(dirtshadow,(100,30)),'x':4750,'y':1450},#12
        {'image':pygame.transform.scale(dirtshadow,(650,30)),'x':4850,'y':1500},#13
        {'image':pygame.transform.scale(dirtshadow,(400,30)),'x':5500,'y':1150},#14
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':5000,'y':1300},#15
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':5300,'y':1100},#16
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':4700,'y':650},#17
        {'image':pygame.transform.scale(dirt,(200,770)),'x':600,'y':930},#1
        {'image':pygame.transform.scale(dirt,(200,770)),'x':1200,'y':930},#2
        {'image':pygame.transform.scale(dirt,(200,770)),'x':1800,'y':930},#3
        {'image':pygame.transform.scale(dirt,(200,170)),'x':800,'y':1530},#4
        {'image':pygame.transform.scale(dirt,(200,170)),'x':1400,'y':1530},#5
        {'image':pygame.transform.scale(dirt,(200,170)),'x':2000,'y':1530},#6
        {'image':pygame.transform.scale(dirt,(200,520)),'x':2400,'y':1180},#7
        {'image':pygame.transform.scale(dirt,(300,270)),'x':2600,'y':1180},#8
        {'image':pygame.transform.scale(dirt,(200,220)),'x':3500,'y':930},#9
        {'image':pygame.transform.scale(dirt,(300,520)),'x':3800,'y':1180},#10
        {'image':pygame.transform.scale(dirt,(650,170)),'x':4100,'y':1530},#11
        {'image':pygame.transform.scale(dirt,(100,220)),'x':4750,'y':1480},#12
        {'image':pygame.transform.scale(dirt,(650,170)),'x':4850,'y':1530},#13
        {'image':pygame.transform.scale(dirt,(400,520)),'x':5500,'y':1180},#14
        {'image':pygame.transform.scale(dirt,(200,120)),'x':5000,'y':1330},#15
        {'image':pygame.transform.scale(dirt,(200,320)),'x':5300,'y':1130},#16
        {'image':pygame.transform.scale(dirt,(200,170)),'x':4700,'y':680}#17
        )

    platform=(
        pygame.transform.scale(surface,(400,300)),#1
        pygame.transform.scale(surface,(2200,50)),#2
        pygame.transform.scale(surface,(200,50)),#3
        pygame.transform.scale(surface,(200,50)),#4
        pygame.transform.scale(surface,(200,50)),#5
        pygame.transform.scale(surface,(200,50)),#6
        pygame.transform.scale(surface,(200,50)),#7
        pygame.transform.scale(surface,(200,50)),#8
        pygame.transform.scale(surface,(500,300)),#9
        pygame.transform.scale(surface,(600,300)),#10
        pygame.transform.scale(surface,(600,600)),#11
        pygame.transform.scale(surface,(200,50)),#12
        pygame.transform.scale(surface,(400,300)),#13
        pygame.transform.scale(surface,(2200,50)),#14
        pygame.transform.scale(surface,(650,50)),#15
        pygame.transform.scale(surface,(400,600)),#16
        pygame.transform.scale(surface,(650,50)),#17
        pygame.transform.scale(surface,(200,50)),#18
        pygame.transform.scale(surface,(200,50)),#19
        pygame.transform.scale(surface,(200,50)),#20
        pygame.transform.scale(surface,(400,300)),#21
        pygame.transform.scale(surface,(600,900))#22 
        )
    obstacles=(
        spike400,#1
        spike400,#2
        spike400,#3
        spike400,#4
        spike400,#5
        spike200,#6
        pygame.transform.rotate(spike250,90),#7
        pygame.transform.rotate(spike250,90),#8
        pygame.transform.rotate(spike250,-90),#9
        pygame.transform.rotate(spike400,90),#10
        pygame.transform.rotate(spike200,90),#11
        pygame.transform.flip(spike400,False,True),#12
        pygame.transform.flip(spike250,False,True),#13
        pygame.transform.flip(spike400,False,True),#14
        pygame.transform.flip(spike250,False,True)#15
        )

    showpoint=None
    timepoint=pygame.time.get_ticks()


    
    Life=4 #player life
    starno=0 #no of stars collected
    collectedcoins=0
    nogold=collectedcoins
    glist=[]
    for j in range(len(str(nogold))):
        glist.insert(0,nogold%10)
        nogold=nogold//10 
    dead=False #True if player is dead
    Hurt=False #True if player is hurt by traps
    injuredtime=pygame.time.get_ticks()
    timehurt=pygame.time.get_ticks()

    goright=False #True if player is moving right
    goleft=False #True if player is moving left
    onground=False #True if player is on platform/surface/ground
    jump_=False
    face_r=True #True if player is facing right, False if facing left
    Attack_r=True
    attack=False
    attacking=False
    ai=0
    
    playerpos={'x':0,'y':1350}#initial player position

    #-----------------platforms
    box=[
        {'x':0,'y':1450,'w':400,'h':300},#1
        {'x':400,'y':1700,'w':2200,'h':50},#2
        {'x':600,'y':850,'w':200,'h':50},#3
        {'x':800,'y':1450,'w':200,'h':50},#4
        {'x':1200,'y':850,'w':200,'h':50},#5
        {'x':1400,'y':1450,'w':200,'h':50},#6
        {'x':1800,'y':850,'w':200,'h':50},#7
        {'x':2000,'y':1450,'w':200,'h':50},#8
        {'x':2400,'y':850,'w':500,'h':300},#9
        {'x':2600,'y':1450,'w':600,'h':300},#10
        {'x':3200,'y':1150,'w':600,'h':600},#11
        {'x':3500,'y':850,'w':200,'h':50},#12
        {'x':3700,'y':850,'w':400,'h':300},#13
        {'x':3800,'y':1700,'w':2200,'h':50},#14
        {'x':4100,'y':1450,'w':650,'h':50},#15
        {'x':4600,'y':850,'w':400,'h':600},#16
        {'x':4850,'y':1450,'w':650,'h':50},#17
        {'x':4700,'y':600,'w':200,'h':50},#18
        {'x':5000,'y':1250,'w':200,'h':50},#19
        {'x':5300,'y':1050,'w':200,'h':50},#20
        {'x':5500,'y':850,'w':400,'h':300},#21
        {'x':5900,'y':850,'w':600,'h':900}#22
        ]
    
    #-----------------traps
    
    trap=[
        {'x':400,'y':1650,'w':400,'h':50},#1
        {'x':800,'y':1650,'w':400,'h':50},#2
        {'x':1200,'y':1650,'w':400,'h':50},#3
        {'x':1600,'y':1650,'w':400,'h':50},#4
        {'x':2000,'y':1650,'w':400,'h':50},#5
        {'x':2400,'y':1650,'w':200,'h':50},#6
        {'x':3150,'y':1175,'w':50,'h':250},#7
        {'x':3650,'y':900,'w':50,'h':250},#8
        {'x':4100,'y':850,'w':50,'h':250},#9
        {'x':4550,'y':850,'w':50,'h':400},#10
        {'x':4550,'y':1250,'w':50,'h':200},#11
        {'x':4100,'y':1500,'w':400,'h':50},#12
        {'x':4500,'y':1500,'w':250,'h':50},#13
        {'x':4850,'y':1500,'w':400,'h':50},#14
        {'x':5250,'y':1500,'w':250,'h':50}#15
        ]
    

    #-----------------stars
    starpoint=[
        {'x':2400,'y':750,'w':50,'h':50},
        {'x':4775,'y':1450,'w':50,'h':50},
        {'x':4775,'y':500,'w':50,'h':50}       
        ]
    goldcoin=[
        {'x':835,'y':1420,'w':30,'h':30},
        {'x':885,'y':1420,'w':30,'h':30},
        {'x':935,'y':1420,'w':30,'h':30},
        {'x':1435,'y':1420,'w':30,'h':30},
        {'x':1485,'y':1420,'w':30,'h':30},
        {'x':1535,'y':1420,'w':30,'h':30},
        {'x':2035,'y':1420,'w':30,'h':30},
        {'x':2085,'y':1420,'w':30,'h':30},
        {'x':2135,'y':1420,'w':30,'h':30},
        {'x':635,'y':820,'w':30,'h':30},
        {'x':685,'y':820,'w':30,'h':30},
        {'x':735,'y':820,'w':30,'h':30},
        {'x':1235,'y':820,'w':30,'h':30},
        {'x':1285,'y':820,'w':30,'h':30},
        {'x':1335,'y':820,'w':30,'h':30},        
        {'x':1835,'y':820,'w':30,'h':30},
        {'x':1885,'y':820,'w':30,'h':30},
        {'x':1935,'y':820,'w':30,'h':30},
        {'x':3235,'y':1120,'w':30,'h':30},
        {'x':3285,'y':1120,'w':30,'h':30},
        {'x':3335,'y':1120,'w':30,'h':30},
        {'x':3385,'y':1120,'w':30,'h':30},
        {'x':3435,'y':1120,'w':30,'h':30},
        {'x':3485,'y':1120,'w':30,'h':30},
        {'x':3760,'y':820,'w':30,'h':30},
        {'x':3810,'y':820,'w':30,'h':30},
        {'x':3860,'y':820,'w':30,'h':30},
        {'x':3910,'y':820,'w':30,'h':30},
        {'x':3960,'y':820,'w':30,'h':30},
        {'x':4010,'y':820,'w':30,'h':30},
        {'x':4660,'y':1670,'w':30,'h':30},
        {'x':4710,'y':1670,'w':30,'h':30},
        {'x':4760,'y':1670,'w':30,'h':30},
        {'x':4810,'y':1670,'w':30,'h':30},
        {'x':4860,'y':1670,'w':30,'h':30},
        {'x':4910,'y':1670,'w':30,'h':30},
        {'x':5035,'y':1220,'w':30,'h':30},
        {'x':5085,'y':1220,'w':30,'h':30},
        {'x':5135,'y':1220,'w':30,'h':30},
        {'x':5335,'y':1020,'w':30,'h':30},
        {'x':5385,'y':1020,'w':30,'h':30},
        {'x':5435,'y':1020,'w':30,'h':30}
        ]
    collectlife=[]
    movegold=[]

    monster=[
        {'x':2750,'y':1400,'w':50,'h':50,'move':5,'times':50,'increment':-1,'health':3},
        {'x':3000,'y':1400,'w':50,'h':50,'move':5,'times':1,'increment':1,'health':3},
        {'x':2500,'y':800,'w':50,'h':50,'move':5,'times':50,'increment':-1,'health':3},
        {'x':2750,'y':800,'w':50,'h':50,'move':5,'times':1,'increment':1,'health':3},
        {'x':4650,'y':800,'w':50,'h':50,'move':5,'times':50,'increment':-1,'health':3},
        {'x':4900,'y':800,'w':50,'h':50,'move':5,'times':1,'increment':1,'health':3},
        {'x':4150,'y':1400,'w':50,'h':50,'move':5,'times':50,'increment':-1,'health':3},
        {'x':4400,'y':1400,'w':50,'h':50,'move':5,'times':1,'increment':1,'health':3},
        {'x':5150,'y':1400,'w':50,'h':50,'move':5,'times':50,'increment':-1,'health':3},
        {'x':5400,'y':1400,'w':50,'h':50,'move':5,'times':1,'increment':1,'health':3},
        {'x':4150,'y':1650,'w':50,'h':50,'move':5,'times':50,'increment':-1,'health':3},
        {'x':4400,'y':1650,'w':50,'h':50,'move':5,'times':1,'increment':1,'health':3},
        {'x':5150,'y':1650,'w':50,'h':50,'move':5,'times':50,'increment':-1,'health':3},
        {'x':5400,'y':1650,'w':50,'h':50,'move':5,'times':1,'increment':1,'health':3}
        ]
    messagebordpos=[
        {'x':0,'y':1300},
        {'x':6350,'y':700}
        ]
    
    i=0 #player index
    player=standing_r
    timeindex=pygame.time.get_ticks()

    g=3 #gravity
    down=0 #down value

    timedelay=pygame.time.get_ticks()
    doublejump=True #True if player is onair and can be only used once, refills when player comes back to the ground
    landing=False #True when playe touches ground after jump
    freeze=False #True and makes player freeze for some time while landing

    changex=changey=0 #for camera movement
    timeeffect=timestar=pygame.time.get_ticks()
    hi=si=0
    playheartbreak=False
    playstarcollect=False
    sx=sy=0
    heal=False
    phi=0
    
    enemyx,enemyy,enemyexplode=0,0,False
    exi=0
    


    #-------------player margin on screen
    

    lmargin=400
    rmargin=880
    umargin=150
    bmargin=570
    levelX=levelY=0
    lwidth,lheight=6500,1750


    gamebgmusic.set_volume(0)
    gamebgmusic.play(-1)
    playrip=True
    runsoundplaying=False
    
    onRetry=False
    onMenu=False

    startwelcome=True
    timeintro=pygame.time.get_ticks()
    introsound.play()
    
    while True:
        
        mx,my=pygame.mouse.get_pos()#mouse position
        
        playerpast={'x':playerpos['x'],'y':playerpos['y']}#past position of player

        for event in pygame.event.get():#gets user interactions
            
            if event.type==QUIT:#checks if user clicked on quit
                pygame.quit()
                sys.exit()
            if not startwelcome:
                if event.type==KEYDOWN and event.key==K_ESCAPE:
                    gamebgmusic.stop()
                    runsound.stop()
                    runsoundplaying=False
                    Mode(data)
                
                if not dead:
                    if event.type==KEYDOWN and event.key==K_RIGHT:#right move
                        goright=True
                        goleft=False
                        face_r=True
                        player=walking_r
                    if event.type==KEYUP and event.key==K_RIGHT:
                        goright=False
                        if goleft:
                            player=walking_l
                        else:
                            player=standing_r
                            runsound.stop()

                    if event.type==KEYDOWN and event.key==K_LEFT:#left move
                        goright=False
                        goleft=True
                        face_r=False
                        player=walking_l
                    if event.type==KEYUP and event.key==K_LEFT:
                        goleft=False
                        if goright:
                            player=walking_r
                        else:
                            player=standing_l

                    if not freeze:
                        if onground and (event.type==KEYDOWN and event.key==K_UP):#jump move
                            jumpsound.play()
                            down=-30
                            onground=False
                        elif doublejump and (event.type==KEYDOWN and event.key==K_UP):
                            jumpsound.play()
                            down=-30
                            doublejump=False
                        if not attacking and (event.type==KEYDOWN and event.key==K_SPACE):
                            attacksound.play()
                            attack=attacking=True
                            if face_r:
                                Attack_r=True
                            else:
                                Attack_r=False
                            ai=0
                if dead and not Hurt:
                    if event.type==MOUSEBUTTONDOWN:
                        if onRetry:
                            buttonclickedsound.play()
                            screen.blit(afterdeathmessage[4],(265,210))
                            screen.blit(mouse,(mx,my))
                            pygame.display.update()
                            fpsclock.tick(FPS)
                            gamebgmusic.stop()
                            runsound.stop()
                            runsoundplaying=False
                            Level2(data)
                        if onMenu:
                            buttonclickedsound.play()
                            screen.blit(afterdeathmessage[2],(265,210))
                            screen.blit(mouse,(mx,my))
                            pygame.display.update()
                            fpsclock.tick(FPS)
                            gamebgmusic.stop()
                            runsound.stop()
                            runsoundplaying=False
                            Mode(data)

                                
        if not onground:#gravity pull/jump
            playerpos['y']+=down
            down+=g

        if not freeze:#right left motion
            if goright:
                playerpos['x']+=10
                                                    
            if goleft:
                playerpos['x']-=10

            if (onground and not runsoundplaying) and (goright or goleft):
                runsound.play(-1)
                runsoundplaying=True
            if (not goright and not goleft) or not onground:
                runsound.stop()
                runsoundplaying=False
                

        playerpos,onground,down,doublejump,landing,timedelay=collide(playerpast,playerpos,box,down,onground,doublejump,landing,timedelay)#changes playerpos accorting to platforms

        for j in range(len(monster)):            
            monster[j]['x']-=monster[j]['move']*monster[j]['increment']
            monster[j]['times']+=monster[j]['increment']
            if monster[j]['times']<=1:
                monster[j]['increment']=1
            elif monster[j]['times']>=50:
                monster[j]['increment']=-1

        Life,collectlife,collectedcoins,goldcoin,movegold,heal,showpoint,timepoint,phi=points(playerpos,Life,goldcoin,collectlife,collectedcoins,movegold,heal,showpoint,timepoint,phi)

        remove=None
        for j in range(len(movegold)):
            if 170<movegold[j]['x']<220 and 10<movegold[j]['y']<60:
                pointsound.play()
                remove=j
                showpoint=goldplus[movegold[j]['gold']]
                timepoint=pygame.time.get_ticks()
                glist=[]
                nogold=collectedcoins
                for k in range(len(str(nogold))):
                    glist.insert(0,nogold%10)
                    nogold=nogold//10 
                break
            else:
                movegold[j]['x']+=movegold[j]['cx']
                movegold[j]['y']+=movegold[j]['cy']
        if remove != None:
            movegold.pop(remove)
                
        starpoint,sx,sy,playstarcollect,timestar,starno=Star(starpoint,playerpos,playstarcollect,timestar,sx,sy,starno)#checks no of stars collected
        
        
        if not Hurt and not dead:
            timehurt,Life,Hurt,timeeffect,playheartbreak=_obstacle(playerpos,trap,timehurt,Life,Hurt,timeeffect,playheartbreak)#checks if player is hurt by obstacles
            if not Hurt:
                timehurt,Life,Hurt,timeeffect,playheartbreak=_obstacle(playerpos,monster,timehurt,Life,Hurt,timeeffect,playheartbreak)#checks if player is hurt by enemy
            if Life==0:
                dead=True
                goright=False
                goleft=False
                
                
        else:
            if pygame.time.get_ticks()>timehurt+1000:                
                Hurt=False
                
        if landing:
            landsound.play()
            freeze=True
        if pygame.time.get_ticks()>timedelay+100:
            freeze=False
            
        if attack:
            monster,attack,collectlife,goldcoin,enemyx,enemyy,enemyexplode=Playerattack(monster,playerpos,Attack_r,attack,collectlife,goldcoin,enemyx,enemyy,enemyexplode)

        #changes for camera movement

        if playerpos['x']<lmargin:
            if levelX>=0:
                changex=0-levelX
            else:                
                changex=lmargin-playerpos['x']
                if changex>-levelX:
                    changex=-levelX
        elif (playerpos['x']+pw)>rmargin:
            if levelX<=1280-lwidth:
                changex=1280-(levelX+lwidth)
            else:
                changex=rmargin-(playerpos['x']+pw)
                if changex<1280-(levelX+lwidth):
                    changex=1280-(levelX+lwidth)
        else:
            changex=0
        if playerpos['y']<umargin:
            if levelY>=0:
                changey=0-levelY
            else:
                changey=umargin-playerpos['y']
                if changey>-levelY:
                    changey=-levelY
        elif (playerpos['y']+ph)>bmargin:
            if levelY<=720-lheight:
                changey=720-(levelY+lheight)
            else:                
                changey=bmargin-(playerpos['y']+ph)
                if changey<720-(levelY+lheight):
                    changey=720-(levelY+lheight)
        else:
            changey=0

        if changex!=0:#changes x value for camera movement
            levelX+=changex
            playerpos['x']+=changex
            sx+=changex
            for k in range(len(box)):
                box[k]['x']+=changex
            for k in range(len(trap)):
                trap[k]['x']+=changex
            for k in range(len(starpoint)):
                starpoint[k]['x']+=changex
            for k in range(len(goldcoin)):
                goldcoin[k]['x']+=changex
            for k in range(len(collectlife)):
                collectlife[k]['x']+=changex
            for k in range(len(monster)):
                monster[k]['x']+=changex
            for k in range(len(mud)):
                mud[k]['x']+=changex
            for k in range(len(messagebordpos)):
                messagebordpos[k]['x']+=changex
                    
        if changey!=0:#changes y value for camera movement
            levelY+=changey
            playerpos['y']+=changey
            sy+=changey
            for k in range(len(box)):
                box[k]['y']+=changey
            for k in range(len(trap)):
                trap[k]['y']+=changey            
            for k in range(len(starpoint)):
                starpoint[k]['y']+=changey
            for k in range(len(goldcoin)):
                goldcoin[k]['y']+=changey
            for k in range(len(collectlife)):
                collectlife[k]['y']+=changey
            for k in range(len(monster)):
                monster[k]['y']+=changey
            for k in range(len(mud)):
                mud[k]['y']+=changey
            for k in range(len(messagebordpos)):
                messagebordpos[k]['y']+=changey

        if playerpos['x']+pw<0:
            gamebgmusic.stop()
            runsound.stop()
            runsoundplaying=False
            Mode(data)
        elif playerpos['x']>1280:
            #----------------------------------------------------------------------save progress
            gamebgmusic.stop()
            runsound.stop()
            runsoundplaying=False
            data[1]+=collectedcoins
            if data[0]['l2']<starno:
                data[0]['l2']=starno
            if data[0]['l3']==None:
                data[0]['l3']=0
            f=open('sprites/data/donotdelete.txt','wb')
            pickle.dump(data,f)
            f.close()
            Level3(data)


        

        #-----------------------------------------------------------blitting images
                
        screen.blit(background,(0,0))
        for j in range(len(messagebordpos)):
            screen.blit(messagebord[j],(messagebordpos[j]['x'],messagebordpos[j]['y']))
        for j in range(len(mud)):
            screen.blit(mud[j]['image'],(mud[j]['x'],mud[j]['y']))
        for j in range(len(box)):
            screen.blit(platform[j],(box[j]['x'],box[j]['y']))
        for j in range(len(trap)):
            screen.blit(obstacles[j],(trap[j]['x'],trap[j]['y']))
        for j in range(len(monster)):
            if monster[j]['increment']==-1:
                screen.blit(enemy1_l[i],(monster[j]['x'],monster[j]['y']))
            else:
                screen.blit(enemy1_r[i],(monster[j]['x'],monster[j]['y']))
            screen.blit(healthbar[monster[j]['health']-1],(monster[j]['x'],monster[j]['y']-15))
        for j in range(len(goldcoin)):
            screen.blit(dropgold,(goldcoin[j]['x'],goldcoin[j]['y']))
        for j in range(len(movegold)):
            screen.blit(dropgold,(movegold[j]['x'],movegold[j]['y']))
        for j in range(len(collectlife)):
            screen.blit(dropheart,(collectlife[j]['x'],collectlife[j]['y']))
        if enemyexplode:
            screen.blit(enemyblast[exi],(enemyx,enemyy))
            if exi==8:
                exi=0
                enemyexplode=False
            else:
                exi+=1

        for j in range(len(starpoint)):#star
            screen.blit(star_r[i],(starpoint[j]['x'],starpoint[j]['y']))

        #------------------------------------------------------------------player

        if Hurt and pygame.time.get_ticks()<injuredtime+100:
            if attacking:
                if face_r:
                    if onground:
                        screen.blit(p_hurt_r[2],(playerpos['x'],playerpos['y']-25))
                    elif not onground:
                        screen.blit(p_hurt_r[3],(playerpos['x'],playerpos['y']-25))
                elif not face_r:
                    if onground:
                        screen.blit(p_hurt_l[2],(playerpos['x']-50,playerpos['y']-25))
                    elif not onground:
                        screen.blit(p_hurt_l[3],(playerpos['x']-50,playerpos['y']-25))
            elif not attacking:            
                if face_r:
                    if onground:
                        screen.blit(p_hurt_r[0],(playerpos['x'],playerpos['y']))
                    elif not onground:
                        screen.blit(p_hurt_r[1],(playerpos['x'],playerpos['y']))
                elif not face_r:
                    if onground:
                        screen.blit(p_hurt_l[0],(playerpos['x'],playerpos['y']))
                    elif not onground:
                        screen.blit(p_hurt_l[1],(playerpos['x'],playerpos['y']))
        elif not Hurt and dead:
            if playrip:
                ripsound.play()
                playrip=False
            screen.blit(dead_p,(playerpos['x'],playerpos['y']))           

        else:
            if freeze:
                if face_r:
                    screen.blit(land_r,(playerpos['x'],playerpos['y']))
                elif not face_r:
                    screen.blit(land_l,(playerpos['x'],playerpos['y']))
            elif attacking:
                if face_r:
                    if onground:
                        screen.blit(attack_r[ai],(playerpos['x'],playerpos['y']-25))
                    elif not onground:
                        screen.blit(airattack_r[ai],(playerpos['x'],playerpos['y']-25))
                elif not face_r:
                    if onground:
                        screen.blit(attack_l[ai],(playerpos['x']-50,playerpos['y']-25))
                    elif not onground:
                        screen.blit(airattack_l[ai],(playerpos['x']-50,playerpos['y']-25))
            elif onground:
                screen.blit(player[i],(playerpos['x'],playerpos['y']))
            elif not onground:
                if face_r:
                    screen.blit(jump_r,(playerpos['x'],playerpos['y']))
                elif not face_r:
                    screen.blit(jump_l,(playerpos['x'],playerpos['y']))
        if pygame.time.get_ticks()>injuredtime+200:
            injuredtime=pygame.time.get_ticks()
        if heal:
            screen.blit(healtheffect[phi],(playerpos['x']-25,playerpos['y']-25))
            if phi==8:
                phi=0
                heal=False
            else:
                phi+=1
            
        #------------------------------------------------------------------player
    
            
        if playstarcollect:#starcollect
            screen.blit(starcollected[si],(sx,sy))
            if si==8:
                si=0
                playstarcollect=False
            elif pygame.time.get_ticks()>timestar+100:
                si+=1
                timestar=pygame.time.get_ticks()

        screen.blit(star_r[0],(25,25))#blits no of star collected
        screen.blit(_x,(75,35))
        screen.blit(_no[starno],(105,35))

        screen.blit(_gold,(185,25))
        screen.blit(_x,(235,35))
        gpx=265
        for j in glist:
            screen.blit(_no[j],(gpx,35))
            gpx+=30

            
        xheart=502
        for j in range(4):#heart
            if j<Life:
                screen.blit(heart[1],(xheart,25))
            else:
                screen.blit(heart[0],(xheart,25))
            xheart+=75
            
        if playheartbreak:#heartbreak
            screen.blit(heartbreak[hi],(477+(Life*75),0))
            if hi==8:
                hi=0
                playheartbreak=False
            elif pygame.time.get_ticks()>timeeffect+100:
                hi+=1
                timeeffect=pygame.time.get_ticks()
        screen.blit(esc_exit,(1105,25))
        
        if showpoint != None:
            screen.blit(showpoint,(565,100))
            if pygame.time.get_ticks()>timepoint+3000:
                showpoint=None
            

        #----------------------------------------------------------------------------index change
        

        if pygame.time.get_ticks()>timeindex+200:#change player index
            if i==3:
                i=0
            else:
                i+=1
            timeindex=pygame.time.get_ticks()
        if ai==3:
            ai=0
            attack=False
            attacking=False
        else:
            ai+=1
        if dead and not Hurt:
            screen.blit(blackscreen,(0,0))
            if 360<my<460:
                if 315<mx<615:
                    if not onRetry:
                        onbuttonsound.play()
                    onRetry=True
                else:
                    onRetry=False
                if 665<mx<965:
                    if not onMenu:
                        onbuttonsound.play()
                    onMenu=True
                else:
                    onMenu=False

            if onRetry:
                screen.blit(afterdeathmessage[3],(265,210))
            elif onMenu:
                screen.blit(afterdeathmessage[1],(265,210))
            else:
                screen.blit(afterdeathmessage[0],(265,210))
            screen.blit(mouse,(mx,my))
            pygame.display.update()
            fpsclock.tick(FPS)
            
        elif startwelcome:
            screen.blit(blackscreen,(0,0))
            screen.blit(levelbanner[1],(440,285))
            if pygame.time.get_ticks()>timeintro+4000:
                startwelcome=False
                gamebgmusic.set_volume(0.5)
            pygame.display.update()
            fpsclock.tick(FPS)   


        #screen.blit(mouse,(mx,my))#mouse
        else:       
            pygame.display.update()
            fpsclock.tick(FPS)

def Level3(data):
    surface=pygame.image.load('sprites/images/platform.png')
    obstacle=pygame.image.load('sprites/images/obstacle.png')
    spike200=pygame.image.load('sprites/images/spike200.png')
    spike250=pygame.image.load('sprites/images/spike250.png')
    spike400=pygame.image.load('sprites/images/spike400.png')
    dirt=pygame.image.load('sprites/images/dirt.png')
    dirtshadow=pygame.image.load('sprites/images/dirtshadow.png')
    mud=(
        {'image':pygame.transform.scale(dirtshadow,(300,30)),'x':400,'y':1000},#1
        {'image':pygame.transform.scale(dirtshadow,(400,30)),'x':1400,'y':1200},#2
        {'image':pygame.transform.scale(dirtshadow,(250,30)),'x':2650,'y':900},#3
        {'image':pygame.transform.scale(dirtshadow,(650,30)),'x':2250,'y':1450},#4
        {'image':pygame.transform.scale(dirtshadow,(300,30)),'x':3150,'y':1450},#5
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':3400,'y':1250},#6
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':4200,'y':900},#7
        {'image':pygame.transform.scale(dirtshadow,(100,30)),'x':4500,'y':1100},#8
        {'image':pygame.transform.scale(dirtshadow,(400,30)),'x':4600,'y':1100},#8
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':4650,'y':650},#9
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':5100,'y':900},#10
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':5300,'y':1100},#11
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':6100,'y':1100},#12
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':6300,'y':800},#13
        {'image':pygame.transform.scale(dirt,(300,220)),'x':400,'y':1030},#1
        {'image':pygame.transform.scale(dirt,(400,470)),'x':1400,'y':1230},#2
        {'image':pygame.transform.scale(dirt,(250,220)),'x':2650,'y':930},#3
        {'image':pygame.transform.scale(dirt,(650,220)),'x':2250,'y':1480},#4
        {'image':pygame.transform.scale(dirt,(300,220)),'x':3150,'y':1480},#5
        {'image':pygame.transform.scale(dirt,(200,420)),'x':3400,'y':1280},#6
        {'image':pygame.transform.scale(dirt,(200,370)),'x':4200,'y':930},#7
        {'image':pygame.transform.scale(dirt,(100,320)),'x':4500,'y':1130},#8
        {'image':pygame.transform.scale(dirt,(400,520)),'x':4600,'y':1130},#8
        {'image':pygame.transform.scale(dirt,(200,370)),'x':4650,'y':680},#9
        {'image':pygame.transform.scale(dirt,(200,420)),'x':5100,'y':930},#10
        {'image':pygame.transform.scale(dirt,(200,270)),'x':5300,'y':1130},#11
        {'image':pygame.transform.scale(dirt,(200,220)),'x':6100,'y':1130},#12
        {'image':pygame.transform.scale(dirt,(200,570)),'x':6300,'y':830}#13
        )

    platform=(
        pygame.transform.scale(surface,(900,500)),#1
        pygame.transform.scale(surface,(300,50)),#2
        pygame.transform.scale(surface,(500,250)),#3
        pygame.transform.scale(surface,(400,50)),#4
        pygame.transform.scale(surface,(400,50)),#5
        pygame.transform.scale(surface,(450,300)),#6
        pygame.transform.scale(surface,(850,300)),#7
        pygame.transform.scale(surface,(250,50)),#8
        pygame.transform.scale(surface,(1350,50)),#9
        pygame.transform.scale(surface,(250,300)),#10
        pygame.transform.scale(surface,(200,100)),#11
        pygame.transform.scale(surface,(600,300)),#12
        pygame.transform.scale(surface,(400,300)),#13
        pygame.transform.scale(surface,(200,50)),#14
        pygame.transform.scale(surface,(200,450)),#15
        pygame.transform.scale(surface,(200,300)),#16
        pygame.transform.scale(surface,(500,100)),#17
        pygame.transform.scale(surface,(500,50)),#18
        pygame.transform.scale(surface,(200,50)),#19
        pygame.transform.scale(surface,(200,400)),#20
        pygame.transform.scale(surface,(200,50)),#21
        pygame.transform.scale(surface,(200,50)),#22
        pygame.transform.scale(surface,(500,350)),#23
        pygame.transform.scale(surface,(500,400)),#24
        pygame.transform.scale(surface,(200,50)),#25
        pygame.transform.scale(surface,(200,350)),#26
        pygame.transform.scale(surface,(200,50)),#27
        pygame.transform.scale(surface,(200,400)),#28
        pygame.transform.scale(surface,(600,200))#29        
        )
    obstacles=(
        pygame.transform.flip(spike400,False,True),#1
        spike400,#2
        pygame.transform.rotate(spike250,-90),#3
        spike200,#4
        #spike200,#5
        spike200,#6
        pygame.transform.flip(spike200,False,True),#7
        pygame.transform.flip(spike200,False,True),#8
        spike200,#9
        pygame.transform.rotate(spike200,-90)#10
        )

    showpoint=None
    timepoint=pygame.time.get_ticks()


    
    Life=4 #player life
    starno=0 #no of stars collected
    collectedcoins=0
    nogold=collectedcoins
    glist=[]
    for j in range(len(str(nogold))):
        glist.insert(0,nogold%10)
        nogold=nogold//10 
    dead=False #True if player is dead
    Hurt=False #True if player is hurt by traps
    injuredtime=pygame.time.get_ticks()
    timehurt=pygame.time.get_ticks()

    goright=False #True if player is moving right
    goleft=False #True if player is moving left
    onground=False #True if player is on platform/surface/ground
    jump_=False
    face_r=True #True if player is facing right, False if facing left
    Attack_r=True
    attack=False
    attacking=False
    ai=0
    
    playerpos={'x':0,'y':100}#initial player position

    #-----------------platforms
    box=[
        {'x':0,'y':1250,'w':900,'h':500},#1
        {'x':400,'y':950,'w':300,'h':50},#2
        {'x':900,'y':1500,'w':500,'h':250},#3
        {'x':1400,'y':1150,'w':400,'h':50},#4
        {'x':1400,'y':1700,'w':400,'h':50},#5
        {'x':1800,'y':1450,'w':450,'h':300},#6
        {'x':2050,'y':1150,'w':850,'h':300},#7
        {'x':2650,'y':850,'w':250,'h':50},#8
        {'x':2250,'y':1700,'w':1350,'h':50},#9
        {'x':3150,'y':1150,'w':250,'h':300},#10
        {'x':3400,'y':1150,'w':200,'h':100},#11
        {'x':3600,'y':1450,'w':600,'h':300},#12
        {'x':3800,'y':1150,'w':400,'h':300},#13
        {'x':4200,'y':850,'w':200,'h':50},#14
        {'x':4200,'y':1300,'w':200,'h':450},#15
        {'x':4400,'y':1450,'w':200,'h':300},#16
        {'x':4600,'y':1650,'w':500,'h':100},#17
        {'x':4500,'y':1050,'w':500,'h':50},#18
        {'x':4650,'y':600,'w':200,'h':50},#19
        {'x':5100,'y':1350,'w':200,'h':400},#20
        {'x':5100,'y':850,'w':200,'h':50},#21
        {'x':5300,'y':1050,'w':200,'h':50},#22
        {'x':5300,'y':1400,'w':500,'h':350},#23
        {'x':5800,'y':1350,'w':500,'h':400},#24
        {'x':6100,'y':1050,'w':200,'h':50},#25
        {'x':6300,'y':1400,'w':200,'h':350},#26
        {'x':6300,'y':750,'w':200,'h':50},#27
        {'x':6500,'y':1350,'w':200,'h':400},#28
        {'x':6700,'y':1550,'w':600,'h':200}#29
        ]
    
    #-----------------traps
    
    trap=[
        {'x':1400,'y':1200,'w':400,'h':50},#1
        {'x':1400,'y':1650,'w':400,'h':50},#2
        {'x':2250,'y':1450,'w':50,'h':250},#3
        {'x':4200,'y':1250,'w':200,'h':50},#4
        #{'x':4400,'y':1400,'w':200,'h':50},#5
        {'x':4600,'y':1600,'w':200,'h':50},#6
        {'x':5300,'y':1100,'w':200,'h':50},#7
        {'x':6100,'y':1100,'w':200,'h':50},#8
        {'x':6300,'y':1350,'w':200,'h':50},#9
        {'x':6700,'y':1350,'w':50,'h':200}#10
        ]
    

    #-----------------stars
    starpoint=[
        {'x':2350,'y':1550,'w':50,'h':50},
        {'x':5000,'y':1450,'w':50,'h':50},
        {'x':6375,'y':800,'w':50,'h':50}       
        ]
    goldcoin=[
        {'x':460,'y':920,'w':30,'h':30},
        {'x':510,'y':920,'w':30,'h':30},
        {'x':560,'y':920,'w':30,'h':30},
        {'x':610,'y':920,'w':30,'h':30},
        {'x':1870,'y':1420,'w':30,'h':30},
        {'x':1920,'y':1420,'w':30,'h':30},
        {'x':1970,'y':1420,'w':30,'h':30},
        {'x':2720,'y':820,'w':30,'h':30},
        {'x':2770,'y':820,'w':30,'h':30},
        {'x':2820,'y':820,'w':30,'h':30},
        {'x':2920,'y':1670,'w':30,'h':30},
        {'x':2970,'y':1670,'w':30,'h':30},
        {'x':3020,'y':1670,'w':30,'h':30},
        {'x':3070,'y':1670,'w':30,'h':30},
        {'x':3120,'y':1670,'w':30,'h':30},        
        {'x':3220,'y':1120,'w':30,'h':30},
        {'x':3270,'y':1120,'w':30,'h':30},
        {'x':3320,'y':1120,'w':30,'h':30},
        {'x':3370,'y':1120,'w':30,'h':30},
        {'x':3420,'y':1120,'w':30,'h':30},
        {'x':3470,'y':1120,'w':30,'h':30},
        {'x':3520,'y':1120,'w':30,'h':30},
        {'x':4285,'y':820,'w':30,'h':30},
        {'x':4735,'y':570,'w':30,'h':30},
        {'x':5185,'y':820,'w':30,'h':30},
        {'x':6345,'y':720,'w':30,'h':30},
        {'x':6395,'y':720,'w':30,'h':30},
        {'x':6445,'y':720,'w':30,'h':30}
        ]
    collectlife=[]
    movegold=[]

    monster=[
        {'x':1000,'y':1450,'w':50,'h':50,'move':5,'times':50,'increment':-1,'health':3},
        {'x':1700,'y':1100,'w':50,'h':50,'move':5,'times':1,'increment':1,'health':3},
        {'x':2200,'y':1100,'w':50,'h':50,'move':5,'times':50,'increment':-1,'health':3},
        {'x':2450,'y':1100,'w':50,'h':50,'move':5,'times':1,'increment':1,'health':3},
        {'x':2600,'y':1650,'w':50,'h':50,'move':5,'times':50,'increment':-1,'health':3},
        {'x':3400,'y':1650,'w':50,'h':50,'move':5,'times':1,'increment':1,'health':3},
        {'x':4600,'y':1000,'w':50,'h':50,'move':5,'times':50,'increment':-1,'health':3},
        {'x':4850,'y':1000,'w':50,'h':50,'move':5,'times':1,'increment':1,'health':3},
        {'x':5400,'y':1350,'w':50,'h':50,'move':5,'times':50,'increment':-1,'health':3},
        {'x':5650,'y':1350,'w':50,'h':50,'move':5,'times':1,'increment':1,'health':3},
        {'x':6800,'y':1500,'w':50,'h':50,'move':5,'times':50,'increment':-1,'health':3},
        {'x':7050,'y':1500,'w':50,'h':50,'move':5,'times':1,'increment':1,'health':3}
        ]
    messagebordpos=[
        {'x':1,'y':1100},
        {'x':7150,'y':1400}
        ]
    
    i=0 #player index
    player=standing_r
    timeindex=pygame.time.get_ticks()

    g=3 #gravity
    down=0 #down value

    timedelay=pygame.time.get_ticks()
    doublejump=True #True if player is onair and can be only used once, refills when player comes back to the ground
    landing=False #True when playe touches ground after jump
    freeze=False #True and makes player freeze for some time while landing

    changex=changey=0 #for camera movement
    timeeffect=timestar=pygame.time.get_ticks()
    hi=si=0
    playheartbreak=False
    playstarcollect=False
    sx=sy=0
    heal=False
    phi=0
    
    enemyx,enemyy,enemyexplode=0,0,False
    exi=0
    


    #-------------player margin on screen
    

    lmargin=400
    rmargin=880
    umargin=150
    bmargin=570
    levelX=levelY=0
    lwidth,lheight=7300,1750


    gamebgmusic.set_volume(0)
    gamebgmusic.play(-1)
    playrip=True
    runsoundplaying=False

    onRetry=False
    onMenu=False

    startwelcome=True
    timeintro=pygame.time.get_ticks()
    introsound.play()
    
    while True:
        
        mx,my=pygame.mouse.get_pos()#mouse position
        
        playerpast={'x':playerpos['x'],'y':playerpos['y']}#past position of player

        for event in pygame.event.get():#gets user interactions
            
            if event.type==QUIT:#checks if user clicked on quit
                pygame.quit()
                sys.exit()
            if not startwelcome:
                if event.type==KEYDOWN and event.key==K_ESCAPE:
                    gamebgmusic.stop()
                    runsound.stop()
                    runsoundplaying=False
                    Mode(data)
                
                if not dead:
                    if event.type==KEYDOWN and event.key==K_RIGHT:#right move
                        goright=True
                        goleft=False
                        face_r=True
                        player=walking_r
                    if event.type==KEYUP and event.key==K_RIGHT:
                        goright=False
                        if goleft:
                            player=walking_l
                        else:
                            player=standing_r
                            runsound.stop()

                    if event.type==KEYDOWN and event.key==K_LEFT:#left move
                        goright=False
                        goleft=True
                        face_r=False
                        player=walking_l
                    if event.type==KEYUP and event.key==K_LEFT:
                        goleft=False
                        if goright:
                            player=walking_r
                        else:
                            player=standing_l

                    if not freeze:
                        if onground and (event.type==KEYDOWN and event.key==K_UP):#jump move
                            jumpsound.play()
                            down=-30
                            onground=False
                        elif doublejump and (event.type==KEYDOWN and event.key==K_UP):
                            jumpsound.play()
                            down=-30
                            doublejump=False
                        if not attacking and (event.type==KEYDOWN and event.key==K_SPACE):
                            attacksound.play()
                            attack=attacking=True
                            if face_r:
                                Attack_r=True
                            else:
                                Attack_r=False
                            ai=0
                if dead and not Hurt:
                    if event.type==MOUSEBUTTONDOWN:
                        if onRetry:
                            buttonclickedsound.play()
                            screen.blit(afterdeathmessage[4],(265,210))
                            screen.blit(mouse,(mx,my))
                            pygame.display.update()
                            fpsclock.tick(FPS)
                            gamebgmusic.stop()
                            runsound.stop()
                            runsoundplaying=False
                            Level3(data)
                        if onMenu:
                            buttonclickedsound.play()
                            screen.blit(afterdeathmessage[2],(265,210))
                            screen.blit(mouse,(mx,my))
                            pygame.display.update()
                            fpsclock.tick(FPS)
                            gamebgmusic.stop()
                            runsound.stop()
                            runsoundplaying=False
                            Mode(data)

                                
        if not onground:#gravity pull/jump
            playerpos['y']+=down
            down+=g

        if not freeze:#right left motion
            if goright:
                playerpos['x']+=10
                                                    
            if goleft:
                playerpos['x']-=10

            if (onground and not runsoundplaying) and (goright or goleft):
                runsound.play(-1)
                runsoundplaying=True
            if (not goright and not goleft) or not onground:
                runsound.stop()
                runsoundplaying=False
                

        playerpos,onground,down,doublejump,landing,timedelay=collide(playerpast,playerpos,box,down,onground,doublejump,landing,timedelay)#changes playerpos accorting to platforms

        for j in range(len(monster)):            
            monster[j]['x']-=monster[j]['move']*monster[j]['increment']
            monster[j]['times']+=monster[j]['increment']
            if monster[j]['times']<=1:
                monster[j]['increment']=1
            elif monster[j]['times']>=50:
                monster[j]['increment']=-1

        Life,collectlife,collectedcoins,goldcoin,movegold,heal,showpoint,timepoint,phi=points(playerpos,Life,goldcoin,collectlife,collectedcoins,movegold,heal,showpoint,timepoint,phi)

        remove=None
        for j in range(len(movegold)):
            if 170<movegold[j]['x']<220 and 10<movegold[j]['y']<60:
                pointsound.play()
                remove=j
                showpoint=goldplus[movegold[j]['gold']]
                timepoint=pygame.time.get_ticks()
                glist=[]
                nogold=collectedcoins
                for k in range(len(str(nogold))):
                    glist.insert(0,nogold%10)
                    nogold=nogold//10 
                break
            else:
                movegold[j]['x']+=movegold[j]['cx']
                movegold[j]['y']+=movegold[j]['cy']
        if remove != None:
            movegold.pop(remove)
                
        starpoint,sx,sy,playstarcollect,timestar,starno=Star(starpoint,playerpos,playstarcollect,timestar,sx,sy,starno)#checks no of stars collected
        
        
        if not Hurt and not dead:
            timehurt,Life,Hurt,timeeffect,playheartbreak=_obstacle(playerpos,trap,timehurt,Life,Hurt,timeeffect,playheartbreak)#checks if player is hurt by obstacles
            if not Hurt:
                timehurt,Life,Hurt,timeeffect,playheartbreak=_obstacle(playerpos,monster,timehurt,Life,Hurt,timeeffect,playheartbreak)#checks if player is hurt by enemy
            if Life==0:
                dead=True
                goright=False
                goleft=False
                
                
        else:
            if pygame.time.get_ticks()>timehurt+1000:                
                Hurt=False
                
        if landing:
            landsound.play()
            freeze=True
        if pygame.time.get_ticks()>timedelay+100:
            freeze=False
            
        if attack:
            monster,attack,collectlife,goldcoin,enemyx,enemyy,enemyexplode=Playerattack(monster,playerpos,Attack_r,attack,collectlife,goldcoin,enemyx,enemyy,enemyexplode)

        #changes for camera movement

        if playerpos['x']<lmargin:
            if levelX>=0:
                changex=0-levelX
            else:                
                changex=lmargin-playerpos['x']
                if changex>-levelX:
                    changex=-levelX
        elif (playerpos['x']+pw)>rmargin:
            if levelX<=1280-lwidth:
                changex=1280-(levelX+lwidth)
            else:
                changex=rmargin-(playerpos['x']+pw)
                if changex<1280-(levelX+lwidth):
                    changex=1280-(levelX+lwidth)
        else:
            changex=0
        if playerpos['y']<umargin:
            if levelY>=0:
                changey=0-levelY
            else:
                changey=umargin-playerpos['y']
                if changey>-levelY:
                    changey=-levelY
        elif (playerpos['y']+ph)>bmargin:
            if levelY<=720-lheight:
                changey=720-(levelY+lheight)
            else:                
                changey=bmargin-(playerpos['y']+ph)
                if changey<720-(levelY+lheight):
                    changey=720-(levelY+lheight)
        else:
            changey=0

        if changex!=0:#changes x value for camera movement
            levelX+=changex
            playerpos['x']+=changex
            sx+=changex
            for k in range(len(box)):
                box[k]['x']+=changex
            for k in range(len(trap)):
                trap[k]['x']+=changex
            for k in range(len(starpoint)):
                starpoint[k]['x']+=changex
            for k in range(len(goldcoin)):
                goldcoin[k]['x']+=changex
            for k in range(len(collectlife)):
                collectlife[k]['x']+=changex
            for k in range(len(monster)):
                monster[k]['x']+=changex
            for k in range(len(mud)):
                mud[k]['x']+=changex
            for k in range(len(messagebordpos)):
                messagebordpos[k]['x']+=changex
                    
        if changey!=0:#changes y value for camera movement
            levelY+=changey
            playerpos['y']+=changey
            sy+=changey
            for k in range(len(box)):
                box[k]['y']+=changey
            for k in range(len(trap)):
                trap[k]['y']+=changey            
            for k in range(len(starpoint)):
                starpoint[k]['y']+=changey
            for k in range(len(goldcoin)):
                goldcoin[k]['y']+=changey
            for k in range(len(collectlife)):
                collectlife[k]['y']+=changey
            for k in range(len(monster)):
                monster[k]['y']+=changey
            for k in range(len(mud)):
                mud[k]['y']+=changey
            for k in range(len(messagebordpos)):
                messagebordpos[k]['y']+=changey

        if playerpos['x']+pw<0:
            gamebgmusic.stop()
            runsound.stop()
            runsoundplaying=False
            Mode(data)
        elif playerpos['x']>1280:
            #----------------------------------------------------------------------save progress
            gamebgmusic.stop()
            runsound.stop()
            runsoundplaying=False
            data[1]+=collectedcoins
            if data[0]['l3']<starno:
                data[0]['l3']=starno
            if data[0]['l4']==None:
                data[0]['l4']=0
            f=open('sprites/data/donotdelete.txt','wb')
            pickle.dump(data,f)
            f.close()
            Level(4)


        

        #-----------------------------------------------------------blitting images
                
        screen.blit(background,(0,0))
        for j in range(len(messagebordpos)):
            screen.blit(messagebord[j],(messagebordpos[j]['x'],messagebordpos[j]['y']))
        for j in range(len(mud)):
            screen.blit(mud[j]['image'],(mud[j]['x'],mud[j]['y']))
        for j in range(len(box)):
            screen.blit(platform[j],(box[j]['x'],box[j]['y']))
        for j in range(len(trap)):
            screen.blit(obstacles[j],(trap[j]['x'],trap[j]['y']))
        for j in range(len(monster)):
            if monster[j]['increment']==-1:
                screen.blit(enemy1_l[i],(monster[j]['x'],monster[j]['y']))
            else:
                screen.blit(enemy1_r[i],(monster[j]['x'],monster[j]['y']))
            screen.blit(healthbar[monster[j]['health']-1],(monster[j]['x'],monster[j]['y']-15))
        for j in range(len(goldcoin)):
            screen.blit(dropgold,(goldcoin[j]['x'],goldcoin[j]['y']))
        for j in range(len(movegold)):
            screen.blit(dropgold,(movegold[j]['x'],movegold[j]['y']))
        for j in range(len(collectlife)):
            screen.blit(dropheart,(collectlife[j]['x'],collectlife[j]['y']))
        if enemyexplode:
            screen.blit(enemyblast[exi],(enemyx,enemyy))
            if exi==8:
                exi=0
                enemyexplode=False
            else:
                exi+=1

        for j in range(len(starpoint)):#star
            screen.blit(star_r[i],(starpoint[j]['x'],starpoint[j]['y']))

        #------------------------------------------------------------------player

        if Hurt and pygame.time.get_ticks()<injuredtime+100:
            if attacking:
                if face_r:
                    if onground:
                        screen.blit(p_hurt_r[2],(playerpos['x'],playerpos['y']-25))
                    elif not onground:
                        screen.blit(p_hurt_r[3],(playerpos['x'],playerpos['y']-25))
                elif not face_r:
                    if onground:
                        screen.blit(p_hurt_l[2],(playerpos['x']-50,playerpos['y']-25))
                    elif not onground:
                        screen.blit(p_hurt_l[3],(playerpos['x']-50,playerpos['y']-25))
            elif not attacking:            
                if face_r:
                    if onground:
                        screen.blit(p_hurt_r[0],(playerpos['x'],playerpos['y']))
                    elif not onground:
                        screen.blit(p_hurt_r[1],(playerpos['x'],playerpos['y']))
                elif not face_r:
                    if onground:
                        screen.blit(p_hurt_l[0],(playerpos['x'],playerpos['y']))
                    elif not onground:
                        screen.blit(p_hurt_l[1],(playerpos['x'],playerpos['y']))
        elif not Hurt and dead:
            if playrip:
                ripsound.play()
                playrip=False
            screen.blit(dead_p,(playerpos['x'],playerpos['y']))           

        else:
            if freeze:
                if face_r:
                    screen.blit(land_r,(playerpos['x'],playerpos['y']))
                elif not face_r:
                    screen.blit(land_l,(playerpos['x'],playerpos['y']))
            elif attacking:
                if face_r:
                    if onground:
                        screen.blit(attack_r[ai],(playerpos['x'],playerpos['y']-25))
                    elif not onground:
                        screen.blit(airattack_r[ai],(playerpos['x'],playerpos['y']-25))
                elif not face_r:
                    if onground:
                        screen.blit(attack_l[ai],(playerpos['x']-50,playerpos['y']-25))
                    elif not onground:
                        screen.blit(airattack_l[ai],(playerpos['x']-50,playerpos['y']-25))
            elif onground:
                screen.blit(player[i],(playerpos['x'],playerpos['y']))
            elif not onground:
                if face_r:
                    screen.blit(jump_r,(playerpos['x'],playerpos['y']))
                elif not face_r:
                    screen.blit(jump_l,(playerpos['x'],playerpos['y']))
        if pygame.time.get_ticks()>injuredtime+200:
            injuredtime=pygame.time.get_ticks()
        if heal:
            screen.blit(healtheffect[phi],(playerpos['x']-25,playerpos['y']-25))
            if phi==8:
                phi=0
                heal=False
            else:
                phi+=1
            
        #------------------------------------------------------------------player
    
            
        if playstarcollect:#starcollect
            screen.blit(starcollected[si],(sx,sy))
            if si==8:
                si=0
                playstarcollect=False
            elif pygame.time.get_ticks()>timestar+100:
                si+=1
                timestar=pygame.time.get_ticks()

        screen.blit(star_r[0],(25,25))#blits no of star collected
        screen.blit(_x,(75,35))
        screen.blit(_no[starno],(105,35))

        screen.blit(_gold,(185,25))
        screen.blit(_x,(235,35))
        gpx=265
        for j in glist:
            screen.blit(_no[j],(gpx,35))
            gpx+=30

            
        xheart=502
        for j in range(4):#heart
            if j<Life:
                screen.blit(heart[1],(xheart,25))
            else:
                screen.blit(heart[0],(xheart,25))
            xheart+=75
            
        if playheartbreak:#heartbreak
            screen.blit(heartbreak[hi],(477+(Life*75),0))
            if hi==8:
                hi=0
                playheartbreak=False
            elif pygame.time.get_ticks()>timeeffect+100:
                hi+=1
                timeeffect=pygame.time.get_ticks()
        screen.blit(esc_exit,(1105,25))
        
        if showpoint != None:
            screen.blit(showpoint,(565,100))
            if pygame.time.get_ticks()>timepoint+3000:
                showpoint=None
            

        #----------------------------------------------------------------------------index change
        

        if pygame.time.get_ticks()>timeindex+200:#change player index
            if i==3:
                i=0
            else:
                i+=1
            timeindex=pygame.time.get_ticks()
        if ai==3:
            ai=0
            attack=False
            attacking=False
        else:
            ai+=1
        if dead and not Hurt:
            screen.blit(blackscreen,(0,0))
            if 360<my<460:
                if 315<mx<615:
                    if not onRetry:
                        onbuttonsound.play()
                    onRetry=True
                else:
                    onRetry=False
                if 665<mx<965:
                    if not onMenu:
                        onbuttonsound.play()
                    onMenu=True
                else:
                    onMenu=False

            if onRetry:
                screen.blit(afterdeathmessage[3],(265,210))
            elif onMenu:
                screen.blit(afterdeathmessage[1],(265,210))
            else:
                screen.blit(afterdeathmessage[0],(265,210))
            screen.blit(mouse,(mx,my))
            pygame.display.update()
            fpsclock.tick(FPS)  

        elif startwelcome:
            screen.blit(blackscreen,(0,0))
            screen.blit(levelbanner[2],(440,285))
            if pygame.time.get_ticks()>timeintro+4000:
                startwelcome=False
                gamebgmusic.set_volume(0.5)
            pygame.display.update()
            fpsclock.tick(FPS)
            
        #screen.blit(mouse,(mx,my))#mouse
        else:       
            pygame.display.update()
            fpsclock.tick(FPS)

def Level4(data):
    surface=pygame.image.load('sprites/images/platform.png')
    obstacle=pygame.image.load('sprites/images/obstacle.png')
    spike200=pygame.image.load('sprites/images/spike200.png')
    spike250=pygame.image.load('sprites/images/spike250.png')
    spike400=pygame.image.load('sprites/images/spike400.png')
    dirt=pygame.image.load('sprites/images/dirt.png')
    dirtshadow=pygame.image.load('sprites/images/dirtshadow.png')
    mud=(
        {'image':pygame.transform.scale(dirtshadow,(300,30)),'x':400,'y':1000},#1
        {'image':pygame.transform.scale(dirtshadow,(400,30)),'x':1400,'y':1200},#2
        {'image':pygame.transform.scale(dirtshadow,(250,30)),'x':2650,'y':900},#3
        {'image':pygame.transform.scale(dirtshadow,(650,30)),'x':2250,'y':1450},#4
        {'image':pygame.transform.scale(dirtshadow,(300,30)),'x':3150,'y':1450},#5
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':3400,'y':1250},#6
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':4200,'y':900},#7
        {'image':pygame.transform.scale(dirtshadow,(100,30)),'x':4500,'y':1100},#8
        {'image':pygame.transform.scale(dirtshadow,(400,30)),'x':4600,'y':1100},#8
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':4650,'y':650},#9
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':5100,'y':900},#10
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':5300,'y':1100},#11
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':6100,'y':1100},#12
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':6300,'y':800},#13
        {'image':pygame.transform.scale(dirt,(300,220)),'x':400,'y':1030},#1
        {'image':pygame.transform.scale(dirt,(400,470)),'x':1400,'y':1230},#2
        {'image':pygame.transform.scale(dirt,(250,220)),'x':2650,'y':930},#3
        {'image':pygame.transform.scale(dirt,(650,220)),'x':2250,'y':1480},#4
        {'image':pygame.transform.scale(dirt,(300,220)),'x':3150,'y':1480},#5
        {'image':pygame.transform.scale(dirt,(200,420)),'x':3400,'y':1280},#6
        {'image':pygame.transform.scale(dirt,(200,370)),'x':4200,'y':930},#7
        {'image':pygame.transform.scale(dirt,(100,320)),'x':4500,'y':1130},#8
        {'image':pygame.transform.scale(dirt,(400,520)),'x':4600,'y':1130},#8
        {'image':pygame.transform.scale(dirt,(200,370)),'x':4650,'y':680},#9
        {'image':pygame.transform.scale(dirt,(200,420)),'x':5100,'y':930},#10
        {'image':pygame.transform.scale(dirt,(200,270)),'x':5300,'y':1130},#11
        {'image':pygame.transform.scale(dirt,(200,220)),'x':6100,'y':1130},#12
        {'image':pygame.transform.scale(dirt,(200,570)),'x':6300,'y':830}#13
        )

    platform=(
        pygame.transform.scale(surface,(900,500)),#1
        pygame.transform.scale(surface,(300,50)),#2
        pygame.transform.scale(surface,(500,250)),#3
        pygame.transform.scale(surface,(400,50)),#4
        pygame.transform.scale(surface,(400,50)),#5
        pygame.transform.scale(surface,(450,300)),#6
        pygame.transform.scale(surface,(850,300)),#7
        pygame.transform.scale(surface,(250,50)),#8
        pygame.transform.scale(surface,(1350,50)),#9
        pygame.transform.scale(surface,(250,300)),#10
        pygame.transform.scale(surface,(200,100)),#11
        pygame.transform.scale(surface,(600,300)),#12
        pygame.transform.scale(surface,(400,300)),#13
        pygame.transform.scale(surface,(200,50)),#14
        pygame.transform.scale(surface,(200,450)),#15
        pygame.transform.scale(surface,(200,300)),#16
        pygame.transform.scale(surface,(500,100)),#17
        pygame.transform.scale(surface,(500,50)),#18
        pygame.transform.scale(surface,(200,50)),#19
        pygame.transform.scale(surface,(200,400)),#20
        pygame.transform.scale(surface,(200,50)),#21
        pygame.transform.scale(surface,(200,50)),#22
        pygame.transform.scale(surface,(500,350)),#23
        pygame.transform.scale(surface,(500,400)),#24
        pygame.transform.scale(surface,(200,50)),#25
        pygame.transform.scale(surface,(200,350)),#26
        pygame.transform.scale(surface,(200,50)),#27
        pygame.transform.scale(surface,(200,400)),#28
        pygame.transform.scale(surface,(600,200))#29        
        )
    obstacles=(
        pygame.transform.flip(spike400,False,True),#1
        spike400,#2
        pygame.transform.rotate(spike250,-90),#3
        spike200,#4
        #spike200,#5
        spike200,#6
        pygame.transform.flip(spike200,False,True),#7
        pygame.transform.flip(spike200,False,True),#8
        spike200,#9
        pygame.transform.rotate(spike200,-90)#10
        )

    showpoint=None
    timepoint=pygame.time.get_ticks()


    
    Life=4 #player life
    starno=0 #no of stars collected
    collectedcoins=0
    nogold=collectedcoins
    glist=[]
    for j in range(len(str(nogold))):
        glist.insert(0,nogold%10)
        nogold=nogold//10 
    dead=False #True if player is dead
    Hurt=False #True if player is hurt by traps
    injuredtime=pygame.time.get_ticks()
    timehurt=pygame.time.get_ticks()

    goright=False #True if player is moving right
    goleft=False #True if player is moving left
    onground=False #True if player is on platform/surface/ground
    jump_=False
    face_r=True #True if player is facing right, False if facing left
    Attack_r=True
    attack=False
    attacking=False
    ai=0
    
    playerpos={'x':0,'y':100}#initial player position

    #-----------------platforms
    box=[
        {'x':0,'y':1250,'w':900,'h':500},#1
        {'x':400,'y':950,'w':300,'h':50},#2
        {'x':900,'y':1500,'w':500,'h':250},#3
        {'x':1400,'y':1150,'w':400,'h':50},#4
        {'x':1400,'y':1700,'w':400,'h':50},#5
        {'x':1800,'y':1450,'w':450,'h':300},#6
        {'x':2050,'y':1150,'w':850,'h':300},#7
        {'x':2650,'y':850,'w':250,'h':50},#8
        {'x':2250,'y':1700,'w':1350,'h':50},#9
        {'x':3150,'y':1150,'w':250,'h':300},#10
        {'x':3400,'y':1150,'w':200,'h':100},#11
        {'x':3600,'y':1450,'w':600,'h':300},#12
        {'x':3800,'y':1150,'w':400,'h':300},#13
        {'x':4200,'y':850,'w':200,'h':50},#14
        {'x':4200,'y':1300,'w':200,'h':450},#15
        {'x':4400,'y':1450,'w':200,'h':300},#16
        {'x':4600,'y':1650,'w':500,'h':100},#17
        {'x':4500,'y':1050,'w':500,'h':50},#18
        {'x':4650,'y':600,'w':200,'h':50},#19
        {'x':5100,'y':1350,'w':200,'h':400},#20
        {'x':5100,'y':850,'w':200,'h':50},#21
        {'x':5300,'y':1050,'w':200,'h':50},#22
        {'x':5300,'y':1400,'w':500,'h':350},#23
        {'x':5800,'y':1350,'w':500,'h':400},#24
        {'x':6100,'y':1050,'w':200,'h':50},#25
        {'x':6300,'y':1400,'w':200,'h':350},#26
        {'x':6300,'y':750,'w':200,'h':50},#27
        {'x':6500,'y':1350,'w':200,'h':400},#28
        {'x':6700,'y':1550,'w':600,'h':200}#29
        ]
    
    #-----------------traps
    
    trap=[
        {'x':1400,'y':1200,'w':400,'h':50},#1
        {'x':1400,'y':1650,'w':400,'h':50},#2
        {'x':2250,'y':1450,'w':50,'h':250},#3
        {'x':4200,'y':1250,'w':200,'h':50},#4
        #{'x':4400,'y':1400,'w':200,'h':50},#5
        {'x':4600,'y':1600,'w':200,'h':50},#6
        {'x':5300,'y':1100,'w':200,'h':50},#7
        {'x':6100,'y':1100,'w':200,'h':50},#8
        {'x':6300,'y':1350,'w':200,'h':50},#9
        {'x':6700,'y':1350,'w':50,'h':200}#10
        ]
    

    #-----------------stars
    starpoint=[
        {'x':2350,'y':1550,'w':50,'h':50},
        {'x':5000,'y':1450,'w':50,'h':50},
        {'x':6375,'y':800,'w':50,'h':50}       
        ]
    goldcoin=[
        {'x':460,'y':920,'w':30,'h':30},
        {'x':510,'y':920,'w':30,'h':30},
        {'x':560,'y':920,'w':30,'h':30},
        {'x':610,'y':920,'w':30,'h':30},
        {'x':1870,'y':1420,'w':30,'h':30},
        {'x':1920,'y':1420,'w':30,'h':30},
        {'x':1970,'y':1420,'w':30,'h':30},
        {'x':2720,'y':820,'w':30,'h':30},
        {'x':2770,'y':820,'w':30,'h':30},
        {'x':2820,'y':820,'w':30,'h':30},
        {'x':2920,'y':1670,'w':30,'h':30},
        {'x':2970,'y':1670,'w':30,'h':30},
        {'x':3020,'y':1670,'w':30,'h':30},
        {'x':3070,'y':1670,'w':30,'h':30},
        {'x':3120,'y':1670,'w':30,'h':30},        
        {'x':3220,'y':1120,'w':30,'h':30},
        {'x':3270,'y':1120,'w':30,'h':30},
        {'x':3320,'y':1120,'w':30,'h':30},
        {'x':3370,'y':1120,'w':30,'h':30},
        {'x':3420,'y':1120,'w':30,'h':30},
        {'x':3470,'y':1120,'w':30,'h':30},
        {'x':3520,'y':1120,'w':30,'h':30},
        {'x':4285,'y':820,'w':30,'h':30},
        {'x':4735,'y':570,'w':30,'h':30},
        {'x':5185,'y':820,'w':30,'h':30},
        {'x':6345,'y':720,'w':30,'h':30},
        {'x':6395,'y':720,'w':30,'h':30},
        {'x':6445,'y':720,'w':30,'h':30}
        ]
    collectlife=[]
    movegold=[]

    monster=[
        {'x':1000,'y':1450,'w':50,'h':50,'move':5,'times':50,'increment':-1,'health':3},
        {'x':1700,'y':1100,'w':50,'h':50,'move':5,'times':1,'increment':1,'health':3},
        {'x':2200,'y':1100,'w':50,'h':50,'move':5,'times':50,'increment':-1,'health':3},
        {'x':2450,'y':1100,'w':50,'h':50,'move':5,'times':1,'increment':1,'health':3},
        {'x':2600,'y':1650,'w':50,'h':50,'move':5,'times':50,'increment':-1,'health':3},
        {'x':3400,'y':1650,'w':50,'h':50,'move':5,'times':1,'increment':1,'health':3},
        {'x':4600,'y':1000,'w':50,'h':50,'move':5,'times':50,'increment':-1,'health':3},
        {'x':4850,'y':1000,'w':50,'h':50,'move':5,'times':1,'increment':1,'health':3},
        {'x':5400,'y':1350,'w':50,'h':50,'move':5,'times':50,'increment':-1,'health':3},
        {'x':5650,'y':1350,'w':50,'h':50,'move':5,'times':1,'increment':1,'health':3},
        {'x':6800,'y':1500,'w':50,'h':50,'move':5,'times':50,'increment':-1,'health':3},
        {'x':7050,'y':1500,'w':50,'h':50,'move':5,'times':1,'increment':1,'health':3}
        ]
    messagebordpos=[
        {'x':1,'y':1100},
        {'x':7150,'y':1400}
        ]
    
    i=0 #player index
    player=standing_r
    timeindex=pygame.time.get_ticks()

    g=3 #gravity
    down=0 #down value

    timedelay=pygame.time.get_ticks()
    doublejump=True #True if player is onair and can be only used once, refills when player comes back to the ground
    landing=False #True when playe touches ground after jump
    freeze=False #True and makes player freeze for some time while landing

    changex=changey=0 #for camera movement
    timeeffect=timestar=pygame.time.get_ticks()
    hi=si=0
    playheartbreak=False
    playstarcollect=False
    sx=sy=0
    heal=False
    phi=0
    
    enemyx,enemyy,enemyexplode=0,0,False
    exi=0
    


    #-------------player margin on screen
    

    lmargin=400
    rmargin=880
    umargin=150
    bmargin=570
    levelX=levelY=0
    lwidth,lheight=7300,1750


    gamebgmusic.set_volume(0)
    gamebgmusic.play(-1)
    playrip=True
    runsoundplaying=False

    onRetry=False
    onMenu=False

    startwelcome=True
    timeintro=pygame.time.get_ticks()
    introsound.play()
    
    while True:
        
        mx,my=pygame.mouse.get_pos()#mouse position
        
        playerpast={'x':playerpos['x'],'y':playerpos['y']}#past position of player

        for event in pygame.event.get():#gets user interactions
            
            if event.type==QUIT:#checks if user clicked on quit
                pygame.quit()
                sys.exit()
            if not startwelcome:
                if event.type==KEYDOWN and event.key==K_ESCAPE:
                    gamebgmusic.stop()
                    runsound.stop()
                    runsoundplaying=False
                    Mode(data)
                
                if not dead:
                    if event.type==KEYDOWN and event.key==K_RIGHT:#right move
                        goright=True
                        goleft=False
                        face_r=True
                        player=walking_r
                    if event.type==KEYUP and event.key==K_RIGHT:
                        goright=False
                        if goleft:
                            player=walking_l
                        else:
                            player=standing_r
                            runsound.stop()

                    if event.type==KEYDOWN and event.key==K_LEFT:#left move
                        goright=False
                        goleft=True
                        face_r=False
                        player=walking_l
                    if event.type==KEYUP and event.key==K_LEFT:
                        goleft=False
                        if goright:
                            player=walking_r
                        else:
                            player=standing_l

                    if not freeze:
                        if onground and (event.type==KEYDOWN and event.key==K_UP):#jump move
                            jumpsound.play()
                            down=-30
                            onground=False
                        elif doublejump and (event.type==KEYDOWN and event.key==K_UP):
                            jumpsound.play()
                            down=-30
                            doublejump=False
                        if not attacking and (event.type==KEYDOWN and event.key==K_SPACE):
                            attacksound.play()
                            attack=attacking=True
                            if face_r:
                                Attack_r=True
                            else:
                                Attack_r=False
                            ai=0
                if dead and not Hurt:
                    if event.type==MOUSEBUTTONDOWN:
                        if onRetry:
                            buttonclickedsound.play()
                            screen.blit(afterdeathmessage[4],(265,210))
                            screen.blit(mouse,(mx,my))
                            pygame.display.update()
                            fpsclock.tick(FPS)
                            gamebgmusic.stop()
                            runsound.stop()
                            runsoundplaying=False
                            Level4(data)
                        if onMenu:
                            buttonclickedsound.play()
                            screen.blit(afterdeathmessage[2],(265,210))
                            screen.blit(mouse,(mx,my))
                            pygame.display.update()
                            fpsclock.tick(FPS)
                            gamebgmusic.stop()
                            runsound.stop()
                            runsoundplaying=False
                            Mode(data)

                                
        if not onground:#gravity pull/jump
            playerpos['y']+=down
            down+=g

        if not freeze:#right left motion
            if goright:
                playerpos['x']+=10
                                                    
            if goleft:
                playerpos['x']-=10

            if (onground and not runsoundplaying) and (goright or goleft):
                runsound.play(-1)
                runsoundplaying=True
            if (not goright and not goleft) or not onground:
                runsound.stop()
                runsoundplaying=False
                

        playerpos,onground,down,doublejump,landing,timedelay=collide(playerpast,playerpos,box,down,onground,doublejump,landing,timedelay)#changes playerpos accorting to platforms

        for j in range(len(monster)):            
            monster[j]['x']-=monster[j]['move']*monster[j]['increment']
            monster[j]['times']+=monster[j]['increment']
            if monster[j]['times']<=1:
                monster[j]['increment']=1
            elif monster[j]['times']>=50:
                monster[j]['increment']=-1

        Life,collectlife,collectedcoins,goldcoin,movegold,heal,showpoint,timepoint,phi=points(playerpos,Life,goldcoin,collectlife,collectedcoins,movegold,heal,showpoint,timepoint,phi)

        remove=None
        for j in range(len(movegold)):
            if 170<movegold[j]['x']<220 and 10<movegold[j]['y']<60:
                pointsound.play()
                remove=j
                showpoint=goldplus[movegold[j]['gold']]
                timepoint=pygame.time.get_ticks()
                glist=[]
                nogold=collectedcoins
                for k in range(len(str(nogold))):
                    glist.insert(0,nogold%10)
                    nogold=nogold//10 
                break
            else:
                movegold[j]['x']+=movegold[j]['cx']
                movegold[j]['y']+=movegold[j]['cy']
        if remove != None:
            movegold.pop(remove)
                
        starpoint,sx,sy,playstarcollect,timestar,starno=Star(starpoint,playerpos,playstarcollect,timestar,sx,sy,starno)#checks no of stars collected
        
        
        if not Hurt and not dead:
            timehurt,Life,Hurt,timeeffect,playheartbreak=_obstacle(playerpos,trap,timehurt,Life,Hurt,timeeffect,playheartbreak)#checks if player is hurt by obstacles
            if not Hurt:
                timehurt,Life,Hurt,timeeffect,playheartbreak=_obstacle(playerpos,monster,timehurt,Life,Hurt,timeeffect,playheartbreak)#checks if player is hurt by enemy
            if Life==0:
                dead=True
                goright=False
                goleft=False
                
                
        else:
            if pygame.time.get_ticks()>timehurt+1000:                
                Hurt=False
                
        if landing:
            landsound.play()
            freeze=True
        if pygame.time.get_ticks()>timedelay+100:
            freeze=False
            
        if attack:
            monster,attack,collectlife,goldcoin,enemyx,enemyy,enemyexplode=Playerattack(monster,playerpos,Attack_r,attack,collectlife,goldcoin,enemyx,enemyy,enemyexplode)

        #changes for camera movement

        if playerpos['x']<lmargin:
            if levelX>=0:
                changex=0-levelX
            else:                
                changex=lmargin-playerpos['x']
                if changex>-levelX:
                    changex=-levelX
        elif (playerpos['x']+pw)>rmargin:
            if levelX<=1280-lwidth:
                changex=1280-(levelX+lwidth)
            else:
                changex=rmargin-(playerpos['x']+pw)
                if changex<1280-(levelX+lwidth):
                    changex=1280-(levelX+lwidth)
        else:
            changex=0
        if playerpos['y']<umargin:
            if levelY>=0:
                changey=0-levelY
            else:
                changey=umargin-playerpos['y']
                if changey>-levelY:
                    changey=-levelY
        elif (playerpos['y']+ph)>bmargin:
            if levelY<=720-lheight:
                changey=720-(levelY+lheight)
            else:                
                changey=bmargin-(playerpos['y']+ph)
                if changey<720-(levelY+lheight):
                    changey=720-(levelY+lheight)
        else:
            changey=0

        if changex!=0:#changes x value for camera movement
            levelX+=changex
            playerpos['x']+=changex
            sx+=changex
            for k in range(len(box)):
                box[k]['x']+=changex
            for k in range(len(trap)):
                trap[k]['x']+=changex
            for k in range(len(starpoint)):
                starpoint[k]['x']+=changex
            for k in range(len(goldcoin)):
                goldcoin[k]['x']+=changex
            for k in range(len(collectlife)):
                collectlife[k]['x']+=changex
            for k in range(len(monster)):
                monster[k]['x']+=changex
            for k in range(len(mud)):
                mud[k]['x']+=changex
            for k in range(len(messagebordpos)):
                messagebordpos[k]['x']+=changex
                    
        if changey!=0:#changes y value for camera movement
            levelY+=changey
            playerpos['y']+=changey
            sy+=changey
            for k in range(len(box)):
                box[k]['y']+=changey
            for k in range(len(trap)):
                trap[k]['y']+=changey            
            for k in range(len(starpoint)):
                starpoint[k]['y']+=changey
            for k in range(len(goldcoin)):
                goldcoin[k]['y']+=changey
            for k in range(len(collectlife)):
                collectlife[k]['y']+=changey
            for k in range(len(monster)):
                monster[k]['y']+=changey
            for k in range(len(mud)):
                mud[k]['y']+=changey
            for k in range(len(messagebordpos)):
                messagebordpos[k]['y']+=changey

        if playerpos['x']+pw<0:
            gamebgmusic.stop()
            runsound.stop()
            runsoundplaying=False
            Mode(data)
        elif playerpos['x']>1280:
            #----------------------------------------------------------------------save progress
            gamebgmusic.stop()
            runsound.stop()
            runsoundplaying=False
            data[1]+=collectedcoins
            if data[0]['l4']<starno:
                data[0]['l4']=starno
            if data[0]['l5']==None:
                data[0]['l5']=0
            f=open('sprites/data/donotdelete.txt','wb')
            pickle.dump(data,f)
            f.close()
            Level5(data)


        

        #-----------------------------------------------------------blitting images
                
        screen.blit(background,(0,0))
        for j in range(len(messagebordpos)):
            screen.blit(messagebord[j],(messagebordpos[j]['x'],messagebordpos[j]['y']))
        for j in range(len(mud)):
            screen.blit(mud[j]['image'],(mud[j]['x'],mud[j]['y']))
        for j in range(len(box)):
            screen.blit(platform[j],(box[j]['x'],box[j]['y']))
        for j in range(len(trap)):
            screen.blit(obstacles[j],(trap[j]['x'],trap[j]['y']))
        for j in range(len(monster)):
            if monster[j]['increment']==-1:
                screen.blit(enemy1_l[i],(monster[j]['x'],monster[j]['y']))
            else:
                screen.blit(enemy1_r[i],(monster[j]['x'],monster[j]['y']))
            screen.blit(healthbar[monster[j]['health']-1],(monster[j]['x'],monster[j]['y']-15))
        for j in range(len(goldcoin)):
            screen.blit(dropgold,(goldcoin[j]['x'],goldcoin[j]['y']))
        for j in range(len(movegold)):
            screen.blit(dropgold,(movegold[j]['x'],movegold[j]['y']))
        for j in range(len(collectlife)):
            screen.blit(dropheart,(collectlife[j]['x'],collectlife[j]['y']))
        if enemyexplode:
            screen.blit(enemyblast[exi],(enemyx,enemyy))
            if exi==8:
                exi=0
                enemyexplode=False
            else:
                exi+=1

        for j in range(len(starpoint)):#star
            screen.blit(star_r[i],(starpoint[j]['x'],starpoint[j]['y']))

        #------------------------------------------------------------------player

        if Hurt and pygame.time.get_ticks()<injuredtime+100:
            if attacking:
                if face_r:
                    if onground:
                        screen.blit(p_hurt_r[2],(playerpos['x'],playerpos['y']-25))
                    elif not onground:
                        screen.blit(p_hurt_r[3],(playerpos['x'],playerpos['y']-25))
                elif not face_r:
                    if onground:
                        screen.blit(p_hurt_l[2],(playerpos['x']-50,playerpos['y']-25))
                    elif not onground:
                        screen.blit(p_hurt_l[3],(playerpos['x']-50,playerpos['y']-25))
            elif not attacking:            
                if face_r:
                    if onground:
                        screen.blit(p_hurt_r[0],(playerpos['x'],playerpos['y']))
                    elif not onground:
                        screen.blit(p_hurt_r[1],(playerpos['x'],playerpos['y']))
                elif not face_r:
                    if onground:
                        screen.blit(p_hurt_l[0],(playerpos['x'],playerpos['y']))
                    elif not onground:
                        screen.blit(p_hurt_l[1],(playerpos['x'],playerpos['y']))
        elif not Hurt and dead:
            if playrip:
                ripsound.play()
                playrip=False
            screen.blit(dead_p,(playerpos['x'],playerpos['y']))           

        else:
            if freeze:
                if face_r:
                    screen.blit(land_r,(playerpos['x'],playerpos['y']))
                elif not face_r:
                    screen.blit(land_l,(playerpos['x'],playerpos['y']))
            elif attacking:
                if face_r:
                    if onground:
                        screen.blit(attack_r[ai],(playerpos['x'],playerpos['y']-25))
                    elif not onground:
                        screen.blit(airattack_r[ai],(playerpos['x'],playerpos['y']-25))
                elif not face_r:
                    if onground:
                        screen.blit(attack_l[ai],(playerpos['x']-50,playerpos['y']-25))
                    elif not onground:
                        screen.blit(airattack_l[ai],(playerpos['x']-50,playerpos['y']-25))
            elif onground:
                screen.blit(player[i],(playerpos['x'],playerpos['y']))
            elif not onground:
                if face_r:
                    screen.blit(jump_r,(playerpos['x'],playerpos['y']))
                elif not face_r:
                    screen.blit(jump_l,(playerpos['x'],playerpos['y']))
        if pygame.time.get_ticks()>injuredtime+200:
            injuredtime=pygame.time.get_ticks()
        if heal:
            screen.blit(healtheffect[phi],(playerpos['x']-25,playerpos['y']-25))
            if phi==8:
                phi=0
                heal=False
            else:
                phi+=1
            
        #------------------------------------------------------------------player
    
            
        if playstarcollect:#starcollect
            screen.blit(starcollected[si],(sx,sy))
            if si==8:
                si=0
                playstarcollect=False
            elif pygame.time.get_ticks()>timestar+100:
                si+=1
                timestar=pygame.time.get_ticks()

        screen.blit(star_r[0],(25,25))#blits no of star collected
        screen.blit(_x,(75,35))
        screen.blit(_no[starno],(105,35))

        screen.blit(_gold,(185,25))
        screen.blit(_x,(235,35))
        gpx=265
        for j in glist:
            screen.blit(_no[j],(gpx,35))
            gpx+=30

            
        xheart=502
        for j in range(4):#heart
            if j<Life:
                screen.blit(heart[1],(xheart,25))
            else:
                screen.blit(heart[0],(xheart,25))
            xheart+=75
            
        if playheartbreak:#heartbreak
            screen.blit(heartbreak[hi],(477+(Life*75),0))
            if hi==8:
                hi=0
                playheartbreak=False
            elif pygame.time.get_ticks()>timeeffect+100:
                hi+=1
                timeeffect=pygame.time.get_ticks()
        screen.blit(esc_exit,(1105,25))
        
        if showpoint != None:
            screen.blit(showpoint,(565,100))
            if pygame.time.get_ticks()>timepoint+3000:
                showpoint=None
            

        #----------------------------------------------------------------------------index change
        

        if pygame.time.get_ticks()>timeindex+200:#change player index
            if i==3:
                i=0
            else:
                i+=1
            timeindex=pygame.time.get_ticks()
        if ai==3:
            ai=0
            attack=False
            attacking=False
        else:
            ai+=1
        if dead and not Hurt:
            screen.blit(blackscreen,(0,0))
            if 360<my<460:
                if 315<mx<615:
                    if not onRetry:
                        onbuttonsound.play()
                    onRetry=True
                else:
                    onRetry=False
                if 665<mx<965:
                    if not onMenu:
                        onbuttonsound.play()
                    onMenu=True
                else:
                    onMenu=False

            if onRetry:
                screen.blit(afterdeathmessage[3],(265,210))
            elif onMenu:
                screen.blit(afterdeathmessage[1],(265,210))
            else:
                screen.blit(afterdeathmessage[0],(265,210))
            screen.blit(mouse,(mx,my))
            pygame.display.update()
            fpsclock.tick(FPS)  

        elif startwelcome:
            screen.blit(blackscreen,(0,0))
            screen.blit(levelbanner[3],(440,285))
            if pygame.time.get_ticks()>timeintro+4000:
                startwelcome=False
                gamebgmusic.set_volume(0.5)
            pygame.display.update()
            fpsclock.tick(FPS)
            
        #screen.blit(mouse,(mx,my))#mouse
        else:       
            pygame.display.update()
            fpsclock.tick(FPS)
   
def Level5(data):
    surface=pygame.image.load('sprites/images/platform.png')
    obstacle=pygame.image.load('sprites/images/obstacle.png')
    spike200=pygame.image.load('sprites/images/spike200.png')
    spike250=pygame.image.load('sprites/images/spike250.png')
    spike400=pygame.image.load('sprites/images/spike400.png')
    dirt=pygame.image.load('sprites/images/dirt.png')
    dirtshadow=pygame.image.load('sprites/images/dirtshadow.png')
    mud=(
        {'image':pygame.transform.scale(dirtshadow,(300,30)),'x':400,'y':1000},#1
        {'image':pygame.transform.scale(dirtshadow,(400,30)),'x':1400,'y':1200},#2
        {'image':pygame.transform.scale(dirtshadow,(250,30)),'x':2650,'y':900},#3
        {'image':pygame.transform.scale(dirtshadow,(650,30)),'x':2250,'y':1450},#4
        {'image':pygame.transform.scale(dirtshadow,(300,30)),'x':3150,'y':1450},#5
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':3400,'y':1250},#6
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':4200,'y':900},#7
        {'image':pygame.transform.scale(dirtshadow,(100,30)),'x':4500,'y':1100},#8
        {'image':pygame.transform.scale(dirtshadow,(400,30)),'x':4600,'y':1100},#8
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':4650,'y':650},#9
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':5100,'y':900},#10
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':5300,'y':1100},#11
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':6100,'y':1100},#12
        {'image':pygame.transform.scale(dirtshadow,(200,30)),'x':6300,'y':800},#13
        {'image':pygame.transform.scale(dirt,(300,220)),'x':400,'y':1030},#1
        {'image':pygame.transform.scale(dirt,(400,470)),'x':1400,'y':1230},#2
        {'image':pygame.transform.scale(dirt,(250,220)),'x':2650,'y':930},#3
        {'image':pygame.transform.scale(dirt,(650,220)),'x':2250,'y':1480},#4
        {'image':pygame.transform.scale(dirt,(300,220)),'x':3150,'y':1480},#5
        {'image':pygame.transform.scale(dirt,(200,420)),'x':3400,'y':1280},#6
        {'image':pygame.transform.scale(dirt,(200,370)),'x':4200,'y':930},#7
        {'image':pygame.transform.scale(dirt,(100,320)),'x':4500,'y':1130},#8
        {'image':pygame.transform.scale(dirt,(400,520)),'x':4600,'y':1130},#8
        {'image':pygame.transform.scale(dirt,(200,370)),'x':4650,'y':680},#9
        {'image':pygame.transform.scale(dirt,(200,420)),'x':5100,'y':930},#10
        {'image':pygame.transform.scale(dirt,(200,270)),'x':5300,'y':1130},#11
        {'image':pygame.transform.scale(dirt,(200,220)),'x':6100,'y':1130},#12
        {'image':pygame.transform.scale(dirt,(200,570)),'x':6300,'y':830}#13
        )

    platform=(
        pygame.transform.scale(surface,(900,500)),#1
        pygame.transform.scale(surface,(300,50)),#2
        pygame.transform.scale(surface,(500,250)),#3
        pygame.transform.scale(surface,(400,50)),#4
        pygame.transform.scale(surface,(400,50)),#5
        pygame.transform.scale(surface,(450,300)),#6
        pygame.transform.scale(surface,(850,300)),#7
        pygame.transform.scale(surface,(250,50)),#8
        pygame.transform.scale(surface,(1350,50)),#9
        pygame.transform.scale(surface,(250,300)),#10
        pygame.transform.scale(surface,(200,100)),#11
        pygame.transform.scale(surface,(600,300)),#12
        pygame.transform.scale(surface,(400,300)),#13
        pygame.transform.scale(surface,(200,50)),#14
        pygame.transform.scale(surface,(200,450)),#15
        pygame.transform.scale(surface,(200,300)),#16
        pygame.transform.scale(surface,(500,100)),#17
        pygame.transform.scale(surface,(500,50)),#18
        pygame.transform.scale(surface,(200,50)),#19
        pygame.transform.scale(surface,(200,400)),#20
        pygame.transform.scale(surface,(200,50)),#21
        pygame.transform.scale(surface,(200,50)),#22
        pygame.transform.scale(surface,(500,350)),#23
        pygame.transform.scale(surface,(500,400)),#24
        pygame.transform.scale(surface,(200,50)),#25
        pygame.transform.scale(surface,(200,350)),#26
        pygame.transform.scale(surface,(200,50)),#27
        pygame.transform.scale(surface,(200,400)),#28
        pygame.transform.scale(surface,(600,200))#29        
        )
    obstacles=(
        pygame.transform.flip(spike400,False,True),#1
        spike400,#2
        pygame.transform.rotate(spike250,-90),#3
        spike200,#4
        #spike200,#5
        spike200,#6
        pygame.transform.flip(spike200,False,True),#7
        pygame.transform.flip(spike200,False,True),#8
        spike200,#9
        pygame.transform.rotate(spike200,-90)#10
        )

    showpoint=None
    timepoint=pygame.time.get_ticks()


    
    Life=4 #player life
    starno=0 #no of stars collected
    collectedcoins=0
    nogold=collectedcoins
    glist=[]
    for j in range(len(str(nogold))):
        glist.insert(0,nogold%10)
        nogold=nogold//10 
    dead=False #True if player is dead
    Hurt=False #True if player is hurt by traps
    injuredtime=pygame.time.get_ticks()
    timehurt=pygame.time.get_ticks()

    goright=False #True if player is moving right
    goleft=False #True if player is moving left
    onground=False #True if player is on platform/surface/ground
    jump_=False
    face_r=True #True if player is facing right, False if facing left
    Attack_r=True
    attack=False
    attacking=False
    ai=0
    
    playerpos={'x':0,'y':100}#initial player position

    #-----------------platforms
    box=[
        {'x':0,'y':1250,'w':900,'h':500},#1
        {'x':400,'y':950,'w':300,'h':50},#2
        {'x':900,'y':1500,'w':500,'h':250},#3
        {'x':1400,'y':1150,'w':400,'h':50},#4
        {'x':1400,'y':1700,'w':400,'h':50},#5
        {'x':1800,'y':1450,'w':450,'h':300},#6
        {'x':2050,'y':1150,'w':850,'h':300},#7
        {'x':2650,'y':850,'w':250,'h':50},#8
        {'x':2250,'y':1700,'w':1350,'h':50},#9
        {'x':3150,'y':1150,'w':250,'h':300},#10
        {'x':3400,'y':1150,'w':200,'h':100},#11
        {'x':3600,'y':1450,'w':600,'h':300},#12
        {'x':3800,'y':1150,'w':400,'h':300},#13
        {'x':4200,'y':850,'w':200,'h':50},#14
        {'x':4200,'y':1300,'w':200,'h':450},#15
        {'x':4400,'y':1450,'w':200,'h':300},#16
        {'x':4600,'y':1650,'w':500,'h':100},#17
        {'x':4500,'y':1050,'w':500,'h':50},#18
        {'x':4650,'y':600,'w':200,'h':50},#19
        {'x':5100,'y':1350,'w':200,'h':400},#20
        {'x':5100,'y':850,'w':200,'h':50},#21
        {'x':5300,'y':1050,'w':200,'h':50},#22
        {'x':5300,'y':1400,'w':500,'h':350},#23
        {'x':5800,'y':1350,'w':500,'h':400},#24
        {'x':6100,'y':1050,'w':200,'h':50},#25
        {'x':6300,'y':1400,'w':200,'h':350},#26
        {'x':6300,'y':750,'w':200,'h':50},#27
        {'x':6500,'y':1350,'w':200,'h':400},#28
        {'x':6700,'y':1550,'w':600,'h':200}#29
        ]
    
    #-----------------traps
    
    trap=[
        {'x':1400,'y':1200,'w':400,'h':50},#1
        {'x':1400,'y':1650,'w':400,'h':50},#2
        {'x':2250,'y':1450,'w':50,'h':250},#3
        {'x':4200,'y':1250,'w':200,'h':50},#4
        #{'x':4400,'y':1400,'w':200,'h':50},#5
        {'x':4600,'y':1600,'w':200,'h':50},#6
        {'x':5300,'y':1100,'w':200,'h':50},#7
        {'x':6100,'y':1100,'w':200,'h':50},#8
        {'x':6300,'y':1350,'w':200,'h':50},#9
        {'x':6700,'y':1350,'w':50,'h':200}#10
        ]
    

    #-----------------stars
    starpoint=[
        {'x':2350,'y':1550,'w':50,'h':50},
        {'x':5000,'y':1450,'w':50,'h':50},
        {'x':6375,'y':800,'w':50,'h':50}       
        ]
    goldcoin=[
        {'x':460,'y':920,'w':30,'h':30},
        {'x':510,'y':920,'w':30,'h':30},
        {'x':560,'y':920,'w':30,'h':30},
        {'x':610,'y':920,'w':30,'h':30},
        {'x':1870,'y':1420,'w':30,'h':30},
        {'x':1920,'y':1420,'w':30,'h':30},
        {'x':1970,'y':1420,'w':30,'h':30},
        {'x':2720,'y':820,'w':30,'h':30},
        {'x':2770,'y':820,'w':30,'h':30},
        {'x':2820,'y':820,'w':30,'h':30},
        {'x':2920,'y':1670,'w':30,'h':30},
        {'x':2970,'y':1670,'w':30,'h':30},
        {'x':3020,'y':1670,'w':30,'h':30},
        {'x':3070,'y':1670,'w':30,'h':30},
        {'x':3120,'y':1670,'w':30,'h':30},        
        {'x':3220,'y':1120,'w':30,'h':30},
        {'x':3270,'y':1120,'w':30,'h':30},
        {'x':3320,'y':1120,'w':30,'h':30},
        {'x':3370,'y':1120,'w':30,'h':30},
        {'x':3420,'y':1120,'w':30,'h':30},
        {'x':3470,'y':1120,'w':30,'h':30},
        {'x':3520,'y':1120,'w':30,'h':30},
        {'x':4285,'y':820,'w':30,'h':30},
        {'x':4735,'y':570,'w':30,'h':30},
        {'x':5185,'y':820,'w':30,'h':30},
        {'x':6345,'y':720,'w':30,'h':30},
        {'x':6395,'y':720,'w':30,'h':30},
        {'x':6445,'y':720,'w':30,'h':30}
        ]
    collectlife=[]
    movegold=[]

    monster=[
        {'x':1000,'y':1450,'w':50,'h':50,'move':5,'times':50,'increment':-1,'health':3},
        {'x':1700,'y':1100,'w':50,'h':50,'move':5,'times':1,'increment':1,'health':3},
        {'x':2200,'y':1100,'w':50,'h':50,'move':5,'times':50,'increment':-1,'health':3},
        {'x':2450,'y':1100,'w':50,'h':50,'move':5,'times':1,'increment':1,'health':3},
        {'x':2600,'y':1650,'w':50,'h':50,'move':5,'times':50,'increment':-1,'health':3},
        {'x':3400,'y':1650,'w':50,'h':50,'move':5,'times':1,'increment':1,'health':3},
        {'x':4600,'y':1000,'w':50,'h':50,'move':5,'times':50,'increment':-1,'health':3},
        {'x':4850,'y':1000,'w':50,'h':50,'move':5,'times':1,'increment':1,'health':3},
        {'x':5400,'y':1350,'w':50,'h':50,'move':5,'times':50,'increment':-1,'health':3},
        {'x':5650,'y':1350,'w':50,'h':50,'move':5,'times':1,'increment':1,'health':3},
        {'x':6800,'y':1500,'w':50,'h':50,'move':5,'times':50,'increment':-1,'health':3},
        {'x':7050,'y':1500,'w':50,'h':50,'move':5,'times':1,'increment':1,'health':3}
        ]
    messagebordpos=[
        {'x':1,'y':1100},
        {'x':7150,'y':1400}
        ]
    
    i=0 #player index
    player=standing_r
    timeindex=pygame.time.get_ticks()

    g=3 #gravity
    down=0 #down value

    timedelay=pygame.time.get_ticks()
    doublejump=True #True if player is onair and can be only used once, refills when player comes back to the ground
    landing=False #True when playe touches ground after jump
    freeze=False #True and makes player freeze for some time while landing

    changex=changey=0 #for camera movement
    timeeffect=timestar=pygame.time.get_ticks()
    hi=si=0
    playheartbreak=False
    playstarcollect=False
    sx=sy=0
    heal=False
    phi=0
    
    enemyx,enemyy,enemyexplode=0,0,False
    exi=0
    


    #-------------player margin on screen
    

    lmargin=400
    rmargin=880
    umargin=150
    bmargin=570
    levelX=levelY=0
    lwidth,lheight=7300,1750


    gamebgmusic.set_volume(0)
    gamebgmusic.play(-1)
    playrip=True
    runsoundplaying=False

    onRetry=False
    onMenu=False

    startwelcome=True
    timeintro=pygame.time.get_ticks()
    introsound.play()
    
    while True:
        
        mx,my=pygame.mouse.get_pos()#mouse position
        
        playerpast={'x':playerpos['x'],'y':playerpos['y']}#past position of player

        for event in pygame.event.get():#gets user interactions
            
            if event.type==QUIT:#checks if user clicked on quit
                pygame.quit()
                sys.exit()
            if not startwelcome:
                if event.type==KEYDOWN and event.key==K_ESCAPE:
                    gamebgmusic.stop()
                    runsound.stop()
                    runsoundplaying=False
                    Mode(data)
                
                if not dead:
                    if event.type==KEYDOWN and event.key==K_RIGHT:#right move
                        goright=True
                        goleft=False
                        face_r=True
                        player=walking_r
                    if event.type==KEYUP and event.key==K_RIGHT:
                        goright=False
                        if goleft:
                            player=walking_l
                        else:
                            player=standing_r
                            runsound.stop()

                    if event.type==KEYDOWN and event.key==K_LEFT:#left move
                        goright=False
                        goleft=True
                        face_r=False
                        player=walking_l
                    if event.type==KEYUP and event.key==K_LEFT:
                        goleft=False
                        if goright:
                            player=walking_r
                        else:
                            player=standing_l

                    if not freeze:
                        if onground and (event.type==KEYDOWN and event.key==K_UP):#jump move
                            jumpsound.play()
                            down=-30
                            onground=False
                        elif doublejump and (event.type==KEYDOWN and event.key==K_UP):
                            jumpsound.play()
                            down=-30
                            doublejump=False
                        if not attacking and (event.type==KEYDOWN and event.key==K_SPACE):
                            attacksound.play()
                            attack=attacking=True
                            if face_r:
                                Attack_r=True
                            else:
                                Attack_r=False
                            ai=0
                if dead and not Hurt:
                    if event.type==MOUSEBUTTONDOWN:
                        if onRetry:
                            buttonclickedsound.play()
                            screen.blit(afterdeathmessage[4],(265,210))
                            screen.blit(mouse,(mx,my))
                            pygame.display.update()
                            fpsclock.tick(FPS)
                            gamebgmusic.stop()
                            runsound.stop()
                            runsoundplaying=False
                            Level5(data)
                        if onMenu:
                            buttonclickedsound.play()
                            screen.blit(afterdeathmessage[2],(265,210))
                            screen.blit(mouse,(mx,my))
                            pygame.display.update()
                            fpsclock.tick(FPS)
                            gamebgmusic.stop()
                            runsound.stop()
                            runsoundplaying=False
                            Mode(data)

                                
        if not onground:#gravity pull/jump
            playerpos['y']+=down
            down+=g

        if not freeze:#right left motion
            if goright:
                playerpos['x']+=10
                                                    
            if goleft:
                playerpos['x']-=10

            if (onground and not runsoundplaying) and (goright or goleft):
                runsound.play(-1)
                runsoundplaying=True
            if (not goright and not goleft) or not onground:
                runsound.stop()
                runsoundplaying=False
                

        playerpos,onground,down,doublejump,landing,timedelay=collide(playerpast,playerpos,box,down,onground,doublejump,landing,timedelay)#changes playerpos accorting to platforms

        for j in range(len(monster)):            
            monster[j]['x']-=monster[j]['move']*monster[j]['increment']
            monster[j]['times']+=monster[j]['increment']
            if monster[j]['times']<=1:
                monster[j]['increment']=1
            elif monster[j]['times']>=50:
                monster[j]['increment']=-1

        Life,collectlife,collectedcoins,goldcoin,movegold,heal,showpoint,timepoint,phi=points(playerpos,Life,goldcoin,collectlife,collectedcoins,movegold,heal,showpoint,timepoint,phi)

        remove=None
        for j in range(len(movegold)):
            if 170<movegold[j]['x']<220 and 10<movegold[j]['y']<60:
                pointsound.play()
                remove=j
                showpoint=goldplus[movegold[j]['gold']]
                timepoint=pygame.time.get_ticks()
                glist=[]
                nogold=collectedcoins
                for k in range(len(str(nogold))):
                    glist.insert(0,nogold%10)
                    nogold=nogold//10 
                break
            else:
                movegold[j]['x']+=movegold[j]['cx']
                movegold[j]['y']+=movegold[j]['cy']
        if remove != None:
            movegold.pop(remove)
                
        starpoint,sx,sy,playstarcollect,timestar,starno=Star(starpoint,playerpos,playstarcollect,timestar,sx,sy,starno)#checks no of stars collected
        
        
        if not Hurt and not dead:
            timehurt,Life,Hurt,timeeffect,playheartbreak=_obstacle(playerpos,trap,timehurt,Life,Hurt,timeeffect,playheartbreak)#checks if player is hurt by obstacles
            if not Hurt:
                timehurt,Life,Hurt,timeeffect,playheartbreak=_obstacle(playerpos,monster,timehurt,Life,Hurt,timeeffect,playheartbreak)#checks if player is hurt by enemy
            if Life==0:
                dead=True
                goright=False
                goleft=False
                
                
        else:
            if pygame.time.get_ticks()>timehurt+1000:                
                Hurt=False
                
        if landing:
            landsound.play()
            freeze=True
        if pygame.time.get_ticks()>timedelay+100:
            freeze=False
            
        if attack:
            monster,attack,collectlife,goldcoin,enemyx,enemyy,enemyexplode=Playerattack(monster,playerpos,Attack_r,attack,collectlife,goldcoin,enemyx,enemyy,enemyexplode)

        #changes for camera movement

        if playerpos['x']<lmargin:
            if levelX>=0:
                changex=0-levelX
            else:                
                changex=lmargin-playerpos['x']
                if changex>-levelX:
                    changex=-levelX
        elif (playerpos['x']+pw)>rmargin:
            if levelX<=1280-lwidth:
                changex=1280-(levelX+lwidth)
            else:
                changex=rmargin-(playerpos['x']+pw)
                if changex<1280-(levelX+lwidth):
                    changex=1280-(levelX+lwidth)
        else:
            changex=0
        if playerpos['y']<umargin:
            if levelY>=0:
                changey=0-levelY
            else:
                changey=umargin-playerpos['y']
                if changey>-levelY:
                    changey=-levelY
        elif (playerpos['y']+ph)>bmargin:
            if levelY<=720-lheight:
                changey=720-(levelY+lheight)
            else:                
                changey=bmargin-(playerpos['y']+ph)
                if changey<720-(levelY+lheight):
                    changey=720-(levelY+lheight)
        else:
            changey=0

        if changex!=0:#changes x value for camera movement
            levelX+=changex
            playerpos['x']+=changex
            sx+=changex
            for k in range(len(box)):
                box[k]['x']+=changex
            for k in range(len(trap)):
                trap[k]['x']+=changex
            for k in range(len(starpoint)):
                starpoint[k]['x']+=changex
            for k in range(len(goldcoin)):
                goldcoin[k]['x']+=changex
            for k in range(len(collectlife)):
                collectlife[k]['x']+=changex
            for k in range(len(monster)):
                monster[k]['x']+=changex
            for k in range(len(mud)):
                mud[k]['x']+=changex
            for k in range(len(messagebordpos)):
                messagebordpos[k]['x']+=changex
                    
        if changey!=0:#changes y value for camera movement
            levelY+=changey
            playerpos['y']+=changey
            sy+=changey
            for k in range(len(box)):
                box[k]['y']+=changey
            for k in range(len(trap)):
                trap[k]['y']+=changey            
            for k in range(len(starpoint)):
                starpoint[k]['y']+=changey
            for k in range(len(goldcoin)):
                goldcoin[k]['y']+=changey
            for k in range(len(collectlife)):
                collectlife[k]['y']+=changey
            for k in range(len(monster)):
                monster[k]['y']+=changey
            for k in range(len(mud)):
                mud[k]['y']+=changey
            for k in range(len(messagebordpos)):
                messagebordpos[k]['y']+=changey

        if playerpos['x']+pw<0:
            gamebgmusic.stop()
            runsound.stop()
            runsoundplaying=False
            Mode(data)
        elif playerpos['x']>1280:
            #----------------------------------------------------------------------save progress
            gamebgmusic.stop()
            runsound.stop()
            runsoundplaying=False
            data[1]+=collectedcoins
            if data[0]['l5']<starno:
                data[0]['l5']=starno
            f=open('sprites/data/donotdelete.txt','wb')
            pickle.dump(data,f)
            f.close()
            Mode(data)


        

        #-----------------------------------------------------------blitting images
                
        screen.blit(background,(0,0))
        for j in range(len(messagebordpos)):
            screen.blit(messagebord[j],(messagebordpos[j]['x'],messagebordpos[j]['y']))
        for j in range(len(mud)):
            screen.blit(mud[j]['image'],(mud[j]['x'],mud[j]['y']))
        for j in range(len(box)):
            screen.blit(platform[j],(box[j]['x'],box[j]['y']))
        for j in range(len(trap)):
            screen.blit(obstacles[j],(trap[j]['x'],trap[j]['y']))
        for j in range(len(monster)):
            if monster[j]['increment']==-1:
                screen.blit(enemy1_l[i],(monster[j]['x'],monster[j]['y']))
            else:
                screen.blit(enemy1_r[i],(monster[j]['x'],monster[j]['y']))
            screen.blit(healthbar[monster[j]['health']-1],(monster[j]['x'],monster[j]['y']-15))
        for j in range(len(goldcoin)):
            screen.blit(dropgold,(goldcoin[j]['x'],goldcoin[j]['y']))
        for j in range(len(movegold)):
            screen.blit(dropgold,(movegold[j]['x'],movegold[j]['y']))
        for j in range(len(collectlife)):
            screen.blit(dropheart,(collectlife[j]['x'],collectlife[j]['y']))
        if enemyexplode:
            screen.blit(enemyblast[exi],(enemyx,enemyy))
            if exi==8:
                exi=0
                enemyexplode=False
            else:
                exi+=1

        for j in range(len(starpoint)):#star
            screen.blit(star_r[i],(starpoint[j]['x'],starpoint[j]['y']))

        #------------------------------------------------------------------player

        if Hurt and pygame.time.get_ticks()<injuredtime+100:
            if attacking:
                if face_r:
                    if onground:
                        screen.blit(p_hurt_r[2],(playerpos['x'],playerpos['y']-25))
                    elif not onground:
                        screen.blit(p_hurt_r[3],(playerpos['x'],playerpos['y']-25))
                elif not face_r:
                    if onground:
                        screen.blit(p_hurt_l[2],(playerpos['x']-50,playerpos['y']-25))
                    elif not onground:
                        screen.blit(p_hurt_l[3],(playerpos['x']-50,playerpos['y']-25))
            elif not attacking:            
                if face_r:
                    if onground:
                        screen.blit(p_hurt_r[0],(playerpos['x'],playerpos['y']))
                    elif not onground:
                        screen.blit(p_hurt_r[1],(playerpos['x'],playerpos['y']))
                elif not face_r:
                    if onground:
                        screen.blit(p_hurt_l[0],(playerpos['x'],playerpos['y']))
                    elif not onground:
                        screen.blit(p_hurt_l[1],(playerpos['x'],playerpos['y']))
        elif not Hurt and dead:
            if playrip:
                ripsound.play()
                playrip=False
            screen.blit(dead_p,(playerpos['x'],playerpos['y']))           

        else:
            if freeze:
                if face_r:
                    screen.blit(land_r,(playerpos['x'],playerpos['y']))
                elif not face_r:
                    screen.blit(land_l,(playerpos['x'],playerpos['y']))
            elif attacking:
                if face_r:
                    if onground:
                        screen.blit(attack_r[ai],(playerpos['x'],playerpos['y']-25))
                    elif not onground:
                        screen.blit(airattack_r[ai],(playerpos['x'],playerpos['y']-25))
                elif not face_r:
                    if onground:
                        screen.blit(attack_l[ai],(playerpos['x']-50,playerpos['y']-25))
                    elif not onground:
                        screen.blit(airattack_l[ai],(playerpos['x']-50,playerpos['y']-25))
            elif onground:
                screen.blit(player[i],(playerpos['x'],playerpos['y']))
            elif not onground:
                if face_r:
                    screen.blit(jump_r,(playerpos['x'],playerpos['y']))
                elif not face_r:
                    screen.blit(jump_l,(playerpos['x'],playerpos['y']))
        if pygame.time.get_ticks()>injuredtime+200:
            injuredtime=pygame.time.get_ticks()
        if heal:
            screen.blit(healtheffect[phi],(playerpos['x']-25,playerpos['y']-25))
            if phi==8:
                phi=0
                heal=False
            else:
                phi+=1
            
        #------------------------------------------------------------------player
    
            
        if playstarcollect:#starcollect
            screen.blit(starcollected[si],(sx,sy))
            if si==8:
                si=0
                playstarcollect=False
            elif pygame.time.get_ticks()>timestar+100:
                si+=1
                timestar=pygame.time.get_ticks()

        screen.blit(star_r[0],(25,25))#blits no of star collected
        screen.blit(_x,(75,35))
        screen.blit(_no[starno],(105,35))

        screen.blit(_gold,(185,25))
        screen.blit(_x,(235,35))
        gpx=265
        for j in glist:
            screen.blit(_no[j],(gpx,35))
            gpx+=30

            
        xheart=502
        for j in range(4):#heart
            if j<Life:
                screen.blit(heart[1],(xheart,25))
            else:
                screen.blit(heart[0],(xheart,25))
            xheart+=75
            
        if playheartbreak:#heartbreak
            screen.blit(heartbreak[hi],(477+(Life*75),0))
            if hi==8:
                hi=0
                playheartbreak=False
            elif pygame.time.get_ticks()>timeeffect+100:
                hi+=1
                timeeffect=pygame.time.get_ticks()
        screen.blit(esc_exit,(1105,25))
        
        if showpoint != None:
            screen.blit(showpoint,(565,100))
            if pygame.time.get_ticks()>timepoint+3000:
                showpoint=None
            

        #----------------------------------------------------------------------------index change
        

        if pygame.time.get_ticks()>timeindex+200:#change player index
            if i==3:
                i=0
            else:
                i+=1
            timeindex=pygame.time.get_ticks()
        if ai==3:
            ai=0
            attack=False
            attacking=False
        else:
            ai+=1
        if dead and not Hurt:
            screen.blit(blackscreen,(0,0))
            if 360<my<460:
                if 315<mx<615:
                    if not onRetry:
                        onbuttonsound.play()
                    onRetry=True
                else:
                    onRetry=False
                if 665<mx<965:
                    if not onMenu:
                        onbuttonsound.play()
                    onMenu=True
                else:
                    onMenu=False

            if onRetry:
                screen.blit(afterdeathmessage[3],(265,210))
            elif onMenu:
                screen.blit(afterdeathmessage[1],(265,210))
            else:
                screen.blit(afterdeathmessage[0],(265,210))
            screen.blit(mouse,(mx,my))
            pygame.display.update()
            fpsclock.tick(FPS)  

        elif startwelcome:
            screen.blit(blackscreen,(0,0))
            screen.blit(levelbanner[4],(440,285))
            if pygame.time.get_ticks()>timeintro+4000:
                startwelcome=False
                gamebgmusic.set_volume(0.5)
            pygame.display.update()
            fpsclock.tick(FPS)   

        #screen.blit(mouse,(mx,my))#mouse
        else:       
            pygame.display.update()
            fpsclock.tick(FPS)



def checkonbuttons(mx,my,buttons):#checks buttons
    onbuttonplay=False
    for j in range(len(buttons)):
        if buttons[j]['x']<mx<buttons[j]['w']+buttons[j]['x'] and buttons[j]['y']<my<buttons[j]['h']+buttons[j]['y']:
            if buttons[j]['state']==False:
                onbuttonplay=True
            buttons[j]['state']=True
        else:
            buttons[j]['state']=False
    return buttons,onbuttonplay

def Quit():
    pygame.quit()
    sys.exit()

def Mode(data):
    i=0
    timeindex=pygame.time.get_ticks()
    collectedcoins=data[1]
    nogold=collectedcoins
    glist=[]
    for j in range(len(str(nogold))):
        glist.insert(0,nogold%10)
        nogold=nogold//10 
    
    lbuttons=(
        {'w':50,'h':50,'x':1205,'y':25,'state':False,'name':_back,'destination':0,},
        {'w':200,'h':200,'x':90,'y':70,'state':False,'name':_level1,'destination':1,'starno':data[0]['l1']},
        {'w':200,'h':200,'x':390,'y':70,'state':False,'name':_level2,'destination':2,'starno':data[0]['l2']},
        {'w':200,'h':200,'x':690,'y':70,'state':False,'name':_level3,'destination':3,'starno':data[0]['l3']},
        {'w':200,'h':200,'x':990,'y':70,'state':False,'name':_level4,'destination':4,'starno':data[0]['l4']},
        {'w':200,'h':200,'x':540,'y':395,'state':False,'name':_level5,'destination':5,'starno':data[0]['l5']}
        )
    onbuttonplay=False
    while True:
        mx,my=pygame.mouse.get_pos()
        lbuttons,onbuttonplay=checkonbuttons(mx,my,lbuttons)
        if onbuttonplay:
            onbuttonsound.play()
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            for j in range(6):
                if lbuttons[j]['state']==True:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        buttonclickedsound.play()
                        if j==0:
                            screen.blit(lbuttons[j]['name'][2],(lbuttons[j]['x'],lbuttons[j]['y']))
                            screen.blit(mouse,(mx,my))
                            pygame.display.update()
                            fpsclock.tick(FPS)
                            menu(data)
                        else:
                            if lbuttons[j]['starno']==None:
                                screen.blit(_levellocked[2],(lbuttons[j]['x'],lbuttons[j]['y']))
                                screen.blit(mouse,(mx,my))
                                pygame.display.update()
                                fpsclock.tick(FPS)
                            else:                            
                                if lbuttons[j]['destination']==1:
                                    screen.blit(lbuttons[j]['name'][2],(lbuttons[j]['x'],lbuttons[j]['y']))
                                    screen.blit(mouse,(mx,my))
                                    pygame.display.update()
                                    fpsclock.tick(FPS)            
                                    Level1(data)
                                if lbuttons[j]['destination']==2:
                                    screen.blit(lbuttons[j]['name'][2],(lbuttons[j]['x'],lbuttons[j]['y']))
                                    screen.blit(mouse,(mx,my))
                                    pygame.display.update()
                                    fpsclock.tick(FPS)
                                    Level2(data)                            
                                if lbuttons[j]['destination']==3:
                                    screen.blit(lbuttons[j]['name'][2],(lbuttons[j]['x'],lbuttons[j]['y']))
                                    screen.blit(mouse,(mx,my))
                                    pygame.display.update()
                                    fpsclock.tick(FPS)
                                    Level3(data)
                                if lbuttons[j]['destination']==4:
                                    screen.blit(lbuttons[j]['name'][2],(lbuttons[j]['x'],lbuttons[j]['y']))
                                    screen.blit(mouse,(mx,my))
                                    pygame.display.update()
                                    fpsclock.tick(FPS)
                                    Level4(data)                            
                                if lbuttons[j]['destination']==5:
                                    screen.blit(lbuttons[j]['name'][2],(lbuttons[j]['x'],lbuttons[j]['y']))
                                    screen.blit(mouse,(mx,my))
                                    pygame.display.update()
                                    fpsclock.tick(FPS)
                                    Level5(data)
                            
        screen.blit(menubg[i],(0,0))
        for j in range(6):
            if j==0:
                if lbuttons[j]['state']==False:
                    screen.blit(lbuttons[j]['name'][0],(lbuttons[j]['x'],lbuttons[j]['y']))
                if lbuttons[j]['state']==True:
                    screen.blit(lbuttons[j]['name'][1],(lbuttons[j]['x'],lbuttons[j]['y']))
            else:
                if lbuttons[j]['starno']==None:
                    for k in range(3):
                        screen.blit(_0star,(lbuttons[j]['x']+(75*k),lbuttons[j]['y']+200))
                    if lbuttons[j]['state']==False:
                        screen.blit(_levellocked[0],(lbuttons[j]['x'],lbuttons[j]['y']))
                    else:
                        screen.blit(_levellocked[1],(lbuttons[j]['x'],lbuttons[j]['y']))                   
                else:
                    for k in range(3):
                        if k<lbuttons[j]['starno']:
                            screen.blit(_1star,(lbuttons[j]['x']+(75*k),lbuttons[j]['y']+200))
                        else:
                            screen.blit(_0star,(lbuttons[j]['x']+(75*k),lbuttons[j]['y']+200))
                    if lbuttons[j]['state']==False:
                        screen.blit(lbuttons[j]['name'][0],(lbuttons[j]['x'],lbuttons[j]['y']))
                    else:
                        screen.blit(lbuttons[j]['name'][1],(lbuttons[j]['x'],lbuttons[j]['y']))
        screen.blit(_gold,(25,25))
        screen.blit(_x,(75,35))
        gpx=105
        for j in glist:
            screen.blit(_no[j],(gpx,35))
            gpx+=30
        screen.blit(mouse,(mx,my))
        if pygame.time.get_ticks()>timeindex+200:#change player index
            if i==3:
                i=0
            else:
                i+=1
            timeindex=pygame.time.get_ticks()
        pygame.display.update()
        fpsclock.tick(FPS)
    
    
    return
def Shop():
    return
def Settings():
    return

def menu(data):
    i=0
    timeindex=pygame.time.get_ticks()
    buttons=(
        {'w':50,'h':50,'x':1205,'y':25,'state':False,'name':_quit,'destination':1},
        {'w':400,'h':100,'x':855,'y':125,'state':False,'name':_mode,'destination':2},
        {'w':400,'h':100,'x':855,'y':275,'state':False,'name':_shop,'destination':3},
        {'w':400,'h':100,'x':855,'y':425,'state':False,'name':_settings,'destination':4}     
        )
    onbuttonplay=False

    while True:
        mx,my=pygame.mouse.get_pos()
        buttons,onbuttonplay=checkonbuttons(mx,my,buttons)
        if onbuttonplay:
            onbuttonsound.play()
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            for j in range(4):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if buttons[j]['state']==True:
                        buttonclickedsound.play()
                        screen.blit(buttons[j]['name'][2],(buttons[j]['x'],buttons[j]['y']))
                        screen.blit(mouse,(mx,my))
                        pygame.display.update()
                        fpsclock.tick(FPS)
                        if buttons[j]['destination']==1:
                            Quit()
                        if buttons[j]['destination']==2:
                            Mode(data)
                        if buttons[j]['destination']==3:
                            Shop()                            
                        if buttons[j]['destination']==4:
                            Settings()
                        
        screen.blit(menubg[i],(0,0))
        for j in range(4):
            if buttons[j]['state']==False:
                screen.blit(buttons[j]['name'][0],(buttons[j]['x'],buttons[j]['y']))
            else:
                screen.blit(buttons[j]['name'][1],(buttons[j]['x'],buttons[j]['y']))
        screen.blit(mouse,(mx,my))
        if pygame.time.get_ticks()>timeindex+200:#change player index
            if i==3:
                i=0
            else:
                i+=1
            timeindex=pygame.time.get_ticks()
        pygame.display.update()
        fpsclock.tick(FPS)

        
            
                        
                        
            
            
        





if __name__ == "__main__":
    pw=50
    ph=75
    mouse=pygame.image.load('sprites/images/mouse.png')
    background=pygame.image.load('sprites/images/mode1bg.jpg')
    #------------------------------------------menu images
    menubg=(
        pygame.image.load('sprites/images/gamemenu1.jpg'),
        pygame.image.load('sprites/images/gamemenu2.jpg'),
        pygame.image.load('sprites/images/gamemenu3.jpg'),
        pygame.image.load('sprites/images/gamemenu4.jpg')
        )
    _quit=(
        pygame.image.load('sprites/images/quit.png'),
        pygame.image.load('sprites/images/onquit.png'),
        pygame.image.load('sprites/images/quitclicked.png')
        )
    _mode=(
        pygame.image.load('sprites/images/mode.png'),
        pygame.image.load('sprites/images/onmode.png'),
        pygame.image.load('sprites/images/modeclicked.png')
        )
    _settings=(
        pygame.image.load('sprites/images/settings.png'),
        pygame.image.load('sprites/images/onsettings.png'),
        pygame.image.load('sprites/images/settingsclicked.png')
        )
    _shop=(
        pygame.image.load('sprites/images/shop.png'),
        pygame.image.load('sprites/images/onshop.png'),
        pygame.image.load('sprites/images/shopclicked.png')
        )
    #------------------------------------------menu images
    _level1=(
        pygame.image.load('sprites/images/level1.png'),
        pygame.image.load('sprites/images/onlevel1.png'),
        pygame.image.load('sprites/images/level1clicked.png')
        )
    _level2=(
        pygame.image.load('sprites/images/level2.png'),
        pygame.image.load('sprites/images/onlevel2.png'),
        pygame.image.load('sprites/images/level2clicked.png')
        )
    _level3=(
        pygame.image.load('sprites/images/level3.png'),
        pygame.image.load('sprites/images/onlevel3.png'),
        pygame.image.load('sprites/images/level3clicked.png')
        )
    _level4=(
        pygame.image.load('sprites/images/level4.png'),
        pygame.image.load('sprites/images/onlevel4.png'),
        pygame.image.load('sprites/images/level4clicked.png')
        )
    _level5=(
        pygame.image.load('sprites/images/level5.png'),
        pygame.image.load('sprites/images/onlevel5.png'),
        pygame.image.load('sprites/images/level5clicked.png')
        )
    _levellocked=(
        pygame.image.load('sprites/images/levellock.png'),
        pygame.image.load('sprites/images/onlevellock.png'),
        pygame.image.load('sprites/images/levellockclicked.png')
        )
    _back=(
        pygame.image.load('sprites/images/back.png'),
        pygame.image.load('sprites/images/onback.png'),
        pygame.image.load('sprites/images/backclicked.png')
        )
    #------------------------------------------icon images
    _1star=pygame.image.load('sprites/images/1star.png')
    _0star=pygame.image.load('sprites/images/0star.png')
    _gold=pygame.image.load('sprites/images/gold.png')
    _no=(
        pygame.image.load('sprites/images/0.png'),
        pygame.image.load('sprites/images/1.png'),
        pygame.image.load('sprites/images/2.png'),
        pygame.image.load('sprites/images/3.png'),
        pygame.image.load('sprites/images/4.png'),
        pygame.image.load('sprites/images/5.png'),
        pygame.image.load('sprites/images/6.png'),
        pygame.image.load('sprites/images/7.png'),
        pygame.image.load('sprites/images/8.png'),
        pygame.image.load('sprites/images/9.png')
        )
    _x=pygame.image.load('sprites/images/x.png')
    #------------------------------------------player images
    standing_r=(
        pygame.image.load('sprites/images/player1.png'),
        pygame.image.load('sprites/images/player2.png'),
        pygame.image.load('sprites/images/player3.png'),
        pygame.image.load('sprites/images/player4.png')
        )
    standing_l=(
        pygame.transform.flip(standing_r[0],True,False),
        pygame.transform.flip(standing_r[1],True,False),
        pygame.transform.flip(standing_r[2],True,False),
        pygame.transform.flip(standing_r[3],True,False)
        )
    walking_r=(
        pygame.image.load('sprites/images/playerwalking1.png'),
        pygame.image.load('sprites/images/playerwalking2.png'),
        pygame.image.load('sprites/images/playerwalking3.png'),
        pygame.image.load('sprites/images/playerwalking4.png')
        )
    walking_l=(
        pygame.transform.flip(walking_r[0],True,False),
        pygame.transform.flip(walking_r[1],True,False),
        pygame.transform.flip(walking_r[2],True,False),
        pygame.transform.flip(walking_r[3],True,False)
        )
    attack_r=(
        pygame.image.load('sprites/images/pattack_ground1.png'),
        pygame.image.load('sprites/images/pattack_ground2.png'),
        pygame.image.load('sprites/images/pattack_ground3.png'),
        pygame.image.load('sprites/images/pattack_ground4.png')
        )
    attack_l=(
        pygame.transform.flip(attack_r[0],True,False),
        pygame.transform.flip(attack_r[1],True,False),
        pygame.transform.flip(attack_r[2],True,False),
        pygame.transform.flip(attack_r[3],True,False)
        )
    airattack_r=(
        pygame.image.load('sprites/images/pattack_air1.png'),
        pygame.image.load('sprites/images/pattack_air2.png'),
        pygame.image.load('sprites/images/pattack_air3.png'),
        pygame.image.load('sprites/images/pattack_air4.png')
        )
    airattack_l=(
        pygame.transform.flip(airattack_r[0],True,False),
        pygame.transform.flip(airattack_r[1],True,False),
        pygame.transform.flip(airattack_r[2],True,False),
        pygame.transform.flip(airattack_r[3],True,False)
        )
    jump_r=pygame.image.load('sprites/images/playeron air.png')
    jump_l=pygame.transform.flip(jump_r,True,False)
    land_r=pygame.image.load('sprites/images/playerland.png')
    land_l=pygame.transform.flip(land_r,True,False)
    p_hurt_r=(
        pygame.image.load('sprites/images/playerhurt_s.png'),
        pygame.image.load('sprites/images/playerhurt_j.png'),
        pygame.image.load('sprites/images/playerhurt_ag.png'),
        pygame.image.load('sprites/images/playerhurt_aa.png'),
        )
    p_hurt_l=(
        pygame.transform.flip(p_hurt_r[0],True,False),
        pygame.transform.flip(p_hurt_r[1],True,False),
        pygame.transform.flip(p_hurt_r[2],True,False),
        pygame.transform.flip(p_hurt_r[3],True,False)
        )
    dead_p=pygame.image.load('sprites/images/playerdied.png')

    #------------------------------------------effect images
    heart=(
        pygame.image.load('sprites/images/life0.png'),
        pygame.image.load('sprites/images/life1.png')
        )
    heartbreak=(
        pygame.image.load('sprites/images/heartbreak1.png'),
        pygame.image.load('sprites/images/heartbreak2.png'),
        pygame.image.load('sprites/images/heartbreak3.png'),
        pygame.image.load('sprites/images/heartbreak4.png'),
        pygame.image.load('sprites/images/heartbreak5.png'),
        pygame.image.load('sprites/images/heartbreak6.png'),
        pygame.image.load('sprites/images/heartbreak7.png'),
        pygame.image.load('sprites/images/heartbreak8.png'),
        pygame.image.load('sprites/images/heartbreak9.png')
        )
    starcollected=(
        pygame.image.load('sprites/images/starcollect1.png'),
        pygame.image.load('sprites/images/starcollect2.png'),
        pygame.image.load('sprites/images/starcollect3.png'),
        pygame.image.load('sprites/images/starcollect4.png'),
        pygame.image.load('sprites/images/starcollect5.png'),
        pygame.image.load('sprites/images/starcollect6.png'),
        pygame.image.load('sprites/images/starcollect7.png'),
        pygame.image.load('sprites/images/starcollect8.png'),
        pygame.image.load('sprites/images/starcollect9.png')
        )
    star_r=(
        pygame.image.load('sprites/images/star1.png'),
        pygame.image.load('sprites/images/star2.png'),
        pygame.image.load('sprites/images/star3.png'),
        pygame.image.load('sprites/images/star4.png')
        )
    enemy1_r=(
        pygame.image.load('sprites/images/p_enemy1.png'),
        pygame.image.load('sprites/images/p_enemy2.png'),
        pygame.image.load('sprites/images/p_enemy3.png'),
        pygame.image.load('sprites/images/p_enemy4.png')
        )
    enemy1_l=(
        pygame.transform.flip(enemy1_r[0],True,False),
        pygame.transform.flip(enemy1_r[1],True,False),
        pygame.transform.flip(enemy1_r[2],True,False),
        pygame.transform.flip(enemy1_r[3],True,False)
        )
    enemyblast=(
        pygame.image.load('sprites/images/enemydie1.png'),
        pygame.image.load('sprites/images/enemydie2.png'),
        pygame.image.load('sprites/images/enemydie3.png'),
        pygame.image.load('sprites/images/enemydie4.png'),
        pygame.image.load('sprites/images/enemydie5.png'),
        pygame.image.load('sprites/images/enemydie6.png'),
        pygame.image.load('sprites/images/enemydie7.png'),
        pygame.image.load('sprites/images/enemydie8.png'),
        pygame.image.load('sprites/images/enemydie9.png')
        )
    healthbar=(
        pygame.image.load('sprites/images/health1.png'),
        pygame.image.load('sprites/images/health2.png'),
        pygame.image.load('sprites/images/health3.png')
        )
    esc_exit=pygame.image.load('sprites/images/escback.png')
    dropgold=pygame.image.load('sprites/images/dropgold.png')
    dropheart=pygame.image.load('sprites/images/dropheart.png')
    lifeadd1=pygame.image.load('sprites/images/life+1.png')
    healtheffect=(
        pygame.image.load('sprites/images/healtheffect1.png'),
        pygame.image.load('sprites/images/healtheffect2.png'),
        pygame.image.load('sprites/images/healtheffect3.png'),
        pygame.image.load('sprites/images/healtheffect4.png'),
        pygame.image.load('sprites/images/healtheffect5.png'),
        pygame.image.load('sprites/images/healtheffect6.png'),
        pygame.image.load('sprites/images/healtheffect7.png'),
        pygame.image.load('sprites/images/healtheffect8.png'),
        pygame.image.load('sprites/images/healtheffect9.png')
        )
    goldplus=(
        pygame.image.load('sprites/images/gold+1.png'),
        pygame.image.load('sprites/images/gold+5.png'),
        pygame.image.load('sprites/images/gold+10.png'),
        pygame.image.load('sprites/images/gold+50.png'),
        pygame.image.load('sprites/images/gold+100.png')
        )
    messagebord=(
        pygame.image.load('sprites/images/bord menu.png'),
        pygame.image.load('sprites/images/bord next level.png')
        )
    afterdeathmessage=(
        pygame.image.load('sprites/images/diedmessage.png'),
        pygame.image.load('sprites/images/diedmessageonmenu.png'),
        pygame.image.load('sprites/images/diedmessagemenuclicked.png'),
        pygame.image.load('sprites/images/diedmessageonretry.png'),
        pygame.image.load('sprites/images/diedmessageretryclicked.png')
        )
    blackscreen=pygame.image.load('sprites/images/blackscreen.png')
    levelbanner=(
        pygame.image.load('sprites/images/level1bord.png'),
        pygame.image.load('sprites/images/level2bord.png'),
        pygame.image.load('sprites/images/level3bord.png'),
        pygame.image.load('sprites/images/level4bord.png'),
        pygame.image.load('sprites/images/level5bord.png')
        )
    #----------------------------------------------------------------------------------audio files
    gamebgmusic=pygame.mixer.Sound('sprites/audio/backgroundmusic.wav')
    onbuttonsound=pygame.mixer.Sound('sprites/audio/oniconsound.wav')
    buttonclickedsound=pygame.mixer.Sound('sprites/audio/buttonclick.wav')
    attacksound=pygame.mixer.Sound('sprites/audio/attack.wav')
    coincollectsound=pygame.mixer.Sound('sprites/audio/coin collect.wav')
    enemyblastsound=pygame.mixer.Sound('sprites/audio/enemyblast.wav')
    enemyhurtsound=pygame.mixer.Sound('sprites/audio/enemyhurt.wav')
    healsound=pygame.mixer.Sound('sprites/audio/heal.wav')
    hurtsound=pygame.mixer.Sound('sprites/audio/hurt.wav')
    jumpsound=pygame.mixer.Sound('sprites/audio/jump.wav')
    landsound=pygame.mixer.Sound('sprites/audio/land.wav')
    pointsound=pygame.mixer.Sound('sprites/audio/point.wav')
    runsound=pygame.mixer.Sound('sprites/audio/run.wav')
    starcollectsound=pygame.mixer.Sound('sprites/audio/starcollect.wav')
    ripsound=pygame.mixer.Sound('sprites/audio/rip.wav')



    try:
        f=open('sprites/data/donotdelete.txt','rb')
        data=pickle.load(f)
        f.close()
        print(data)
    except FileNotFoundError:
        f=open('sprites/data/donotdelete.txt','wb')
        data=[{'l1':0,'l2':None,'l3':None,'l4':None,'l5':None},1000]
        pickle.dump(data,f)
        f.close()

    
    menu(data)#-------Function call menu

    


