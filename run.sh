uname="$(uname -s)"
if [ $uname == "MINGW64_NT-10.0-22000" ]; then
    py compiler/parser_tests.py $1
    py virtual_machine/virtual_machine.py
else
    python3 compiler/parser_tests.py $1
    python3 virtual_machine/virtual_machine.py
fi