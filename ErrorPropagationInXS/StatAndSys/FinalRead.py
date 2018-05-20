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




MCFile60A  = root.TFile("Final60A.root")
stat60A = MCFile60A.Get("XS60A_StatOnly")
sys60A  = MCFile60A.Get("grXS60A")

MCFile100A = root.TFile("Final100A.root")
stat100A = MCFile100A.Get("XS100A_StatOnly")
sys100A  = MCFile100A.Get("grXS100A")

cXS = TCanvas("cXS","cXS",600,600)
cXS.SetGrid()
sys100A.SetLineColor(kBlue)

sys60A.GetXaxis().SetRangeUser(0,1200.)
sys60A.GetYaxis().SetRangeUser(0,2.5)
sys60A.Draw("AP")
stat60A.Draw("e0same")
sys100A.Draw("P")
stat100A.Draw("e0same")
gr . Draw ( "PL" ) ;
#lariatHead.DrawLatex(0.6,0.90,"LArIAT Preliminary");
#lariatHead.DrawLatex(0.13,0.84,"same"); 
legendXS = TLegend(.54,.52,.84,.70);
legendXS.AddEntry(gr,"G4 Prediction Tot XS")
legendXS.AddEntry(stat60A ,"-60A Data Stat Only");
legendXS.AddEntry(sys60A  ,"-60A Data Stat and Sys");
legendXS.AddEntry(stat100A,"-100A Data Stat Only");
legendXS.AddEntry(sys100A ,"-100A Data Stat and Sys");
legendXS.Draw("same")
cXS.Update()











'''

grInt.SetTitle(";Kinetic Energy [MeV]; N_{Interacting} per 50 MeV")
grInc.SetTitle(";Kinetic Energy [MeV]; N_{Incident} per 50 MeV")
grXS.SetTitle("; Kinetic Energy [MeV]; #sigma_{TOT} per 50 MeV [barn]")

hInteractingKE_Stat.GetYaxis().SetTitleOffset(1.6)
hIncidentKE_Stat   .GetYaxis().SetTitleOffset(1.6)
XS_Stat            .GetYaxis().SetTitleOffset(1.2)


p1 = TCanvas("cHistos1","cHistos",600,600)
p1.SetGrid()
p1.SetLeftMargin(0.13)

#lariatHead.DrawLatex(0.13,0.84,""); 
grInt.GetXaxis().SetRangeUser(0,1200.)
grInt.GetYaxis().SetRangeUser(0,3000.)
grInt.Draw("AP")
hInteractingKE_Stat.Draw("e0same")
lariatHead.DrawLatex(0.6,0.90,"LArIAT Preliminary");

legendInt = TLegend(.54,.75,.90,.90);
legendInt.AddEntry(hInteractingKE_Stat,"Raw -100A Data Stat Only");
legendInt.AddEntry(grInt,   "Raw -100A Data Stat and Sys");
legendInt.Draw("same")
p1.Update()
p1.SaveAs(noRootFileName+"_Data_Int_StatSyst.png")

p2 = TCanvas("cHistos2","cHistos",600,600)
p2.SetGrid()
p2.SetLeftMargin(0.13)
grInc.GetXaxis().SetRangeUser(0,1200.)
grInc.GetYaxis().SetRangeUser(0,400000.)
grInc.Draw("AP")
hIncidentKE_Stat.Draw("e0same")
lariatHead.DrawLatex(0.6,0.90,"LArIAT Preliminary");
#lariatHead.DrawLatex(0.13,0.84,""); 

legendInc = TLegend(.54,.75,.90,.90);
legendInc.AddEntry(hIncidentKE_Stat,"Raw -100A Data Stat Only");
legendInc.AddEntry(grInc,   "Raw -100A Data Stat and Sys");
legendInc.Draw("same")
p2.Update()
p2.SaveAs(noRootFileName+"_Data_Inc_StatSyst.png")

cXS = TCanvas("cXS","cXS",600,600)
cXS.SetGrid()
grXS.GetXaxis().SetRangeUser(0,1200.)
grXS.GetYaxis().SetRangeUser(0,4.)
grXS.Draw("AP")
XS_Stat.Draw("e0same")
lariatHead.DrawLatex(0.6,0.90,"LArIAT Preliminary");
#lariatHead.DrawLatex(0.13,0.84,"same"); 
legendXS = TLegend(.54,.52,.84,.70);
legendXS.AddEntry(XS_Stat,"Raw -100A Data Stat Only");
legendXS.AddEntry(grXS,   "Raw -100A Data Stat and Sys");
legendXS.Draw("same")
cXS.Update()
cXS.SaveAs(noRootFileName+"_Data_XS_StatSyst.png")



'''
raw_input()

