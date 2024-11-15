import os
import copy
import platform


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


matrices = {}
matRes = None
running = True


class Matrix:
    def __init__(self, entries):
        self.entries = entries
        self.rows = len(entries)
        self.cols = len(entries[0])

    def getEntry(self, row, col):
        return self.entries[row-1][col-1]


def clear_console():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def num(s):
    try:
        return float(s)
    except:
        try:
            return int(s)
        except:
            return "ERR"


def create_matrix():
    name = ""
    while name == "":
        name = "".join(char for char in input(
            f"{bcolors.HEADER}Enter a name for the matrix: {bcolors.ENDC}") if char.isalpha()).capitalize()
        if name in matrices.keys():
            clear_console()
            isSure = input(
                f"{bcolors.WARNING}mat{name} already exist. Do you want to replace it? [Y]yes [N]no :{bcolors.ENDC}")
            if isSure.lower() != "y":
                name = ""
        else:
            clear_console()
            print(f"{bcolors.WARNING}Please enter an alphabetical name{
                  bcolors.ENDC}\n")
    clear_console()
    rows = None
    while rows == None:
        try:
            rows = int(
                input(f"{bcolors.BOLD+bcolors.WARNING}[0]{bcolors.ENDC} Cancel\n\n{bcolors.HEADER}Enter number of rows:{bcolors.ENDC} "))
        except:
            pass
        if rows == None:
            clear_console()
            print(f"{bcolors.WARNING}Please enter a valid number{bcolors.ENDC}")
        elif rows == 0:
            return

    clear_console()
    cols = None
    while cols == None:
        try:
            cols = int(
                input(f"{bcolors.BOLD+bcolors.WARNING}[0]{bcolors.ENDC} Cancel\n\n{bcolors.HEADER}Enter number of columns: {bcolors.ENDC}"))
        except:
            pass
        if cols == None:
            clear_console()
            print(f"{bcolors.WARNING}Please enter a valid number{bcolors.ENDC}")
        elif cols == 0:
            return
    clear_console()
    entries = []
    for i in range(1, rows+1):
        row = []
        for j in range(1, cols+1):
            clear_console()
            print_dummy_matrix(rows, cols, i, j, entries+[row])
            je = None
            while je == None:
                try:
                    je = float(input(f"{bcolors.HEADER}Entry for {
                               i}x{j}: {bcolors.ENDC}"))
                except:
                    print(f"{bcolors.WARNING}Please enter a valid number{
                        bcolors.ENDC}\n")
            row.append(je)
        entries.append(row)
    matrices[name] = Matrix(entries)


def replace_int(n):
    if n.is_integer():
        return int(n)
    else:
        return n


def print_dummy_matrix(row, col, ci, cj, entries):
    ent = entries
    r = ""
    for i in range(row):
        col_arr = []
        if (i >= len(ent)):
            if (i == ci-1):
                r += "[   ●   "+"◌   "*(cj-1)+"]\n"
            else:
                r += "[   "+"◌   "*col+"]\n"
        else:
            for j in range(col):
                if (j < len(ent[i])):
                    col_arr.append(replace_int(ent[i][j]))
                elif j == cj-1:
                    col_arr.append("●")
                else:
                    col_arr.append("◌")
            r += "[   "+"   ".join(map(str, col_arr))+"   ]\n"
    print(bcolors.OKCYAN+r+bcolors.ENDC)


def print_matrix(m):
    e = ""
    for r in m.entries:
        e += "[  "+"   ".join(map(str, map(replace_int, r)))+"   ]\n"
    print(e)


def print_matrices():
    mstr = ""
    for m in matrices:
        e = ""
        for r in matrices[m].entries:
            e += "[  "+"   ".join(map(str, map(replace_int, r)))+"   ]\n"
        mstr += bcolors.OKBLUE+bcolors.BOLD+"mat"+m+":\n" + \
            bcolors.ENDC+bcolors.ENDC+bcolors.OKGREEN+e+bcolors.ENDC+"\n"
    print(mstr)
    if len(mstr) == 0:
        print(f"{bcolors.BOLD+bcolors.WARNING}NO MATRIX TO SHOW{bcolors.ENDC}")
    print("_"*90+"\n")


def operate(flag):
    global matRes
    operating = True
    f = False
    variables = list(map(lambda a: str("mat"+a), matrices.keys()))
    if flag:
        print(bcolors.OKCYAN+bcolors.BOLD+"Valid variables: " +
              bcolors.ENDC + ", ".join(variables))
        print(f"{bcolors.OKCYAN+bcolors.BOLD}Valid operators:{
            bcolors.ENDC} *, +, inv(), trans(), det(), adj()")
        print(f"{bcolors.OKGREEN + bcolors.BOLD}[h]{bcolors.ENDC} Help\n")

    exp = input(
        f"{bcolors.HEADER+bcolors.BOLD}Enter operation: {bcolors.ENDC}")

    if "*" in exp:
        parts = exp.split("*", 1)
        a = parts[0].strip().split(" ")[-1]
        b = parts[1].strip().split(" ")[0]
        if a in variables and b in variables:
            matR = m_multiply(matrices[a.replace("mat", "")],
                              matrices[b.replace("mat", "")])
            if matR != "ERR":
                matRes = matR
                print_matrix(matR)
        elif (a in variables and b not in variables and num(b) != "ERR") or (b in variables and a not in variables and num(a) != "ERR"):
            matR = None
            if (a in variables):
                matR = s_multiply(matrices[a.replace("mat", "")], num(b))
            else:
                matR = s_multiply(matrices[b.replace("mat", "")], num(a))
            if matR != "ERR":
                matRes = matR
                print_matrix(matR)
        else:
            print(f"{bcolors.FAIL}Variable/s not defined{bcolors.ENDC}")

    elif "+" in exp:
        parts = exp.split("+", 1)
        a = parts[0].strip().split(" ")[-1]
        b = parts[1].strip().split(" ")[0]
        if a in variables and b in variables:
            matR = m_add(matrices[a.replace("mat", "")],
                         matrices[b.replace("mat", "")])
            if matR != "ERR":

                matRes = matR
                print_matrix(matR)
        else:
            print(f"{bcolors.FAIL}Variable/s not defined{bcolors.ENDC}")

    elif "det(" in exp:
        a = exp.split("det(")[1].split(")")[0]
        if a in variables:
            matA = matrices[a.replace("mat", "")]
            d = m_det(matA)
            if d != "ERR":
                print(f"{bcolors.OKGREEN}determinant of {a},\ndet(matR)={
                    bcolors.ENDC+bcolors.BOLD+str(replace_int(d))+bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL}Variable {bcolors.BOLD +
                  a+bcolors.ENDC} not defined{bcolors.ENDC}")

    elif "adj(" in exp:
        a = exp.split("adj(")[1].split(")")[0]
        if a in variables:
            matA = matrices[a.replace("mat", "")]
            d = m_adj(matA)
            if d != "ERR":
                print(f"{bcolors.OKGREEN}adjoint of {a},\n{
                    bcolors.ENDC+bcolors.BOLD}adj({a}):{bcolors.ENDC}")

                matRes = d
                print_matrix(d)
        else:
            print(f"{bcolors.FAIL}Variable {bcolors.BOLD +
                  a+bcolors.ENDC} not defined{bcolors.ENDC}")

    elif "trans(" in exp:
        a = exp.split("trans(")[1].split(")")[0]
        if a in variables:
            matA = matrices[a.replace("mat", "")]
            d = m_trans(matA)
            if d != "ERR":
                print(f"{bcolors.OKGREEN}transpose of {a},\n{
                    bcolors.ENDC+bcolors.BOLD}trans({a}):{bcolors.ENDC}")

                matRes = d
                print_matrix(d)
        else:
            print(f"{bcolors.FAIL}Variable {bcolors.BOLD +
                  a+bcolors.ENDC} not defined{bcolors.ENDC}")

    elif "inv(" in exp:
        a = exp.split("inv(")[1].split(")")[0]
        if a in variables:
            matA = matrices[a.replace("mat", "")]
            d = m_inv(matA)
            if d != "ERR":
                print(f"{bcolors.OKGREEN}inverse of {a},\n{
                    bcolors.ENDC+bcolors.BOLD}inv({a}):{bcolors.ENDC}")
                matRes = d
                print_matrix(d)
        else:
            print(f"{bcolors.FAIL}Variable {bcolors.BOLD +
                  a+bcolors.ENDC} not defined{bcolors.ENDC}")
    elif exp == "b":
        operating = False
    elif exp == "n":
        create_matrix()
        clear_console()
        operate(True)
    elif exp == "0":
        global running
        operating = False
        running = False
        clear_console()
    elif exp == "s":
        if matRes:
            isSure = input(f"{bcolors.OKBLUE}Do you want to save this matrix?{bcolors.ENDC} \n{
                bcolors.BOLD+bcolors.OKGREEN}[y]{bcolors.ENDC}yes {bcolors.BOLD+bcolors.OKGREEN}[n]{bcolors.ENDC}no")
            print_matrix(matRes)
            if isSure.lower() == "y":
                name = ""
                while name == "":
                    name = "".join(char for char in input(
                        f"{bcolors.HEADER}Enter a name for the matrix: {bcolors.ENDC}") if char.isalpha()).capitalize()
                    if name in matrices.keys():
                        clear_console()
                        isSure = input(
                            f"{bcolors.WARNING}mat{name} already exist. Do you want to replace it? [Y]yes [N]no :{bcolors.ENDC}")
                        if isSure.lower() != "y":
                            name = ""
                    else:
                        clear_console()
                        print(f"{bcolors.WARNING}Please enter an alphabetical name{
                            bcolors.ENDC}\n")
                clear_console()
                matrices[name] = matRes
                clear_console()
                f = True

    elif exp == "h":
        clear_console()
        print(
            f"{bcolors.OKCYAN+bcolors.BOLD}Add:{bcolors.ENDC} two matrix by calling'matA+matB'\n{bcolors.OKCYAN+bcolors.BOLD}Multiply:{bcolors.ENDC} Multiply two matrix by calling 'matA*matB'\n{bcolors.BOLD+bcolors.OKCYAN}Scale:{bcolors.ENDC} Multiply with a scaler by calling 'a*matA'\n{bcolors.OKCYAN+bcolors.BOLD}Determinant:{bcolors.ENDC} Find the determinant of a matrix by calling 'det(matA)'\n{bcolors.OKCYAN+bcolors.BOLD}Adjoint:{bcolors.ENDC} Find the adjoint matrix by calling 'adj(matA)'\n{bcolors.OKCYAN+bcolors.BOLD}Transpose:{bcolors.ENDC}Find the transpose matrix by calling'trans(matA)'\n{bcolors.OKCYAN+bcolors.BOLD}Inverse:{bcolors.ENDC} Find the inverse of a matrix by calling 'inv(matA)'\n\n{bcolors.WARNING+bcolors.BOLD}Enter one expression at a time{bcolors.ENDC}\n\n{bcolors.OKGREEN+bcolors.BOLD}[n]{bcolors.ENDC} Define a new variable\n{bcolors.OKGREEN+bcolors.BOLD}[s]{bcolors.ENDC} Save last result{bcolors.OKGREEN+bcolors.BOLD}\n[b]{bcolors.ENDC} Go back\n{bcolors.OKGREEN+bcolors.BOLD}[0]{bcolors.ENDC} Exit")
        print("_"*90+"\n")
        f = True
    else:
        print(f"{bcolors.FAIL}Invalid expression{bcolors.ENDC}")
    if operating:
        operate(f)


def m_inv(matA):
    d = m_det(matA)
    if d != 0:
        a = m_adj(matA)
        return s_multiply(a, 1/d)
    else:
        print(
            f"{bcolors.FAIL}INVERSE_ERR: Must be a non-singular matrix! {bcolors.ENDC}")
        return "ERR"


def s_multiply(matA, s):
    entA = matA.entries
    entA = list(map(lambda a: list(map(lambda b: b*s, a)), entA))
    return Matrix(entA)


def m_multiply(matA, matB):
    if (matA.cols == matB.rows):
        entR = []
        for i in range(1, matA.rows+1):
            col = []
            for j in range(1, matB.cols+1):
                c = 0
                for n in range(1, matA.cols+1):
                    c += matA.getEntry(i, n) * matB.getEntry(n, j)
                col.append(c)
            entR.append(col)
        return Matrix(entR)
    else:
        print(f"{bcolors.FAIL}MULTIPLY_ERR: Column number of first matrix must be equal to the row numbers of the second!{
              bcolors.ENDC}")
        return "ERR"


def m_add(matA, matB):
    if matA.rows == matB.rows and matA.cols == matB.cols:
        entR = []
        for i in range(1, matA.rows+1):
            col = []
            for j in range(1, matA.cols+1):
                col.append(matA.getEntry(i, j)+matB.getEntry(i, j))
            entR.append(col)
        return Matrix(entR)
    else:
        print(f"{bcolors.FAIL}ADD_ERR: Must be a same size matrix! {bcolors.ENDC}")
        return "ERR"


def m_det(matA):
    if matA.rows == matA.cols:
        if matA.rows == 1:
            return matA.entries[0][0]
        else:
            det = 0
            for j in range(matA.cols):
                det += cof(matA, 1, j+1)*matA.getEntry(1, j+1)
            return det
    else:
        print(f"{bcolors.FAIL}DET_ERR: Must be a square matrix! {bcolors.ENDC}")
        return "ERR"


def m_adj(matA):
    if (matA.rows == matA.cols):
        if (matA.rows == 1):
            return matA
        else:
            entR = []
            for i in range(matA.rows):
                rows = []
                for j in range(matA.cols):
                    rows.append(cof(matA, i+1, j+1))
                entR.append(rows)
            return m_trans(Matrix(entR))
    else:
        print(f"{bcolors.FAIL}ADJ_ERR: Must be a square matrix! {bcolors.ENDC}")
        return "ERR"


def cof(matA, i, j):
    entA = copy.deepcopy(matA.entries)
    del entA[i-1]
    for n in range(len(entA)):
        del entA[n][j-1]
    matO = Matrix(entA)
    r = ((-1)**(i+j))*m_det(matO)
    return r


def m_trans(matA):
    entT = []
    for j in range(matA.cols):
        row = []
        for i in range(matA.rows):
            row.append(matA.getEntry(i+1, j+1))
        entT.append(row)
    return Matrix(entT)


def main():
    global running
    clear_console()
    while (running):
        i = ""
        try:
            i = int(input(f"{bcolors.OKGREEN+bcolors.BOLD}[1]{bcolors.ENDC} Define a matrix\n{bcolors.OKGREEN+bcolors.BOLD}[2]{bcolors.ENDC} Show recorded matrices\n{bcolors.OKGREEN+bcolors.BOLD}[3]{bcolors.ENDC} Operate\n\n{bcolors.WARNING+bcolors.BOLD}[0]{bcolors.ENDC} Exit{
                bcolors.ENDC} \n\n{bcolors.HEADER+bcolors.BOLD}Select an option: {bcolors.ENDC}"))
        except:
            pass
        if i == 1:
            clear_console()
            create_matrix()
            clear_console()
        elif i == 2:
            clear_console()
            print_matrices()
        elif i == 3:
            clear_console()
            operate(True)
        elif i == 0:
            clear_console()
            running = False
        else:
            clear_console()
            print(f"{bcolors.WARNING}Please enter a valid input{
                bcolors.ENDC}\n")

main()
