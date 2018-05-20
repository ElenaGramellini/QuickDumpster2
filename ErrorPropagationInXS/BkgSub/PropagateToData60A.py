from ROOT import *
import ROOT as root
import numpy as np
import argparse
import os

gStyle.SetOptStat(0)

outFileName = "BkgSubWithBuoundaries_60A.root"

bkgFileName_1_1 = "bkgFiles/BkgSub_1.0muons_1.0electrons_60A.root"
bkgFile_1_1     = TFile.Open(bkgFileName_1_1)
bkgC_XS_60A_1_1 = bkgFile_1_1.Get("move_XS_60A")

bkgFileName_2_1 = "bkgFiles/BkgSub_2.0muons_1.0electrons_60A.root"
bkgFile_2_1     = TFile.Open(bkgFileName_2_1)
bkgC_XS_60A_2_1 = bkgFile_2_1.Get("move_XS_60A")

bkgFileName_1_2 = "bkgFiles/BkgSub_1.0muons_2.0electrons_60A.root"
bkgFile_1_2     = TFile.Open(bkgFileName_1_2)
bkgC_XS_60A_1_2 = bkgFile_1_2.Get("move_XS_60A")

bkgFileName_1_05 = "bkgFiles/BkgSub_1.0muons_0.5electrons_60A.root"
bkgFile_1_05     = TFile.Open(bkgFileName_1_05)
bkgC_XS_60A_1_05 = bkgFile_1_05.Get("move_XS_60A")


dataFileName  = "../StatOnly/XSRaw_StatOnlyUnc_Data60A.root"
dataFile      = TFile.Open(dataFileName)
dataC_XS_60A  = dataFile.Get("XS_Out")


XS_BkgSub = dataC_XS_60A.Clone("XS_BkgSub60A")
XS_BkgSub.Multiply(bkgC_XS_60A_1_1)

XS_BkgSub_2_1 = dataC_XS_60A.Clone("XS_BkgSub_2_1")
XS_BkgSub_2_1.Multiply(bkgC_XS_60A_2_1)

XS_BkgSub_1_2 = dataC_XS_60A.Clone("XS_BkgSub_1_2")
XS_BkgSub_1_2.Multiply(bkgC_XS_60A_1_2)

XS_BkgSub_1_05 = dataC_XS_60A.Clone("XS_BkgSub_1_05")
XS_BkgSub_1_05.Multiply(bkgC_XS_60A_1_05)

XS_BkgSub_Max = dataC_XS_60A.Clone("XS_BkgSub_Max60A")
XS_BkgSub_Min = dataC_XS_60A.Clone("XS_BkgSub_Min60A")

for i in xrange(XS_BkgSub.GetSize()):
    XS_values = []
    XS_values.append(XS_BkgSub.GetBinContent(i))
    XS_values.append(XS_BkgSub_2_1.GetBinContent(i))
    XS_values.append(XS_BkgSub_1_2.GetBinContent(i))
    XS_values.append(XS_BkgSub_1_05.GetBinContent(i))

    XS_BkgSub_Max.SetBinContent(i, max(XS_values))
    XS_BkgSub_Min.SetBinContent(i, min(XS_values))
    XS_BkgSub_Max.SetBinError(i, 0)
    XS_BkgSub_Min.SetBinError(i, 0)


## Check Staggered Plots Make Sense
c0 = TCanvas("c0","c0",600,600)
p1c0 = c0.cd(1)
p1c0.SetGrid()

XS_BkgSub_Max.SetLineColor(kBlack)
XS_BkgSub_Min.SetLineColor(kBlack)

XS_BkgSub       .SetLineColor(kBlue)
XS_BkgSub_2_1   .SetLineColor(kRed+1)
XS_BkgSub_1_2   .SetLineColor(kRed+2)
XS_BkgSub_1_05  .SetLineColor(kRed+3)

XS_BkgSub_Max.SetFillColor(0)
XS_BkgSub_Min.SetFillColor(0)
XS_BkgSub       .SetFillColor(0)
XS_BkgSub_2_1   .SetFillColor(0)
XS_BkgSub_1_2   .SetFillColor(0)
XS_BkgSub_1_05  .SetFillColor(0)

XS_BkgSub       .SetLineWidth(2)
XS_BkgSub_2_1   .SetLineWidth(2)
XS_BkgSub_1_2   .SetLineWidth(2)
XS_BkgSub_1_05  .SetLineWidth(2)

XS_BkgSub.GetYaxis().SetRangeUser(0,3.5)
XS_BkgSub.GetXaxis().SetRangeUser(0,1000)

XS_BkgSub     .Draw("pesame")
XS_BkgSub_2_1 .Draw("histosame")
XS_BkgSub_1_2 .Draw("histosame")
XS_BkgSub_1_05.Draw("histosame")

#XS_BkgSub_Max.Draw("histo")
#XS_BkgSub_Min.Draw("histosame")

outFile = TFile(outFileName,"recreate")
outFile.cd()

XS_BkgSub     .Write() 
XS_BkgSub_Max .Write() 
XS_BkgSub_Min .Write() 

outFile.Write()
outFile.Close()

raw_input()

