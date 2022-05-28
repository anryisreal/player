

map_level0 = 'WWWW  WWWW\n' \
             'W        W\n' \
             '         W\n' \
             'W        W\n' \
             'WWWWW WWWW\n'


def fill_map(map, map_object, screen, player):
    for object in map_object:
        print(object.x)
        '''for i in range((object.x), (object.x + object.wall.get_width())):
            for j in range((object.y), (object.y + object.wall.get_height())):
                map[i][j] = "W"
            print(object.x, object.x + object.wall.get_width())
    for i in range(int(player.x), int(player.x + player.width)):
        for j in range(int(player.y), int(player.y + player.height)):
            map[i][j] = "P"'''