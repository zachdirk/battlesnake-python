import bottle
import os
import random

class GameBoard:
    def __init__(self, id, width, height):
        self.id = id
        self.width = width
        self.height = height
    
    def parseSnakes(self, snakesIn):
        snakes = []
        for snake in snakesIn:
            newSnake = []
            for piece in snake["body"]["data"]:
                x = piece["x"]
                y = piece["y"]
                newSnake.append((x,y))
            snakes.append(newSnake)
        return(snakes)
        
    def parseMe(self, meIn):
        me = []
        for piece in meIn["body"]["data"]:
            x = piece["x"]
            y = piece["y"]
            me.append((x,y))
        return(me)
    
    def safeSquare(self, x, y):
        if x < 0 or x == self.width:
            return False
        elif y < 0 or y == self.height:
            return False
        for snake in self.snakes:
            for piece in snake:
                if piece[0] == x and piece[1] == y:
                    return False
        return True
    
    
    def parse(self, data):
        self.data = data
        self.snakes = []
        snakesIn = self.data["snakes"]["data"]
        self.snakes = self.parseSnakes(snakesIn)            
        meIn = self.data["you"]
        self.me = self.parseMe(meIn)
        
    def directions(self):
        x,y = self.me[0]
        safes = []
        if self.safeSquare(x+1, y):
            safes.append("right")
        if self.safeSquare(x,y-1):
            safes.append("up")
        if self.safeSquare(x-1,y):
            safes.append("left")
        if self.safeSquare(x,y+1):
            safes.append("down")
            
        return(safes)

G = None
@bottle.route('/')
def static():
    return "the server is running"


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data.get('game_id')
    board_width = data.get('width')
    board_height = data.get('height')
    global G
    G = GameBoard(game_id, board_width, board_height)
    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#FF0000',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url
    }


@bottle.post('/move')
def move():
    data = bottle.request.json
    G.data = data
    G.parse(data)
    # TODO: Do things with data
    directions = G.directions()
    print(directions)
    direction = random.choice(directions)
    print direction
    return {
        'move': direction,
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '192.168.96.168'),
        port=os.getenv('PORT', '8080'),
        debug = True)
