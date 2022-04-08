from pecan_parser import parser

no_tests = 2
test_files = ['test' + str(i) + '.in' for i in range(1, no_tests + 1)]

print("---PROBANDO ANALIZADOR SINTÁCTICO---")

for i, test in enumerate(test_files):
    try:
        s = open('tests/parser/' + test, 'r').read()
        parser.parse(s)
        print('test no.', i + 1, ': apropiado')
    except SyntaxError:
        print('There was a syntax error in test. no', i + 1)
    except EOFError:
        break