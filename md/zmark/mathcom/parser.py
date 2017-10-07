import nodes
import api


class ParseError(ValueError):
    def __init__(self, token, pos):
        ValueError.__init__(self, '')
        self.token = token
        self.pos = pos


def init(operators):
    tokens = (
        'NAME', 'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE',
        'COMMA', 'VERTBAR',
        'PLUS', 'MINUS', 'PLUS_MINUS', 'MULTIPLY', 'DIVIDE', 'EXP', 'SUB',
        'EQ', 'NE', 'LE', 'LT', 'GE', 'GT', 'RELATION_OP',
        'MODULAR',
        'SQRT',
    )

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_PLUS_MINUS = r'\+-'
    t_MULTIPLY = r'\*'
    t_DIVIDE = r'/'
    t_EXP = r'\^'
    t_SUB = r'_'
    t_EQ = r'='
    t_NE = r'!='
    t_LE = r'<='
    t_LT = r'<'
    t_GE = r'>='
    t_GT = r'>'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LBRACE = r'{'
    t_RBRACE = r'}'
    t_VERTBAR = r'\|'
    t_COMMA = r','
    t_MODULAR = r'%'

    t_ignore = ' \n\t\r'

    def t_NAME(t):
        r'[a-zA-Z0-9.]+'
        if t.value in operators['preu']:
            t.type = t.value.upper()
        if t.value in operators['rel']:
            t.type = 'RELATION_OP'
        return t

    def t_error(t):
        raise ParseError(t.value, t.lexpos)

    import ply.lex as lex
    lex.lex()

    precedence = (
        ('right', 'RELATION_OP'),
        ('left', 'EQ', 'NE', 'LE', 'LT', 'GE', 'GT'),
        ('left', 'PLUS', 'MINUS', 'PLUS_MINUS'),
        ('left', 'DIVIDE'),
        ('left', 'MULTIPLY'),
        ('right', 'UMINUS', 'UPLUS', 'UPLUS_MINUS', 'SQRT'),
        ('right', 'EXP'),
        ('left', 'SUB'),
    )

    def p_expression(t):
        '''expression : equation
                      | comod'''
        t[0] = t[1]

    def p_equation_eq(t):
        '''equation : equationeq
                    | equationeq LE equationtail
                    | equationeq LT equationtail
                    | equationeq GE equationtail
                    | equationeq GT equationtail
        '''
        if len(t) == 2 and len(t[1]) == 1:
            t[0] = t[1][0]
            return
        t[0] = nodes.Equation(t[1][0], ['='] * (len(t[1]) - 1), t[1][1:])
        if len(t) == 4:
            t[0]['ops'].append(t[2])
            t[0]['ops'].extend(t[3][0])
            t[0]['tails'].extend(t[3][1])

    def p_equation_ne(t):
        '''equation : equationne
                    | equationne LE equationtail
                    | equationne LT equationtail
                    | equationne GE equationtail
                    | equationne GT equationtail
                    | equationne EQ equationtail
        '''
        t[0] = nodes.Equation(t[1][0], ['='] * (len(t[1]) - 2), t[1][1:])
        t[0]['ops'].append('!=')
        if len(t) == 4:
            t[0]['ops'].append(t[2])
            t[0]['ops'].extend(t[3][0])
            t[0]['tails'].extend(t[3][1])

    def p_equationeq_or_modchain(t):
        '''equationeq : equationeq EQ arithmetics
                      | arithmetics
        '''
        if len(t) == 2:
            t[0] = [t[1]]
        else:
            t[1].append(t[3])
            t[0] = t[1]

    def p_equationne_or_modchain(t):
        '''equationne : equationeq NE arithmetics'''
        t[1].append(t[3])
        t[0] = t[1]

    def p_equationtail_chain_eq(t):
        '''equationtail : equationtail LE arithmetics
                        | equationtail LT arithmetics
                        | equationtail GE arithmetics
                        | equationtail GT arithmetics
                        | equationtail EQ arithmetics
                        | equationtail NE arithmetics
                        | arithmetics
        '''
        if len(t) == 2:
            t[0] = ([], [t[1]])
        else:
            t[0] = t[1]
            t[0][0].append(t[2])
            t[0][1].append(t[3])

    def p_comod_congruence(t):
        '''comod : equationeq MODULAR arithmetics'''
        t[0] = nodes.CongruentModulo(t[1][:-1], t[1][-1], '==', t[3])

    def p_comod_not(t):
        '''comod : equationne MODULAR arithmetics'''
        t[0] = nodes.CongruentModulo(t[1][:-1], t[1][-1], '!==', t[3])

    def p_arithmetics_binop(t):
        '''arithmetics : arithmetics PLUS arithmetics
                       | arithmetics MINUS arithmetics
                       | arithmetics PLUS_MINUS arithmetics
                       | arithmetics MULTIPLY arithmetics
                       | arithmetics DIVIDE arithmetics
        '''
        if t[2] == '+' or t[2] == '-' or t[2] == '+-':
            t[0] = nodes.additive_binary(t[2], t[1], t[3])
        elif t[2] == '*':
            t[0] = nodes.multiplication(t[1], t[3])
        else:
            t[0] = nodes.division(t[1], t[3])

    def p_arithmetics_rel(t):
        '''arithmetics : arithmetics RELATION_OP arithmetics'''
        t[0] = nodes.relation_op(t[2], t[1], t[3])

    def p_arguments(t):
        '''arguments : arithmetics
                     | arguments COMMA arithmetics
        '''
        if len(t) == 2:
            t[0] = [t[1]]
        else:
            t[1].append(t[3])
            t[0] = t[1]

    def p_relations(t):
        '''relations : equation
                     | relations COMMA equation
        '''
        if len(t) == 2:
            t[0] = [t[1]]
        else:
            t[1].append(t[3])
            t[0] = t[1]

    def p_set(t):
        '''arithmetics : LBRACE arguments RBRACE
                       | LBRACE arguments VERTBAR relations RBRACE'''
        if len(t) == 4:
            t[0] = nodes.set_node(t[2], [])
        else:
            t[0] = nodes.set_node(t[2], t[4])

    def p_arithmetics_preunary(t):
        '''arithmetics : MINUS arithmetics %prec UMINUS
                       | PLUS arithmetics %prec UPLUS
                       | PLUS_MINUS arithmetics %prec UPLUS_MINUS
                       | SQRT arithmetics
        '''
        if t[1] == 'sqrt':
            t[0] = nodes.square_root(t[2])
        else:
            t[0] = nodes.PreUnaryOp(t[1], t[2])

    def p_arithmetics_exp(t):
        '''arithmetics : arithmetics EXP arithmetics'''
        t[0] = nodes.Exponentiation(t[1], t[3])

    def p_arithmetics_quadratic_struct(t):
        '''arithmetics : arithmetics LBRACKET arithmetics RBRACKET'''
        t[0] = nodes.QuadraticStruct(t[1], t[3])

    def p_arithmetics_item(t):
        '''arithmetics : item'''
        t[0] = t[1]

    def p_item_subscript(t):
        '''item : item SUB item'''
        t[0] = nodes.Subscript(t[1], t[3])

    def p_item_name(t):
        '''item : NAME'''
        t[0] = nodes.Name(t[1])

    def p_item_absval(t):
        '''item : VERTBAR arithmetics VERTBAR'''
        t[0] = nodes.absolute_value(t[2])

    def p_item_group(t):
        '''item : LPAREN arguments RPAREN'''
        if len(t[2]) == 1:
            t[0] = t[2][0]
        else:
            t[0] = nodes.expr_tuple(t[2])

    def p_item_function(t):
        '''item : item LPAREN arguments RPAREN'''
        t[0] = nodes.Function(t[1], t[3])

    def p_error(t):
        if t is None:
            raise ParseError('', -1)
        raise ParseError(t.value, t.lexpos)

    import ply.yacc as yacc
    yacc.yacc()

    return yacc.parse
