# ===== Importando as bibliotecas =====
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from time import sleep
import pandas as pd
import time

timeResponse = 3000

# ===== Funcoes Auxiliares =====
def convertString(content): #Converte arquivo lido em string formatada
    separator = ""
    aux = separator.join(content).replace("      ", " ").replace("     ", " ").replace("    ", " ").replace("   ", " ").replace("  ", " ").split("\n")[:-1]
    result = []
    for line in aux:
        line = line[1:]
        result.append(line.split(" "))
    return result

def convertList(lista): #Converte lista (unitaria) no padrao de colunas certo
    #O motivo de existencia desta funcao e que apos o split(" ") podem ser geradas listas de tamanhos diferentes
    #A lista "result" obrigatoriamente tera 7 colunas, que eh o padrao do projeto
    result = []
    result.append(lista[0])
    string = ""
    for element in lista[1:-5]:  
        string = string + element
    result.append(string)
    [result.append(lista[index]) for index in [-5, -4, -3, -2, -1]]
    return result

def readContent(): #Funcao de leitura de arquivo txt
    #Importante ressaltar que essa funcao transforma o conteudo do txt em um DataFrame Pandas
    #Tambem ordena o DataFrame dando preferencia para os maiores valores de %CPU
    #O retorno desta funcao apenas leva os 15 registros de maior %CPU
    with open("processos.txt", "r") as log:
        content = log.readlines()
        log.close()
        content = convertString(content)
        colunas = convertList(content[0])
        content = pd.DataFrame([convertList(linha) for linha in content[1:]], columns=colunas)
        content["%CPU"] = content["%CPU"].astype(float)
        content["PRI"] = content["PRI"].astype(int)
        content = content.sort_values(by = ["%CPU", "PRI"], ascending=False).head(15)
    return content.reset_index(drop=True)

def updateWindow(): #Essa funcao eh chamada indefinidamente para atualizar a interface
    try:
        content = readContent()
        contRunTime = int(time.time() - initTime)
        for child in MiddleFrame.winfo_children():
            child.destroy()
        table = Table(MiddleFrame, content) #Atualiza a lista
        runtime = Label(BottomFrame, text = "Runtime [s]: " + str(contRunTime), font = ("Verdana", 16), bg = "WHITE", fg = "BLACK")
        runtime.place(relx = 0.05, rely=0.1)
        janela.after(timeResponse, updateWindow) #Aqui deixa marcado a chamada de updateWindow apos 1000 ms
    except:
        janela.after(500, updateWindow)

class Table:
    def __init__(self,MiddleFrame,content):
        colunas = content.columns
        #MiddleFrame.config(background = "BLACK")
        for colIndex in range(6): #Se o range de colunas mudar, esse range aqui tbm precisa mudar
            if colIndex == 1:
                largura = 30 #A coluna "CMD" eh mais larga
            else:
                largura = 10
            self.e = Entry(MiddleFrame, width=largura, bg = "BLACK", fg = "WHITE",font=('Arial',16,'bold'), justify = "center")
            self.e.grid(row=0, column=colIndex)
            self.e.insert(END, colunas[colIndex])
        for index, row in content.iterrows():
            for colIndex in range(6): #Se o range de colunas mudar, esse range aqui tbm precisa mudar
                if colIndex == 1:
                    largura = 30 #A coluna "CMD" eh mais larga
                else:
                    largura = 10
                self.e = Entry(MiddleFrame, width=largura, bg = "BLACK", fg = "WHITE",font=('Arial',16,'bold'), justify = "center")
                self.e.grid(row=index + 1, column=colIndex)
                self.e.insert(END, row[colunas[colIndex]])
                

def killProcess(): #Funcao para matar processo. Note que a variavel digitadoPID controla o kill
    f = open("acoes.txt", "w")
    f.write("kill "+digitadoPID.get())
    f.close()
    
    
def stopProcess(): #Funcao para matar processo. Note que a variavel digitadoPID controla o kill
    f = open("acoes.txt", "w")
    f.write("stop "+digitadoPID.get())
    f.close()
    
    
def continueProcess(): #Funcao para matar processo. Note que a variavel digitadoPID controla o kill
    f = open("acoes.txt", "w")
    f.write("continue "+digitadoPID.get())
    f.close()
    
    
def filterProcess(): #Funcao para matar processo. Note que a variavel digitadoPID controla o kill
    f = open("acoes.txt", "w")
    f.write("filtrar "+digitadoPID.get())
    f.close()
    
def removeFilter():
    f = open("acoes.txt", "w")
    f.write("retiraFiltro")
    f.close()
    
