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

outFileName = "BkgSub_sec_WithDK.root"

#kaonMC_FileName = "/Volumes/Seagate/Elena/TPC/Kaons/MCKaon_Picky.root"
kaonMC_FileName = "/Volumes/Seagate/Elena/TPC/reco_histo_20000.root"

# Get Monte Carlo files
interactingPlotString = "RecoXS/hRecoInteractingKE"
incidentPlotString    = "RecoXS/hRecoIncidentKE"
kaonMC_File   = TFile.Open(kaonMC_FileName)


# Get Interacting and Incident plots
MC_IntDK    = kaonMC_File.Get("RecoXSAll/hRecoInteractingKE_DK") 
kaonMC_Int  = kaonMC_File.Get("RecoXSKaonOnly/hRecoInteractingKE")
secoMC_Int  = kaonMC_File.Get("RecoXSSec/hRecoInteractingKE")
kaonMC_Inc  = kaonMC_File.Get("RecoXSKaonOnly/hRecoIncidentKE")
secoMC_Inc  = kaonMC_File.Get("RecoXSSec/hRecoIncidentKE")

kaonMC_Int.Add(MC_IntDK,-1)

# Let's assign a color scheme
kaonMC_Int.SetFillColor(kMagenta-8)
secoMC_Int.SetFillColor(kRed-2)
kaonMC_Inc.SetFillColor(kMagenta-8)    
secoMC_Inc.SetFillColor(kRed-2)


legend = TLegend(.54,.52,.84,.70);
legend.AddEntry(kaonMC_Int,"MC  kaons");
legend.AddEntry(secoMC_Int,"MC  secondaries");



# Form staggered plots for incident
interactingStack = THStack("interactingStack", "Interacting MC #pi/#mu/e; Interacting K.E. [MeV]; Entries per 50 MeV");
interactingStack.Add(secoMC_Int )
interactingStack.Add(MC_IntDK )
interactingStack.Add(kaonMC_Int )

# Form staggered plots for incident
incidentStack = THStack("incidentStack", "Incident MC #pi/#mu/e; Incident K.E. [MeV]; Entries per 50 MeV");
incidentStack.Add(secoMC_Inc )
incidentStack.Add(kaonMC_Inc )

# Staggered plots by hand
totHisto_Int = kaonMC_Int.Clone("totHisto_Int")
totHisto_Inc = kaonMC_Inc.Clone("totHisto_Inc")
for i in xrange(kaonMC_Int.GetSize()):
    totHisto_Int.SetBinContent(i,  kaonMC_Int.GetBinContent(i) + secoMC_Int.GetBinContent(i) + MC_IntDK.GetBinContent(i))
    totHisto_Inc.SetBinContent(i,  kaonMC_Inc.GetBinContent(i) + secoMC_Inc.GetBinContent(i))
    totHisto_Int.SetBinError(i, TMath.Sqrt( kaonMC_Int.GetBinContent(i) + secoMC_Int.GetBinContent(i) + MC_IntDK.GetBinContent(i)))
    totHisto_Inc.SetBinError(i, TMath.Sqrt( kaonMC_Inc.GetBinContent(i) + secoMC_Inc.GetBinContent(i)))

xsMC = kaonMC_Int.Clone("XS_KaonMCOnly")
xsMC.Scale(101.10968)
xsMC.Divide(kaonMC_Inc)   


kaon_Content_Int = kaonMC_Int.Clone("kaon_Content_Int")
kaon_Content_Int.Sumw2()
totHisto_Int.Sumw2()
kaon_Content_Int.Divide(totHisto_Int)   


kaon_Content_Inc = kaonMC_Inc.Clone("kaon_Content_Inc")
kaon_Content_Inc.Sumw2()
totHisto_Inc.Sumw2()
kaon_Content_Inc.Divide(totHisto_Inc)   

moveXS = kaon_Content_Int.Clone("move_XS")
moveXS.Divide(kaon_Content_Inc)   
#moveXS.Sumw2()

xsMC             .SetFillColor(kWhite) 
kaon_Content_Int .SetFillColor(kWhite) 
kaon_Content_Inc .SetFillColor(kWhite) 
moveXS           .SetFillColor(kWhite) 



                           
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
kaon_Content_Int .Write() 
kaon_Content_Inc .Write() 
moveXS           .Write() 


outFile.Write()
outFile.Close()


for i in xrange(4):
    kaon_Content_Int.SetBinContent(i,0)
    kaon_Content_Int.SetBinError(i,0)
    kaon_Content_Inc.SetBinContent(i,0)
    kaon_Content_Inc.SetBinError(i,0)

for i in xrange(16,40):
    kaon_Content_Int.SetBinContent(i,0)
    kaon_Content_Int.SetBinError(i,0)
    kaon_Content_Inc.SetBinContent(i,0)
    kaon_Content_Inc.SetBinError(i,0)



## Check Staggered Plots Make Sense
c0 = TCanvas("c0","c0",1200,600)
c0.Divide(2,1)
p1c0 = c0.cd(1)
p1c0.SetGrid()
kaon_Content_Int.SetLineColor(kAzure+6)
kaon_Content_Int.SetLineWidth(2)
kaon_Content_Int.SetTitle(";Kinetic Energy [MeV];C^{K MC}_{Interacting}")
kaon_Content_Int.GetXaxis().SetRangeUser(0,1000)
kaon_Content_Int.GetYaxis().SetRangeUser(0.5,1.5)
kaon_Content_Int.Draw("histo][")

p2c0 = c0.cd(2)
p2c0.SetGrid()
c0.Update()
kaon_Content_Inc.SetLineColor(kAzure+6)
kaon_Content_Inc.SetLineWidth(2)
kaon_Content_Inc.SetTitle(";Kinetic Energy [MeV];C^{K MC}_{Incident}")
kaon_Content_Inc.GetXaxis().SetRangeUser(0,1000)
kaon_Content_Inc.GetYaxis().SetRangeUser(0.5,1.5)
kaon_Content_Inc.Draw("histo][")

c0.Update()
c0.SaveAs("KaonBkgSub_WithDK.pdf")
raw_input()

