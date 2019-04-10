class Sbot():

    def morde(self, snakeposx, snakeposy, movimento):

        largura = 600
        cobray = list(snakeposy)
        cobrax = list(snakeposx)

        if (movimento ==1):

            if (cobray[0]+20 > largura):
                return True

            cabeca= str(cobrax[0])+ str(cobray[0]+20)

        if (movimento ==2):

            if (cobray[0]-20 <0):
                return True

            cabeca= str(cobrax[0])+ str(cobray[0]-20)

        if (movimento ==3):

            if (cobray[0]+20 > largura):
                return True

            cabeca= str(cobrax[0]+20)+ str(cobray[0])

        if (movimento ==6):

            if (cobray[0]-20 < 0):
                return True

            cabeca= str(cobrax[0]-20)+ str(cobray[0])

        cobrax.pop(0)
        cobray.pop(0)
        y= len(cobrax)

        for x in range(0, y):
            if (str(cobrax[x]) + str(cobray[x]) == str(cabeca) ):
                return True
        return False




    def controle(self, applepos, snakeposx, snakeposy, lastdiers):

        
        if (applepos[1] > snakeposy[0] and lastdiers != 2 and self.morde(snakeposx, snakeposy, 1) ==False):
        #    print("baixo")
            return 1
        elif (applepos[0] > snakeposx[0]and lastdiers != 6 and self.morde(snakeposx, snakeposy, 3) ==False):
        #    print("direita")
            return 3
        elif (applepos[0] < snakeposx[0]and lastdiers != 3 and self.morde(snakeposx, snakeposy, 6) ==False):
        #    print("esquerda")
            return 6
        elif (applepos[1] < snakeposy[0]and lastdiers != 1 and self.morde(snakeposx, snakeposy, 2) ==False ):
        #    print("cima")
            return 2

        elif (self.morde(snakeposx, snakeposy, 1) == False):
        #    print("baixo")
            return 1

        elif (self.morde(snakeposx, snakeposy, 2) == False):
        #    print("cima")
            return 2
        
        elif (self.morde(snakeposx, snakeposy, 3) == False):
        #    print("direita")
            return 3

        elif (self.morde(snakeposx, snakeposy, 6) == False):
        #    print("esquerda")
            return 6

        return (lastdiers)
