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

fnameTxT   = "/Users/elenag/Desktop/LArIATTrueCrossSec/KaonPlusG4.txt"

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

MCFile  = root.TFile("Final.root")
stat = MCFile.Get("XS_StatOnly")
sys  = MCFile.Get("grXS")


sys .SetLineWidth(2)
stat .SetMarkerStyle(22)
stat .SetMarkerSize(1.0)
sys.SetTitle("; Kinetic Energy [MeV]; #sigma^{K}_{TOT} per 50 MeV [barn]")
sys.GetXaxis().SetRangeUser(0,1200.)
sys.GetYaxis().SetRangeUser(0,1.5)


cXS = TCanvas("cXS","cXS",600,600)
cXS.SetGrid()
sys.Draw("AP")
gr . Draw ( "PL" ) ;
stat.Draw("e1same")
lariatHead.DrawLatex(0.6,0.90,"LArIAT Preliminary");
legendXS = TLegend(.40,.68,.86,.86);
legendXS.AddEntry(gr,"Geant4 Prediction ")
legendXS.AddEntry(stat,"Kaon Data Stat Only");
legendXS.AddEntry(sys ,"Kaon Data Stat and Sys");
legendXS.Draw("same")
cXS.Update()
cXS.SaveAs("TheMoneyPlotK.pdf")



raw_input()

