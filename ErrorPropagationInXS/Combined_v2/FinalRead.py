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
'''
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
'''

lariatHead = TLatex();
lariatHead.SetNDC();
lariatHead.SetTextFont(62);
lariatHead.SetTextSize(0.04);
lariatHead.SetTextAlign(40);


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




MCFile60A  = root.TFile("Combined.root")
stat60A = MCFile60A.Get("XS_Combined")
sys60A  = MCFile60A.Get("XS_Sys_Combined")

sys60A .SetLineWidth(2)
stat60A .SetMarkerStyle(20)
stat60A .SetMarkerSize(0.5)
sys60A.SetTitle("; Kinetic Energy [MeV]; #sigma^{#pi}_{TOT} per 50 MeV [barn]")
sys60A.GetXaxis().SetRangeUser(0,1200.)
sys60A.GetYaxis().SetRangeUser(0,2.5)


sys60A.SetLineColor(kBlack)
sys60A.SetFillColor(0)

for i in xrange(5):
    stat60A.SetBinContent(i,-100)

cXS60A = TCanvas("cXS60A","cXS60A",600,800)
p1  = TPad("pad1", "The pad 80% of the height",0.0,0.2,1.0,1.0,21) 
p2  = TPad("pad2", "The pad 80% of the height",0.0,0.0,1.0,0.2,22)
p1.Draw()
p1.SetFillColor(0)
p2.SetFillColor(0)
p1.SetLeftMargin(0.12)
p1.SetTopMargin(0.12)
p2.SetLeftMargin(0.12)
p2.Draw() 
p1.cd()
p1.SetGrid()
p2.SetGrid()
sys60A.Draw("AP")
#gr . Draw ( "PL" ) ;
XS_45.Draw("][histosame")
stat60A.SetLineColor(1)
stat60A.SetFillColor(0)
stat60A.Draw("e1same")
lariatHead.DrawLatex(0.6,0.90,"LArIAT Preliminary");
legendXS60A = TLegend(.30,.68,.86,.86);
legendXS60A.AddEntry(XS_45,"FTFP_BERT Geant4 Prediction True Angle > 5.0 Deg")
legendXS60A.AddEntry(stat60A,"Combined Datasets (Stat. #oplus Syst Unc.)");
#legendXS60A.AddEntry(sys60A ,"-60A Data Stat and Sys");
legendXS60A.Draw("same")
#cXS60A.cd()

y_XS  , eyl_XS  , eyh_XS   = array( 'd' ), array( 'd' ), array( 'd' )
x_XS  , exl_XS  , exh_XS   = array( 'd' ), array( 'd' ), array( 'd' )

residual    = stat60A.Clone("res")
residualTGr = sys60A.Clone()
residual.SetTitle(";Kinetic Energy [MeV]; #sigma_{MC} - #sigma^{#pi-}")
residual.GetYaxis().SetRangeUser(-1,1)
residual.GetXaxis().SetRangeUser(0,1200)

residual.GetXaxis().SetTitleOffset(.5);
residual.GetXaxis().SetTitleSize(.10);
residual.GetYaxis().SetTitleOffset(.2);
residual.GetYaxis().SetTitleSize(.10);

xRes     = sys60A .GetX()
errYHigh = sys60A .GetEYhigh()
errYLow  = sys60A .GetEYlow()

for i in xrange(residual.GetSize()-2):
    if stat60A.GetBinContent(i):
        residual.SetBinContent(i, (stat60A.GetBinContent(i) - XS_45.GetBinContent(i))/stat60A.GetBinContent(i)  )
    else:
        residual.SetBinContent(i, -100. )

    if i < 5:
        x_XS   .append(-100.)
    else:
        x_XS   .append(xRes[i])
        exl_XS .append(25.)
        exh_XS .append(25.)
        
    if stat60A.GetBinContent(i):
        y_XS   .append( (stat60A.GetBinContent(i) - XS_45.GetBinContent(i))/ stat60A.GetBinContent(i) )
    else:
        y_XS   .append( -100.)
    eyh_XS .append(errYHigh[i])
    eyl_XS .append(errYLow[i])
    

grRes_Combo  = TGraphAsymmErrors(residual.GetSize()-2,x_XS, y_XS, exl_XS, exh_XS, eyl_XS, eyh_XS)

grRes_Combo.SetTitle(";Kinetic Energy [MeV]; #frac{#sigma^{#pi-}_{TOT} - #sigma_{MC}}{#sigma^{#pi-}_{TOT}}")
grRes_Combo.GetYaxis().SetRangeUser(-1,1)
grRes_Combo.GetXaxis().SetRangeUser(0,1200)

grRes_Combo.GetXaxis().SetTitleOffset(.5);
grRes_Combo.GetXaxis().SetTitleSize(.13);
grRes_Combo.GetYaxis().SetTitleOffset(.5);
grRes_Combo.GetYaxis().SetTitleSize(.13);

p2.cd()
residual.Draw()
grRes_Combo.Draw("AP")

cXS60A.Update()
cXS60A.SaveAs("TheRealMoneyPlot.pdf")

raw_input()





