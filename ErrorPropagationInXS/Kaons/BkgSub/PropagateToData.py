from ROOT import *
import ROOT as root
import numpy as np
import argparse
import os

gStyle.SetOptStat(0)

outFileName = "BkgSubWithBuoundaries.root"

bkgFileName_1_1 = "BkgSub_sec_WithDK.root"
bkgFile_1_1     = TFile.Open(bkgFileName_1_1)
bkgC_XS__1_1 = bkgFile_1_1.Get("move_XS")


dataFileName  = "../StatOnly/XSRaw_StatOnlyUnc_KaonDataPicky.root"
dataFile      = TFile.Open(dataFileName)
dataC_XS_  = dataFile.Get("XS_Out")


XS_BkgSub = dataC_XS_.Clone("XS_BkgSub")
XS_BkgSub.Multiply(bkgC_XS__1_1)

XS_BkgSub_Max = dataC_XS_.Clone("XS_BkgSub_Max")
XS_BkgSub_Min = dataC_XS_.Clone("XS_BkgSub_Min")

for i in xrange(XS_BkgSub.GetSize()):
    XS_values = []
    XS_values.append(XS_BkgSub.GetBinContent(i))

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


XS_BkgSub_Max.SetFillColor(0)
XS_BkgSub_Min.SetFillColor(0)
XS_BkgSub       .SetFillColor(0)

XS_BkgSub       .SetLineWidth(2)


XS_BkgSub.GetYaxis().SetRangeUser(0,3.5)
XS_BkgSub.GetXaxis().SetRangeUser(0,1000)

XS_BkgSub     .Draw("pesame")


outFile = TFile(outFileName,"recreate")
outFile.cd()

XS_BkgSub     .Write() 
XS_BkgSub_Max .Write() 
XS_BkgSub_Min .Write() 

outFile.Write()
outFile.Close()

raw_input()

