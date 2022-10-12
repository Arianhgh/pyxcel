"""pyxcel is a simple programming language inspired by excel and written in python which enables you to make tables with desired number of cells, edit those cells by putting different values in them, copying, moving, making them be a function of other cells and ...
to code in pyxcel you just have to run the pyxcel.py and start coding in the terminal.
to create a table:
create({table name},{column length},{row length})
to select a table:(you have to always select a table before trying to edit it even if you have only created one table)
context({table name})
to assign a value to a certain cell:
<cell_name> = number or "string"
(cell names can be written in two formats: 1-{Capital chars}{number} example: A1,Z12,AA2
                                           2-[{expression which results in Capital chars}][{expression which results in a number}] example: data = ["AA"+1][3*4] = ["AB"][12])
example: B12 = "some text"
         AC45 = 90
to set a certain cell to be a function of other cells:
setFunc({cell name},{expression}).
example: setFunc(E2,A2+B2) E2 will be evaluated as the sum of the values in A2 and B2
to define a variable:
<var_name> = value or expression
(variable names should start with small characters and the variables themselves can be either integers or strings)
(you can assign a cells value to a variable and vice versa)
to print:
print({expression or value})
examples: print(A12)
          print(var)
          print("Hello" + " Pyxcel")
          print(120)
          print(["A"][var])
to display the table:
display({table name})
pyxcel only supports if conditional statements and while loops
if condition syntax:
if(condition){
    order1
    order2
    …
}
while loop syntax:
while(condition){
    order1
    order2
    …
}
you can also comment anything by putting $ before it."""
import re
n = int(input())
orders = []
active = None
tables = dict()
variables = dict()
for i in range(n):
    orders.append(input())
for i in range(len(orders)):
    orders[i] = re.sub(r"\$.+","", orders[i])
dict1 = {}
dict2 = {}
j = 65
for i in range(26):
    dict1[i] = chr(j)
    dict2[chr(j)] = i + 1
    j += 1
def solve(x,y):
    global active
    a = re.findall(r"[A-Z]+\d+|\[[A-Z0-9a-z+\-*/\"]+]\[[A-Z0-9a-z+\-*/]+]", active.cellsdic[(x,y)])
    for i in a:
        if re.search(r"[A-Z]+\d+",i):
            tmp = re.search(r"([A-Z]+)(\d+)",i)
            if (int(tmp.group(2))-1,wordtonum(tmp.group(1))) in active.cellsdic:
                solve(int(tmp.group(2))-1,wordtonum(tmp.group(1)))
        elif re.search(r"\[[A-Z0-9a-z+\-*/\"]+]\[[A-Z0-9a-z+\-*/]+]",i):
            tmp = re.search(r"(\[[A-Z0-9a-z+\-*/\"]+])(\[[A-Z0-9a-z+\-*/]+])",i)
            if (evalstring3(active.table,variables,tmp.group(2)[1:-1]),evalstring3(active.table,variables,tmp.group(1)[1:-1])[1:-1]) in active.cellsdic:
                solve(evalstring3(active.table,variables,tmp.group(2)[1:-1]),evalstring3(active.table,variables,tmp.group(1)[1:-1])[1:-1])
    active.table[x][y] = evalstring3(active.table, variables, active.cellsdic[(x, y)])
    return
def replacement(string):
    def rep(match:re.Match):
        global active
        x = evalstring3(active.table, variables, match.group(2)[1:-1])[1:-1]
        y = evalstring3(active.table, variables, match.group(3)[1:-1])
        return str(x+y)
    string = re.sub(r"((\[[A-Z0-9a-z+\-*/\"]+])(\[[A-Z0-9a-z+\-*/\"]+]))",rep, string)
    return string
