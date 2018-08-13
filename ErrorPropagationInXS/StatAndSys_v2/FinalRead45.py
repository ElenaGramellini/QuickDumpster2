from ROOT import *
import ROOT as root
import numpy as np
from array import array

gStyle.SetOptStat(0)


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

fnameTxT   = "/Users/elenag/Desktop/LArIATTrueCrossSec/PionMinusG4.txt"

kineticEnergy = []
crossSec      = []
zero          = []


title = ""
with open(fnameTxT) as f:
    for fLine in f.readlines():
        w = fLine.split()
        if is_number(w[0]):
            runIn    = int(w[0])
            ke       = float(w[1])
            xstot       = float(w[4])
            kineticEnergy.append(ke)
            crossSec.append(xstot)
            zero.append(0.)
        else:
            if "for" not in fLine: 
                continue
            title =  fLine[9:]

g4x      = array('f', kineticEnergy )
g4y      = array('f', crossSec)
g4exl    = array('f', zero)
g4exr    = array('f', zero)


nPoints=len(g4x)
gr      = TGraphErrors ( nPoints , g4x , g4y     , g4exl, g4exr )
gr.SetTitle(title+"; Kinetic Energy [MeV]; Cross Section [barn]")
gr . GetXaxis().SetRangeUser(0,1000)
gr . GetYaxis().SetRangeUser(0,2.)
gr . SetLineWidth(2) ;
gr . SetLineColor(kGreen-2) ;
gr . SetFillColor(0)

#gr . Draw ( "APL" ) ;


lariatHead = TLatex();
lariatHead.SetNDC();
lariatHead.SetTextFont(62);
lariatHead.SetTextSize(0.04);
lariatHead.SetTextAlign(40);

MCFile60A  = root.TFile("Final60A.root")
stat60A = MCFile60A.Get("XS60A_StatOnly")
sys60A  = MCFile60A.Get("grXS60A")

MCFile100A = root.TFile("Final100A.root")
stat100A = MCFile100A.Get("XS100A_StatOnly")
sys100A  = MCFile100A.Get("grXS100A")

true60AF = root.TFile("/Volumes/Seagate/Elena/TPC/AngleCut_0.08334_histo_60A.root")
XS60_45  = true60AF.Get("AngleCutTrueXS/hCrossSection")
true100AF = root.TFile("/Volumes/Seagate/Elena/TPC/AngleCut_0.08334_new_histo.root")
XS100_Int  = true100AF.Get("AngleCutTrueXS083/hInteractingKE")
XS100_Inc  = true100AF.Get("AngleCutTrueXS083/hIncidentKE")
XS100_45 = XS100_Int.Clone("XS100_45")
XS100_45.Scale(101.)
XS100_45.Divide(XS100_Inc)
c333 = TCanvas("c33","c22",800,800)
c333.cd()
XS60_45.SetLineColor(kGreen -2)
XS100_45.SetLineColor(kRed -2)
for i in range(40):
    if i < 10 or i > 23:
        XS100_45.SetBinContent(i,0)
        XS100_45.SetBinError(i,0)
    if i < 4 or i > 9:
        XS60_45.SetBinContent(i,0)
        XS60_45.SetBinError(i,0)
XS_45 = XS60_45.Clone("XS60_45")
XS_45.SetLineWidth(2)
XS_45.Add(XS100_45)
XS_45.Draw("histo")
XS60_45.Draw("pesame")
XS100_45.Draw("pesame")



sys100A.SetLineColor(kBlue)
sys100A.SetLineWidth(2)
sys60A .SetLineWidth(2)
stat60A .SetMarkerStyle(22)
stat100A.SetMarkerStyle(23)
stat60A .SetMarkerSize(1.0)
stat100A.SetMarkerSize(1.0)
sys60A.SetTitle("; Kinetic Energy [MeV]; #sigma^{#pi}_{TOT} per 50 MeV [barn]")
sys100A.SetTitle("; Kinetic Energy [MeV]; #sigma^{#pi}_{TOT} per 50 MeV [barn]")
sys60A.GetXaxis().SetRangeUser(0,1200.)
sys60A.GetYaxis().SetRangeUser(0,2.5)
sys100A.GetXaxis().SetRangeUser(0,1200.)
sys100A.GetYaxis().SetRangeUser(0,2.5)


cXS = TCanvas("cXS","cXS",600,600)
cXS.SetGrid()
sys60A.Draw("AP")
#gr . Draw ( "PL" ) ;
XS_45.Draw("histosame][")
stat60A.Draw("e1same")
sys100A.Draw("P")
stat100A.Draw("e1same")
lariatHead.DrawLatex(0.6,0.90,"LArIAT Preliminary");
legendXS = TLegend(.30,.68,.86,.86);
stat60A.SetLineColor(kRed)
stat100A.SetLineColor(kBlue)
legendXS.AddEntry(XS_45,"FTFP_BERT Geant4 Prediction Angle > 5.0 Deg")
legendXS.AddEntry(stat60A ,"-60A Data (Stat. #oplus Syst Unc.)");
#legendXS.AddEntry(sys60A  ,"-60A Data Stat and Sys");
legendXS.AddEntry(stat100A,"-100A Data (Stat. #oplus Syst Unc.)");
#legendXS.AddEntry(sys100A ,"-100A Data Stat and Sys");
legendXS.Draw("same")
cXS.Update()
cXS.SaveAs("TheMoneyPlot.pdf")


cXS100A = TCanvas("cXS100A","cXS100A",600,600)
cXS100A.SetGrid()
sys100A.Draw("AP")
#gr . Draw ( "PL" ) ;
XS_45.Draw("histosame][")
stat100A.Draw("e1same")
lariatHead.DrawLatex(0.6,0.90,"LArIAT Preliminary");
legendXS100A = TLegend(.30,.68,.86,.86);
legendXS100A.AddEntry(XS_45,"FTFP_BERT Geant4 Prediction Angle > 5.0 Deg")
legendXS100A.AddEntry(stat100A ,"-100A Data (Stat. #oplus Syst Unc.)");
#legendXS100A.AddEntry(sys100A ,"-100A Data Stat and Sys");
legendXS100A.Draw("same")
cXS100A.Update()
cXS100A.SaveAs("TheMoneyPlot100A.pdf")


cXS60A = TCanvas("cXS60A","cXS60A",600,600)
cXS60A.SetGrid()
sys60A.Draw("AP")
XS_45.Draw("histosame][")
#gr . Draw ( "PL" ) ;
stat60A.Draw("e1same")
lariatHead.DrawLatex(0.6,0.90,"LArIAT Preliminary");
legendXS60A = TLegend(.30,.68,.86,.86);
legendXS60A.AddEntry(XS_45,"FTFP_BERT Geant4 Prediction Angle > 5.0 Deg")
legendXS60A.AddEntry(stat60A ,"-60A Data (Stat. #oplus Syst Unc.)");
#legendXS60A.AddEntry(stat60A,"-60A Data Stat Only");
#legendXS60A.AddEntry(sys60A ,"-60A Data Stat and Sys");
legendXS60A.Draw("same")
cXS60A.Update()
cXS60A.SaveAs("TheMoneyPlot60A.pdf")



raw_input()

