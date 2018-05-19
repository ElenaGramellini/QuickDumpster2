from ROOT import *
import ROOT as root
import numpy as np
from array import array

gStyle.SetOptStat(0)


inFileName          = "../StatOnly/XSRaw_StatOnlyUnc_Data60A.root"
f                   = root.TFile(inFileName)
hInteractingKE_Stat = f.Get("hInteractingKE_Out")
hIncidentKE_Stat    = f.Get("hIncidentKE_Out")
XS_Stat             = f.Get("XS_Out")

#hInteractingKE_StatSys = hInteractingKE_Stat.Clone("hInteractingKE_StatSys")
#hIncidentKE_StatSys    = hIncidentKE_Stat   .Clone("hIncidentKE_StatSys")
#XS_StatSys             = XS_Stat            .Clone("XS_Stat_StatSys")

inFileNameSys          = "../Systematics/XSRaw_SysOnlyUnc_SystematicsEnergy60A.root"
fSys                  = root.TFile(inFileNameSys)
hInteractingKE_SysMax = fSys.Get("hInteractingKE_ErrMax")
hIncidentKE_SysMax    = fSys.Get("hIncidentKE_ErrMax")
XS_SysMax             = fSys.Get("XS_ErrMax")
hInteractingKE_SysMin = fSys.Get("hInteractingKE_ErrMin")
hIncidentKE_SysMin    = fSys.Get("hIncidentKE_ErrMin")
XS_SysMin             = fSys.Get("XS_ErrMin")

noRootFileName = "Plots60A"
#####################################################################
###################    Error Propagation   ##########################
#####################################################################


intMaxErr_StaSys, incMaxErr_StaSys, XSMaxErr_StaSys = array( 'd' ), array( 'd' ), array( 'd' )
intMinErr_StaSys, incMinErr_StaSys, XSMinErr_StaSys = array( 'd' ), array( 'd' ), array( 'd' )
intErr_Central  , incErr_Central  , XSErr_Central   = array( 'd' ), array( 'd' ), array( 'd' )
x               , exl             , exh             = array( 'd' ), array( 'd' ), array( 'd' )

for i in xrange(hInteractingKE_Stat.GetSize()):

    statErrInteracting = hInteractingKE_Stat.GetBinError(i)
    statErrIncident    = hIncidentKE_Stat   .GetBinError(i)
    statErrXS          = XS_Stat            .GetBinError(i)

    sysMaxInteracting = hInteractingKE_SysMax .GetBinError(i)
    sysMaxIncident    = hIncidentKE_SysMax    .GetBinError(i)
    sysMaxXS          = XS_SysMax             .GetBinError(i)

    sysMinInteracting = hInteractingKE_SysMin .GetBinError(i)
    sysMinIncident    = hIncidentKE_SysMin    .GetBinError(i)
    sysMinXS          = XS_SysMin             .GetBinError(i)

    intMaxErr_StaSys .append(TMath.Sqrt(statErrInteracting*statErrInteracting + sysMaxInteracting*sysMaxInteracting))
    incMaxErr_StaSys .append(TMath.Sqrt(statErrIncident*statErrIncident + sysMaxIncident*sysMaxIncident))
    XSMaxErr_StaSys  .append(TMath.Sqrt(statErrXS*statErrXS + sysMaxXS*sysMaxXS))
 
    intMinErr_StaSys .append(TMath.Sqrt(statErrInteracting*statErrInteracting + sysMinInteracting*sysMinInteracting))
    incMinErr_StaSys .append(TMath.Sqrt(statErrIncident*statErrIncident + sysMinIncident*sysMinIncident))
    XSMinErr_StaSys  .append(TMath.Sqrt(statErrXS*statErrXS + sysMinXS*sysMinXS))

    intErr_Central .append(hInteractingKE_Stat.GetBinContent(i))
    incErr_Central .append(hIncidentKE_Stat   .GetBinContent(i))
    XSErr_Central  .append(XS_Stat            .GetBinContent(i))

    x   .append(-125+50*i)
    exl .append(25.)
    exh .append(25.)