def condition(text,table,variables):
    #print(text,variables)
    results=[]
    sep1 = re.split(r"and|or",text)
    sep1operands = re.findall(r"and|or",text)
    for i in range(len(sep1)):
        sep1[i] = sep1[i].strip()
    for i in sep1:
        sep2 = re.split(r" *>|<|== *",i)
        sep2operands = re.findall(r">|<|==",i)
        if i != "true" and i != "false":
            r1 = evalstring3(table,variables,sep2[0])
            r2 = evalstring3(table,variables,sep2[1])
            if not chr(34) in r1 and not chr(34) in r2:
                r1 = int(r1)
                r2 = int(r2)
                if sep2operands[0] == ">":
                    results.append(r1 > r2)
                elif sep2operands[0] == "<":
                    results.append(r1<r2)
                else:
                    results.append(r1==r2)
            elif chr(34) in r1 and chr(34) in r2:
                r1 = r1.strip()
                r2 = r2.strip()
                if sep2operands[0] == ">":
                    results.append(r1[1:-1] > r2[1:-1])
                elif sep2operands[0] == "<":
                    results.append(r1[1:-1]<r2[1:-1])
                else:
                    results.append(r1[1:-1]==r2[1:-1])
            else:
                print("typeError")
                exit()
        else:
            if i == "true":
                results.append(True)
            else:
                results.append(False)
    while len(results) > 1:
        op = sep1operands[0]
        a = results[0]
        b = results[1]
        if op == "or":
            c = a or b
            sep1operands.pop(0)
            results.pop(0)
            results.pop(0)
            results.insert(0,c)
        elif op == "and":
            c = a and b
            sep1operands.pop(0)
            results.pop(0)
            results.pop(0)
            results.insert(0, c)
    if results[0] == False:
        return False
    else:
        return True
def bracketfinder(x):
    global orders
    a = 1
    b = 0
    while True:
        if "{" in orders[x+1]:
            a += 1
        elif "}" in orders[x+1]:
            b += 1
        if a == b:
            return x+1
        x += 1
def printx(mat):
    lens = [max(map(len, col)) for col in zip(*mat)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in mat]
    print('\n'.join(table))
def wordtonum(str1):
    i = len(str1) - 1
    resu = 0
    while len(str1) != 1:
        tmp = str1[0]
        resu = resu + dict2[tmp] * (26 ** i)
        str1 = str1[1:]
        i -= 1
    resu += dict2[str1] - 1
    return resu
def numtoword(a):
    if 0 <= ord(a[0]) <= 57:
        a = int(a)
        res = dict1[a % 26]
        a = a // 26
        while a != 0:
            tmp = a % 26
            if tmp != 0:
                # print(tmp)
                res += dict1[tmp - 1]
                a = a // 26
            else:
                res += dict1[25]
                break
        return res[::-1]
