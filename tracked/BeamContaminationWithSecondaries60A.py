from ROOT import *
import os
import math
import argparse

gStyle.SetOptStat(0)

parser = argparse.ArgumentParser()
parser.add_argument("muon"   , nargs='?', default = 1., type = float, help="insert fileName")
parser.add_argument("electron"   , nargs='?', default = 1., type = float, help="insert fileName")
args    = parser.parse_args()
changeMuon      = args.muon
changeElectron  = args.electron

# Get BeamComposition: percentage of pions, muons and electrons in a 60A beam configuration
#                       The beam at 60A is 
#pionInBeam60A = 0.642  # 68.8% pions
#muonInBeam60A = 0.092  #  4.6% muons
#elecInBeam60A = 0.266  # 26.6% electrons


#pionInBeam60A = 0.688  # 68.8% pions
muonInBeam60A = 0.046  #  4.6% muons
elecInBeam60A = 0.266  # 26.6% electrons

#changeMuon     = 1.
#changeElectron = 1.
muonInBeam60A = changeMuon*muonInBeam60A
elecInBeam60A = changeElectron*elecInBeam60A
pionInBeam60A = 1. - elecInBeam60A - muonInBeam60A
# Electron to Pion and Muon to Pion Ratio
elecScale = elecInBeam60A/pionInBeam60A
muonScale = muonInBeam60A/pionInBeam60A


pionMC_FileName = "/Volumes/Seagate/Elena/TPC/XSMCPionWithSecondaries60A_histo.root"
muonMC_FileName = "/Volumes/Seagate/Elena/TPC/MC60A_Muon.root"
elecMC_FileName = "/Volumes/Seagate/Elena/TPC/MC60A_Electron.root"


# Get Monte Carlo files
interactingPlotString = "RecoXS/hRecoInteractingKE"
incidentPlotString    = "RecoXS/hRecoIncidentKE"
pionMC_File   = TFile.Open(pionMC_FileName)
muonMC_File   = TFile.Open(muonMC_FileName)
elecMC_File   = TFile.Open(elecMC_FileName)


# Get Interacting and Incident plots
pionMC_Int  = pionMC_File.Get("RecoXSPionOnly/hRecoInteractingKE")
secoMC_Int  = pionMC_File.Get("RecoXSSec/hRecoInteractingKE")
muonMC_Int  = muonMC_File.Get(interactingPlotString)
elecMC_Int  = elecMC_File.Get(interactingPlotString)
pionMC_Inc  = pionMC_File.Get("RecoXSPionOnly/hRecoIncidentKE")
secoMC_Inc  = pionMC_File.Get("RecoXSSec/hRecoIncidentKE")
muonMC_Inc  = muonMC_File.Get(incidentPlotString)
elecMC_Inc  = elecMC_File.Get(incidentPlotString)




# Let's assign a color scheme --> check color scheme is the same as G4Beamline

pionMC_Int.SetFillColor(9)
secoMC_Int.SetFillColor(kRed-2)
muonMC_Int.SetFillColor(41)
elecMC_Int.SetFillColor(40)    
pionMC_Inc.SetFillColor(9)    
secoMC_Inc.SetFillColor(kRed-2)
muonMC_Inc.SetFillColor(41)
elecMC_Inc.SetFillColor(40)   



legend = TLegend(.54,.52,.84,.70);
legend.AddEntry(pionMC_Int,"MC 60A pions");
legend.AddEntry(secoMC_Int,"MC 60A secondaries");
legend.AddEntry(muonMC_Int,"MC 60A muons");
legend.AddEntry(elecMC_Int,"MC 60A electrons");


#Scale according to beam composition, both interacting and incident plots
elecMC_Int.Scale(elecScale)
elecMC_Inc.Scale(elecScale)
muonMC_Int.Scale(muonScale)
muonMC_Inc.Scale(muonScale)

 


# Form staggered plots for incident
interactingStack60A = THStack("interactingStack60A", "Interacting MC #pi/#mu/e; Interacting K.E. [MeV]; Entries per 50 MeV");
interactingStack60A.Add(elecMC_Int )
interactingStack60A.Add(muonMC_Int )
interactingStack60A.Add(secoMC_Int )
interactingStack60A.Add(pionMC_Int )

# Form staggered plots for incident
incidentStack60A = THStack("incidentStack60A", "Incident MC #pi/#mu/e; Incident K.E. [MeV]; Entries per 50 MeV");
incidentStack60A.Add(elecMC_Inc )
incidentStack60A.Add(muonMC_Inc )
incidentStack60A.Add(secoMC_Inc )
incidentStack60A.Add(pionMC_Inc )

# Staggered plots by hand
totHisto_Int = pionMC_Int.Clone("totHisto_Int")
totHisto_Inc = pionMC_Inc.Clone("totHisto_Inc")
for i in xrange(pionMC_Int.GetSize()):
    totHisto_Int.SetBinContent(i, muonMC_Int.GetBinContent(i)+elecMC_Int.GetBinContent(i)+ pionMC_Int.GetBinContent(i) + secoMC_Int.GetBinContent(i))
    totHisto_Inc.SetBinContent(i, muonMC_Inc.GetBinContent(i)+elecMC_Inc.GetBinContent(i)+ pionMC_Inc.GetBinContent(i) + secoMC_Inc.GetBinContent(i))


