from ROOT import *
import ROOT as root
import numpy as np
import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument("muon"     , nargs='?', default = 1., type = float, help="insert fileName")
parser.add_argument("electron" , nargs='?', default = 1., type = float, help="insert fileName")
args     = parser.parse_args()
changeMu = args.muon
changeE  = args.electron


gStyle.SetOptStat(0)

########################################################################
########################    MC Part   ##################################
########################################################################

#pionInBeam100A = 0.87 # 87.4% pions
muonInBeam100A = changeMu*0.037  #  3.7% muons
elecInBeam100A = changeE*0.089  #  8.9% electrons



pionInBeam100A = 1. - muonInBeam100A - elecInBeam100A


# Electron to Pion and Muon to Pion Ratio
elecScale = elecInBeam100A/pionInBeam100A
muonScale = muonInBeam100A/pionInBeam100A

outFileName = "bkgFiles/BkgSub_"+str(changeMu)+"muons_"+str(changeE)+"electrons_100A.root"
#outFileName = "BkgSub_"+str(changeMu)+"muons_"+str(changeE)+"electrons_100A.root"

pionMC_FileName = "/Volumes/Seagate/Elena/TPC/MC100A_Pions.root"
muonMC_FileName = "/Volumes/Seagate/Elena/TPC/MC100A_Muon.root"
elecMC_FileName = "/Volumes/Seagate/Elena/TPC/MC100A_Electron.root"


# Get Monte Carlo files
interactingPlotString = "RecoXSAll/hRecoInteractingKE"
incidentPlotString    = "RecoXSAll/hRecoIncidentKE"
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




# Let's assign a color scheme
pionMC_Int.SetFillColor(9)
secoMC_Int.SetFillColor(kRed-2)
muonMC_Int.SetFillColor(41)
elecMC_Int.SetFillColor(40)    
pionMC_Inc.SetFillColor(9)    
secoMC_Inc.SetFillColor(kRed-2)
muonMC_Inc.SetFillColor(41)
elecMC_Inc.SetFillColor(40)   



legend = TLegend(.54,.52,.84,.70);
legend.AddEntry(pionMC_Int,"MC 100A pions");
legend.AddEntry(secoMC_Int,"MC 100A secondaries");
legend.AddEntry(muonMC_Int,"MC 100A muons");
legend.AddEntry(elecMC_Int,"MC 100A electrons");


#Scale according to beam composition, both interacting and incident plots
elecMC_Int.Scale(elecScale)
elecMC_Inc.Scale(elecScale)
muonMC_Int.Scale(muonScale)
muonMC_Inc.Scale(muonScale)


# Form staggered plots for incident
interactingStack100A = THStack("interactingStack100A", "Interacting MC #pi/#mu/e; Interacting K.E. [MeV]; Entries per 50 MeV");
interactingStack100A.Add(elecMC_Int )
interactingStack100A.Add(muonMC_Int )
interactingStack100A.Add(secoMC_Int )
interactingStack100A.Add(pionMC_Int )

# Form staggered plots for incident
incidentStack100A = THStack("incidentStack100A", "Incident MC #pi/#mu/e; Incident K.E. [MeV]; Entries per 50 MeV");
incidentStack100A.Add(elecMC_Inc )
incidentStack100A.Add(muonMC_Inc )
incidentStack100A.Add(secoMC_Inc )
incidentStack100A.Add(pionMC_Inc )

# Staggered plots by hand
totHisto_Int = pionMC_Int.Clone("totHisto_Int")
totHisto_Inc = pionMC_Inc.Clone("totHisto_Inc")
for i in xrange(pionMC_Int.GetSize()):
    totHisto_Int.SetBinContent(i, muonMC_Int.GetBinContent(i)+elecMC_Int.GetBinContent(i)+ pionMC_Int.GetBinContent(i) + secoMC_Int.GetBinContent(i))
    totHisto_Inc.SetBinContent(i, muonMC_Inc.GetBinContent(i)+elecMC_Inc.GetBinContent(i)+ pionMC_Inc.GetBinContent(i) + secoMC_Inc.GetBinContent(i))
    totHisto_Int.SetBinError(i, TMath.Sqrt(muonMC_Int.GetBinContent(i)+elecMC_Int.GetBinContent(i)+ pionMC_Int.GetBinContent(i) + secoMC_Int.GetBinContent(i)))
    totHisto_Inc.SetBinError(i, TMath.Sqrt(muonMC_Inc.GetBinContent(i)+elecMC_Inc.GetBinContent(i)+ pionMC_Inc.GetBinContent(i) + secoMC_Inc.GetBinContent(i)))

xsMC = pionMC_Int.Clone("XS_PionMCOnly")
xsMC.Scale(101.10968)
xsMC.Divide(pionMC_Inc)   


pion_Content_Int = pionMC_Int.Clone("pion_Content_Int_100A")
pion_Content_Int.Sumw2()
totHisto_Int.Sumw2()
pion_Content_Int.Divide(totHisto_Int)   


pion_Content_Inc = pionMC_Inc.Clone("pion_Content_Inc_100A")
pion_Content_Inc.Sumw2()
totHisto_Inc.Sumw2()
pion_Content_Inc.Divide(totHisto_Inc)   

moveXS = pion_Content_Int.Clone("move_XS_100A")
moveXS.Divide(pion_Content_Inc)   
#moveXS.Sumw2()

xsMC             .SetFillColor(kWhite) 
pion_Content_Int .SetFillColor(kWhite) 
pion_Content_Inc .SetFillColor(kWhite) 
moveXS           .SetFillColor(kWhite) 


## Check Staggered Plots Make Sense
c0 = TCanvas("c0","c0",1200,600)
c0.Divide(2,1)
p1c0 = c0.cd(1)
p1c0.SetGrid()
pion_Content_Int.Draw("pe")

p2c0 = c0.cd(2)
p2c0.SetGrid()
c0.Update()
pion_Content_Inc.Draw("pe")
                           
## Check Staggered Plots Make Sense
c0C = TCanvas("c0C","c0C",1200,600)
c0C.Divide(2,1)
p1c0C = c0C.cd(1)
p1c0C.SetGrid()
p1c0C.Update()
xsMC.Draw("pe")
p2c0C = c0C.cd(2)
p2c0C.SetGrid()
moveXS.Draw("pe")
c0C.Update()
     
                                


#####################################################################
#######################    Save to File   ###########################
#####################################################################


outFile = TFile(outFileName,"recreate")
outFile.cd()

xsMC             .Write() 
pion_Content_Int .Write() 
pion_Content_Inc .Write() 
moveXS           .Write() 


outFile.Write()
outFile.Close()

#raw_input()

