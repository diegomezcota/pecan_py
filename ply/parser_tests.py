from pecan_parser import parser
import sys

no_tests = 6
test_no = str(sys.argv[1]) if len(sys.argv) > 1 else None
test_files = ['test' + str(i) + '.gmc' for i in range(1, no_tests + 1)]

print("---PROBANDO ANALIZADOR SINTÁCTICO---")

if test_no:
    try:
        s = open('tests/parser/' + 'test' + test_no + '.gmc', 'r').read()
        parser.parse(s)
        print('test no.', test_no, ': apropiado')
    except SyntaxError:
        print('There was a syntax error in test. no', test_no)
else:
    for i, test in enumerate(test_files):
        try:
            s = open('tests/parser/' + test, 'r').read()
            parser.parse(s)
            print('test no.', i + 1, ': apropiado')
        except SyntaxError:
            print('There was a syntax error in test. no', i + 1)
        except EOFError:
            break