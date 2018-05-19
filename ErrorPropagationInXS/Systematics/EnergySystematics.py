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

inFileName = "/Volumes/Seagate/Elena/TPC/Data60A.root"

f = root.TFile(inFileName)
myTree = f.Get("RecoXS/effTree")


hInteractingKEComp = f.Get("RecoXS/hRecoInteractingKE")
hIncidentKEComp    = f.Get("RecoXS/hRecoIncidentKE")

outFileName = inFileName[:-5]+"_out.root"
outF = TFile(outFileName,"recreate")
outF.cd()


hInteractingKE   = TH1D("hInteractingKE","hInteractingKE" , hInteractingKEComp.GetSize()-2, hInteractingKEComp.GetXaxis().GetXmin(),  hInteractingKEComp.GetXaxis().GetXmax())
hIncidentKE      = TH1D("hIncidentKE"   ,"hIncidentKE"    , hIncidentKEComp.GetSize()   -2, hIncidentKEComp.GetXaxis().GetXmin()   ,  hIncidentKEComp.GetXaxis().GetXmax()   )

hInteractingKEMax = TH1D("hInteractingKEMax","hInteractingKEMax",hInteractingKEComp.GetSize()-2, hInteractingKEComp.GetXaxis().GetXmin(),  hInteractingKEComp.GetXaxis().GetXmax())
hIncidentKEMax    = TH1D("hIncidentKEMax"   ,"hIncidentKEMax"   , hIncidentKEComp.GetSize()  -2, hIncidentKEComp.GetXaxis().GetXmin()   ,  hIncidentKEComp.GetXaxis().GetXmax()   )

hInteractingKEMin = TH1D("hInteractingKEMin","hInteractingKEMin",hInteractingKEComp.GetSize()-2, hInteractingKEComp.GetXaxis().GetXmin(),  hInteractingKEComp.GetXaxis().GetXmax())
hIncidentKEMin    = TH1D("hIncidentKEMin"   ,"hIncidentKEMin"   , hIncidentKEComp.GetSize()  -2, hIncidentKEComp.GetXaxis().GetXmin()   ,  hIncidentKEComp.GetXaxis().GetXmax()   )

uncertaintyEDep     = 0.06
uncertaintyMomentum = 1.
uncertaintyELoss    = 7.

print myTree.GetEntry()
sillyCount =0 
for entry in myTree:
     sillyCount += 1
     if not sillyCount % 10000:
          print sillyCount
#     if sillyCount == 40000:
#          break
     # Now you have acess to the leaves/branches of each entry in the tree, e.g.
     eventN     = entry.eventN
     recoIncidentKE     = entry.recoIncidentKE
     recoZPosition      = entry.recoZPosition
     isTrackInteracting = entry.isTrackInteracting
     momentum           = entry.WCMom
     uncertaintyMomentum = 0.02*momentum

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
     
     correction = 0
     for i in xrange(len(recoKESkim)):
         correction = uncertaintyMomentum*uncertaintyMomentum + uncertaintyELoss*uncertaintyELoss + i*i*uncertaintyEDep*uncertaintyEDep
         correction = TMath.Sqrt(correction)
         hIncidentKE.Fill(recoKESkim[i])
         hIncidentKEMax.Fill(recoKESkim[i]+correction)
         hIncidentKEMin.Fill(recoKESkim[i]-correction)

     if isTrackInteracting:
         hInteractingKE.Fill(recoKESkim[len(recoKESkim)-1])
         hInteractingKEMax.Fill(recoKESkim[len(recoKESkim)-1]+correction)
         hInteractingKEMin.Fill(recoKESkim[len(recoKESkim)-1]-correction)



XS      = calculateXSPlot(hInteractingKE   , hIncidentKE    , "XS")
XSMax   = calculateXSPlot(hInteractingKEMax, hIncidentKEMax , "XSMax")
XSMin   = calculateXSPlot(hInteractingKEMin, hIncidentKEMin , "XSMin")


outFile = TFile("SystematicsEnergy.root","recreate")
outFile.cd()

hInteractingKEComp.Write("hInteractingKEComp",TObject.kWriteDelete)  
hIncidentKEComp.Write("hIncidentKEComp",TObject.kWriteDelete)  

hInteractingKE.Write()
hIncidentKE.Write()
hInteractingKEMax.Write()
hIncidentKEMax.Write()
hInteractingKEMin.Write()
hIncidentKEMin.Write()
XS.Write()
XSMax.Write()
XSMin.Write()



outFile.Write()
outFile.Close()


