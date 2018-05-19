from ROOT import *
import os
import math
import argparse

gStyle.SetOptStat(0)
# Get BeamComposition: percentage of pions, muons and electrons in a 60A beam configuration

effCorrectionFile  = TFile.Open("EfficiencyCorrectionPions60A.root")


# Interacting and Incident Names
interactingName = "effCorr_Int_NoFilt"
incidentName    = "effCorr_Inc_NoFilt"


# Interacting Plot
eff_Int   = effCorrectionFile .Get(interactingName)
eff_Inc   = effCorrectionFile .Get(incidentName)


eff_Int  .SetLineWidth(2)
eff_Inc  .SetLineWidth(2)
eff_Int  .SetLineColor(kMagenta-10)
eff_Inc  .SetLineColor(kMagenta-10)
eff_Int  .SetFillColor(kMagenta-10)
eff_Inc  .SetFillColor(kMagenta-10)

c60A_Int_Multiple = TCanvas("c60A_Int_Multiple" ,"XSM Contributions" ,200 ,10 ,1200 ,600)
c60A_Int_Multiple.Divide(2,1)
p1 = c60A_Int_Multiple.cd(1)
p1.SetGrid()
eff_Int.Draw("pe")

p2 = c60A_Int_Multiple.cd(2)
p2.SetGrid()
eff_Inc.Draw("pe")

raw_input()  


