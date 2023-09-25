class Numeric:
    PRECISION   = 1e-6

class Keyword:
    TRUE        = 'true'
    FALSE       = 'false'
    CASE        = 'case'
    ELSE        = 'else'
    END         = 'end'
    UNIT        = 'unit'
    SOURCE      = 'source'
    OPTIONS     = 'options'
    CONSTANT    = 'constant'
    FORMAT      = 'format'
    CONDITION   = 'condition'

class Sign:
    QUERY       = '?'
    WILDCARD    = '*'
    NEGATE      = '~'
    DEFINED     = '!'
    SEPARATOR   = '.'
    CONDITION   = '@'
    VARIABLE    = '$'
    VALIDATION  = '!'

class Namespace:
    NODES       = 1
    UNITS       = 2
    SOURCES     = 3
    
class Format:
    VALUE       = 1
    TUPLE       = 2
    TYPE        = 3
    NODE        = 4
