from ROOT import *
import ROOT as root
import numpy as np

#gStyle.SetOptStat(0)
def calculateXSPlot(InteractingHisto, IncidentHisto, Name  ):
    XS =  InteractingHisto.Clone(Name)
   # XS.Sumw2()
   # IncidentHisto.Sumw2()
    XS.Scale(101.10968)
    XS.Divide(IncidentHisto)
    return XS

inFileName = "/Volumes/Seagate/Elena/TPC/MC100A_Pions.root"
inFileName = "/Volumes/Seagate/Elena/TPC/XSMCPionWithSecondaries60A_histo.root"

f = root.TFile(inFileName)
myTree = f.Get("RecoXSPionOnly/effTree")


hInteractingKEComp = f.Get("RecoXSPionOnly/hRecoInteractingKE")
hIncidentKEComp    = f.Get("RecoXSPionOnly/hRecoIncidentKE")

outFileName = inFileName[:-5]+"_out.root"
outF = TFile(outFileName,"recreate")
outF.cd()


hInteractingKE   = TH1D("hInteractingKE","hInteractingKE" , hInteractingKEComp.GetSize()-2, hInteractingKEComp.GetXaxis().GetXmin(),  hInteractingKEComp.GetXaxis().GetXmax())
hIncidentKE      = TH1D("hIncidentKE"   ,"hIncidentKE"    , hIncidentKEComp.GetSize()   -2, hIncidentKEComp.GetXaxis().GetXmin()   ,  hIncidentKEComp.GetXaxis().GetXmax()   )

lenghtCuts = [10,20,30,40,50,60,70,80,90]

intList =[]
incList =[]

for i in xrange(len(lenghtCuts)):
    print lenghtCuts[i]
    hInteractingKE = TH1D("hInteractingKE_"+str(lenghtCuts[i]),"hInteractingKE_"+str(lenghtCuts[i]), 42, hInteractingKEComp.GetXaxis().GetXmin(),  hInteractingKEComp.GetXaxis().GetXmax())
    hIncidentKE    = TH1D("hIncidentKE_"+str(lenghtCuts[i])   ,"hIncidentKE_"+str(lenghtCuts[i])   , 42, hIncidentKEComp.GetXaxis().GetXmin()   ,  hIncidentKEComp.GetXaxis().GetXmax()   )
    intList.append(hInteractingKE)
    incList.append(hIncidentKE)

print "Check lenghts", len(intList),len(incList), len(lenghtCuts)

print myTree.GetEntry()
sillyCount =0 
for entry in myTree:
     sillyCount += 1
     if not sillyCount % 10000:
         print sillyCount
#     if sillyCount == 10000:
#         break
     # Now you have acess to the leaves/branches of each entry in the tree, e.g.
     eventN     = entry.eventN
     recoIncidentKE     = entry.recoIncidentKE
     recoZPosition      = entry.recoZPosition
     isTrackInteracting = entry.isTrackInteracting
     recoZposSkim = []
     recoKESkim   = []
     for i in recoZPosition:
          if i > -900.0:
               recoZposSkim.append(i)

     for i in recoIncidentKE:
          if i > -900.0:
               recoKESkim.append(i)

     
     recoZposSkim = recoZposSkim[:-1]
     recoKESkim   = recoKESkim[:-1]
     recoZposSkim.insert(0,0.)

     if len(recoZposSkim) != len(recoKESkim):
          print len(recoZposSkim), len(recoKESkim)
          continue
     

     for i in xrange(len(recoKESkim)):
          hIncidentKE.Fill(recoKESkim[i])
          for j in  xrange(len(lenghtCuts)):
              if recoZposSkim[i] < lenghtCuts[j]:
                  incList[j].Fill(recoKESkim[i])

    
     if isTrackInteracting:
          hInteractingKE.Fill(recoKESkim[len(recoKESkim)-1])

          for j in  xrange(len(lenghtCuts)):
              if recoZposSkim[len(recoZposSkim) -1] < lenghtCuts[j]:
                  intList[j].Fill(recoKESkim[len(recoKESkim) -1])






XS    = calculateXSPlot(hInteractingKE   , hIncidentKE    , "XS")

XS_list = []
for j in  xrange(len(lenghtCuts)):
    XSTemp = calculateXSPlot(intList[j]   , incList[j]    , "XS_"+str(lenghtCuts[j]))
    XS_list.append(XSTemp)


outFile = TFile("FuntionOFZ_60APionsMC.root","recreate")
outFile.cd()

hInteractingKEComp.Write("hInteractingKEComp",TObject.kWriteDelete)  
hIncidentKEComp.Write("hIncidentKEComp",TObject.kWriteDelete)  

hInteractingKE.Write()
hIncidentKE.Write()
XS.Write()

for j in  xrange(len(lenghtCuts)):
    intList[j].Write()
    incList[j].Write()
    XS_list[j].Write()


outFile.Write()
outFile.Close()


'''

'''
