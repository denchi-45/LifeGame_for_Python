import tkinter as tk

CS = 10                                 #セルサイズ
NUM_ROW = 50                             #列の個数
NUM_COL = 50                            #行の個数
SCR_HEIGHT = int(NUM_COL*CS)            #行の画像サイズ
SCR_WIDTH  = int(NUM_ROW*CS)            #列の画像サイズ
field_size = NUM_ROW * NUM_COL          #フィールドサイズ
DEAD, ALIVE = 0, 1                      #セルが死んでいるか生きているか

#判定用配列（リスト）
directions = [-NUM_ROW-1, -NUM_ROW, -NUM_ROW+1,
              -1        ,                   +1,
              NUM_ROW-1 ,  NUM_ROW,  NUM_ROW+1 ]


#各種wigetの設定
class Frame(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self,master)

        #世代数を表示するためのラベル
        self.generation_lb = tk.Label(self,text=f'{lg.generation}　世代目')
        self.generation_lb.grid(row=0,column=0,pady=5)

        self.create_button()

        self.cvs = tk.Canvas(self,
                             width = CS*NUM_ROW,
                             height = CS*NUM_COL,
                             bg="white")
        self.cvs.grid(row=1,column=0,columnspan=6)


        Rect.canvas = self.cvs
        LifeGame.canvas = self.cvs

        for row in range(NUM_ROW):
            for col in range(NUM_COL):
                Rect(row,col)
    #各種ボタンを生成する
    def create_button(self):

        self.step = tk.Button(self,text='１世代進める',command=lg.step_generation )
        self.loop_step = tk.Button(self,text='スタート',command=self.start)
        self.loop_stop = tk.Button(self,text='一時停止',command=self.stop)
        self.clear = tk.Button(self,text='全消去',command=lg.clear)
        self.garaxy = tk.Button(self,text='ギャラクシー',command=lg.garaxy)


        self.step.grid(row=0,column=1,pady=5)
        self.loop_step.grid(row=0,column=2,pady=5)
        self.loop_stop.grid(row=0,column=3,pady=5)
        self.clear.grid(row=0,column=4,pady=5)
        self.garaxy.grid(row=0,column=5,pady=5)

    def start(self):
        if lg.run == False:
            lg.run = True
            lg.loop()

    def stop(self):
        lg.run = False

#セルとその処理
class Rect(Frame):
    canvas = None
    def __init__(self,row,col):
        self.ID = self.canvas.create_rectangle(col*CS,
                                               row*CS,
                                               col*CS+CS,
                                               row*CS+CS,
                                               outline="#202020",
                                               fill='black')

        self.canvas.tag_bind(self.ID,'<1>',self.pressed)
        self.canvas.tag_bind(self.ID,'<Button1-Motion>',self.dragging)
    #クリックされたときの処理
    def pressed(self,event):
        #print(self.ID)
        self.cell_status = lg.current_field[self.ID - 1]
        if self.cell_status == ALIVE:
            lg.current_field[self.ID - 1] = DEAD
            self.canvas.itemconfig(self.ID,fill='black')
        else:
            lg.current_field[self.ID - 1] = ALIVE
            self.canvas.itemconfig(self.ID,fill='green')
    #ドラッグされたときの処理
    def dragging(self,event):
        X = event.x//CS
        Y = event.y//CS
        if X >= 0 and X < 50 and Y >= 0 and Y < 50:
            self.id = int(event.x // CS + NUM_ROW * (event.y // CS) + 1)
            #print(self.id)
            if self.cell_status == ALIVE:
                lg.current_field[self.id - 1] = DEAD
                self.canvas.itemconfig(self.id,fill='black')
            else:
                lg.current_field[self.id - 1] = ALIVE
                self.canvas.itemconfig(self.id,fill='green')

#ゲームのメイン処理部
class LifeGame(Rect):
    def __init__(self):
        self.field = [DEAD for i in range(NUM_ROW*NUM_COL)]         #処理用
        self.current_field = [DEAD for i in range(NUM_ROW*NUM_COL)] #描画用
        self.generation = 0  # 世代数
        self.run = False  # シミュレーション実行中か？

    def loop(self):
        if self.run:
            self.step_generation()
            root.after(1,self.loop)

    #一世代進める
    def step_generation(self):
        self.generation += 1
        frame.generation_lb.configure(text=f'{self.generation} 世代目')
        self.field = self.current_field[:]
        for step_id in range(field_size):
            num_alive_cells = self.check_cell(step_id)
            if num_alive_cells == 2:
                continue
            if num_alive_cells == 3:
                self.current_field[step_id] = ALIVE
                self.canvas.itemconfig(step_id+1,fill='green')
            else:
                self.current_field[step_id] = DEAD
                self.canvas.itemconfig(step_id+1,fill='black')

    #周囲の生きているセルを返す
    def check_cell(self,step_id):
        living_cells = 0
        for direction in directions:
            if step_id % NUM_ROW == 0 and (step_id+direction) % NUM_ROW == NUM_ROW - 1:
                continue
            elif step_id % NUM_ROW == NUM_ROW-1 and (step_id + direction) % NUM_ROW == 0:
                continue
            elif step_id + direction < 0:
                continue
            elif step_id + direction >= field_size:
                continue
            if self.field[step_id + direction] == ALIVE:
                living_cells += 1
        return living_cells

    def clear(self):
        self.generation = 0
        frame.generation_lb.configure(text=f'{self.generation} 世代目')
        for i in range(field_size):
            self.field[i] = DEAD
            self.canvas.itemconfig(i+1,fill='black')
        self.current_field = self.field[:]
        self.stop()


    def chenge_cell(self,tmp_id):
        self.field[tmp_id] = ALIVE
        self.canvas.itemconfig(tmp_id,fill='green')
        self.current_field = self.field[:]

    def garaxy(self):
        self.tmp_garaxy = [819 ,820 ,821 ,822 ,823 ,824 ,0   ,826 ,827 ,
                           869 ,870 ,871 ,872 ,873 ,874 ,0   ,876 ,877 ,
                           0   ,0   ,0   ,0   ,0   ,0   ,0   ,926 ,927 ,
                           969 ,970 ,0   ,0   ,0   ,0   ,0   ,976 ,977 ,
                           1019,1020,0   ,0   ,0   ,0   ,0   ,1026,1027,
                           1069,1070,0   ,0   ,0   ,0   ,0   ,1076,1077,
                           1119,1120,0   ,0   ,0   ,0   ,0   ,0   ,0   ,
                           1169,1170,0   ,1172,1173,1174,1175,1176,1177,
                           1219,1220,0   ,1222,1223,1224,1225,1226,1227]
        for i in self.tmp_garaxy:
            self.chenge_cell(i)




if __name__ == '__main__':
    root = tk.Tk()
    root.title('LifeGame')

    lg = LifeGame()
    frame = Frame()
    frame.pack()

    root.mainloop()