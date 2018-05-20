from ROOT import *
import ROOT as root
import numpy as np
from array import array

gStyle.SetOptStat(0)

#MCName = "/Users/elenag/Desktop/BeamLineCompoForPion/MCCorrection/ErrorPropagationInXS/MC/MC_Staggered_Data100A.root"
#MCFile = root.TFile(MCName)
#MC_Int = MCFile.Get("interactingStack100A")
#MC_Inc = MCFile.Get("incidentStack100A"   )
#MC_XS  = MCFile.Get("XS_100A")

#MC_XS.SetBinContent(1,0)
#MC_XS.SetBinContent(2,0)
#MC_XS.SetBinContent(3,0)
#MC_XS.SetBinContent(4,0)
#MC_XS.SetBinContent(5,0)
#MC_XS.SetBinContent(6,0)
#MC_XS.SetBinContent(24,0)
#MC_XS.SetBinContent(25,0)
#MC_XS.SetBinContent(26,0)
#MC_XS.SetBinError(1,0)
#MC_XS.SetBinError(2,0)
#MC_XS.SetBinError(3,0)
#MC_XS.SetBinError(4,0)
#MC_XS.SetBinError(5,0)
#MC_XS.SetBinError(6,0)
#MC_XS.SetBinError(24,0)
#MC_XS.SetBinError(25,0)
#MC_XS.SetBinError(26,0)

#pionMC_Int = MCFile.Get("pionMC_Int100A")
#secoMC_Int = MCFile.Get("secoMC_Int100A")
#muonMC_Int = MCFile.Get("muonMC_Int100A")
#elecMC_Int = MCFile.Get("elecMC_Int100A")

#pionMC_Int.SetFillColor(9)
#secoMC_Int.SetFillColor(kRed-2)
#muonMC_Int.SetFillColor(41)
#elecMC_Int.SetFillColor(40)    
#MC_XS.SetFillColor(kWhite)

inFileName          = "../StatOnly/XSRaw_StatOnlyUnc_Data100A.root"
f                   = root.TFile(inFileName)
XS_Stat             = f.Get("XS_Out")
XS_Stat.SetBinContent(3,-100)
XS_Stat.SetBinError(3,0)

inFileNameSys          = "../Systematics/XSRaw_SysOnlyUnc_SystematicsEnergy100A.root"
fSys                  = root.TFile(inFileNameSys)
XS_SysMax             = fSys.Get("XS_ErrMax")
XS_SysMin             = fSys.Get("XS_ErrMin")


inFileNameBkg          = "../BkgSub/BkgSubWithBuoundaries_100A.root"
fBkg                  = root.TFile(inFileNameBkg)
XS_BkgSub             = fBkg.Get("XS_BkgSub100A")
XS_BkgMax             = fBkg.Get("XS_BkgSub_Max100A")
XS_BkgMin             = fBkg.Get("XS_BkgSub_Min100A")



noRootFileName = "Plots100A_BkgSub"
#####################################################################
###################    Error Propagation   ##########################
#####################################################################


intMaxErr_StaSys, incMaxErr_StaSys, XSMaxErr_StaSys = array( 'd' ), array( 'd' ), array( 'd' )
intMinErr_StaSys, incMinErr_StaSys, XSMinErr_StaSys = array( 'd' ), array( 'd' ), array( 'd' )
intErr_Central  , incErr_Central  , XSErr_Central   = array( 'd' ), array( 'd' ), array( 'd' )
x               , exl             , exh             = array( 'd' ), array( 'd' ), array( 'd' )

for i in xrange(XS_Stat.GetSize()):
    
    bin_XS_BkgSub = XS_BkgSub.GetBinError(i)   
    bin_XS_BkgMax = XS_BkgMax.GetBinError(i)  
    bin_XS_BkgMin = XS_BkgMin.GetBinError(i)  

    err_XS_BkgMax = bin_XS_BkgMax - bin_XS_BkgSub  
    err_XS_BkgMin = bin_XS_BkgSub - bin_XS_BkgMin

    statErrXS         = XS_Stat  .GetBinError(i)
    sysMaxXS          = XS_SysMax.GetBinError(i)
    sysMinXS          = XS_SysMin.GetBinError(i)

    XSMaxErr_StaSys  .append(TMath.Sqrt(statErrXS*statErrXS + sysMaxXS*sysMaxXS + err_XS_BkgMax*err_XS_BkgMax))
    XSMinErr_StaSys  .append(TMath.Sqrt(statErrXS*statErrXS + sysMinXS*sysMinXS + err_XS_BkgMin*err_XS_BkgMin))
    XSErr_Central    .append(XS_BkgSub            .GetBinContent(i))
    XS_Stat.SetBinContent(i, XS_BkgSub            .GetBinContent(i))

    x   .append(-125+50*i)
    exl .append(25.)
    exh .append(25.)

grXS  = TGraphAsymmErrors(XS_Stat.GetSize(),x,XSErr_Central ,exl,exh,XSMinErr_StaSys ,XSMaxErr_StaSys);

grXS.SetLineColor(kRed)
grXS.SetFillColor(kWhite)


#####################################################################
#######################    Aestetics   ##############################
#####################################################################

lariatHead = TLatex();
lariatHead.SetNDC();
lariatHead.SetTextFont(62);
lariatHead.SetTextSize(0.04);
lariatHead.SetTextAlign(40);


XS_Stat            .SetFillColor(kWhite)
XS_Stat            .SetLineColor(kBlack)
XS_Stat            .SetMarkerStyle(8)
XS_Stat            .SetMarkerSize(0.5)

grXS.SetTitle("; Kinetic Energy [MeV]; #sigma_{#pi} per 50 MeV [barn]")
XS_Stat            .GetYaxis().SetTitleOffset(1.2)


cXS = TCanvas("cXS","cXS",600,600)
cXS.SetGrid()
grXS.GetXaxis().SetRangeUser(0,1200.)
grXS.GetYaxis().SetRangeUser(0,4.)
grXS.Draw("AP")
#MC_XS.Draw("histosame][")
grXS.Draw("P")
XS_Stat.Draw("e0same")
lariatHead.DrawLatex(0.6,0.90,"LArIAT Preliminary");
#lariatHead.DrawLatex(0.13,0.84,"same"); 
legendXS = TLegend(.54,.65,.90,.90)
legendXS.AddEntry(XS_Stat,"Raw -100A Data Stat Only");
legendXS.AddEntry(grXS,   "Raw -100A Data Stat and Sys");
#legendXS.AddEntry(MC_XS,  "MC Reco -100A #pi/#mu/e");

legendXS.Draw("same")
cXS.Update()
cXS.SaveAs(noRootFileName+"_MCData_XS_StatSyst_BkgSub.pdf")

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

