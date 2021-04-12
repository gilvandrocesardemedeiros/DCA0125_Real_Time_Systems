#include<iostream>
#include<fstream>
#include <stdlib.h> // system()
#include <signal.h> // definição dos sinais de interrupções
#include <unistd.h>
#include <cstring>
#include <sys/time.h>     // getpriority(int which, int who)  setpriority(int which, int who, int prio);
#include <sys/resource.h>

using namespace std;

int main() {
   ifstream myReadFile;
   string output;
   string acao;
   int pid;
   int prio;
   string spid;
   string sprio;
   string comando;
   bool filtroAtivo = 0;
   while(1){
       myReadFile.open("acoes.txt");
       if (myReadFile.is_open()){
            int i = 0;
            while (!myReadFile.eof()) {
                myReadFile >> output;
                if(i == 0)acao = output;
                
                if(i == 1)spid = output;
          
                if(i == 2)sprio = output;
                i++;
            }
       }
       myReadFile.close();
       myReadFile.open("acoes.txt", ofstream::out | ofstream::trunc);
       myReadFile.close();
       
       if(acao == "kill"){
               pid = stoi(spid);
               cout<<"Matando processo: "<<pid<<endl;
	 	kill(pid, SIGKILL);
	 	cout<<"Processo morto"<<endl;      
       }

       else if(acao == "stop"){
               pid = stoi(spid);
               cout<<"Parando processo: "<<pid<<endl;
	 	kill(pid, SIGSTOP);
	 	cout<<"Processo parado"<<endl;        
       }     
       
       else if(acao == "continue"){
               pid = stoi(spid);
               cout<<"Continuando processo: "<<pid<<endl;
	 	kill(pid, SIGCONT);
	 	cout<<"Processo continuado"<<endl;       
       }

       else if(acao == "filtrar"){
               filtroAtivo = 1;
       }
       
       else if(acao == "retiraFiltro"){
               filtroAtivo = 0;           
       }
           
       else if(acao == "mudaPrio"){
               pid = stoi(spid);
               prio = stoi(sprio);
               cout << "valor da prioridade do processo "<<pid<<" " << getpriority(PRIO_PROCESS, pid) <<endl;
               setpriority(PRIO_PROCESS, pid , prio);
               cout << "valor da prioridade do processo: " << getpriority(PRIO_PROCESS, pid) <<endl;          
       }
       
       else if(acao == "mudaNice"){
              cout<< "muda nice"<<endl;
              comando = "renice -n "+ sprio+ " -p " +spid;
              char * cstr = new char [comando.length()+1];
              strcpy (cstr, comando.c_str());

              system(cstr);
              
              delete cstr;
              
       }
       
       else if(acao == "alocarCPU"){
              cout<<"alocaCPU"<<endl;
              comando = "taskset -pc "+sprio+ " "+spid;
              char * cstr = new char [comando.length()+1];
              strcpy (cstr, comando.c_str());

              system(cstr);
              
              delete cstr;
       }
           
           
       else if(acao == ""){
            cout<<"Sem acao"<<endl;
       }
   
       if(filtroAtivo){
           cout<<"Filtro ativo"<<endl;
           comando = "(ps af -o pid,cmd,pri,nice,stat,%cpu,time |head -1; ps af -o pid,cmd,pri,nice,stat,%cpu,time | grep " + spid + ") > processos.txt";
           char * cstr = new char [comando.length()+1];
           strcpy (cstr, comando.c_str());
           system(cstr);
           delete cstr;
       }
       
       else{
           system("ps af -o pid,cmd,pri,nice,stat,%cpu,time > processos.txt");
       }
              
       acao = "";
       pid = NULL;
       
       //system("sar -P ALL 1 1 | head -12  > cpuperc.txt");
       
       sleep(1);   
  }
return 0;
}
