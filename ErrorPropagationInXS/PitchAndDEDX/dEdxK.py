from ROOT import *
import os
import math

gStyle.SetOptStat(0)
gStyle.SetOptFit(0)

filePionData   = TFile('KaonData_dEdXPlot.root' )
filePionMC     = TFile('KaonMC_dEdXPlot.root' )


cPida = TCanvas("cPida","cPida",600,600)
cPida.cd()
cPida.SetGrid()

hDataPionataDEdXC   = filePionData.Get( "hRecodEdX" )
hDataPionataDEdX = hDataPionataDEdXC.Clone("Reco_DEdX_Data")
hDataPionataDEdX.SetLineColor(kBlack);
hDataPionataDEdX.SetMarkerColor(kBlack);
hDataPionataDEdX.SetMarkerStyle(8);


hMCPionataDEdXC   = filePionMC.Get( "hRecodEdX" )
hMCPionataDEdX = hMCPionataDEdXC.Clone("Reco_DEdX_MC")
hMCPionataDEdX.SetLineColor(kBlue);


hDataPionataDEdX.Scale(1./hDataPionataDEdX.Integral())
hMCPionataDEdX.Scale(1./hMCPionataDEdX.Integral())

hMCPionataDEdX.SetTitle("; Track dE/dX [MeV/cm]; Entries per 0.25 MeV/cm")
hMCPionataDEdX.GetXaxis().SetRangeUser(0,20.)
hMCPionataDEdX.Draw("histo")
hDataPionataDEdX.Draw("pe1sames")


data_dedx_landau = TF1("data_dedx_landau","landau",1.0, 40);
data_dedx_landau.SetLineWidth(2)
mc_dedx_landau   = TF1("data_dedx_landau","landau",1.0, 40);
mc_dedx_landau.SetLineColor(kAzure+9)
mc_dedx_landau.SetLineWidth(2)

print "-----------------> DATA  "
hDataPionataDEdX.Fit(data_dedx_landau,"R+","0",1.0 , 40);
print "-----------------> MC  "
hMCPionataDEdX.Fit(mc_dedx_landau,"R+","0",1.0 , 40);

data_dedx_landau.Draw("same")
mc_dedx_landau.Draw("same")

legend = TLegend(0.38,0.65,0.90,0.88);
legend.SetTextAlign(12);
legend.SetHeader("LArIAT Negative Polarity #pi/#mu/e");
legend.SetFillColor(kWhite);
legend.SetLineColor(kWhite);
legend.SetShadowColor(kWhite);
legend.AddEntry(hDataPionataDEdX,"Data")
legend.AddEntry(hMCPionataDEdX  ,"Pion MC")
legend.AddEntry(data_dedx_landau,"Data Fit: MPV = 2.18 #sigma = 0.30");
legend.AddEntry(mc_dedx_landau," MC  Fit: MPV = 2.30 #sigma = 0.25");
#legend.AddEntry(hProtonPIDA,"Protons")
legend.Draw("same")


raw_input()  

