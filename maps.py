

map_level0 = 'WWWW  WWWW\n' \
             'W        W\n' \
             '         W\n' \
             'W        W\n' \
             'WWWW  WWWW\n'


def fill_map(map, map_object, screen, player):
    for object in map_object:
        for i in range(int(object.y), int(object.y + object.wall.get_height())):
            for j in range(int(object.x), int(object.x + object.wall.get_width())):
                map[i][j] = "W"
    for i in range(int(player.y), int(player.y + player.height)):
        for j in range(int(player.x), int(player.x + player.width)):
            map[i][j] = "P"