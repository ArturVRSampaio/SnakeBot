def bite(snake_position, movement):

    width = 600
    snake = list(snake_position)

    head = str(snake[0][0]) + str(snake[1][0])

    if movement == 1 and snake[1][0] + 20 <= width:
        head = str(snake[0][0]) + str(snake[1][0] + 20)
    #	print("down")

    if movement == 2 and snake[1][0] - 20 >= 0:
        head = str(snake[0][0]) + str(snake[1][0] - 20)
    #	print("up")

    if movement == 3 and snake[0][0] + 20 <= width:
        head = str(snake[0][0] + 20) + str(snake[1][0])
    #	print("right")

    if movement == 6 and snake[0][0] - 20 >= 0:
        head = str(snake[0][0] - 20) + str(snake[1][0])
    #	print("left")

    y = len(snake)

    for x in range(0, y):
        if str(snake[0][x]) + str(snake[1][x]) == str(head):
            return True

    #        print("no choice")
    return False


class SnakeBot:

    def control(self, apple_position, snake_position, last_direction):

        if apple_position[1] > snake_position[1][0] and last_direction != 2 and bite(snake_position, 1) == False:
            return 1
        #    print("baixo")
        elif apple_position[1] < snake_position[1][0] and last_direction != 1 and bite(snake_position, 2) == False:
            return 2
        #    print("cima")
        elif apple_position[0] > snake_position[0][0] and last_direction != 6 and bite(snake_position, 3) == False:
            return 3
        #    print("direita")
        elif apple_position[0] < snake_position[0][0] and last_direction != 3 and bite(snake_position, 6) == False:
            return 6
        #    print("esquerda")

        ################# ##########
        # impossivel ir ate a maca  #
        ################# ##########

        elif last_direction != 2 and bite(snake_position, 1) == False:
            return 1
        #    print("baixo")

        elif last_direction != 1 and bite(snake_position, 2) == False:
            return 2
        #    print("cima")

        elif last_direction != 6 and bite(snake_position, 3) == False:
            return 3
        #    print("direita")

        elif last_direction != 3 and bite(snake_position, 6) == False:
            return 6
        #    print("esquerda")

        # print("sem escolha")
        return last_direction