'''

basis_Int.GetXaxis().SetRangeUser(0,1200.)
basis_Int.GetYaxis().SetRangeUser(0,1.6)
basis_Int.GetYaxis().SetTitleOffset(1.3)

legend = TLegend(.54,.52,.84,.70);
legend.AddEntry(basis_Int,"Estimated #pi content");
legend.AddEntry(muonHalf_Int,"Muons x 2");
legend.AddEntry(muonTwice_Int,"Muons x 0.5");
legend.AddEntry(elecTwice_Int,"Electrons x 2");
legend.AddEntry(elecHalf_Int,"Electrons x 0.5");


              
c60A_Int_Multiple = TCanvas("c60A_Int_Multiple" ,"XSM Contributions" ,200 ,10 ,1200 ,600)
c60A_Int_Multiple.Divide(2,1)
p1 = c60A_Int_Multiple.cd(1)
p1.SetGrid()

basis_Int.Draw("pe")
#basis_Int.Draw("pe")
muonHalf_Int   .Draw("pesame")
muonTwice_Int  .Draw("pesame")
elecHalf_Int   .Draw("pesame")
elecTwice_Int  .Draw("pesame")
#basis_Int      .Draw("pesame")

legend.Draw("same")
c60A_Int_Multiple.Update()


c60A_Int_Multiple.cd(2)
p2 = c60A_Int_Multiple.cd(2)
p2.SetGrid()
Systematic_Int = basis_Int.Clone("Systematic_Int")
binValues = []
for i in xrange(basis_Int.GetSize()):
    binValues.append(basis_Int.GetBinContent(i))
    binValues.append(muonHalf_Int .GetBinContent(i))
    binValues.append(muonTwice_Int.GetBinContent(i))
    binValues.append(elecHalf_Int .GetBinContent(i))
    binValues.append(elecTwice_Int.GetBinContent(i))

    maxValue = max(binValues)
    minValue = min(binValues)
    #print minValue, maxValue
    #print binValues

    sysBinValue = (maxValue+minValue)/2.
    sysBinError = (maxValue-minValue)/2.

    #Fix Some representation problem
    if sysBinValue < 0.001:
        sysBinValue = 0
        sysBinError = 0
    Systematic_Int.SetBinContent(i, sysBinValue)
    Systematic_Int.SetBinError(i, sysBinError)

    binValues = []


Systematic_Int.SetLineColor(kAzure-1)
Systematic_Int.SetFillColor(kAzure-1)
Systematic_Int.Draw("pe3")
basis_Int.Draw("pesame")

legend2 = TLegend(.54,.52,.84,.70);
legend2.AddEntry(basis_Int,"#pi Content Interacting, Stat Only");
legend2.AddEntry(Systematic_Int,"#pi Content Interacting, Systematics");
legend2.Draw("same")

c60A_Int_Multiple.Update()

#############################################################################################################
# Incident Plot
muonHalf_Inc   = fmuonHalf .Get(incidentName)
muonTwice_Inc  = fmuonTwice.Get(incidentName)
elecHalf_Inc   = felecHalf .Get(incidentName)
elecTwice_Inc  = felecTwice.Get(incidentName)
basis_Inc      = fbasis    .Get(incidentName)


muonHalf_Inc   .SetLineWidth(2)
muonTwice_Inc  .SetLineWidth(2)
elecHalf_Inc   .SetLineWidth(2)
elecTwice_Inc  .SetLineWidth(2)
basis_Inc      .SetLineWidth(4)

muonHalf_Inc   .SetFillColor(0)
muonTwice_Inc  .SetFillColor(0)
elecHalf_Inc   .SetFillColor(0)
elecTwice_Inc  .SetFillColor(0)
basis_Inc      .SetFillColor(kAzure+6)
basis_Inc      .SetMarkerColor(kAzure+6)

muonHalf_Inc   .SetLineColor(kBlue-2)
muonTwice_Inc  .SetLineColor(kBlue)
elecHalf_Inc   .SetLineColor(kRed-2)
elecTwice_Inc  .SetLineColor(kRed)
basis_Inc      .SetLineColor(kAzure+6)


basis_Inc.GetXaxis().SetRangeUser(0,1200.)
basis_Inc.GetYaxis().SetRangeUser(0,1.6)
basis_Inc.GetYaxis().SetTitleOffset(1.3)

legend3 = TLegend(.54,.52,.84,.70);
legend3.AddEntry(basis_Inc,"Estimated #pi content");
legend3.AddEntry(muonHalf_Inc,"Muons x 2");
legend3.AddEntry(muonTwice_Inc,"Muons x 0.5");
legend3.AddEntry(elecTwice_Inc,"Electrons x 2");
legend3.AddEntry(elecHalf_Inc,"Electrons x 0.5");


              
c60A_Inc_Multiple = TCanvas("c60A_Inc_Multiple" ,"XSM Contributions" ,200 ,10 ,1200 ,600)
c60A_Inc_Multiple.Divide(2,1)
p1 = c60A_Inc_Multiple.cd(1)
p1.SetGrid()

basis_Inc.Draw("pe")
#basis_Inc.Draw("pe")
muonHalf_Inc   .Draw("pesame")
muonTwice_Inc  .Draw("pesame")
elecHalf_Inc   .Draw("pesame")
elecTwice_Inc  .Draw("pesame")
#basis_Inc      .Draw("pesame")

legend3.Draw("same")
c60A_Inc_Multiple.Update()


c60A_Inc_Multiple.cd(2)
p2 = c60A_Inc_Multiple.cd(2)
p2.SetGrid()
Systematic_Inc = basis_Inc.Clone("Systematic_Inc")
binValues = []
for i in xrange(basis_Inc.GetSize()):
    binValues.append(basis_Inc.GetBinContent(i))
    binValues.append(muonHalf_Inc .GetBinContent(i))
    binValues.append(muonTwice_Inc.GetBinContent(i))
    binValues.append(elecHalf_Inc .GetBinContent(i))
    binValues.append(elecTwice_Inc.GetBinContent(i))

    maxValue = max(binValues)
    minValue = min(binValues)
    #print minValue, maxValue
    #print binValues

    sysBinValue = (maxValue+minValue)/2.
    sysBinError = (maxValue-minValue)/2.
    
    #Fix Some representation problem
    if sysBinValue < 0.001:
        sysBinValue = 0
        sysBinError = 0

    Systematic_Inc.SetBinContent(i, sysBinValue)
    Systematic_Inc.SetBinError(i, sysBinError)

    binValues = []


Systematic_Inc.SetLineColor(kAzure-1)
Systematic_Inc.SetFillColor(kAzure-1)
Systematic_Inc.Draw("pe3")
basis_Inc.Draw("pesame")

legend4 = TLegend(.54,.52,.84,.70);
legend4.AddEntry(basis_Inc,"#pi Content Incident, Stat Only");
legend4.AddEntry(Systematic_Inc,"#pi Content Incident, Systematics");
legend4.Draw("same")

c60A_Inc_Multiple.Update()


c60A_Multiple = TCanvas("c60A_Multiple" ,"XSM Contributions" ,200 ,10 ,1200 ,600)
c60A_Multiple.Divide(2,1)
pM1 =c60A_Multiple.cd(1) 
pM1.SetGrid()
Systematic_Int.Draw("pe3")
basis_Int.Draw("pesame")
legend2.Draw("same")

pM2 =c60A_Multiple.cd(2) 
pM2.SetGrid()
Systematic_Inc.Draw("pe3")
basis_Inc.Draw("pesame")
legend4.Draw("same")
'''




