#! /usr/bin/env python

import argparse
import os
import subprocess

def main():
    filename = 'shellog.txt'
    if os.path.exists(filename):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not
    logf = open(filename,append_write)

    parser = argparse.ArgumentParser(description='Process bash commmand line arguments')
    parser.add_argument('-c', help='shell command')
    args = vars(parser.parse_args())
    preCommand=args['c']


    print("Command is: " + preCommand + " \n")

    # Get enviromental variables from parent process user-space
    pid=os.getpid()
    # parent process pid
    ppid=os.popen("ps -o %d= -p 1111"%pid).read()
    envVarList=os.popen("cat /proc/%s/environ"%ppid).read()

    if('QUERY_STR' in os.environ.keys() ):
        userReq=os.environ['QUERY_STR']
    else:
        userReq=''
    #print("User env variables are:" + envVarList + " \n")
    logf.write("New Request Analysis: "+ '\n')
    logf.write(userReq)
    logf.write("New Command Analysis: "+ '\n')
    logf.write(preCommand)
    logf.write('\n')
    logf.close()
    userParams=userReq.split('&')
    injectionFlag=0
    for par in userParams:
        values=par.split('=')
        print values
        if(len(values)>1):
            potValue=values[1]
            print potValue
            if(potValue in preCommand):
                p = subprocess.Popen(['/home/ShellParser.py',
                 preCommand, potValue]
                 ,
                stdout=subprocess.PIPE
                #,
                #stderr=subprocess.PIPE
                )
                print(out)
                #print err
                if(out=="0"):
                    injectionFlag=1

    if(injectionFlag==0 and preCommand):
        #os.chdir('/')
        os.execve('/bin/shh', ["/bin/shh", "-c", preCommand],os.environ)

        os._exit(1)

    else:
        print("injection Found")
        os._exit(0)




if __name__== "__main__":
  main()
