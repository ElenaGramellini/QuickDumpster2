from ROOT import *
import os
import math

gStyle.SetOptStat(1101)

fileKaonData   = TFile('KaonData_dEdXPlot.root' )
fileKaonMC     = TFile('KaonMC_dEdXPlot.root' )

cPida = TCanvas("cPida","cPida",600,600)
cPida.cd()
cPida.SetGrid()

hDataKaonataPitchC   = fileKaonData.Get( "hRecoPitch" )
hDataKaonataPitch = hDataKaonataPitchC.Clone("Reco_Pitch_Data")
hDataKaonataPitch.SetLineColor(kBlack);
hDataKaonataPitch.SetMarkerColor(kBlack);
hDataKaonataPitch.SetMarkerStyle(8);


hMCKaonataPitchC   = fileKaonMC.Get( "hRecoPitch" )
hMCKaonataPitch = hMCKaonataPitchC.Clone("Reco_Pitch_MC")
hMCKaonataPitch.SetLineColor(kRed);


hDataKaonataPitch.Scale(1./hDataKaonataPitch.Integral())
hMCKaonataPitch.Scale(1./hMCKaonataPitch.Integral())

hMCKaonataPitch.SetTitle("Track Pitch; Track Pitch [cm]; Entries per 0.25 mm")
hMCKaonataPitch.GetXaxis().SetRangeUser(0,2.)
hMCKaonataPitch.GetYaxis().SetTitleOffset(1.5)
hMCKaonataPitch.Draw("histo")
hDataKaonataPitch.Draw("pe1sames")


legend = TLegend(.44,.52,.74,.75)
legend.AddEntry(hDataKaonataPitch,"Kaon Data Pitch")
legend.AddEntry(hMCKaonataPitch  ,"Kaon MC Pitch")
#legend.AddEntry(hProtonPIDA,"Protons")
legend.Draw("same")

raw_input()  