def prioProcess(): #Funcao para matar processo. Note que a variavel digitadoPID controla o kill
    f = open("acoes.txt", "w")
    f.write("mudaPrio "+digitadoPID.get()+" "+digitadoPrioNice.get())
    f.close()

def niceProcess(): #Funcao para matar processo. Note que a variavel digitadoPID controla o kill
    f = open("acoes.txt", "w")
    f.write("mudaNice "+digitadoPID.get()+" "+digitadoPrioNice.get())
    f.close()

def alocaProcess(): #Funcao para matar processo. Note que a variavel digitadoPID controla o kill
    f = open("acoes.txt", "w")
    f.write("alocarCPU "+digitadoPID.get()+" "+digitadoCPU.get())
    f.close()
    
def on_closing(): #Parar processo apos fechamento da janela
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        janela.destroy()

# ===== Criando janela =====
janela = Tk()
janela.title("Gerenciador de Processos")
janela.geometry("1400x800")
janela.configure(background = "BLACK")
janela.resizable(width = True, height = True)

# ===== Carregando imagens =====
logo = PhotoImage(file = "logo.png")

# ===== Widgets =====
TopFrame = Frame(janela, width = 1400, height = 50, bg = "MIDNIGHTBLUE", relief = "raise")
TopFrame.pack(side=TOP)

LogoLabel = Label(TopFrame, image = logo, bg = "MIDNIGHTBLUE")
LogoLabel.place(relx=0.5, rely=0.5, anchor=CENTER)

MiddleFrame = Frame(janela, width = 1400, height = 500, bg = "BLACK", relief = "raise")	
MiddleFrame.pack(side=TOP)

BottomFrame = Frame(janela, width = 1400, height = 100, bg = "WHITE", relief = "raise")
BottomFrame.pack(side=BOTTOM)

contRunTime = 0

labelPID = Label(BottomFrame, text="PID")
labelPID.place(relx = 0.28,rely = 0.1)

labelPrioNice = Label(BottomFrame, text="Prio/Nice")
labelPrioNice.place(relx = 0.255,rely = 0.4)

labelCPU = Label(BottomFrame, text="CPU's")
labelCPU.place(relx = 0.27,rely = 0.7)

digitadoPID = StringVar() #Aqui comeca a funcionalidade do botao kill + entrada kill. A variavel nesse caso eh digitadoPID
pidEntry = Entry(BottomFrame, width = 10, textvariable=digitadoPID, justify = "center")
pidEntry.place(relx = 0.3, rely=0.1)

digitadoPrioNice = StringVar() #Aqui comeca a funcionalidade do botao kill + entrada kill. A variavel nesse caso eh digitadoPID
prioNiceEntry = Entry(BottomFrame, width = 10, textvariable=digitadoPrioNice, justify = "center")
prioNiceEntry.place(relx = 0.3, rely=0.4)

digitadoCPU = StringVar() #Aqui comeca a funcionalidade do botao kill + entrada kill. A variavel nesse caso eh digitadoPID
cpuEntry = Entry(BottomFrame, width = 10, textvariable=digitadoCPU, justify = "center")
cpuEntry.place(relx = 0.3, rely=0.7)

killButton = Button(BottomFrame, text = "KILL BY PID", width = 10, command = killProcess, justify = "center")
killButton.place(relx = 0.4, rely=0.1)

stopButton = Button(BottomFrame, text = "STOP BY PID", width = 10, command = stopProcess, justify = "center")
stopButton.place(relx = 0.5, rely=0.1)

continueButton = Button(BottomFrame, text = "CONTINUE BY PID", width = 15, command = continueProcess, justify = "center")
continueButton.place(relx = 0.6, rely=0.1)

filterButton = Button(BottomFrame, text = "FILTER BY PID", width = 10, command = filterProcess, justify = "center")
filterButton.place(relx = 0.9, rely=0.2)

unfilterButton = Button(BottomFrame, text = "REMOVE FILTER", width = 10, command = removeFilter, justify = "center")
unfilterButton.place(relx = 0.9, rely=0.5)

prioButton = Button(BottomFrame, text = "SET PRIORITY", width = 10, command = prioProcess, justify = "center")
prioButton.place(relx = 0.4, rely=0.4)

niceButton = Button(BottomFrame, text = "SET NICENESS", width = 10, command = niceProcess, justify = "center")
niceButton.place(relx = 0.5, rely=0.4)

alocaButton = Button(BottomFrame, text = "ALOCA CPU", width = 10, command = alocaProcess, justify = "center")
alocaButton.place(relx = 0.4, rely=0.7)


# ===== Atualizando conteudo =====

initTime = time.time()
janela.after(1000, updateWindow)
janela.protocol("WM_DELETE_WINDOW", on_closing)
janela.mainloop()