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

MCFileTrue =  root.TFile("../EffCorrection/Eff_Correction.root")
XSTrue45 = MCFileTrue.Get("XS45Deg")
for i in xrange(16,40):
    XSTrue45.SetBinContent(i,0)
    XSTrue45.SetBinError(i,0)
XSTrue45.SetLineColor(kGreen-2)

sys .SetLineWidth(2)
stat .SetMarkerStyle(22)
stat .SetMarkerSize(1.0)
sys.SetTitle("; Kinetic Energy [MeV]; #sigma^{K}_{TOT} per 50 MeV [barn]")
sys.GetXaxis().SetRangeUser(0,800.)
sys.GetYaxis().SetRangeUser(0,1.5)
sys.SetLineColor(kBlack)

cXS = TCanvas("cXS","cXS",600,600)
cXS.SetGrid()
sys.Draw("AP")
#gr . Draw ( "PL" ) ;
stat.Draw("e1same")
XSTrue45.Draw("histosame][")
lariatHead.DrawLatex(0.6,0.90,"LArIAT Preliminary");
legendXS = TLegend(.30,.68,.86,.86);
legendXS.AddEntry(XSTrue45,"FTFP_BERT Geant4 Prediction Angle > 5.0 Deg")
legendXS.AddEntry(stat,"Kaon Data (Stat. #oplus Syst Unc.)");
#legendXS.AddEntry(sys ,"Kaon Data Stat and Sys");
legendXS.Draw("same")
cXS.Update()
#cXS.SaveAs("TheFinalMoneyPlotK.pdf")



############################################################
cXS60A = TCanvas("cXS60A","cXS60A",600,800)
p1  = TPad("pad1", "The pad 80% of the height",0.0,0.2,1.0,1.0,21) 
p2  = TPad("pad2", "The pad 80% of the height",0.0,0.0,1.0,0.2,22)
p1.Draw()
p1.SetFillColor(0)
p2.SetFillColor(0)
p1.SetLeftMargin(0.12)
#p2.SetLeftMargin(0.12)
p2.Draw() 
p1.cd()
p1.SetGrid()
p2.SetGrid()
sys.Draw("AP")
#gr . Draw ( "PL" ) ;
XSTrue45.Draw("][histosame")
stat.SetLineColor(1)
stat.SetFillColor(0)
stat.Draw("e1same")
lariatHead.DrawLatex(0.6,0.90,"LArIAT Preliminary");
legendXS.Draw("same")


y_XS  , eyl_XS  , eyh_XS   = array( 'd' ), array( 'd' ), array( 'd' )
x_XS  , exl_XS  , exh_XS   = array( 'd' ), array( 'd' ), array( 'd' )

residual    = stat.Clone("res")
residualTGr = sys.Clone()
residual.SetTitle(";Kinetic Energy [MeV]; #sigma_{MC} - #sigma^{#pi-}")
residual.GetYaxis().SetRangeUser(-1,1)
residual.GetXaxis().SetRangeUser(0,800)

residual.GetXaxis().SetTitleOffset(.5);
residual.GetXaxis().SetTitleSize(.10);
residual.GetYaxis().SetTitleOffset(.5);
residual.GetYaxis().SetTitleSize(.10);

xRes     = sys .GetX()
errYHigh = sys .GetEYhigh()
errYLow  = sys .GetEYlow()

for i in xrange(residual.GetSize()-2):
    if stat.GetBinContent(i):
        residual.SetBinContent(i, (stat.GetBinContent(i) - XSTrue45.GetBinContent(i))/stat.GetBinContent(i)  )
    else:
        residual.SetBinContent(i, -100. )


    x_XS   .append(xRes[i])
    exl_XS .append(25.)
    exh_XS .append(25.)
    
    if i < 5 or i > 15:
        y_XS   .append(-100.)
    elif stat.GetBinContent(i):
        y_XS   .append( (stat.GetBinContent(i) - XSTrue45.GetBinContent(i))/ stat.GetBinContent(i) )
    else:
        y_XS   .append( -100.)
    eyh_XS .append(errYHigh[i])
    eyl_XS .append(errYLow[i])
    

grRes_Combo  = TGraphAsymmErrors(residual.GetSize()-2,x_XS, y_XS, exl_XS, exh_XS, eyl_XS, eyh_XS)

grRes_Combo.SetTitle(";Kinetic Energy [MeV]; #frac{#sigma^{K}_{TOT} - #sigma_{MC}}{#sigma^{K}_{TOT}}")
grRes_Combo.GetYaxis().SetRangeUser(-2,2)
grRes_Combo.GetXaxis().SetRangeUser(0,800)

grRes_Combo.GetXaxis().SetTitleOffset(.5);
grRes_Combo.GetXaxis().SetTitleSize(.13);
grRes_Combo.GetYaxis().SetTitleOffset(.5);
grRes_Combo.GetYaxis().SetTitleSize(.13);

p2.cd()
#residual.Draw()
grRes_Combo.Draw("AP")

cXS60A.Update()
cXS60A.SaveAs("TheRealMoneyPlot.pdf")





raw_input()

