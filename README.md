# pyxcel
pyxcel is a simple programming language inspired by excel and written in python which enables you to make tables with desired number of cells, edit those cells by putting different values in them, copying, moving, making them be a function of other cells and ...
to code in pyxcel you just have to run the pyxcel.py and start coding in the terminal
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
setFunc({cell name},{expression})
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
you can also comment anything by putting $ before it.

