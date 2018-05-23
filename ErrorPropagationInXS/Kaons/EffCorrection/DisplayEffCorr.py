from ROOT import *
import ROOT as root
import numpy as np
import argparse
import os

gStyle.SetOptStat(0)

inFileNameA  = "Eff_Correction.root"


inFileA  = TFile.Open(inFileNameA)

eff_Corr_All_Int = inFileA.Get("eff_Corr_All_Int")
eff_Corr_All_Inc = inFileA.Get("eff_Corr_All_Inc")
eff_Corr_45_Int  = inFileA.Get("eff_Corr_45_Int")
eff_Corr_45_Inc  = inFileA.Get("eff_Corr_45_Inc")

err_Int   = eff_Corr_All_Int.Clone("err_Int")
err_Inc   = eff_Corr_All_Int.Clone("err_Inc")


err_Int   .SetFillColor(kRed) 
err_Inc   .SetFillColor(kRed) 

err_Int   .SetLineColor(kRed) 
err_Inc   .SetLineColor(kRed) 

err_Int   .SetMarkerColor(kRed) 
err_Inc   .SetMarkerColor(kRed) 

eff_Corr_45_Int   .SetLineColor(kBlue) 
eff_Corr_45_Inc  .SetLineColor(kBlue) 



for i in xrange(eff_Corr_All_Int.GetSize()):
    err_Int  .SetBinContent(i,float(eff_Corr_All_Int .GetBinContent(i) + eff_Corr_45_Int .GetBinContent(i)) /2. )
    err_Inc  .SetBinContent(i,float(eff_Corr_All_Inc .GetBinContent(i) + eff_Corr_45_Inc .GetBinContent(i)) /2. )
    err_Int  .SetBinError(i,TMath.Abs(float(eff_Corr_All_Int .GetBinContent(i) - eff_Corr_45_Int .GetBinContent(i)))/2. )
    err_Inc  .SetBinError(i,TMath.Abs(float(eff_Corr_All_Inc .GetBinContent(i) - eff_Corr_45_Inc .GetBinContent(i)))/2. )



for i in xrange(40):
    if i < 5 or i > 16:
        err_Int  .SetBinContent(i,-100)
        err_Inc  .SetBinContent(i,-100)
        eff_Corr_45_Int.SetBinContent(i,-100)
        eff_Corr_45_Inc.SetBinContent(i,-100)

## Check Staggered Plots Make Sense
c0 = TCanvas("c0","c0",1200,600)
c0.Divide(2,1)
p1c0 = c0.cd(1)
p1c0.SetGrid()

err_Int.GetYaxis().SetRangeUser(0,1.5)
err_Int.GetXaxis().SetRangeUser(0,1200)
err_Inc.GetYaxis().SetRangeUser(0,1.5)
err_Inc.GetXaxis().SetRangeUser(0,1200)

err_Int.SetTitle(";Kinetic Energy [MeV];#epsilon_{Int}")
err_Inc.SetTitle(";Kinetic Energy [MeV];#epsilon_{Inc}")

err_Int.Draw("pe2")
eff_Corr_45_Int.Draw("pesame")
#eff_Corr_All_Int.Draw("pesame")
legendInt = TLegend(.34,.72,.90,.90)
legendInt.AddEntry(eff_Corr_45_Int,"Eff Correction Interacting Stat Unc")
legendInt.AddEntry(err_Int,"Eff Correction Interacting Syst Unc")
legendInt.Draw("same")

p2c0 = c0.cd(2)
p2c0.SetGrid()
c0.Update()
err_Inc.Draw("pe2")
eff_Corr_45_Inc.Draw("pesame")
#eff_Corr_All_Inc.Draw("pesame")
legendInc = TLegend(.34,.72,.90,.90)
legendInc.AddEntry(eff_Corr_45_Inc,"Eff Correction Interacting Stat Unc")
legendInc.AddEntry(err_Inc,"Eff Correction Interacting Syst Unc")
legendInc.Draw("same")
                           
     


raw_input()

