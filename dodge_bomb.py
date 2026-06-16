import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA={
    pg.K_UP:(0,-5), #上に5
    pg.K_DOWN:(0,+5),#下に5
    pg.K_LEFT:(-5,0),#左
    pg.K_RIGHT:(+5,0),#右
    } #練1
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def chech_bound(rct: pg.Rect)->tuple[bool,bool]:
    """
    引数：こうかとんRect or 爆弾Rect
    戻り値：判定結果タプル(横方向判定結果,縦方向判定結果)
    画面内ならTrue,画面外ならFalse
    """
    yoko,tate=True,True #画面内
    if rct.left < 0 or WIDTH < rct.right: #横
        yoko= False #画面外
    if rct.top < 0 or HEIGHT < rct.bottom: #縦
        tate=False
    return yoko,tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    
    #練2　爆弾挿入
    bb_img = pg.Surface((20,20)) #円のサイズ
    pg.draw.circle(bb_img,(255,0,0),(10,10),10) #
    bb_img.set_colorkey((0,0,0)) # 黒い部分を透明にする
    bb_rct = bb_img.get_rect()
    # 画面内のランダムな位置
    bb_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)#横,縦
    vx,vy=+5,+5


    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for key,mv in DELTA.items(): #練1
            if key_lst[key]:
                sum_mv[0] += mv[0] #横方向の移動量
                sum_mv[1] += mv[1] #縦方向の移動量

        kk_rct.move_ip(sum_mv)
        if chech_bound(kk_rct) !=(True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])#動きをなかったことに
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx,vy) #練2爆弾動く
        yoko,tate=chech_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
