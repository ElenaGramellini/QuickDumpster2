from ROOT import *
import ROOT as root
import numpy as np
import argparse
import os

gStyle.SetOptStat(0)
def calculateXSPlot(InteractingHisto, IncidentHisto, Name  ):
    XS =  InteractingHisto.Clone(Name)
    XS.Scale(101.10968)
    XS.Divide(IncidentHisto)
    return XS


parser = argparse.ArgumentParser()
parser.add_argument("fileName"       , nargs='?', default = "SystematicsEnergy100A.root"  , type = str, help="insert fileName")
args    = parser.parse_args()
inFileName           = args.fileName

inFileNameNoPath = os.path.basename(os.path.normpath(inFileName))
outFileName = "XSRaw_SysOnlyUnc_" + inFileNameNoPath
noRootFileName = outFileName[:-5]
print noRootFileName
f = root.TFile(inFileName)

hInteractingKE     = f.Get("hInteractingKE")
hIncidentKE        = f.Get("hIncidentKE")
XS                 = f.Get("XS")
hInteractingKEMax  = f.Get("hInteractingKEMax")
hIncidentKEMax     = f.Get("hIncidentKEMax")
XSMax              = f.Get("XSMax")
hInteractingKEMin  = f.Get("hInteractingKEMin")
hIncidentKEMin     = f.Get("hIncidentKEMin")
XSMin              = f.Get("XSMin")

ch = TCanvas("cHistos","cHistos",1800,600)
ch.Divide(3,1)
cp0 = ch.cd(1)
cp0.SetGrid()
hInteractingKE   .SetLineColor(kRed)
hInteractingKEMax.SetLineColor(kAzure+4)
hInteractingKEMin.SetLineColor(kBlue)   
hInteractingKE.Draw("")
hInteractingKEMax.Draw("same")
hInteractingKEMin.Draw("same")

cp1 = ch.cd(2)

cp1.SetGrid()
hIncidentKE   .SetLineColor(kRed)    
hIncidentKEMax.SetLineColor(kAzure+4)
hIncidentKEMin.SetLineColor(kBlue)   
hIncidentKE.Draw("")
hIncidentKEMax.Draw("same")
hIncidentKEMin.Draw("same")

cp2 = ch.cd(3)
cp2.SetGrid()
XS   .SetLineColor(kRed)    
XSMax.SetLineColor(kAzure+4)
XSMin.SetLineColor(kBlue)   
XS.Draw("")
XSMax.Draw("same")
XSMin.Draw("same")
ch.Update()

#####################################################################
###################    Error Propagation   ##########################
#####################################################################

XS_Err              = XS   .Clone("XS_Err")   
hInteractingKE_Err  = XSMax.Clone("hInteractingKE_Err")
hIncidentKE_Err     = XSMin.Clone("hIncidentKE_Err")


for i in xrange(hInteractingKE.GetSize()):

    
    binInteracting = hInteractingKE.GetBinContent(i)
    binIncident    = hIncidentKE   .GetBinContent(i)
    binXS          = XS            .GetBinContent(i)
    binInteractingMax = hInteractingKEMax.GetBinContent(i)
    binIncidentMax    = hIncidentKEMax   .GetBinContent(i)
    binXSMax          = XSMax            .GetBinContent(i)
    binInteractingMin = hInteractingKEMin.GetBinContent(i)
    binIncidentMin    = hIncidentKEMin   .GetBinContent(i)
    binXSMin          = XSMin            .GetBinContent(i)

    inte = [binInteracting,binInteractingMax,binInteractingMin  ]
    inc  = [binIncident,   binIncidentMax   ,binIncidentMin     ]
    xs   = [binXS,         binXSMax         ,binXSMin           ]

    val_XS_Err             = float(max(xs) + min(xs))/2.
    err_XS_Err             = float(max(xs) - min(xs))/2.
    val_hInteractingKE_Err = float(max(inte) + min(inte))/2.
    err_hInteractingKE_Err = float(max(inte) - min(inte))/2.
    val_hIncidentKE_Err    = float(max(inc) + min(inc))/2.
    err_hIncidentKE_Err    = float(max(inc) - min(inc))/2.


    

    XS_Err            .SetBinContent(i,val_XS_Err            ) 
    hInteractingKE_Err.SetBinContent(i,val_hInteractingKE_Err) 
    hIncidentKE_Err   .SetBinContent(i,val_hIncidentKE_Err   ) 

    XS_Err            .SetBinError(i,err_XS_Err            ) 
    hInteractingKE_Err.SetBinError(i,err_hInteractingKE_Err) 
    hIncidentKE_Err   .SetBinError(i,err_hIncidentKE_Err   ) 



