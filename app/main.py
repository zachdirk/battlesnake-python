import bottle
import os
import random

class GameBoard:
    def __init__(self, id, width, height):
        self.id = id
        self.width = width
        self.height = height
                
    def parse(self, data):
        self.data = data
        self.snakes = self.data["snakes"]["data"]
        self.me = self.data["you"]

    def direction(self):
        
        

G = None
@bottle.route('/')
def static():
    return "the server is is running"


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
        'color': '#00FF00',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url
    }


@bottle.post('/move')
def move():
    data = bottle.request.json
    G.data = data
    G.parse(data)
    # TODO: Do things with data
    directions = ['up', 'down', 'left', 'right']
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
