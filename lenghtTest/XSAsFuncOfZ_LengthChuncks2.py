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
#inFileName = "/Volumes/Seagate/Elena/TPC/MC100A_Muon.root"
outName ="FuntionOFZ_LenghtChuncks_V2_Pion100A.root"

f = root.TFile(inFileName)
myTree = f.Get("RecoXSPionOnly/effTree")
#myTree = f.Get("RecoXSAll/effTree")
#hInteractingKEComp = f.Get("RecoXSAll/hRecoInteractingKE")
#hIncidentKEComp    = f.Get("RecoXSAll/hRecoIncidentKE")

hInteractingKEComp = f.Get("RecoXSPionOnly/hRecoInteractingKE")
hIncidentKEComp    = f.Get("RecoXSPionOnly/hRecoIncidentKE")

outFileName = inFileName[:-5]+"_out.root"
outF = TFile(outFileName,"recreate")
outF.cd()


hInteractingKE   = TH1D("hInteractingKE","hInteractingKE" , hInteractingKEComp.GetSize()-2, hInteractingKEComp.GetXaxis().GetXmin(),  hInteractingKEComp.GetXaxis().GetXmax())
hIncidentKE      = TH1D("hIncidentKE"   ,"hIncidentKE"    , hIncidentKEComp.GetSize()   -2, hIncidentKEComp.GetXaxis().GetXmin()   ,  hIncidentKEComp.GetXaxis().GetXmax()   )

hInteractingKE30 = TH1D("hInteractingKE30","hInteractingKE30" , hInteractingKEComp.GetSize()-2, hInteractingKEComp.GetXaxis().GetXmin(),  hInteractingKEComp.GetXaxis().GetXmax())
hIncidentKE30    = TH1D("hIncidentKE30"   ,"hIncidentKE30"    , hIncidentKEComp.GetSize()   -2, hIncidentKEComp.GetXaxis().GetXmin()   ,  hIncidentKEComp.GetXaxis().GetXmax()   )

hInteractingKE60   = TH1D("hInteractingKE60","hInteractingKE60" , hInteractingKEComp.GetSize()-2, hInteractingKEComp.GetXaxis().GetXmin(),  hInteractingKEComp.GetXaxis().GetXmax())
hIncidentKE60      = TH1D("hIncidentKE60"   ,"hIncidentKE60"    , hIncidentKEComp.GetSize()   -2, hIncidentKEComp.GetXaxis().GetXmin()   ,  hIncidentKEComp.GetXaxis().GetXmax()   )


hInteractingKE90   = TH1D("hInteractingKE90","hInteractingKE90" , hInteractingKEComp.GetSize()-2, hInteractingKEComp.GetXaxis().GetXmin(),  hInteractingKEComp.GetXaxis().GetXmax())
hIncidentKE90      = TH1D("hIncidentKE90"   ,"hIncidentKE90"    , hIncidentKEComp.GetSize()   -2, hIncidentKEComp.GetXaxis().GetXmin()   ,  hIncidentKEComp.GetXaxis().GetXmax()   )

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
          if recoZposSkim[i] < 90. and recoZposSkim[len(recoZposSkim) -1 ] > 60.:
              hIncidentKE90.Fill(recoKESkim[i])
          if recoZposSkim[i] < 60. and recoZposSkim[len(recoZposSkim) -1 ] > 30.:
              hIncidentKE60.Fill(recoKESkim[i])
          if recoZposSkim[i] < 30.:
              hIncidentKE30.Fill(recoKESkim[i])
    
     if isTrackInteracting:
          hInteractingKE.Fill(recoKESkim[len(recoKESkim)-1])
          if recoZposSkim[len(recoZposSkim) -1 ] < 90 and recoZposSkim[len(recoZposSkim) -1 ] > 60.:
              hInteractingKE90.Fill(recoKESkim[len(recoKESkim)-1])
          if recoZposSkim[len(recoZposSkim) -1 ] < 60 and recoZposSkim[len(recoZposSkim) -1 ] > 30.:
              hInteractingKE60.Fill(recoKESkim[len(recoKESkim)-1])
          if recoZposSkim[len(recoZposSkim) -1 ] < 30:
              hInteractingKE30.Fill(recoKESkim[len(recoKESkim)-1])






XS    = calculateXSPlot(hInteractingKE   , hIncidentKE    , "XS")
XS30  = calculateXSPlot(hInteractingKE30 , hIncidentKE30  , "XS30")
XS60  = calculateXSPlot(hInteractingKE60 , hIncidentKE60  , "XS60")
XS90  = calculateXSPlot(hInteractingKE90 , hIncidentKE90  , "XS90")



outFile = TFile(outName,"recreate")
outFile.cd()

hInteractingKEComp.Write("hInteractingKEComp",TObject.kWriteDelete)  
hIncidentKEComp.Write("hIncidentKEComp",TObject.kWriteDelete)  

hInteractingKE.Write()
hIncidentKE.Write()
XS.Write()

hInteractingKE30.Write()
hIncidentKE30.Write()
XS30.Write()

hInteractingKE60.Write()
hIncidentKE60.Write()
XS60.Write()

hInteractingKE90.Write()
hIncidentKE90.Write()
XS90.Write()

outFile.Write()
outFile.Close()


'''

'''