#####################################################################
#######################    Aestetics   ##############################
#####################################################################

hInteractingKE_Err.SetFillColor(kAzure-2)
hIncidentKE_Err   .SetFillColor(kAzure-2)
XS_Err            .SetFillColor(kAzure-2)
hInteractingKE.SetMarkerColor(kBlack)
hIncidentKE   .SetMarkerColor(kBlack)
XS            .SetMarkerColor(kBlack)
hInteractingKE.SetMarkerStyle(8)
hIncidentKE   .SetMarkerStyle(8)
XS            .SetMarkerStyle(8)
hInteractingKE.SetMarkerSize(0.5)
hIncidentKE   .SetMarkerSize(0.5)
XS            .SetMarkerSize(0.5)

hInteractingKE_Err.SetTitle("Raw Candidate Interacting;Kinetic Energy [MeV]; N_{Interacting} per 50 MeV")
hIncidentKE_Err   .SetTitle("Raw Candidate Incident;Kinetic Energy [MeV]; N_{Incident} per 50 MeV")
XS_Err            .SetTitle("Raw Cross Section; Kinetic Energy [MeV]; #sigma_{TOT} per 50 MeV [barn]")

hInteractingKE_Err.GetYaxis().SetTitleOffset(1.6)
hIncidentKE_Err   .GetYaxis().SetTitleOffset(1.6)
XS_Err            .GetYaxis().SetTitleOffset(1.2)


p1 = TCanvas("cHistos1","cHistos",600,600)
p1.SetGrid()
p1.SetLeftMargin(0.12)
hInteractingKE_Err.SetLineColor(kAzure+4)
hInteractingKE_Err.GetXaxis().SetRangeUser(0,1200.)
hInteractingKE_Err.GetYaxis().SetRangeUser(0,3000.)
hInteractingKE_Err.Draw("pe2")
hInteractingKE.Draw("hist p same")

legendInt = TLegend(.54,.75,.90,.90);
legendInt.AddEntry(hInteractingKE_Err,"Data Syst Only");
legendInt.Draw("same")
p1.Update()
p1.SaveAs(noRootFileName+"_Int.png")

p2 = TCanvas("cHistos2","cHistos",600,600)
p2.SetGrid()
p2.SetLeftMargin(0.12)
hIncidentKE_Err.SetLineColor(kAzure+4)
hIncidentKE_Err.GetXaxis().SetRangeUser(0,1200.)
hIncidentKE_Err.GetYaxis().SetRangeUser(0,400000.)
hIncidentKE_Err.Draw("pe2")
hIncidentKE.Draw("hist p same")
legendInc = TLegend(.54,.75,.90,.90);
legendInc.AddEntry(hIncidentKE_Err,"Data Syst Only");
legendInc.Draw("same")
p2.Update()
p2.SaveAs(noRootFileName+"_Inc.png")

cXS = TCanvas("cXS","cXS",600,600)
cXS.SetGrid()
XS_Err.SetLineColor(kAzure+4)
XS_Err.GetXaxis().SetRangeUser(0,1200.)
XS_Err.GetYaxis().SetRangeUser(0,4.)
XS_Err.Draw("pe2")
XS.Draw("hist p same")
legendXS = TLegend(.54,.52,.84,.70);
legendXS.AddEntry(XS_Err,"Data Syst Only");
legendXS.Draw("same")
cXS.Update()
cXS.SaveAs(noRootFileName+".png")

#####################################################################
#######################    Save to File   ###########################
#####################################################################


outFile = TFile(outFileName,"recreate")
outFile.cd()

hInteractingKE  .Write("hInteractingKE" ,TObject.kWriteDelete)  
hIncidentKE     .Write("hIncidentKE"    ,TObject.kWriteDelete)  
XS              .Write("XS"             ,TObject.kWriteDelete)  
hInteractingKE_Err .Write("hInteractingKE_Err",TObject.kWriteDelete)  
hIncidentKE_Err    .Write("hIncidentKE_Err"   ,TObject.kWriteDelete)  
XS_Err             .Write("XS_Err"            ,TObject.kWriteDelete)  


outFile.Write()
outFile.Close()

raw_input()

