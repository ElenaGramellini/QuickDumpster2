from ROOT import *
import os
import math
import argparse

gStyle.SetOptStat(0)
# Get BeamComposition: percentage of pions, muons and electrons in a 60A beam configuration

fmuonHalf  = TFile.Open("Out_0.5Muons_1.0Electrons.root")
fmuonTwice = TFile.Open("Out_2.0Muons_1.0Electrons.root")
felecHalf  = TFile.Open("Out_1.0Muons_0.5Electrons.root")
felecTwice = TFile.Open("Out_1.0Muons_2.0Electrons.root")
fbasis     = TFile.Open("Out_1.0Muons_1.0Electrons.root")


# Get Interacting and Incident plots
muonHalf   = fmuonHalf .Get("XSMstack")
muonTwice  = fmuonTwice.Get("XSMstack")
elecHalf   = felecHalf .Get("XSMstack")
elecTwice  = felecTwice.Get("XSMstack")
basis      = fbasis    .Get("XSMstack")


muonHalf   .SetLineWidth(2)
muonTwice  .SetLineWidth(2)
elecHalf   .SetLineWidth(2)
elecTwice  .SetLineWidth(2)
basis      .SetLineWidth(4)

muonHalf   .SetFillColor(0)
muonTwice  .SetFillColor(0)
elecHalf   .SetFillColor(0)
elecTwice  .SetFillColor(0)
basis      .SetFillColor(0)

muonHalf   .SetLineColor(kBlue-2)
muonTwice  .SetLineColor(kBlue)
elecHalf   .SetLineColor(kRed-2)
elecTwice  .SetLineColor(kRed)
basis      .SetLineColor(kBlack)

legend = TLegend(.54,.52,.84,.70);
basis.SetFillColor(0);
legend.AddEntry(basis,"Estimated Composition");
legend.AddEntry(muonHalf,"Muons x 2");
legend.AddEntry(muonTwice,"Muons x 0.5");
legend.AddEntry(elecTwice,"Electrons x 2");
legend.AddEntry(elecHalf,"Electrons x 0.5");


              
c60XSM = TCanvas("c60XSM" ,"XSM Contributions" ,200 ,10 ,600 ,600)
c60XSM.cd()
c60XSM.SetGrid()

basis.Draw("pe")
muonHalf   .Draw("pesame")
muonTwice  .Draw("pesame")
elecHalf   .Draw("pesame")
elecTwice  .Draw("pesame")
#basis      .Draw("pesame")

legend.Draw("same")

raw_input()  



