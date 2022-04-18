from lexer import lexer

no_tests = 2
test_files = ['test' + str(i) + '.gmc' for i in range(1, no_tests + 1)]

print("---PROBANDO ANALIZADOR LÉXICO---")

# Give the lexer some input
for i, test in enumerate(test_files):
    print("TEST no.", i + 1)
    data = open('tests/lexer/' + test, 'r').read()
    lexer.input(data)
    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: 
            break      # No more input
        print(tok)