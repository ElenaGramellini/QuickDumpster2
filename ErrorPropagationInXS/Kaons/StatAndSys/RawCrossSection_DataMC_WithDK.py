from ROOT import *
import ROOT as root
import numpy as np
from array import array

gStyle.SetOptStat(0)

MCName = "/Volumes/Seagate/Elena/TPC/reco_histo_20000.root"
MCFile = root.TFile(MCName)
MC_Int = MCFile.Get("RecoXSAll/hRecoInteractingKE")
MC_Inc = MCFile.Get("RecoXSAll/hRecoIncidentKE"   )

MC_IntDK = MCFile.Get("RecoXSAll/hRecoInteractingKE_DK")

MC_IntK = MCFile.Get("RecoXSKaonOnly/hRecoInteractingKE")
MC_IncK = MCFile.Get("RecoXSKaonOnly/hRecoIncidentKE"   )

MC_IntS = MCFile.Get("RecoXSSec/hRecoInteractingKE")
MC_IncS = MCFile.Get("RecoXSSec/hRecoIncidentKE"   )

MC_IntK.Add(MC_IntDK,-1)


for i in xrange(4):
    MC_Int .SetBinContent(i,0)
    MC_Inc .SetBinContent(i,0)
    MC_IntK.SetBinContent(i,0)
    MC_IncK.SetBinContent(i,0)
    MC_IntDK.SetBinContent(i,0)
    MC_IntS.SetBinContent(i,0)
    MC_IncS.SetBinContent(i,0)

    MC_Int .SetBinError(i,0)
    MC_Inc .SetBinError(i,0)
    MC_IntK.SetBinError(i,0)
    MC_IncK.SetBinError(i,0)
    MC_IntDK.SetBinError(i,0)
    MC_IntS.SetBinError(i,0)
    MC_IncS.SetBinError(i,0)

for i in xrange(16,50):
    MC_Int .SetBinContent(i,0)
    MC_Inc .SetBinContent(i,0)
    MC_IntK.SetBinContent(i,0)
    MC_IncK.SetBinContent(i,0)
    MC_IntDK.SetBinContent(i,0)
    MC_IntS.SetBinContent(i,0)
    MC_IncS.SetBinContent(i,0)

    MC_Int .SetBinError(i,0)
    MC_Inc .SetBinError(i,0)
    MC_IntK.SetBinError(i,0)
    MC_IncK.SetBinError(i,0)
    MC_IntDK.SetBinError(i,0)
    MC_IntS.SetBinError(i,0)
    MC_IncS.SetBinError(i,0)


MC_XS  = MC_Int.Clone("XS_MC")
MC_XS.Scale(101.)
MC_XS.Divide(MC_Inc)
MC_XS.Sumw2()
MC_XS.SetFillColor(kWhite)





inFileName          = "../StatOnly/XSRaw_StatOnlyUnc_KaonDataPicky.root"
f                   = root.TFile(inFileName)
hInteractingKE_Stat = f.Get("hInteractingKE_Out")
hIncidentKE_Stat    = f.Get("hIncidentKE_Out")
XS_Stat             = f.Get("XS_Out")
#XS_Stat.SetBinContent(3,-100)
#XS_Stat.SetBinError(3,0)



inFileNameSys          = "../Systematics/XSRaw_SysOnlyUnc_SystematicsEnergy.root"
fSys                  = root.TFile(inFileNameSys)
hInteractingKE_SysMax = fSys.Get("hInteractingKE_ErrMax")
hIncidentKE_SysMax    = fSys.Get("hIncidentKE_ErrMax")
XS_SysMax             = fSys.Get("XS_ErrMax")
hInteractingKE_SysMin = fSys.Get("hInteractingKE_ErrMin")
hIncidentKE_SysMin    = fSys.Get("hIncidentKE_ErrMin")
XS_SysMin             = fSys.Get("XS_ErrMin")

noRootFileName = "Plots"
#####################################################################
###################    Error Propagation   ##########################
#####################################################################


intMaxErr_StaSys, incMaxErr_StaSys, XSMaxErr_StaSys = array( 'd' ), array( 'd' ), array( 'd' )
intMinErr_StaSys, incMinErr_StaSys, XSMinErr_StaSys = array( 'd' ), array( 'd' ), array( 'd' )
intErr_Central  , incErr_Central  , XSErr_Central   = array( 'd' ), array( 'd' ), array( 'd' )
x               , exl             , exh             = array( 'd' ), array( 'd' ), array( 'd' )

dataInt_Int = 0
dataInt_Inc = 0
for i in xrange(hInteractingKE_Stat.GetSize()):
    if i > 3:
        dataInt_Int += hInteractingKE_Stat.GetBinContent(i)
        dataInt_Inc += hIncidentKE_Stat.GetBinContent(i)

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


