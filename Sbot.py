class Sbot():

    def morde(self, snakepos, movimento):
        
        largura = 600
        cobra = list(snakepos)
        
        cabeca= str(cobra[0][0])+ str(cobra[1][0])

        if (movimento ==1 and cobra[1][0]+20 <= largura):
                cabeca= str(cobra[0][0])+ str(cobra[1][0]+20)
            #	print("BAIXO")


        if (movimento ==2 and cobra[1][0]-20 >=0):
                cabeca= str(cobra[0][0])+ str(cobra[1][0]-20)
            #	print("cima")


        if (movimento ==3 and cobra[0][0]+20 <= largura):
                cabeca= str(cobra[0][0]+20)+ str(cobra[1][0])
            #	print("direita")


        if (movimento ==6 and cobra[0][0]-20 >= 0):
                cabeca= str(cobra[0][0]-20)+ str(cobra[1][0])
            #	print("esquerda")


        y= len(cobra)

        for x in range(0, y):
            if (str(cobra[0][x]) + str(cobra[1][x]) == str(cabeca) ):
                return True
        
#        print("sem escolha")
        return False


    def controle(self, applepos, snakepos, lastdiers):

        if   (applepos[1] > snakepos[1][0] and lastdiers != 2 and self.morde(snakepos, 1) ==False):
            return 1
        #    print("baixo")
        elif (applepos[1] < snakepos[1][0] and lastdiers != 1 and self.morde(snakepos, 2) ==False):
            return 2
        #    print("cima")
        elif (applepos[0] > snakepos[0][0] and lastdiers != 6 and self.morde(snakepos, 3) ==False):
            return 3
        #    print("direita")
        elif (applepos[0] < snakepos[0][0] and lastdiers != 3 and self.morde(snakepos, 6) ==False):
            return 6
        #    print("esquerda")

        ################# ##########
        #impossivel ir ate a maca  #
        ################# ##########

        elif ( lastdiers != 2 and self.morde(snakepos, 1) == False):
            return 1
        #    print("baixo")

        elif ( lastdiers != 1 and self.morde(snakepos, 2) == False):
            return 2
        #    print("cima")
        
        elif ( lastdiers != 6 and self.morde(snakepos, 3) == False):
            return 3
        #    print("direita")

        elif (lastdiers != 3 and self.morde(snakepos, 6) == False):
            return 6
        #    print("esquerda")
        
        #print("sem escolha")
        return (lastdiers)
