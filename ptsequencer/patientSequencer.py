import os, sys, operator
from patientSequencerFcns import *

dictfile = "/share/pi/stamang/cie/clever-demo/res/termN2C2.txt"
project = "output"
ppath = "/share/pi/stamang/cie/clever-demo/"+project+"/"
# ptKey = ppath+"mimicKey.txt"  # allows limiting patients to a preidentified set of say patient_id|mimic_id
noteMdata = "/share/pi/stamang/cie/clever-demo/notes/testnotemdata.txt"
target_class = ["ALCOHOL-ABUSE"]
#target_class = ["ABDOMINAL","CAD-DX","CAD-MI","CAD-RX","CREATININE","DIETSUPP","AMP","EYE","NEURO","NEURO","RENAL","HBA1C","KETONE","KETOACIDOCIS","ASPIRIN","SPEAKS","ESL","MAKES-DECISIONS","ALCOHOL-ABUSE","DRUG-ABUSE"]

#m3pts = getPids(0,ptKey)                    #pt ids for subset
termDict = getTerminology(dictfile)          #load terminology

noteMDict = loadMimicNoteMdata(noteMdata)    #load note metada w/format specific to corpus                         
#s6:patient_id|note_id|doc_description|age_at_note_DATE_in_days|note_year
#M3: PATIENT_ID|NOTE_ID|MIMIC_ID|TIMESTAMP|NOTE_TYPE

seqDict = {}
for target in target_class:
    seqFile = ppath +"ants/"+target+"/extraction*.tsv"
    tmpDict = loadSeqs(seqFile,noteMDict,termDict)
    seqDict.update(tmpDict)
print len(seqDict)

pList = []
# get patients w/ sequences
for sid in seqDict:
    tmp = seqDict[sid]
    sinfo = tmp.split("|")
    #print "SINFO:", sinfo
    tmpsinfo = sinfo[0].split("-")
    pt = tmpsinfo[1]
    if pt not in pList:
        pList.append(pt)
#print pList


print "aggregating patient level annotation output..."
#for ptid in m3pts:           # use of preidentified set of patients
#    pt = str(m3pts[ptid])
#    print "patient:", pt
for pt in sorted(pList):      # use all patients with target class annotations
    ptAnts = []
    fout = open(ppath+"ptseq/pt"+pt+".txt","w")
    for sid in seqDict:
        tmp = seqDict[sid]
        sinfo = tmp.split("|")
        #print sinfo
        tmpsinfo = sinfo[0].split("-")
        if tmpsinfo[1]==pt:
            #print "found:",sinfo
            toff = sinfo[7]
            litem = [toff,tmp]
            if litem not in ptAnts:
                ptAnts.append(litem)
    ptList = sorted(ptAnts, key=operator.itemgetter(0))
    #tmpPtList = set(ptList)
    #ptList = list(tmpPtList)
    #print "writing patient level output to files..."
    for item in ptList:
            #print item[0],item[1]
        print >> fout, item[1]
    fout.close()

print "fini!"
