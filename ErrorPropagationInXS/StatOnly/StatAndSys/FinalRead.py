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
gr . Draw ( "PL" ) ;
stat60A.Draw("e1same")
sys100A.Draw("P")
stat100A.Draw("e1same")
lariatHead.DrawLatex(0.6,0.90,"LArIAT Preliminary");
legendXS = TLegend(.40,.68,.86,.86);
legendXS.AddEntry(gr,"Geant4 Prediction ")
legendXS.AddEntry(stat60A ,"-60A Data Stat Only");
legendXS.AddEntry(sys60A  ,"-60A Data Stat and Sys");
legendXS.AddEntry(stat100A,"-100A Data Stat Only");
legendXS.AddEntry(sys100A ,"-100A Data Stat and Sys");
legendXS.Draw("same")
cXS.Update()
cXS.SaveAs("TheMoneyPlot.pdf")


cXS100A = TCanvas("cXS100A","cXS100A",600,600)
cXS100A.SetGrid()
sys100A.Draw("AP")
gr . Draw ( "PL" ) ;
stat100A.Draw("e1same")
lariatHead.DrawLatex(0.6,0.90,"LArIAT Preliminary");
legendXS100A = TLegend(.40,.68,.86,.86);
legendXS100A.AddEntry(gr,"Geant4 Prediction ")
legendXS100A.AddEntry(stat100A,"-100A Data Stat Only");
legendXS100A.AddEntry(sys100A ,"-100A Data Stat and Sys");
legendXS100A.Draw("same")
cXS100A.Update()
cXS100A.SaveAs("TheMoneyPlot100A.pdf")


cXS60A = TCanvas("cXS60A","cXS60A",600,600)
cXS60A.SetGrid()
sys60A.Draw("AP")
gr . Draw ( "PL" ) ;
stat60A.Draw("e1same")
lariatHead.DrawLatex(0.6,0.90,"LArIAT Preliminary");
legendXS60A = TLegend(.40,.68,.86,.86);
legendXS60A.AddEntry(gr,"Geant4 Prediction ")
legendXS60A.AddEntry(stat60A,"-60A Data Stat Only");
legendXS60A.AddEntry(sys60A ,"-60A Data Stat and Sys");
legendXS60A.Draw("same")
cXS60A.Update()
cXS60A.SaveAs("TheMoneyPlot60A.pdf")



raw_input()

