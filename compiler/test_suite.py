from pecan_parser import parser
import sys
import json

from pecan_parser import TypeMismatchError

test_name = None

if len(sys.argv) > 1:
    test_name = sys.argv[1] 
else: 
    raise Exception('Need test name to run file')


try:
    s = open('compiler/tests/test_suite/' + test_name + '.gmc', 'r').read()
    parser.parse(s, tracking=True)
    print('test ', test_name, ': apropiado')
except Exception as e:
    error_msg = "test " + str(test_name) + " : " + str(e)
    # Save ovejota as error
    with open('ovejota.json', "w") as output_file:
        json.dump({'error': error_msg}, output_file, indent=2)
    raise e