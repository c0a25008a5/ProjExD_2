import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA={
    pg.K_UP:(0,-5), #上に5
    pg.K_DOWN:(0,+5),#下に5
    pg.K_LEFT:(-5,0),#左
    pg.K_RIGHT:(+5,0),#右
    } #練1
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def chech_bound(rct: pg.Rect)->tuple[bool,bool]:#練3外いかない
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


def gameover(screen: pg.Surface) -> None:
    go_img=pg.Surface((1100,650))#黒い図
    pg.draw.rect(go_img,(0,0,0),pg.Rect(0,0,1100,650))
    go_img.set_alpha(180)

    fonto=pg.font.Font(None,100)#文字
    txt=fonto.render("Game Over",True,(255,255,255))
    txt_rct = txt.get_rect()
    txt_rct.center = 1100 // 2, 650 // 2
    go_img.blit(txt,txt_rct)

    kc_img_l = pg.image.load("fig/8.png")#泣く
    kc_img_r = pg.transform.flip(kc_img_l, True, False)
    kc_rct_l = kc_img_l.get_rect()
    kc_rct_l.center = 1100 // 2 - 200, 650 // 2
    kc_rct_r = kc_img_r.get_rect()
    kc_rct_r.center = 1100 // 2 + 200, 650 // 2
    
    go_img.blit(kc_img_l, kc_rct_l)
    go_img.blit(kc_img_r, kc_rct_r)
    screen.blit(go_img,[0,0])

    pg.display.update()
    time.sleep(5)
    
def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        bb_img.set_colorkey((0, 0, 0))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
    bb_accs = [a for a in range(1, 11)]
    return bb_imgs, bb_accs

def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """
    押下キーに対する移動量の合計値タプルをキー、
    rotozoomしたSurfaceを値とした辞書を返す
    """
    base_img = pg.image.load("fig/3.png")
    flip_img = pg.transform.flip(base_img, True, False)

    kk_dict={
        (0, 0): pg.transform.rotozoom(flip_img, 0, 0.9),      # キー押下がない場合（初期状態・右向き）
        (+5, 0): pg.transform.rotozoom(flip_img, 0, 0.9),     # 右
        (+5, -5): pg.transform.rotozoom(flip_img, 45, 0.9),   # 右上
        (0, -5): pg.transform.rotozoom(flip_img, 90, 0.9),    # 上
        (-5, -5): pg.transform.rotozoom(base_img, -45, 0.9),  # 左上
        (-5, 0): pg.transform.rotozoom(base_img, 0, 0.9),     # 左
        (-5, +5): pg.transform.rotozoom(base_img, 45, 0.9),   # 左下
        (0, +5): pg.transform.rotozoom(flip_img, -90, 0.9),   # 下
        (+5, +5): pg.transform.rotozoom(flip_img, -45, 0.9),  # 右下
    }
    return kk_dict




def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_imgs = get_kk_imgs()
    # kk_img = kk_imgs[(0, 0)]

    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_imgs, bb_accs = init_bb_imgs()
    
    #練2　爆弾挿入
    bb_img = pg.Surface((20,20)) #円のサイズ
    pg.draw.circle(bb_img,(255,0,0),(10,10),10) #
    bb_img.set_colorkey((0,0,0)) # 黒い部分を透明にする
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    # 画面内のランダムな位置
    bb_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)#横,縦
    vx,vy=+5,+5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:  #ゲーム終了
                return
        if kk_rct.colliderect(bb_rct):#練4鳥と爆弾衝突したら終わる
            gameover(screen)
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
        if chech_bound(kk_rct) !=(True,True):#練3外いかない2
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])#動きをなかったことに
        
        kk_img = kk_imgs[tuple(sum_mv)]
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx,vy) #練2爆弾動く
        yoko,tate=chech_bound(bb_rct) #練3跳ね返る
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

        idx = min(tmr // 500, 9)  # 500フレームごとに段階が上がり、最大インデックスは9
        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]
        bb_img = bb_imgs[idx]

        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height
        bb_rct.move_ip(avx, avy)
        


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
