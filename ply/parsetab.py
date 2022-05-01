
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'AND ASSIGN AT_CLASS BOOL BOOL_VALUE CLASS CLOSE_BRACKET CLOSE_KEY CLOSE_PARENTHESIS COMMA CONSTRUCTOR DIVISION DOT ELSE EQUAL_TO FLOAT FLOAT_VALUE FOR FUNCTION GREATER_THAN GROUP ID IF IN INT INT_VALUE IS LESS_THAN MAIN MINUS MULTIPLICATION NOT_EQUAL_TO OBJ OPEN_BRACKET OPEN_KEY OPEN_PARENTHESIS OR PLUS PROGRAM READ RETURN RETURNS SEMICOLON STRING STRING_VALUE VAR VOID WHILE WRITE\n    program : PROGRAM np_start_func_dir ID SEMICOLON declaration_loop main_function\n    \n    main_function : MAIN OPEN_PARENTHESIS CLOSE_PARENTHESIS OPEN_KEY variable_declaration_loop statement_loop CLOSE_KEY\n    \n    np_start_func_dir : epsilon\n    \n    declaration_loop : declaration declaration_loop\n                     | epsilon\n    \n    statement_loop  : statement statement_loop1\n    \n    statement_loop1 : statement statement_loop1\n                    | epsilon\n    \n    declaration : class_declaration\n                | variable_declaration\n                | function_declaration\n    \n    variable    : ID variable1\n    \n    variable1   : OPEN_BRACKET hyper_exp CLOSE_BRACKET\n                | DOT ID\n                | epsilon\n\n    \n    class_declaration   : CLASS ID class_declaration1 OPEN_KEY class_body CLOSE_KEY SEMICOLON constructor class_declaration2\n    \n    class_declaration1  : IS ID\n                        | epsilon\n    \n    class_declaration2  : class_function class_declaration2\n                        | epsilon\n    \n    class_body  : class_body1 class_body3\n    \n    class_body1 : variable_declaration class_body2\n    \n    class_body2 : variable_declaration class_body2\n                | epsilon\n    \n    class_body3 : class_function_declaration class_body4\n    \n    class_body4 : class_function_declaration class_body4\n                | epsilon\n\n    \n    constructor : CONSTRUCTOR ID OPEN_PARENTHESIS parameter CLOSE_PARENTHESIS OPEN_KEY statement_loop CLOSE_KEY\n    \n    variable_declaration_loop : variable_declaration variable_declaration_loop\n                                | epsilon\n    \n    variable_declaration    : VAR data_type ID SEMICOLON\n                            | GROUP ID ASSIGN data_type OPEN_BRACKET INT_VALUE CLOSE_BRACKET SEMICOLON\n                            | OBJ ID ASSIGN ID OPEN_PARENTHESIS variable_declaration1 CLOSE_PARENTHESIS SEMICOLON\n\n    \n    atomic_var_type    : VAR\n                | GROUP\n    \n    variable_declaration1   : hyper_exp_loop\n                            | epsilon\n    \n    statement   : assignment\n                | conditional\n                | cycle\n                | read\n                | write\n                | function_call\n    \n    assignment  : variable ASSIGN hyper_exp SEMICOLON\n    \n    hyper_exp   : super_exp hyper_exp1\n    \n    hyper_exp1  : AND super_exp hyper_exp1\n                | OR super_exp hyper_exp1\n                | epsilon\n    \n    super_exp   : exp super_exp1\n    \n    super_exp1  : GREATER_THAN exp super_exp1\n                | LESS_THAN exp super_exp1\n                | EQUAL_TO exp super_exp1\n                | NOT_EQUAL_TO exp super_exp1\n                | epsilon\n    \n    exp : term exp1\n    \n    exp1    : PLUS term exp1\n            | MINUS term exp1\n            | epsilon\n    \n    term    : factor term1\n    \n    term1   : MULTIPLICATION factor term1\n            | DIVISION factor term1\n            | epsilon\n    \n    factor  : function_call\n            | FLOAT_VALUE\n            | INT_VALUE\n            | BOOL_VALUE\n            | STRING_VALUE\n            | variable\n            | OPEN_PARENTHESIS hyper_exp CLOSE_PARENTHESIS\n    \n    data_type   : INT\n                | FLOAT\n                | STRING\n                | BOOL\n    \n    class_function_declaration : FUNCTION ID OPEN_PARENTHESIS parameter CLOSE_PARENTHESIS RETURNS return_arg SEMICOLON\n    \n    return_arg  : data_type\n                | VOID\n    \n    parameter   : atomic_var_type data_type ID parameter1\n                | OBJ ID ID parameter1\n                | epsilon\n    \n    parameter1  : COMMA atomic_var_type data_type ID parameter1\n                | COMMA OBJ ID ID parameter1\n                | epsilon\n    \n    conditional : IF OPEN_PARENTHESIS hyper_exp CLOSE_PARENTHESIS OPEN_KEY statement_loop CLOSE_KEY conditional1\n    \n    conditional1    : ELSE OPEN_KEY statement_loop CLOSE_KEY\n                    | epsilon\n    \n    cycle   : FOR OPEN_PARENTHESIS ID IN ID CLOSE_PARENTHESIS cycle1\n            | WHILE OPEN_PARENTHESIS hyper_exp CLOSE_PARENTHESIS cycle1\n    \n    cycle1  : OPEN_KEY statement_loop CLOSE_KEY\n    \n    read    : READ OPEN_PARENTHESIS variable_loop CLOSE_PARENTHESIS SEMICOLON\n    \n    variable_loop   : variable variable_loop1\n    \n    variable_loop1  : COMMA variable variable_loop1\n                    | epsilon\n    \n    write   : WRITE OPEN_PARENTHESIS hyper_exp_loop CLOSE_PARENTHESIS SEMICOLON\n    \n    hyper_exp_loop  : hyper_exp hyper_exp_loop1\n    \n    hyper_exp_loop1 : COMMA hyper_exp hyper_exp_loop1\n                    | epsilon\n\n    \n    function_call   : ID function_call1 OPEN_PARENTHESIS function_call2 CLOSE_PARENTHESIS SEMICOLON\n    \n    function_call1  : DOT ID\n                    | epsilon\n    \n    function_call2  : hyper_exp_loop\n                    | epsilon\n    \n    class_function  : AT_CLASS ID FUNCTION ID OPEN_PARENTHESIS parameter CLOSE_PARENTHESIS RETURNS return_arg OPEN_KEY function_statement_loop function_return CLOSE_KEY\n\n    \n    function_declaration    : FUNCTION ID OPEN_PARENTHESIS parameter CLOSE_PARENTHESIS RETURNS return_arg OPEN_KEY variable_declaration_loop function_statement_loop function_return CLOSE_KEY\n    \n    function_return : RETURN hyper_exp SEMICOLON\n                    | epsilon\n    \n    function_statement_loop  : statement_loop\n                    | epsilon\n    epsilon :'
    