grInt = TGraphAsymmErrors(hInteractingKE_Stat.GetSize(),x,intErr_Central,exl,exh,intMinErr_StaSys,intMaxErr_StaSys);
grInc = TGraphAsymmErrors(hInteractingKE_Stat.GetSize(),x,incErr_Central,exl,exh,incMinErr_StaSys,incMaxErr_StaSys);
grXS  = TGraphAsymmErrors(hInteractingKE_Stat.GetSize(),x,XSErr_Central ,exl,exh,XSMinErr_StaSys ,XSMaxErr_StaSys);

grInt.SetLineColor(kRed)
grInc.SetLineColor(kRed)
grXS.SetLineColor(kRed)
grInt.SetFillColor(kWhite)
grInc.SetFillColor(kWhite)
grXS.SetFillColor(kWhite)


#####################################################################
#######################    Aestetics   ##############################
#####################################################################

lariatHead = TLatex();
lariatHead.SetNDC();
lariatHead.SetTextFont(62);
lariatHead.SetTextSize(0.04);
lariatHead.SetTextAlign(40);




hInteractingKE_Stat.SetFillColor(kWhite)
hIncidentKE_Stat   .SetFillColor(kWhite)
XS_Stat            .SetFillColor(kWhite)
hInteractingKE_Stat.SetLineColor(kBlack)
hIncidentKE_Stat   .SetLineColor(kBlack)
XS_Stat            .SetLineColor(kBlack)
hInteractingKE_Stat.SetMarkerStyle(8)
hIncidentKE_Stat   .SetMarkerStyle(8)
XS_Stat            .SetMarkerStyle(8)
hInteractingKE_Stat.SetMarkerSize(0.5)
hIncidentKE_Stat   .SetMarkerSize(0.5)
XS_Stat            .SetMarkerSize(0.5)

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
grInt.GetYaxis().SetRangeUser(0,5000.)
grInt.Draw("AP")
hInteractingKE_Stat.Draw("e0same")
lariatHead.DrawLatex(0.6,0.90,"LArIAT Preliminary");

legendInt = TLegend(.54,.75,.90,.90);
legendInt.AddEntry(hInteractingKE_Stat,"Raw -60A Data Stat Only");
legendInt.AddEntry(grInt,   "Raw -60A Data Stat and Sys");
legendInt.Draw("same")
p1.Update()
p1.SaveAs(noRootFileName+"_Data_Int_StatSyst.png")

p2 = TCanvas("cHistos2","cHistos",600,600)
p2.SetGrid()
p2.SetLeftMargin(0.13)
grInc.GetXaxis().SetRangeUser(0,1200.)
grInc.GetYaxis().SetRangeUser(0,500000.)
grInc.Draw("AP")
hIncidentKE_Stat.Draw("e0same")
lariatHead.DrawLatex(0.6,0.90,"LArIAT Preliminary");
#lariatHead.DrawLatex(0.13,0.84,""); 

legendInc = TLegend(.54,.75,.90,.90);
legendInc.AddEntry(hIncidentKE_Stat,"Raw -60A Data Stat Only");
legendInc.AddEntry(grInc,   "Raw -60A Data Stat and Sys");
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
legendXS.AddEntry(XS_Stat,"Raw -60A Data Stat Only");
legendXS.AddEntry(grXS,   "Raw -60A Data Stat and Sys");
legendXS.Draw("same")
cXS.Update()
cXS.SaveAs(noRootFileName+"_Data_XS_StatSyst.png")

#####################################################################
#######################    Save to File   ###########################
#####################################################################

'''
outFile = TFile(outFileName,"recreate")
outFile.cd()

hInteractingKE_StatSys  .Write("hInteractingKE_StatSys" ,TObject.kWriteDelete)  
hIncidentKE_StatSys     .Write("hIncidentKE_StatSys"    ,TObject.kWriteDelete)  
XS_StatSys              .Write("XS_StatSys"             ,TObject.kWriteDelete)  
hInteractingKE_Stat .Write("hInteractingKE_Stat",TObject.kWriteDelete)  
hIncidentKE_Stat    .Write("hIncidentKE_Stat"   ,TObject.kWriteDelete)  
XS_Stat             .Write("XS_Stat"            ,TObject.kWriteDelete)  


outFile.Write()
outFile.Close()
'''
raw_input()

