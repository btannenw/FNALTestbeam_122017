#! /usr/bin/env python

import os, sys, commands, time

#look for the current directory
#######################################
pwd = os.environ['PWD']
home = os.environ['HOME']
#######################################
RUN_DIR = pwd
TEMP = pwd
EXE  = "echo"
OUT  = "/eos/uscms/store/user/cmstestbeam/ETL/MT6Section1Data/122017/OTSDAQ/"
TARGET = "default"
QUEUE = ""

def write_sh(srcfile,run,ofile,lfile):
    fsrc = open(srcfile,'w')
    fsrc.write('universe = vanilla \n')
    fsrc.write('executable = '+EXE+" \n")
    fsrc.write('getenv = True \n')
    fsrc.write('Arguments = ');
   
    fsrc.write(run+' > '+ofile+" \n")
   
    fsrc.write('output = '+lfile+" \n")
    fsrc.write('queue \n')
    fsrc.close()

if __name__ == "__main__":
    if not len(sys.argv) > 1 or '-h' in sys.argv or '--help' in sys.argv:
        print "Usage: %s [-q queue] [-list lists/list.list]" % sys.argv[0]
        print
        sys.exit(1)

    argv_pos = 1
  
    if '-q' in sys.argv:
        p = sys.argv.index('-q')
        QUEUE = sys.argv[p+1]
        argv_pos += 2
    if '-list' in sys.argv:
        p = sys.argv.index('-list')
        TARGET = sys.argv[p+1]
        argv_pos += 2

    # input sample list
    listfile = "lists/"+TARGET+".list"
        
    # create and organize output folders
    ROOT = OUT+"/"+TARGET+"/"
    TARGET  = RUN_DIR+"/"+TARGET+"/"
    srcdir  = TARGET+"src/"
    logdir  = TARGET+"log/"

    # make output folders
    os.system("rm -rf "+TARGET)
    os.system("mkdir -p "+TARGET)
    os.system("mkdir -p "+logdir)
    os.system("mkdir -p "+srcdir)
    os.system("rm -rf "+ROOT)
    #os.system("mkdir -p "+ROOT)

    with open(listfile,'r') as f:
        inputlist = f.readlines()
        for line in inputlist:
            line = line.split()
            run_number = line[0]
            write_sh(srcdir+"Run"+run_number+".sh", run_number, ROOT+"Run"+run_number+".root", logdir+"Run"+run_number+".log")
            #os.system('condor_submit '+srcdir+name+".sh")
    