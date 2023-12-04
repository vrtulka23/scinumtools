ROOT_SOURCE   = 'ROOT'
FILE_SOURCE   = 'FILE'
STRING_SOURCE = 'STRING'

class Numeric:
    PRECISION   = 1e-6

class Keyword:
    NONE        = 'none'
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
    TAGS        = 'tags'
    DESCRIPTION = 'description'

class Sign:
    QUERY       = '?'
    WILDCARD    = '*'
    NEGATE      = '~'
    DEFINED     = '!'
    SEPARATOR   = '.'
    CONDITION   = '@'
    VARIABLE    = '$'
    VALIDATION  = '!'
    NEWLINE     = "\n"

class EnvType:
    DATA        = 1   # parse parameter data 
    DOCS        = 2   # parse documentation information
    
class Namespace:
    NODES       = 1
    UNITS       = 2
    SOURCES     = 3
    
class Format:
    VALUE       = 1
    TUPLE       = 2
    TYPE        = 3
    NODE        = 4
    QUANTITY    = 5

class Order:
    NONE        = 0
    NAME        = 1

    