def evalstring3(table, variables, text):
    a = re.split(r" *[+*\-/] *", text)
    b = re.findall(r"[+*\-/]", text)
    c = ""
    while len(a) != 0:
        c += a[0]
        if len(b) != 0:
            c += b[0]
            b.pop(0)
        a.pop(0)
    text = c
    dict1 = {}
    dict2 = {}
    j = 65
    for i in range(26):
        dict1[i] = chr(j)
        dict2[chr(j)] = i + 1
        j += 1
    def evalstring(text):
        a = re.split(r" *[+*\-/] *", text)
        b = re.findall(r"[+*\-/]", text)
        c = ""
        dict1 = {}
        dict2 = {}
        j = 65
        res = ""
        resu = 0
        pattern3 = r"\A(\"[A-Z]+\")"
        for i in range(26):
            dict1[i] = chr(j)
            dict2[chr(j)] = i + 1
            j += 1

        def findid(text: list, target: str):
            x = 0
            for i in range(len(text)):
                if text[i] == target:
                    x = i
                    break
                else:
                    x = -1
            return x

        def wordtonum(str1):
            i = len(str1) - 1
            resu = 0
            while len(str1) != 1:
                tmp = str1[0]
                resu = resu + dict2[tmp] * (26 ** i)
                str1 = str1[1:]
                i -= 1
            resu += dict2[str1] - 1
            return resu

        def numtoword(a):
            if 0 <= ord(a[0]) <= 57:
                a = int(a)
                res = dict1[a % 26]
                a = a // 26
                while a != 0:
                    tmp = a % 26
                    if tmp != 0:
                        # print(tmp)
                        res += dict1[tmp - 1]
                        a = a // 26
                    else:
                        res += dict1[25]
                        break
                return res[::-1]

        def replaceop(match: re.Match):
            x = match.group(1)
            y = match.group(2)
            return str(int(x) * int(y))

        def replaceop1(match: re.Match):
            x = match.group(1)
            y = match.group(2)
            return str(int(x) // int(y))

        def replacesum(match: re.Match):
            x = str(match.group(1))
            y = str(match.group(2))
            if chr(34) in x and chr(34) in y:
                return x[:-1] + y[1:]
            elif chr(34) not in x and chr(34) not in y:
                return str(int(x) + int(y))
            else:
                if not re.search(r"\"[A-Z]*[a-z0-9 ]+[A-Z]*\"", x) and not re.search(r"\"[A-Z]*[a-z0-9 ]+[A-Z]*\"", y):
                    if chr(34) in x and x[1:-1] != "":
                        x = wordtonum(x[1:-1])
                        return "{}{}{}".format(chr(34), numtoword(str(x + int(y))), chr(34))
                    elif chr(34) in y and y[1:-1] != "":
                        return str(int(x) + wordtonum(y[1:-1]))
                    else:
                        print("unsupported operand")
                        exit()
                else:
                    print("unsupported operand")
                    exit()

        def replaceminus(match: re.Match):
            x = str(match.group(1))
            y = str(match.group(2))
            if chr(34) not in x and chr(34) not in y:
                return str(int(x) - int(y))
            elif chr(34) in x and chr(34) in y:
                print("unsupported operand")
                exit()
            else:
                if not re.search(r"\"[A-Z]*[a-z0-9 ]+[A-Z]*\"", x) and not re.search(r"\"[A-Z]*[a-z0-9 ]+[A-Z]*\"", y):
                    if chr(34) in x and x[1:-1] != "":
                        x = wordtonum(x[1:-1])
                        return "{}{}{}".format(chr(34), numtoword(str(x - int(y))), chr(34))
                    elif chr(34) in y and y[1:-1] != "":
                        return str(int(x) - wordtonum(y[1:-1]))
                    else:
                        print("unsupported operand")
                        exit()
                else:
                    print("unsupported operand")
                    exit()

        while len(a) != 0:
            c += a[0]
            if len(b) != 0:
                c += b[0]
                b.pop(0)
            a.pop(0)
        while "*" in c or "/" in c:
            x = findid(c, "*")
            y = findid(c, "/")
            if x != -1 and y == -1:
                c = re.sub(r"(\d+) *\* *(\d+)", replaceop, c, 1)
            elif x == -1 and y != -1:
                c = re.sub(r"(\d+) */ *(\d+)", replaceop1, c, 1)
            elif x != -1 and y != -1:
                if x < y:
                    c = re.sub(r"(\d+) *\* *(\d+)", replaceop, c, 1)
                else:
                    c = re.sub(r"(\d+) */ *(\d+)", replaceop1, c, 1)
        while "+" in c or "-" in c:
            # print(c,1)
            x = findid(c, "+")
            y = findid(c, "-")
            if x != -1 and y == -1:
                c = re.sub(r"(-*\d+|\"[A-Z]+\"|\"[A-Z0-9a-z !]*\") *\+ *(-*\d+|\"[A-Z]+\"|\"[A-Z0-9a-z !]*\")",
                           replacesum, c, 1)
            elif x == -1 and y != -1:
                c = re.sub(r"(-*\d+|\"[A-Z]+\"|\"[A-Z0-9a-z !]*\") *- *(\d+|\"[A-Z]+\"|\"[A-Z0-9a-z !]*\")",
                           replaceminus, c, 1)
            elif x != -1 and y != -1:
                if x < y:
                    c = re.sub(r"(-*\d+|\"[A-Z]+\"|\"[A-Z0-9a-z !]*\") *\+ *(-*\d+|\"[A-Z]+\"|\"[A-Z0-9a-z !]*\")",
                               replacesum, c, 1)
                elif y == 0:
                    y = re.findall(r"(\+|-)", c[1:])
                    if y[0] == "+":
                        c = re.sub(r"(-*\d+|\"[A-Z]+\"|\"[A-Z0-9a-z !]*\") *\+ *(-*\d+|\"[A-Z]+\"|\"[A-Z0-9a-z !]*\")",
                                   replacesum, c, 1)
                    else:
                        c = re.sub(r"(-*\d+|\"[A-Z]+\"|\"[A-Z0-9a-z !]*\") *- *(\d+|\"[A-Z]+\"|\"[A-Z0-9a-z !]*\")",
                                   replaceminus, c, 1)
                else:
                    c = re.sub(r"(-*\d+|\"[A-Z]+\"|\"[A-Z0-9a-z !]*\") *- *(\d+|\"[A-Z]+\"|\"[A-Z0-9a-z !]*\")",
                               replaceminus, c, 1)
            # print(c,2)
            if re.search(r"^-\d+(?! *\+|-)", c):
                break
        return c
    def replacetable(match: re.Match):
        x = match.group(1)
        y = match.group(2)
        x = wordtonum(x)
        return str(table[int(y) - 1][int(x)])
    def replacetable1(match: re.Match):
        x = str(match.group(1))[1:-1]
        y = str(match.group(2))[1:-1]
        if len(x) > 3:
            x = evalstring(x)
        if len(y) > 1:
            y = evalstring(y)
        x = x[1:-1]
        return str(table[int(y) - 1][wordtonum(x)])
    def replacevar(match: re.Match):
        x = str(match.group(0))
        return str(variables[x])
    pattern = r"([A-Z]+)(\d+)(?= *[+\-/*]|\])"
    text1 = re.sub(pattern, replacetable, text)
    pattern = r"([A-Z]+)(\d+)$"
    text1 = re.sub(pattern, replacetable, text1)
    if "None" in text1:
        return "None"
    pattern = r"[a-z]+\w*(?= *[+\-/*]|\]|\n)"
    text1 = re.sub(pattern, replacevar, text1)
    pattern = r"[a-z]+\w*$"
    text1 = re.sub(pattern, replacevar, text1)
    pattern = r"(\[[A-Z0-9+\-*/\"]+])(\[[A-Z0-9+\-*/\"]+])"
    text2 = re.sub(pattern, replacetable1, text1)
    if "None" in text2:
        return "None"
    return evalstring(text2)
def order_eval(e,t,text1):
    #print(text)
    global active
    while e <= t:
        text = text1[e].strip()
        if re.search(r"create\((\w+),(\d+),(\d+)\)",text):
            a = re.search(r"create\((\w+),(\d+),(\d+)\)",text)
            name = a.group(1)
            row = a.group(2)
            column = a.group(3)
            tables[name] = Table(name,int(column),int(row))
        if re.search(r"context\((\w+)\)",text):
            if active != None:
                for (i,j) in active.cellsdic:
                    solve(i,j)
            a = re.search(r"context\((\w+)\)",text)
            active = tables[a.group(1)]
        if re.search(r"if\(.+\){", text):
            a = re.search(r"if\((.+)\){", text)
            brack = bracketfinder(e)
            # print("brack",brack)
            if condition(a.group(1),active.table,variables):
                order_eval(e+1,brack,orders)
            e = brack
        if re.search(r"while\(.+\){", text):
            a = re.search(r"while\((.+)\){", text)
            brack = bracketfinder(e)
            while condition(a.group(1),active.table,variables):
                """for i in active.table:
                    print(i)"""
                order_eval(e+1,brack,orders)
            e = brack
        if re.search(r"([A-Z]+)(\d+)(?= *=)",text):
            a = re.search(r"([A-Z]+)(\d+) *= *(.+)",text)
            active.setitem1(a.group(1),a.group(2), evalstring3(active.table,variables,a.group(3)))
        if re.search(r"[a-z]+\w*(?= *=)",text) and not re.search(r"([a-z]+\w*) *== *(.+)",text):
            a = re.search(r"([a-z]+\w*) *= *(.+)",text)
            """for (i, j) in active.cellsdic:
                active.table[i][j] = evalstring3(active.table, variables, active.cellsdic[(i, j)])
            for i in active.table:
                print(i)"""
            if active == None:
                variables[a.group(1)] = evalstring3([], variables, a.group(2))
            else:
                variables[a.group(1)] = evalstring3(active.table,variables,a.group(2))
        if re.search(r"(\[[A-Z0-9a-z+\-*/\"]+])(\[[A-Z0-9a-z+\-*/\"]+])(?= *=)",text):
            a = re.search(r"(\[[A-Z0-9a-z+\-*/\"]+])(\[[A-Z0-9a-z+\-*/]+]) *= *(.+)",text)
            active.setitem1(evalstring3(active.table,variables,a.group(1)[1:-1])[1:-1],evalstring3(active.table,variables,a.group(2)[1:-1]),evalstring3(active.table,variables,a.group(3)))
        if re.search(r"setFunc\((([A-Z]+)(\d+)) *, *(.+)",text):
            a = re.search(r"setFunc\((([A-Z]+)(\d+)) *, *(.+)",text)
            active.functioncells(wordtonum(a.group(2)),int(a.group(3)), replacement(a.group(4)[:-1]))
            for (i, j) in active.cellsdic:
                solve(i,j)
        if re.search(r"setFunc\(((\[[A-Z0-9a-z+\-*/\"]+])(\[[A-Z0-9a-z+\-*/]+])) *, *(.+)",text):
            a = re.search(r"setFunc\(((\[[A-Z0-9a-z+\-*/\"]+])(\[[A-Z0-9a-z+\-*/\"]+])) *, *(.+)",text)
            active.functioncells(wordtonum(evalstring3(active.table, variables, a.group(2)[1:-1])[1:-1]),
                            int(evalstring3(active.table, variables, a.group(3)[1:-1])),replacement(a.group(4)[:-1]))
            for (i, j) in active.cellsdic:
                solve(i,j)
        if re.search(r"print\((.+)\)",text):
            a = re.search(r"print\((.+)\)",text)
            if active == None:
                print("out:"+evalstring3([],variables,a.group(1)))
            else:
                for (i, j) in active.cellsdic:
                    solve(i,j)
                print("out:"+evalstring3(active.table,variables,a.group(1)))
        if re.search(r"display\(\w+\)",text):
            name = re.search(r"display\((\w+)\)",text).group(1)
            for (i, j) in active.cellsdic:
                solve(i,j)
            tmp = tables[name].table.copy()
            array = [["{}".format(z)] for z in range(len(tmp) + 1)]
            tmp.insert(0, ["{}".format(numtoword(str(i))) for i in range(tables[name].column)])
            for i in range(len(array)):
                tmp[i] = array[i] + tmp[i]
            printx(tmp)
        e += 1

class Table:
    def __init__(self,name,rows,columns):
        self.row = rows
        self.column = columns
        self.name = name
        self.cellsdic = dict()
        self.table = [["None" for i in range(self.column)] for j in range(self.row)]
    def setitem1(self,i,j,value):
        if (int(j)-1,int(wordtonum(i))) not in self.cellsdic:
            self.table[int(j)-1][int(wordtonum(i))] = value
        else:
            self.functioncells(int(wordtonum(i)),int(j),value)
    def functioncells(self,i:int,j:int,value):
        self.cellsdic[(j-1,i)] = value
        #print(variables)
        #print(self.cellsdic)
z = 0
try:
    order_eval(0,len(orders)-1,orders[:])
except:
    print("Error")






