MSG_CELL_ATTR_ERROR = 'Unknown cell attributes descriptor: '

class ParseError(ValueError):
    def __init__(self, message):
        ValueError.__init__(self, message)