#PionMuE Cross Section
cRecoPiMuEXS = TCanvas("cRecoPiMuEXS" ,"#pi/#mu/e Reconstructed Cross Section" ,200 ,10 ,900 ,900)
cRecoPiMuEXS.Divide(2,2) 
PiMuEXS = totHisto_Int.Clone("MC_PiMuERecoXS")
PiMuEXS.Sumw2()
PiMuEXS.Divide(totHisto_Inc)
PiMuEXS.Scale(101.10968) 
PiMuEXS.SetTitle("#pi/#mu/e MC Reconstructed Cross Section; K.E. [MeV]; Total Hadronic Cross Section per 50 MeV [barn]")
PiMuEXS.Draw("pe")

#PionOnly Cross Section
cRecoPionOnlyXS = TCanvas("cRecoPionOnlyXS" ,"#pi Reconstructed Cross Section" ,200 ,10 ,900 ,900)
cRecoPionOnlyXS.Divide(2,2) 
PionOnlyXS = pionMC_Int.Clone("MC_PionOnlyRecoXS")
PionOnlyXS.Sumw2()
PionOnlyXS.Divide(pionMC_Inc)
PionOnlyXS.Scale(101.10968) 
PionOnlyXS.SetTitle("#pi MC Reconstructed Cross Section; K.E. [MeV]; Total Hadronic Cross Section per 50 MeV [barn]")
PionOnlyXS.Draw("pe")


#PionContent
cPion60A = TCanvas("cPion60A" ,"Plots Overlay" ,200 ,10 ,900 ,900)
cPion60A.Divide(2,2) 
p1 = cPion60A.cd(1)
p1.SetGrid()
pionContent_Int = pionMC_Int.Clone("pionContent_Int")
pionContent_Int.Sumw2()
pionContent_Int.Divide(totHisto_Int)
pionContent_Int.Draw("")
p2 = cPion60A.cd(2)
p2.SetGrid()
pionContent_Inc = pionMC_Inc.Clone("pionContent_Inc")
pionContent_Inc.Sumw2()
pionContent_Inc.Divide(totHisto_Inc)
pionContent_Inc.Draw("")
cPion60A.SetGrid()
cPion60A.Update()


##Plot Staggered plots
p3 = cPion60A.cd(3)
p3.SetGrid()
interactingStack60A.Draw("histo")
legend.Draw("same")
p4 = cPion60A.cd(4)
p4.SetGrid()
incidentStack60A.Draw("histo")
legend.Draw("same")
cPion60A.Update()

cHistos = TCanvas("cHistos60A" ,"Plots Overlay" ,200 ,10 ,1200 ,600)
##Plot Staggered plots
cHistos.Divide(2,1)
p3s = cHistos.cd(1)
p3s.SetGrid()
interactingStack60A.Draw("histo")
legend.Draw("same")
p4s = cHistos.cd(2)
p4s.SetGrid()
incidentStack60A.Draw("histo")
legend.Draw("same")
cPion60A.Update()


#C^{\pi MC}_{Interacting} 

#PionContent
cCorrectionInt60A = TCanvas("cCorrectionInt60A" ,"Plots Overlay" ,200 ,10 ,600 ,600)
cCorrectionInt60A.SetGrid()
pionContent_Int.SetTitle("Background Correction, Interacting; Kinetic Energy [MeV];C^{#pi MC}_{Interacting}")
pionContent_Int.GetXaxis().SetRangeUser(0,1200)
pionContent_Int.Draw("pe")
cCorrectionInt60A.Update()

cCorrectionInc60A = TCanvas("cCorrectionInc60A" ,"Plots Overlay" ,200 ,10 ,600 ,600)
cCorrectionInc60A.SetGrid()
pionContent_Inc.SetTitle("Background Correction, Incident; Kinetic Energy [MeV];C^{#pi MC}_{Incident}")
pionContent_Inc.GetXaxis().SetRangeUser(0,1200)
pionContent_Inc.Draw("pe")
cCorrectionInc60A.Update()

fileName = "Out_"+str(changeMuon)+"Muons_"+str(changeElectron)+"Electrons_60A.root"
outFile = TFile(fileName,"recreate")
outFile.cd()
pionContent_Int.Write("backgroundCorrection_Int60A",TObject.kWriteDelete)
pionContent_Inc.Write("backgroundCorrection_Inc60A",TObject.kWriteDelete)
PiMuEXS.Write("MC_PiMuERecoXS60A",TObject.kWriteDelete)
PionOnlyXS.Write("MC_PionOnlyRecoXS60A",TObject.kWriteDelete)
outFile.Write()
outFile.Close()






raw_input()  


