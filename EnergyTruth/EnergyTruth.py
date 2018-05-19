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

inFileName = "/Volumes/Seagate/Elena/TPC/XSMCPionWithSecondaries60A_histo.root"
f = root.TFile(inFileName)
trueDE = f.Get("TrueXS/h_DEDEXUniform")
trueDE.GetXaxis().Set(trueDE.GetSize()-2, 0,trueDE.GetXaxis().GetXmax()*0.47)
recoDEMC = trueDE.Clone("recoDEMC")
for i in xrange(recoDEMC.GetSize()):
    recoDEMC.SetBinContent(i,0)
    recoDEMC.SetBinError(i,0)

print trueDE.GetXaxis().GetXmin(), trueDE.GetXaxis().GetXmax()


myTree = f.Get("RecoXSPionOnly/effTree")

outFileName = inFileName[:-5]+"_out.root"
outF = TFile(outFileName,"recreate")
outF.cd()


print myTree.GetEntry()
sillyCount =0 
for entry in myTree:
     sillyCount += 1
     if not sillyCount % 10000:
          print sillyCount
     if sillyCount == 40000:
          break
     # Now you have acess to the leaves/branches of each entry in the tree, e.g.
     recoEnDep     = entry.recoEnDep
     for j in recoEnDep:
         if j > 0.1 and j < 90:
             recoDEMC.Fill(j)


recoDEMC.Scale(1./recoDEMC.Integral())
trueDE.Scale(1./trueDE.Integral())
recoDEMC.SetLineColor(kBlue)
trueDE.SetLineColor(kRed)

c = TCanvas("c","c",600,600)
c.cd()
c.SetGrid()
trueDE.GetXaxis().SetRangeUser(0,3.5)
trueDE.SetTitle("Energy Deposited, MC true and Reco Comparison; Energy Deposited [MeV]")
recoDEMC.Draw("pe")
trueDE.Draw("histosame")
recoDEMC.Draw("histosames")

legendInc = TLegend(.54,.75,.90,.90);
legendInc.AddEntry(trueDE  ,"True MC Energy Deposited");
legendInc.AddEntry(recoDEMC,"Reco MC Energy Deposited");
legendInc.Draw("same")

outFile = TFile("SystematicsEnergyTrueVsRecoMC.root","recreate")
outFile.cd()

trueDE.Write("trueDE",TObject.kWriteDelete)  
recoDEMC.Write("recoDEMC",TObject.kWriteDelete)  

outFile.Write()
outFile.Close()

raw_input()

