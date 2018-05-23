from ROOT import *
import ROOT as root
import numpy as np
import argparse
import os

gStyle.SetOptStat(0)

outFileName = "Eff_Correction_WithBoundaries.root"

effFileName = "Eff_Correction.root"
effFile     = TFile.Open(effFileName)
effC_XS_45   = effFile.Get("move_XS_45")
effC_XS_All  = effFile.Get("move_XS_All")

dataFileName  = "../BkgSub/BkgSubWithBuoundaries.root"
dataFile      = TFile.Open(dataFileName)
dataC_XS  = dataFile.Get("XS_BkgSub")


XS_Eff_45 = dataC_XS.Clone("XS_Eff_45")
XS_Eff_45.Multiply(effC_XS_45)

XS_Eff_All = dataC_XS.Clone("XS_Eff_All")
XS_Eff_All.Multiply(effC_XS_All)


## Check Staggered Plots Make Sense
c0 = TCanvas("c0","c0",600,600)
p1c0 = c0.cd(1)
p1c0.SetGrid()

#dataC_XS.SetLineColor(kB)
XS_Eff_45   .SetLineColor(kBlack)
XS_Eff_All  .SetLineColor(kRed)

dataC_XS.Draw("pe")
XS_Eff_45   .Draw("pesame")
XS_Eff_All  .Draw("pesame")


XS_Eff     = XS_Eff_45.Clone("XS_Eff")
XS_Eff_Max = XS_Eff_45.Clone("XS_Eff_Max")
XS_Eff_Min = XS_Eff_45.Clone("XS_Eff_Min")

for i in xrange(XS_Eff_45.GetSize()):
    XS_values = []
    XS_values.append(XS_Eff_45.GetBinContent(i))
    XS_values.append(XS_Eff_All.GetBinContent(i))

    XS_Eff_Max.SetBinContent(i, max(XS_values))
    XS_Eff_Min.SetBinContent(i, min(XS_values))
    XS_Eff_Max.SetBinError(i, 0)
    XS_Eff_Min.SetBinError(i, 0)


## Check Staggered Plots Make Sense
c1 = TCanvas("c1","c1",600,600)
p1c1 = c1.cd(1)
p1c1.SetGrid()

XS_Eff_Max.SetLineColor(kBlack)
XS_Eff_Min.SetLineColor(kBlack)
XS_Eff       .SetLineColor(kBlue)

XS_Eff_Max.SetFillColor(0)
XS_Eff_Min.SetFillColor(0)
XS_Eff       .SetFillColor(0)
XS_Eff       .SetLineWidth(2)


XS_Eff.GetYaxis().SetRangeUser(0,3.5)
XS_Eff.GetXaxis().SetRangeUser(0,1000)

XS_Eff     .Draw("pe")
XS_Eff_45.Draw("pesame")
XS_Eff_All.Draw("pesame")
XS_Eff_Max.Draw("histosame")
XS_Eff_Min.Draw("histosame")

outFile = TFile(outFileName,"recreate")
outFile.cd()

XS_Eff     .Write() 
XS_Eff_Max .Write() 
XS_Eff_Min .Write() 

outFile.Write()
outFile.Close()

raw_input()

