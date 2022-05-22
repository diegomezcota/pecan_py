from pecan_parser import parser
import sys

from pecan_parser import TypeMismatchError

no_tests = 8
test_no = str(sys.argv[1]) if len(sys.argv) > 1 else None
test_files = ['test' + str(i) + '.gmc' for i in range(1, no_tests + 1)]

print("---PROBANDO ANALIZADOR SINTÁCTICO---")

if test_no:
    try:
        s = open('compiler/tests/parser/' + 'test' + test_no + '.gmc', 'r').read()
        parser.parse(s, tracking=True)
        print('test no.', test_no, ': apropiado')
    except Exception as e:
        print("test", test_no, ":", e)
else:
    for i, test in enumerate(test_files):
        try:
            s = open('compiler/tests/parser/' + test, 'r').read()
            parser.parse(s, tracking=True)
            print('test no.', i + 1, ': apropiado')
        except Exception as e:
            print(e, "for test", i + 1)
        except EOFError:
            break