import os, sys

def checkLine(line):
    if line.startswith("SUBJECT_ID"): sem = 1
    elif line.startswith('",,'): sem = 2
    else: sem =0
    return sem

cpath = "/share/pi/stamang/data/mimic/"
fin = open(cpath + "testnotes.csv","r") 
fout_nmeta = open(cpath + "testnotemdata.txt","w")
fout_notes = open(cpath + "testnotes_formatted.txt","w")
print >> fout_nmeta,"PATIENT_ID|NOTE_ID|MIMIC_ID|TIMESTAMP|NOTE_TYPE"
nid = 0
pid = 0
text = ""
sem = 0
for line in fin:
    tmp = line.strip()
    if line.startswith("SUBJECT_ID"):
        sem = 1
        continue
    if line.startswith('",,'):
        sem = 2
        continue
    if sem == 0:
        text = text+tmp
        continue
    ptdata = tmp.split(",")
    if sem == 1:
        pid += 1
        if nid != 0:
            print >> fout_notes, str(nid)+"\t"+text
            text = ""
        nid += 1
        print >> fout_nmeta,str(pid)+"|"+str(nid)+"|"+ptdata[0]+"|"+ptdata[4]+"|"+ptdata[9]
        print "NEW PATIENT"
        #print str(pid)+"|"+str(nid)+"|"+ptdata[0]+"|"+ptdata[4]+"|"+ptdata[9]
        sem = 0
    elif sem == 2:
        if line.startswith("SUBJECT_ID"):
            sem = 1
            continue
        else:
            nid += 1
            print >> fout_notes, str(nid)+"\t"+text
            print "printed "+str(len(text))+" characters"
            print "TEXT"
            print nid
            #print text
            text = ""
            print >> fout_nmeta,str(pid)+"|"+str(nid)+"|"+ptdata[0]+"|"+ptdata[4]+"|"+ptdata[9]
            #print str(pid)+"|"+str(nid)+"|"+ptdata[0]+"|"+ptdata[4]+"|"+ptdata[9]
            sem = 0
print >> fout_notes, str(nid)+"\t"+text

fout_notes.close()
fout_nmeta.close()