integral_Int = MC_Int.Integral()
integral_Inc = MC_Inc.Integral()
MC_Int.Scale(dataInt_Int/MC_Int.Integral())
MC_Inc.Scale(dataInt_Inc/MC_Inc.Integral())

MC_IntK.Scale(dataInt_Int/integral_Int)
MC_IncK.Scale(dataInt_Inc/integral_Inc)
MC_IntDK.Scale(dataInt_Int/integral_Int)
MC_IntS.Scale(dataInt_Int/integral_Int)
MC_IncS.Scale(dataInt_Inc/integral_Inc)


interactingStack = THStack("interactingStack", "Interacting MC #pi/#mu/e; Interacting K.E. [MeV]; Entries per 50 MeV");
interactingStack.Add(MC_IntS )
interactingStack.Add(MC_IntDK )
interactingStack.Add(MC_IntK )
MC_IntS.SetFillColor(kRed-2)
MC_IntK.SetFillColor(kMagenta-8)
MC_IntDK.SetFillColor(kOrange+1)
MC_IntS.SetLineColor(kRed-2)
MC_IntK.SetLineColor(kRed-8)
MC_IntDK.SetLineColor(kOrange+1)

incidentStack = THStack("incidentStack", "Incident MC #pi/#mu/e; Incident K.E. [MeV]; Entries per 50 MeV");
incidentStack.Add(MC_IncS )
incidentStack.Add(MC_IncK )
MC_IncS.SetFillColor(kRed-2)
MC_IncK.SetFillColor(kMagenta-8)
MC_IncS.SetLineColor(kRed-2)
MC_IncK.SetLineColor(kRed-8)


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
grInt.GetYaxis().SetRangeUser(0,120.)
grInt.Draw("AP")
interactingStack.Draw("histosame")
grInt.Draw("P")
hInteractingKE_Stat.Draw("e0same")
lariatHead.DrawLatex(0.6,0.90,"LArIAT Preliminary");

legendInt = TLegend(.44,.55,.90,.90);
legendInt.AddEntry(hInteractingKE_Stat,"Raw - Data Stat Only");
legendInt.AddEntry(grInt,   "Raw  Data Stat and Sys");
legendInt.AddEntry(MC_IntK, "MC  Kaons Hadronic Interaction");
legendInt.AddEntry(MC_IntDK, "MC  Kaon Decay");
legendInt.AddEntry(MC_IntS, "MC  Secondaries");
legendInt.Draw("same")
p1.Update()
p1.SaveAs(noRootFileName+"_MCData_Int_StatSystK_WithDK.pdf")


p2 = TCanvas("cHistos2","cHistos",600,600)
p2.SetGrid()
p2.SetLeftMargin(0.15)
grInc.GetXaxis().SetRangeUser(0,1200.)
grInc.GetYaxis().SetRangeUser(0,25000.)
grInc.Draw("AP")
incidentStack.Draw("histosame")
grInc.Draw("P")
hIncidentKE_Stat.Draw("e0same")
lariatHead.DrawLatex(0.6,0.90,"LArIAT Preliminary");
#lariatHead.DrawLatex(0.13,0.84,""); 

legendInc = TLegend(.44,.55,.90,.90);
legendInc.AddEntry(hIncidentKE_Stat,"Raw  Data Stat Only");
legendInc.AddEntry(grInc,   "Raw  Data Stat and Sys");
legendInc.AddEntry(MC_IncK, "MC  Kaons");
legendInc.AddEntry(MC_IncS, "MC  Secondaries");

legendInc.Draw("same")
p2.Update()
p2.SaveAs(noRootFileName+"_MCData_Inc_StatSystK_WithDK.pdf")

cXS = TCanvas("cXS","cXS",600,600)
cXS.SetGrid()
grXS.GetXaxis().SetRangeUser(0,1200.)
grXS.GetYaxis().SetRangeUser(0,4.)
grXS.Draw("AP")
MC_XS.Draw("histosame][")
grXS.Draw("P")
XS_Stat.Draw("e0same")
lariatHead.DrawLatex(0.6,0.90,"LArIAT Preliminary");
#lariatHead.DrawLatex(0.13,0.84,"same"); 
legendXS = TLegend(.44,.65,.90,.90)
legendXS.AddEntry(XS_Stat,"Raw  Data Stat Only");
legendXS.AddEntry(grXS,   "Raw  Data Stat and Sys");
legendXS.AddEntry(MC_XS,  "MC Reco  All K + Secondaries");

legendXS.Draw("same")
cXS.Update()
cXS.SaveAs(noRootFileName+"_MCData_XS_StatSystK_WithDK.pdf")

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

