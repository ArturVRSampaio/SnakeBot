class Sbot():

    def morde(self, snakeposx, snakeposy, movimento):

        largura = 600
        cobray = list(snakeposy)
        cobrax = list(snakeposx)

        cabeca= str(cobrax[0])+ str(cobray[0])

        if (movimento ==1 and cobray[0]+20 <= largura):
                cabeca= str(cobrax[0])+ str(cobray[0]+20)
            #	print("BAIXO")


        if (movimento ==2 and cobray[0]-20 >=0):
                cabeca= str(cobrax[0])+ str(cobray[0]-20)
            #	print("cima")


        if (movimento ==3 and cobrax[0]+20 <= largura):
                cabeca= str(cobrax[0]+20)+ str(cobray[0])
            #	print("direita")


        if (movimento ==6 and cobrax[0]-20 >= 0):
                cabeca= str(cobrax[0]-20)+ str(cobray[0])
            #	print("esquerda")


        y= len(cobrax)

        for x in range(0, y):
            if (str(cobrax[x]) + str(cobray[x]) == str(cabeca) ):
                return True
        
#        print("sem escolha")
        return False


    def controle(self, applepos, snakeposx, snakeposy, lastdiers):

        if   (applepos[1] > snakeposy[0] and lastdiers != 2 and self.morde(snakeposx, snakeposy, 1) ==False):
            return 1
        #    print("baixo")
        elif (applepos[1] < snakeposy[0] and lastdiers != 1 and self.morde(snakeposx, snakeposy, 2) ==False):
            return 2
        #    print("cima")
        elif (applepos[0] > snakeposx[0] and lastdiers != 6 and self.morde(snakeposx, snakeposy, 3) ==False):
            return 3
        #    print("direita")
        elif (applepos[0] < snakeposx[0] and lastdiers != 3 and self.morde(snakeposx, snakeposy, 6) ==False):
            return 6
        #    print("esquerda")

        ################# ##########
        #impossivel ir até a maça  #
        ################# ##########

        elif ( lastdiers != 2 and self.morde(snakeposx, snakeposy, 1) == False):
            return 1
        #    print("baixo")

        elif ( lastdiers != 1 and self.morde(snakeposx, snakeposy, 2) == False):
            return 2
        #    print("cima")
        
        elif ( lastdiers != 6 and self.morde(snakeposx, snakeposy, 3) == False):
            return 3
        #    print("direita")

        elif (lastdiers != 3 and self.morde(snakeposx, snakeposy, 6) == False):
            return 6
        #    print("esquerda")
        
        #print("sem escolha")
        return (lastdiers)
