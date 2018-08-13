from ROOT import *
import ROOT as root
import numpy as np
import argparse
import os

gStyle.SetOptStat(0)

inFileName60A  = "Eff_Correction_60A.root"
inFileName100A = "Eff_Correction_100A.root"

inFile60A  = TFile.Open(inFileName60A)
inFile100A = TFile.Open(inFileName100A)

eff_Corr_All_Int_60A = inFile60A.Get("eff_Corr_All_Int_60A")
eff_Corr_All_Inc_60A = inFile60A.Get("eff_Corr_All_Inc_60A")
eff_Corr_45_Int_60A  = inFile60A.Get("eff_Corr_45_Int_60A")
eff_Corr_45_Inc_60A  = inFile60A.Get("eff_Corr_45_Inc_60A")

eff_Corr_All_Int_100A = inFile100A.Get("eff_Corr_All_Int_100A")
eff_Corr_All_Inc_100A = inFile100A.Get("eff_Corr_All_Inc_100A")
eff_Corr_45_Int_100A  = inFile100A.Get("eff_Corr_45_Int_100A")
eff_Corr_45_Inc_100A  = inFile100A.Get("eff_Corr_45_Inc_100A")


err_Int_60A   = eff_Corr_All_Int_100A.Clone("err_Int_60A")
err_Inc_60A   = eff_Corr_All_Int_100A.Clone("err_Inc_60A")
err_Int_100A  = eff_Corr_All_Int_100A.Clone("err_Int_100A")
err_Inc_100A  = eff_Corr_All_Int_100A.Clone("err_Inc_100A")

for i in xrange(6):
    eff_Corr_45_Int_100A.SetBinContent(i,-100)
    eff_Corr_45_Inc_100A.SetBinContent(i,-100)

err_Int_60A   .SetFillColor(kRed) 
err_Inc_60A   .SetFillColor(kRed) 
err_Int_100A  .SetFillColor(kRed) 
err_Inc_100A  .SetFillColor(kRed) 

err_Int_60A   .SetLineColor(kRed) 
err_Inc_60A   .SetLineColor(kRed) 
err_Int_100A  .SetLineColor(kRed) 
err_Inc_100A  .SetLineColor(kRed) 

err_Int_60A   .SetMarkerColor(kRed) 
err_Inc_60A   .SetMarkerColor(kRed) 
err_Int_100A  .SetMarkerColor(kRed) 
err_Inc_100A  .SetMarkerColor(kRed) 

eff_Corr_45_Int_60A   .SetLineColor(kBlue) 
eff_Corr_45_Inc_60A  .SetLineColor(kBlue) 
eff_Corr_45_Int_100A  .SetLineColor(kBlue) 
eff_Corr_45_Inc_100A  .SetLineColor(kBlue) 


for i in xrange(eff_Corr_All_Int_100A.GetSize()):
    err_Int_60A  .SetBinContent(i,float(eff_Corr_All_Int_60A .GetBinContent(i) + eff_Corr_45_Int_60A .GetBinContent(i)) /2. )
    err_Inc_60A  .SetBinContent(i,float(eff_Corr_All_Inc_60A .GetBinContent(i) + eff_Corr_45_Inc_60A .GetBinContent(i)) /2. )
    err_Int_100A .SetBinContent(i,float(eff_Corr_All_Int_100A.GetBinContent(i) + eff_Corr_45_Int_100A.GetBinContent(i)) /2. )
    err_Inc_100A .SetBinContent(i,float(eff_Corr_All_Inc_100A.GetBinContent(i) + eff_Corr_45_Inc_100A.GetBinContent(i)) /2. )
    err_Int_60A  .SetBinError(i,TMath.Abs(float(eff_Corr_All_Int_60A .GetBinContent(i) - eff_Corr_45_Int_60A .GetBinContent(i)))/2. )
    err_Inc_60A  .SetBinError(i,TMath.Abs(float(eff_Corr_All_Inc_60A .GetBinContent(i) - eff_Corr_45_Inc_60A .GetBinContent(i)))/2. )
    err_Int_100A .SetBinError(i,TMath.Abs(float(eff_Corr_All_Int_100A.GetBinContent(i) - eff_Corr_45_Int_100A.GetBinContent(i))) /2. )
    err_Inc_100A .SetBinError(i,TMath.Abs(float(eff_Corr_All_Inc_100A.GetBinContent(i) - eff_Corr_45_Inc_100A.GetBinContent(i))) /2. )