_lr_action_items = {'PROGRAM':([0,],[2,]),'$end':([1,18,146,],[0,-1,-2,]),'ID':([2,3,4,13,15,16,17,22,23,24,25,26,32,36,41,46,50,55,57,58,59,60,61,65,71,90,91,92,93,94,95,96,103,113,115,119,122,123,126,127,128,129,132,133,136,137,147,150,151,152,153,154,155,157,160,161,165,177,179,192,210,211,212,213,215,219,221,234,236,237,238,241,242,245,247,260,261,262,264,267,269,272,277,279,],[-108,5,-3,21,27,28,29,34,-70,-71,-72,-73,40,43,-31,58,-108,70,87,88,70,-108,-30,108,70,70,-38,-39,-40,-41,-42,-43,-29,162,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,183,70,187,70,193,-32,70,-33,-108,212,225,70,232,233,-44,235,187,240,70,-87,70,-89,-93,255,-97,70,-108,-86,-88,70,-83,-85,70,-84,70,]),'SEMICOLON':([5,23,24,25,26,34,62,70,76,77,78,79,80,81,82,83,84,85,110,112,114,117,121,124,125,130,131,134,135,138,140,141,162,164,167,168,169,170,171,172,173,174,175,176,181,198,200,201,202,203,204,205,206,207,208,209,217,223,228,245,257,259,],[6,-70,-71,-72,-73,41,104,-108,-108,-108,-108,-108,-63,-64,-65,-66,-67,-68,160,-12,-15,165,-45,-48,-49,-54,-55,-58,-59,-62,-75,-76,-14,-69,-108,-108,-108,-108,-108,-108,-108,-108,-108,-108,213,-13,-46,-47,-50,-51,-52,-53,-56,-57,-60,-61,238,241,245,-97,265,266,]),'MAIN':([6,7,8,9,10,11,12,20,41,156,160,165,189,190,191,224,258,274,282,],[-108,19,-108,-5,-9,-10,-11,-4,-31,-108,-32,-33,-16,-108,-20,-19,-103,-28,-102,]),'CLASS':([6,8,10,11,12,41,156,160,165,189,190,191,224,258,274,282,],[13,13,-9,-10,-11,-31,-108,-32,-33,-16,-108,-20,-19,-103,-28,-102,]),'VAR':([6,8,10,11,12,37,39,41,50,53,60,66,143,156,159,160,165,177,189,190,191,224,226,258,263,274,282,],[14,14,-9,-10,-11,48,14,-31,14,14,14,14,48,-108,48,-32,-33,14,-16,-108,-20,-19,48,-103,48,-28,-102,]),'GROUP':([6,8,10,11,12,37,39,41,50,53,60,66,143,156,159,160,165,177,189,190,191,224,226,258,263,274,282,],[15,15,-9,-10,-11,49,15,-31,15,15,15,15,49,-108,49,-32,-33,15,-16,-108,-20,-19,49,-103,49,-28,-102,]),'OBJ':([6,8,10,11,12,37,39,41,50,53,60,66,143,156,159,160,165,177,189,190,191,224,226,258,263,274,282,],[16,16,-9,-10,-11,46,16,-31,16,16,16,16,179,-108,46,-32,-33,16,-16,-108,-20,-19,46,-103,46,-28,-102,]),'FUNCTION':([6,8,10,11,12,41,52,53,64,66,67,68,105,109,156,160,165,189,190,191,224,225,258,265,274,282,],[17,17,-9,-10,-11,-31,65,-108,65,-108,-22,-24,65,-23,-108,-32,-33,-16,-108,-20,-19,242,-103,-74,-28,-102,]),'INT':([14,35,45,48,49,86,178,244,276,],[23,23,23,-34,-35,23,23,23,23,]),'FLOAT':([14,35,45,48,49,86,178,244,276,],[24,24,24,-34,-35,24,24,24,24,]),'STRING':([14,35,45,48,49,86,178,244,276,],[25,25,25,-34,-35,25,25,25,25,]),'BOOL':([14,35,45,48,49,86,178,244,276,],[26,26,26,-34,-35,26,26,26,26,]),'OPEN_PARENTHESIS':([19,29,43,55,70,71,98,99,100,101,102,108,111,114,115,119,122,123,126,127,128,129,132,133,136,137,150,151,153,155,161,162,193,247,255,],[30,37,55,71,-108,71,151,152,153,154,155,159,161,-99,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,-98,226,71,263,]),'IS':([21,],[32,]),'OPEN_KEY':([21,23,24,25,26,31,33,38,40,139,140,141,214,216,252,256,268,278,],[-108,-70,-71,-72,-73,39,-18,50,-17,177,-75,-76,234,237,237,264,272,279,]),'OPEN_BRACKET':([23,24,25,26,42,70,187,],[-70,-71,-72,-73,54,115,115,]),'ASSIGN':([27,28,70,97,112,114,162,198,],[35,36,-108,150,-12,-15,-14,-13,]),'CLOSE_PARENTHESIS':([30,37,44,47,55,70,72,73,74,75,76,77,78,79,80,81,82,83,84,85,87,88,112,114,116,118,120,121,124,125,130,131,134,135,138,142,144,145,159,161,162,164,166,167,168,169,170,171,172,173,174,175,176,182,184,185,186,187,188,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,218,220,222,226,232,233,235,239,240,243,245,249,250,254,263,270,],[38,-108,56,-79,-108,-108,117,-36,-37,-108,-108,-108,-108,-108,-63,-64,-65,-66,-67,-68,-108,-108,-12,-15,164,-94,-96,-45,-48,-49,-54,-55,-58,-59,-62,-77,-82,-78,-108,-108,-14,-69,-108,-108,-108,-108,-108,-108,-108,-108,-108,-108,-108,214,216,217,-108,-108,223,227,228,-100,-101,-13,-95,-46,-47,-50,-51,-52,-53,-56,-57,-60,-61,-90,-92,-15,-108,-108,-108,252,-108,-14,256,-97,-80,-81,-91,-108,273,]),'IF':([41,50,59,60,61,90,91,92,93,94,95,96,103,147,160,165,177,210,213,234,236,237,238,241,245,260,261,262,264,267,269,272,277,279,],[-31,-108,98,-108,-30,98,-38,-39,-40,-41,-42,-43,-29,98,-32,-33,-108,98,-44,98,-87,98,-89,-93,-97,-108,-86,-88,98,-83,-85,98,-84,98,]),'FOR':([41,50,59,60,61,90,91,92,93,94,95,96,103,147,160,165,177,210,213,234,236,237,238,241,245,260,261,262,264,267,269,272,277,279,],[-31,-108,99,-108,-30,99,-38,-39,-40,-41,-42,-43,-29,99,-32,-33,-108,99,-44,99,-87,99,-89,-93,-97,-108,-86,-88,99,-83,-85,99,-84,99,]),'WHILE':([41,50,59,60,61,90,91,92,93,94,95,96,103,147,160,165,177,210,213,234,236,237,238,241,245,260,261,262,264,267,269,272,277,279,],[-31,-108,100,-108,-30,100,-38,-39,-40,-41,-42,-43,-29,100,-32,-33,-108,100,-44,100,-87,100,-89,-93,-97,-108,-86,-88,100,-83,-85,100,-84,100,]),'READ':([41,50,59,60,61,90,91,92,93,94,95,96,103,147,160,165,177,210,213,234,236,237,238,241,245,260,261,262,264,267,269,272,277,279,],[-31,-108,101,-108,-30,101,-38,-39,-40,-41,-42,-43,-29,101,-32,-33,-108,101,-44,101,-87,101,-89,-93,-97,-108,-86,-88,101,-83,-85,101,-84,101,]),'WRITE':([41,50,59,60,61,90,91,92,93,94,95,96,103,147,160,165,177,210,213,234,236,237,238,241,245,260,261,262,264,267,269,272,277,279,],[-31,-108,102,-108,-30,102,-38,-39,-40,-41,-42,-43,-29,102,-32,-33,-108,102,-44,102,-87,102,-89,-93,-97,-108,-86,-88,102,-83,-85,102,-84,102,]),'RETURN':([41,60,61,90,91,92,93,94,95,96,103,147,148,149,160,165,177,180,210,213,229,230,231,236,238,241,245,260,261,262,267,269,277,279,280,],[-31,-108,-30,-108,-38,-39,-40,-41,-42,-43,-29,-108,-6,-8,-32,-33,-108,-7,-108,-44,247,-106,-107,-87,-89,-93,-97,-108,-86,-88,-83,-85,-84,-108,247,]),'CLOSE_KEY':([41,51,60,61,63,64,89,90,91,92,93,94,95,96,103,105,106,107,147,148,149,158,160,165,177,180,210,213,229,230,231,236,238,241,245,246,248,251,253,260,261,262,265,266,267,269,271,275,277,279,280,281,],[-31,62,-108,-30,-21,-108,146,-108,-38,-39,-40,-41,-42,-43,-29,-108,-25,-27,-108,-6,-8,-26,-32,-33,-108,-7,-108,-44,-108,-106,-107,-87,-89,-93,-97,258,-105,260,262,-108,-86,-88,-74,-104,-83,-85,274,277,-84,-108,-108,282,]),'INT_VALUE':([54,55,71,115,119,122,123,126,127,128,129,132,133,136,137,150,151,153,155,161,247,],[69,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,]),'FLOAT_VALUE':([55,71,115,119,122,123,126,127,128,129,132,133,136,137,150,151,153,155,161,247,],[81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,81,]),'BOOL_VALUE':([55,71,115,119,122,123,126,127,128,129,132,133,136,137,150,151,153,155,161,247,],[83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,83,]),'STRING_VALUE':([55,71,115,119,122,123,126,127,128,129,132,133,136,137,150,151,153,155,161,247,],[84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,84,]),'RETURNS':([56,227,273,],[86,244,276,]),'CLOSE_BRACKET':([69,70,76,77,78,79,80,81,82,83,84,85,112,114,121,124,125,130,131,134,135,138,162,163,164,167,168,169,170,171,172,173,174,175,176,198,200,201,202,203,204,205,206,207,208,209,245,],[110,-108,-108,-108,-108,-108,-63,-64,-65,-66,-67,-68,-12,-15,-45,-48,-49,-54,-55,-58,-59,-62,-14,198,-69,-108,-108,-108,-108,-108,-108,-108,-108,-108,-108,-13,-46,-47,-50,-51,-52,-53,-56,-57,-60,-61,-97,]),'DOT':([70,187,],[113,221,]),'MULTIPLICATION':([70,79,80,81,82,83,84,85,112,114,162,164,175,176,198,245,],[-108,136,-63,-64,-65,-66,-67,-68,-12,-15,-14,-69,136,136,-13,-97,]),'DIVISION':([70,79,80,81,82,83,84,85,112,114,162,164,175,176,198,245,],[-108,137,-63,-64,-65,-66,-67,-68,-12,-15,-14,-69,137,137,-13,-97,]),'PLUS':([70,78,79,80,81,82,83,84,85,112,114,135,138,162,164,173,174,175,176,198,208,209,245,],[-108,132,-108,-63,-64,-65,-66,-67,-68,-12,-15,-59,-62,-14,-69,132,132,-108,-108,-13,-60,-61,-97,]),'MINUS':([70,78,79,80,81,82,83,84,85,112,114,135,138,162,164,173,174,175,176,198,208,209,245,],[-108,133,-108,-63,-64,-65,-66,-67,-68,-12,-15,-59,-62,-14,-69,133,133,-108,-108,-13,-60,-61,-97,]),'GREATER_THAN':([70,77,78,79,80,81,82,83,84,85,112,114,131,134,135,138,162,164,169,170,171,172,173,174,175,176,198,206,207,208,209,245,],[-108,126,-108,-108,-63,-64,-65,-66,-67,-68,-12,-15,-55,-58,-59,-62,-14,-69,126,126,126,126,-108,-108,-108,-108,-13,-56,-57,-60,-61,-97,]),'LESS_THAN':([70,77,78,79,80,81,82,83,84,85,112,114,131,134,135,138,162,164,169,170,171,172,173,174,175,176,198,206,207,208,209,245,],[-108,127,-108,-108,-63,-64,-65,-66,-67,-68,-12,-15,-55,-58,-59,-62,-14,-69,127,127,127,127,-108,-108,-108,-108,-13,-56,-57,-60,-61,-97,]),'EQUAL_TO':([70,77,78,79,80,81,82,83,84,85,112,114,131,134,135,138,162,164,169,170,171,172,173,174,175,176,198,206,207,208,209,245,],[-108,128,-108,-108,-63,-64,-65,-66,-67,-68,-12,-15,-55,-58,-59,-62,-14,-69,128,128,128,128,-108,-108,-108,-108,-13,-56,-57,-60,-61,-97,]),'NOT_EQUAL_TO':([70,77,78,79,80,81,82,83,84,85,112,114,131,134,135,138,162,164,169,170,171,172,173,174,175,176,198,206,207,208,209,245,],[-108,129,-108,-108,-63,-64,-65,-66,-67,-68,-12,-15,-55,-58,-59,-62,-14,-69,129,129,129,129,-108,-108,-108,-108,-13,-56,-57,-60,-61,-97,]),'AND':([70,76,77,78,79,80,81,82,83,84,85,112,114,125,130,131,134,135,138,162,164,167,168,169,170,171,172,173,174,175,176,198,202,203,204,205,206,207,208,209,245,],[-108,122,-108,-108,-108,-63,-64,-65,-66,-67,-68,-12,-15,-49,-54,-55,-58,-59,-62,-14,-69,122,122,-108,-108,-108,-108,-108,-108,-108,-108,-13,-50,-51,-52,-53,-56,-57,-60,-61,-97,]),'OR':([70,76,77,78,79,80,81,82,83,84,85,112,114,125,130,131,134,135,138,162,164,167,168,169,170,171,172,173,174,175,176,198,202,203,204,205,206,207,208,209,245,],[-108,123,-108,-108,-108,-63,-64,-65,-66,-67,-68,-12,-15,-49,-54,-55,-58,-59,-62,-14,-69,123,123,-108,-108,-108,-108,-108,-108,-108,-108,-13,-50,-51,-52,-53,-56,-57,-60,-61,-97,]),'COMMA':([70,75,76,77,78,79,80,81,82,83,84,85,87,88,112,114,121,124,125,130,131,134,135,138,162,164,166,167,168,169,170,171,172,173,174,175,176,186,187,198,200,201,202,203,204,205,206,207,208,209,222,232,233,239,240,245,],[-108,119,-108,-108,-108,-108,-63,-64,-65,-66,-67,-68,143,143,-12,-15,-45,-48,-49,-54,-55,-58,-59,-62,-14,-69,119,-108,-108,-108,-108,-108,-108,-108,-108,-108,-108,219,-108,-13,-46,-47,-50,-51,-52,-53,-56,-57,-60,-61,-15,143,143,219,-14,-97,]),'VOID':([86,244,276,],[141,141,141,]),'CONSTRUCTOR':([104,],[157,]),'AT_CLASS':([156,190,274,282,],[192,192,-28,-102,]),'IN':([183,],[215,]),'ELSE':([260,],[268,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'np_start_func_dir':([2,],[3,]),'epsilon':([2,6,8,21,37,50,53,55,60,64,66,70,75,76,77,78,79,87,88,90,105,147,156,159,161,166,167,168,169,170,171,172,173,174,175,176,177,186,187,190,210,226,229,232,233,239,260,263,279,280,],[4,9,9,33,47,61,68,74,61,107,68,114,120,124,130,134,138,144,144,149,107,149,191,47,197,120,124,124,130,130,130,130,134,134,138,138,61,220,222,191,231,47,248,144,144,220,269,47,231,248,]),'declaration_loop':([6,8,],[7,20,]),'declaration':([6,8,],[8,8,]),'class_declaration':([6,8,],[10,10,]),'variable_declaration':([6,8,39,50,53,60,66,177,],[11,11,53,60,66,60,66,60,]),'function_declaration':([6,8,],[12,12,]),'main_function':([7,],[18,]),'data_type':([14,35,45,86,178,244,276,],[22,42,57,140,211,140,140,]),'class_declaration1':([21,],[31,]),'parameter':([37,159,226,263,],[44,194,243,270,]),'atomic_var_type':([37,143,159,226,263,],[45,178,45,45,45,]),'class_body':([39,],[51,]),'class_body1':([39,],[52,]),'variable_declaration_loop':([50,60,177,],[59,103,210,]),'class_body3':([52,],[63,]),'class_function_declaration':([52,64,105,],[64,105,105,]),'class_body2':([53,66,],[67,109,]),'variable_declaration1':([55,],[72,]),'hyper_exp_loop':([55,155,161,],[73,188,196,]),'hyper_exp':([55,71,115,119,150,151,153,155,161,247,],[75,116,163,166,181,182,184,75,75,259,]),'super_exp':([55,71,115,119,122,123,150,151,153,155,161,247,],[76,76,76,76,167,168,76,76,76,76,76,76,]),'exp':([55,71,115,119,122,123,126,127,128,129,150,151,153,155,161,247,],[77,77,77,77,77,77,169,170,171,172,77,77,77,77,77,77,]),'term':([55,71,115,119,122,123,126,127,128,129,132,133,150,151,153,155,161,247,],[78,78,78,78,78,78,78,78,78,78,173,174,78,78,78,78,78,78,]),'factor':([55,71,115,119,122,123,126,127,128,129,132,133,136,137,150,151,153,155,161,247,],[79,79,79,79,79,79,79,79,79,79,79,79,175,176,79,79,79,79,79,79,]),'function_call':([55,59,71,90,115,119,122,123,126,127,128,129,132,133,136,137,147,150,151,153,155,161,210,234,237,247,264,272,279,],[80,96,80,96,80,80,80,80,80,80,80,80,80,80,80,80,96,80,80,80,80,80,96,96,96,80,96,96,96,]),'variable':([55,59,71,90,115,119,122,123,126,127,128,129,132,133,136,137,147,150,151,153,154,155,161,210,219,234,237,247,264,272,279,],[85,97,85,97,85,85,85,85,85,85,85,85,85,85,85,85,97,85,85,85,186,85,85,97,239,97,97,85,97,97,97,]),'statement_loop':([59,210,234,237,264,272,279,],[89,230,251,253,271,275,230,]),'statement':([59,90,147,210,234,237,264,272,279,],[90,147,147,90,90,90,90,90,90,]),'assignment':([59,90,147,210,234,237,264,272,279,],[91,91,91,91,91,91,91,91,91,]),'conditional':([59,90,147,210,234,237,264,272,279,],[92,92,92,92,92,92,92,92,92,]),'cycle':([59,90,147,210,234,237,264,272,279,],[93,93,93,93,93,93,93,93,93,]),'read':([59,90,147,210,234,237,264,272,279,],[94,94,94,94,94,94,94,94,94,]),'write':([59,90,147,210,234,237,264,272,279,],[95,95,95,95,95,95,95,95,95,]),'class_body4':([64,105,],[106,158,]),'function_call1':([70,],[111,]),'variable1':([70,187,],[112,112,]),'hyper_exp_loop1':([75,166,],[118,199,]),'hyper_exp1':([76,167,168,],[121,200,201,]),'super_exp1':([77,169,170,171,172,],[125,202,203,204,205,]),'exp1':([78,173,174,],[131,206,207,]),'term1':([79,175,176,],[135,208,209,]),'return_arg':([86,244,276,],[139,257,278,]),'parameter1':([87,88,232,233,],[142,145,249,250,]),'statement_loop1':([90,147,],[148,180,]),'constructor':([104,],[156,]),'variable_loop':([154,],[185,]),'class_declaration2':([156,190,],[189,224,]),'class_function':([156,190,],[190,190,]),'function_call2':([161,],[195,]),'variable_loop1':([186,239,],[218,254,]),'function_statement_loop':([210,279,],[229,280,]),'cycle1':([216,252,],[236,261,]),'function_return':([229,280,],[246,281,]),'conditional1':([260,],[267,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> PROGRAM np_start_func_dir ID SEMICOLON declaration_loop main_function','program',6,'p_program','pecan_parser.py',26),
  ('main_function -> MAIN OPEN_PARENTHESIS CLOSE_PARENTHESIS OPEN_KEY variable_declaration_loop statement_loop CLOSE_KEY','main_function',7,'p_main_function','pecan_parser.py',34),
  ('np_start_func_dir -> epsilon','np_start_func_dir',1,'p_np_start_func_dir','pecan_parser.py',42),
  ('declaration_loop -> declaration declaration_loop','declaration_loop',2,'p_declaration_loop','pecan_parser.py',50),
  ('declaration_loop -> epsilon','declaration_loop',1,'p_declaration_loop','pecan_parser.py',51),
  ('statement_loop -> statement statement_loop1','statement_loop',2,'p_statement_loop','pecan_parser.py',62),
  ('statement_loop1 -> statement statement_loop1','statement_loop1',2,'p_statement_loop1','pecan_parser.py',69),
  ('statement_loop1 -> epsilon','statement_loop1',1,'p_statement_loop1','pecan_parser.py',70),
  ('declaration -> class_declaration','declaration',1,'p_declaration','pecan_parser.py',80),
  ('declaration -> variable_declaration','declaration',1,'p_declaration','pecan_parser.py',81),
  ('declaration -> function_declaration','declaration',1,'p_declaration','pecan_parser.py',82),
  ('variable -> ID variable1','variable',2,'p_variable','pecan_parser.py',90),
  ('variable1 -> OPEN_BRACKET hyper_exp CLOSE_BRACKET','variable1',3,'p_variable1','pecan_parser.py',97),
  ('variable1 -> DOT ID','variable1',2,'p_variable1','pecan_parser.py',98),
  ('variable1 -> epsilon','variable1',1,'p_variable1','pecan_parser.py',99),
  ('class_declaration -> CLASS ID class_declaration1 OPEN_KEY class_body CLOSE_KEY SEMICOLON constructor class_declaration2','class_declaration',9,'p_class_declaration','pecan_parser.py',107),
  ('class_declaration1 -> IS ID','class_declaration1',2,'p_class_declaration1','pecan_parser.py',114),
  ('class_declaration1 -> epsilon','class_declaration1',1,'p_class_declaration1','pecan_parser.py',115),
  ('class_declaration2 -> class_function class_declaration2','class_declaration2',2,'p_class_declaration2','pecan_parser.py',122),
  ('class_declaration2 -> epsilon','class_declaration2',1,'p_class_declaration2','pecan_parser.py',123),
  ('class_body -> class_body1 class_body3','class_body',2,'p_class_body','pecan_parser.py',130),
  ('class_body1 -> variable_declaration class_body2','class_body1',2,'p_class_body1','pecan_parser.py',137),
  ('class_body2 -> variable_declaration class_body2','class_body2',2,'p_class_body2','pecan_parser.py',144),
  ('class_body2 -> epsilon','class_body2',1,'p_class_body2','pecan_parser.py',145),
  ('class_body3 -> class_function_declaration class_body4','class_body3',2,'p_class_body3','pecan_parser.py',152),
  ('class_body4 -> class_function_declaration class_body4','class_body4',2,'p_class_body4','pecan_parser.py',159),
  ('class_body4 -> epsilon','class_body4',1,'p_class_body4','pecan_parser.py',160),
  ('constructor -> CONSTRUCTOR ID OPEN_PARENTHESIS parameter CLOSE_PARENTHESIS OPEN_KEY statement_loop CLOSE_KEY','constructor',8,'p_constructor','pecan_parser.py',168),
  ('variable_declaration_loop -> variable_declaration variable_declaration_loop','variable_declaration_loop',2,'p_variable_declaration_loop','pecan_parser.py',175),
  ('variable_declaration_loop -> epsilon','variable_declaration_loop',1,'p_variable_declaration_loop','pecan_parser.py',176),
  ('variable_declaration -> VAR data_type ID SEMICOLON','variable_declaration',4,'p_variable_declaration','pecan_parser.py',186),
  ('variable_declaration -> GROUP ID ASSIGN data_type OPEN_BRACKET INT_VALUE CLOSE_BRACKET SEMICOLON','variable_declaration',8,'p_variable_declaration','pecan_parser.py',187),
  ('variable_declaration -> OBJ ID ASSIGN ID OPEN_PARENTHESIS variable_declaration1 CLOSE_PARENTHESIS SEMICOLON','variable_declaration',8,'p_variable_declaration','pecan_parser.py',188),
  ('atomic_var_type -> VAR','atomic_var_type',1,'p_atomic_var_type','pecan_parser.py',201),
  ('atomic_var_type -> GROUP','atomic_var_type',1,'p_atomic_var_type','pecan_parser.py',202),
  ('variable_declaration1 -> hyper_exp_loop','variable_declaration1',1,'p_variable_declaration1','pecan_parser.py',208),
  ('variable_declaration1 -> epsilon','variable_declaration1',1,'p_variable_declaration1','pecan_parser.py',209),
  ('statement -> assignment','statement',1,'p_statement','pecan_parser.py',215),
  ('statement -> conditional','statement',1,'p_statement','pecan_parser.py',216),
  ('statement -> cycle','statement',1,'p_statement','pecan_parser.py',217),
  ('statement -> read','statement',1,'p_statement','pecan_parser.py',218),
  ('statement -> write','statement',1,'p_statement','pecan_parser.py',219),
  ('statement -> function_call','statement',1,'p_statement','pecan_parser.py',220),
  ('assignment -> variable ASSIGN hyper_exp SEMICOLON','assignment',4,'p_assignment','pecan_parser.py',228),
  ('hyper_exp -> super_exp hyper_exp1','hyper_exp',2,'p_hyper_exp','pecan_parser.py',235),
  ('hyper_exp1 -> AND super_exp hyper_exp1','hyper_exp1',3,'p_hyper_exp1','pecan_parser.py',242),
  ('hyper_exp1 -> OR super_exp hyper_exp1','hyper_exp1',3,'p_hyper_exp1','pecan_parser.py',243),
  ('hyper_exp1 -> epsilon','hyper_exp1',1,'p_hyper_exp1','pecan_parser.py',244),
  ('super_exp -> exp super_exp1','super_exp',2,'p_super_exp','pecan_parser.py',251),
  ('super_exp1 -> GREATER_THAN exp super_exp1','super_exp1',3,'p_super_exp1','pecan_parser.py',258),
  ('super_exp1 -> LESS_THAN exp super_exp1','super_exp1',3,'p_super_exp1','pecan_parser.py',259),
  ('super_exp1 -> EQUAL_TO exp super_exp1','super_exp1',3,'p_super_exp1','pecan_parser.py',260),
  ('super_exp1 -> NOT_EQUAL_TO exp super_exp1','super_exp1',3,'p_super_exp1','pecan_parser.py',261),
  ('super_exp1 -> epsilon','super_exp1',1,'p_super_exp1','pecan_parser.py',262),
  ('exp -> term exp1','exp',2,'p_exp','pecan_parser.py',269),
  ('exp1 -> PLUS term exp1','exp1',3,'p_exp1','pecan_parser.py',276),
  ('exp1 -> MINUS term exp1','exp1',3,'p_exp1','pecan_parser.py',277),
  ('exp1 -> epsilon','exp1',1,'p_exp1','pecan_parser.py',278),
  ('term -> factor term1','term',2,'p_term','pecan_parser.py',285),
  ('term1 -> MULTIPLICATION factor term1','term1',3,'p_term1','pecan_parser.py',292),
  ('term1 -> DIVISION factor term1','term1',3,'p_term1','pecan_parser.py',293),
  ('term1 -> epsilon','term1',1,'p_term1','pecan_parser.py',294),
  ('factor -> function_call','factor',1,'p_factor','pecan_parser.py',301),
  ('factor -> FLOAT_VALUE','factor',1,'p_factor','pecan_parser.py',302),
  ('factor -> INT_VALUE','factor',1,'p_factor','pecan_parser.py',303),
  ('factor -> BOOL_VALUE','factor',1,'p_factor','pecan_parser.py',304),
  ('factor -> STRING_VALUE','factor',1,'p_factor','pecan_parser.py',305),
  ('factor -> variable','factor',1,'p_factor','pecan_parser.py',306),
  ('factor -> OPEN_PARENTHESIS hyper_exp CLOSE_PARENTHESIS','factor',3,'p_factor','pecan_parser.py',307),
  ('data_type -> INT','data_type',1,'p_data_type','pecan_parser.py',314),
  ('data_type -> FLOAT','data_type',1,'p_data_type','pecan_parser.py',315),
  ('data_type -> STRING','data_type',1,'p_data_type','pecan_parser.py',316),
  ('data_type -> BOOL','data_type',1,'p_data_type','pecan_parser.py',317),
  ('class_function_declaration -> FUNCTION ID OPEN_PARENTHESIS parameter CLOSE_PARENTHESIS RETURNS return_arg SEMICOLON','class_function_declaration',8,'p_class_function_declaration','pecan_parser.py',324),
  ('return_arg -> data_type','return_arg',1,'p_return_arg','pecan_parser.py',331),
  ('return_arg -> VOID','return_arg',1,'p_return_arg','pecan_parser.py',332),
  ('parameter -> atomic_var_type data_type ID parameter1','parameter',4,'p_parameter','pecan_parser.py',339),
  ('parameter -> OBJ ID ID parameter1','parameter',4,'p_parameter','pecan_parser.py',340),
  ('parameter -> epsilon','parameter',1,'p_parameter','pecan_parser.py',341),
  ('parameter1 -> COMMA atomic_var_type data_type ID parameter1','parameter1',5,'p_parameter1','pecan_parser.py',351),
  ('parameter1 -> COMMA OBJ ID ID parameter1','parameter1',5,'p_parameter1','pecan_parser.py',352),
  ('parameter1 -> epsilon','parameter1',1,'p_parameter1','pecan_parser.py',353),
  ('conditional -> IF OPEN_PARENTHESIS hyper_exp CLOSE_PARENTHESIS OPEN_KEY statement_loop CLOSE_KEY conditional1','conditional',8,'p_conditional','pecan_parser.py',363),
  ('conditional1 -> ELSE OPEN_KEY statement_loop CLOSE_KEY','conditional1',4,'p_conditional1','pecan_parser.py',370),
  ('conditional1 -> epsilon','conditional1',1,'p_conditional1','pecan_parser.py',371),
  ('cycle -> FOR OPEN_PARENTHESIS ID IN ID CLOSE_PARENTHESIS cycle1','cycle',7,'p_cycle','pecan_parser.py',378),
  ('cycle -> WHILE OPEN_PARENTHESIS hyper_exp CLOSE_PARENTHESIS cycle1','cycle',5,'p_cycle','pecan_parser.py',379),
  ('cycle1 -> OPEN_KEY statement_loop CLOSE_KEY','cycle1',3,'p_cycle1','pecan_parser.py',386),
  ('read -> READ OPEN_PARENTHESIS variable_loop CLOSE_PARENTHESIS SEMICOLON','read',5,'p_read','pecan_parser.py',393),
  ('variable_loop -> variable variable_loop1','variable_loop',2,'p_variable_loop','pecan_parser.py',400),
  ('variable_loop1 -> COMMA variable variable_loop1','variable_loop1',3,'p_variable_loop1','pecan_parser.py',407),
  ('variable_loop1 -> epsilon','variable_loop1',1,'p_variable_loop1','pecan_parser.py',408),
  ('write -> WRITE OPEN_PARENTHESIS hyper_exp_loop CLOSE_PARENTHESIS SEMICOLON','write',5,'p_write','pecan_parser.py',415),
  ('hyper_exp_loop -> hyper_exp hyper_exp_loop1','hyper_exp_loop',2,'p_hyper_exp_loop','pecan_parser.py',422),
  ('hyper_exp_loop1 -> COMMA hyper_exp hyper_exp_loop1','hyper_exp_loop1',3,'p_hyper_exp_loop1','pecan_parser.py',429),
  ('hyper_exp_loop1 -> epsilon','hyper_exp_loop1',1,'p_hyper_exp_loop1','pecan_parser.py',430),
  ('function_call -> ID function_call1 OPEN_PARENTHESIS function_call2 CLOSE_PARENTHESIS SEMICOLON','function_call',6,'p_function_call','pecan_parser.py',438),
  ('function_call1 -> DOT ID','function_call1',2,'p_function_call1','pecan_parser.py',445),
  ('function_call1 -> epsilon','function_call1',1,'p_function_call1','pecan_parser.py',446),
  ('function_call2 -> hyper_exp_loop','function_call2',1,'p_function_call2','pecan_parser.py',453),
  ('function_call2 -> epsilon','function_call2',1,'p_function_call2','pecan_parser.py',454),
  ('class_function -> AT_CLASS ID FUNCTION ID OPEN_PARENTHESIS parameter CLOSE_PARENTHESIS RETURNS return_arg OPEN_KEY function_statement_loop function_return CLOSE_KEY','class_function',13,'p_class_function','pecan_parser.py',461),
  ('function_declaration -> FUNCTION ID OPEN_PARENTHESIS parameter CLOSE_PARENTHESIS RETURNS return_arg OPEN_KEY variable_declaration_loop function_statement_loop function_return CLOSE_KEY','function_declaration',12,'p_function_declaration','pecan_parser.py',469),
  ('function_return -> RETURN hyper_exp SEMICOLON','function_return',3,'p_function_return','pecan_parser.py',477),
  ('function_return -> epsilon','function_return',1,'p_function_return','pecan_parser.py',478),
  ('function_statement_loop -> statement_loop','function_statement_loop',1,'p_function_statement_loop','pecan_parser.py',485),
  ('function_statement_loop -> epsilon','function_statement_loop',1,'p_function_statement_loop','pecan_parser.py',486),
  ('epsilon -> <empty>','epsilon',0,'p_epsilon','pecan_parser.py',492),
]
