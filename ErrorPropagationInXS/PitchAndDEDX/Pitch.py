from ROOT import *
import os
import math

gStyle.SetOptStat(1101)

filePionData   = TFile('PionData100A_dEdXPlot.root' )
filePionMC     = TFile('PionMC100A_dEdXPlot.root' )


cPida = TCanvas("cPida","cPida",600,600)
cPida.cd()
cPida.SetGrid()

hDataPionataPitchC   = filePionData.Get( "hRecoPitch" )
hDataPionataPitch = hDataPionataPitchC.Clone("Reco_Pitch_Data")
hDataPionataPitch.SetLineColor(kBlack);
hDataPionataPitch.SetMarkerColor(kBlack);
hDataPionataPitch.SetMarkerStyle(8);


hMCPionataPitchC   = filePionMC.Get( "hRecoPitch" )
hMCPionataPitch = hMCPionataPitchC.Clone("Reco_Pitch_MC")
hMCPionataPitch.SetLineColor(kRed);


hDataPionataPitch.Scale(1./hDataPionataPitch.Integral())
hMCPionataPitch.Scale(1./hMCPionataPitch.Integral())

hMCPionataPitch.SetTitle("Track Pitch; Track Pitch [cm]; Entries per 0.25 mm")
hMCPionataPitch.GetXaxis().SetRangeUser(0,2.)
hMCPionataPitch.GetYaxis().SetTitleOffset(1.3)
hMCPionataPitch.Draw("histo")
hDataPionataPitch.Draw("pe1sames")


legend = TLegend(.44,.52,.74,.75)
legend.AddEntry(hDataPionataPitch,"Data Pitch")
legend.AddEntry(hMCPionataPitch  ,"Pion MC Pitch")
#legend.AddEntry(hProtonPIDA,"Protons")
legend.Draw("same")

raw_input()  