## Check Staggered Plots Make Sense
c0 = TCanvas("c0","c0",1200,600)
c0.Divide(2,1)
p1c0 = c0.cd(1)
p1c0.SetGrid()

err_Int_60A.GetYaxis().SetRangeUser(0,1.5)
err_Int_60A.GetXaxis().SetRangeUser(0,1200)
err_Inc_60A.GetYaxis().SetRangeUser(0,1.5)
err_Inc_60A.GetXaxis().SetRangeUser(0,1200)
err_Int_100A.GetYaxis().SetRangeUser(0,1.5)
err_Int_100A.GetXaxis().SetRangeUser(0,1200)
err_Inc_100A.GetYaxis().SetRangeUser(0,1.5)
err_Inc_100A.GetXaxis().SetRangeUser(0,1200)

err_Int_60A.SetTitle(";Kinetic Energy [MeV];#epsilon_{Int}")
err_Inc_60A.SetTitle(";Kinetic Energy [MeV];#epsilon_{Inc}")
err_Int_100A.SetTitle(";Kinetic Energy [MeV];#epsilon_{Int}")
err_Inc_100A.SetTitle(";Kinetic Energy [MeV];#epsilon_{Inc}")


err_Int_60A.Draw("pe2")
eff_Corr_45_Int_60A.Draw("pesame")
#eff_Corr_All_Int_60A.Draw("pesame")
legendInt60 = TLegend(.34,.72,.90,.90)
legendInt60.AddEntry(eff_Corr_45_Int_60A,"Eff Correction Interacting 60A Stat Unc")
legendInt60.AddEntry(err_Int_60A,"Eff Correction Interacting 60A Syst Unc")
legendInt60.Draw("same")

p2c0 = c0.cd(2)
p2c0.SetGrid()
c0.Update()
err_Inc_60A.Draw("pe2")
eff_Corr_45_Inc_60A.Draw("pesame")
#eff_Corr_All_Inc_60A.Draw("pesame")
legendInc60 = TLegend(.34,.72,.90,.90)
legendInc60.AddEntry(eff_Corr_45_Inc_60A,"Eff Correction Incident 60A Stat Unc")
legendInc60.AddEntry(err_Inc_60A,"Eff Correction Incident 60A Syst Unc")
legendInc60.Draw("same")
                           
## Check Staggered Plots Make Sense
c0C = TCanvas("c0C","c0C",1200,600)
c0C.Divide(2,1)
p1c0C = c0C.cd(1)
p1c0C.SetGrid()
p1c0C.Update()
err_Int_100A.Draw("pe2")
eff_Corr_45_Int_100A.Draw("pesame")
#eff_Corr_All_Int_100A.Draw("pesame")
legendInt100 = TLegend(.34,.72,.90,.90)
legendInt100.AddEntry(eff_Corr_45_Int_100A,"Eff Correction Interacting 100A Stat Unc")
legendInt100.AddEntry(err_Int_100A,"Eff Correction Interacting 100A Syst Unc")
legendInt100.Draw("same")

p2c0C = c0C.cd(2)
p2c0C.SetGrid()
err_Inc_100A.Draw("pe2")
eff_Corr_45_Inc_100A.Draw("pesame")
#eff_Corr_All_Inc_100A.Draw("pesame")
legendInc100 = TLegend(.34,.72,.90,.90)
legendInc100.AddEntry(eff_Corr_45_Inc_100A,"Eff Correction Incident 100A Stat Unc")
legendInc100.AddEntry(err_Inc_100A,"Eff Correction Incident 100A Syst Unc")
legendInc100.Draw("same")
c0C.Update()
     


raw_input()

