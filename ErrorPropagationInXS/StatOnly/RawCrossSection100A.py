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
parser.add_argument("fileName"       , nargs='?', default = "/Volumes/Seagate/Elena/TPC/Data100A.root"  , type = str, help="insert fileName")
parser.add_argument("interactingName", nargs='?', default = "RecoXS/hRecoInteractingKE", type = str, help="interacting plot name")
parser.add_argument("incidentName"   , nargs='?', default = "RecoXS/hRecoIncidentKE"   , type = str, help="incident plot name")
args    = parser.parse_args()
inFileName           = args.fileName
hInteractingKE_Name  = args.interactingName
hIncidentKE_Name     = args.incidentName
inFileNameNoPath = os.path.basename(os.path.normpath(inFileName))
outFileName = "XSRaw_StatOnlyUnc_" + inFileNameNoPath
noRootFileName = outFileName[:-5]
print noRootFileName
f = root.TFile(inFileName)

hInteractingKE_In  = f.Get(hInteractingKE_Name)
hIncidentKE_In     = f.Get(hIncidentKE_Name)

hInteractingKE_Out  = hInteractingKE_In.Clone("hInteractingKE_Out")
hIncidentKE_Out     = hIncidentKE_In   .Clone("hIncidentKE_Out")

XS_In     = calculateXSPlot(hInteractingKE_In   , hIncidentKE_In  , "XS_In")
XS_Out    = calculateXSPlot(hInteractingKE_Out  , hIncidentKE_Out , "XS_Out")

#####################################################################
###################    Error Propagation   ##########################
#####################################################################

for i in xrange(hInteractingKE_Out.GetSize()):
    binInteracting = hInteractingKE_Out.GetBinContent(i)
    binIncident    = hIncidentKE_Out   .GetBinContent(i)
    binXS          = XS_Out            .GetBinContent(i)

    if binInteracting > 0 and binIncident > 0:
        errInc = TMath.Sqrt(binIncident)
        errInt = TMath.Sqrt(binInteracting*(1- binInteracting/binIncident))
        errXS  = binXS*(errInt/binInteracting  + errInc/binIncident )

        hInteractingKE_Out.SetBinError(i,errInt)
        hIncidentKE_Out   .SetBinError(i,errInc)
        XS_Out            .SetBinError(i,errXS)

#for i in xrange(24,hInteractingKE_Out.GetSize()):
#    hInteractingKE_Out.SetBinContent(i,-100)
#    hIncidentKE_Out   .SetBinContent(i,-100)
#    XS_Out            .SetBinContent(i,-100)
#    hInteractingKE_Out.SetBinError(i,0)
#    hIncidentKE_Out   .SetBinError(i,0)
#    XS_Out            .SetBinError(i,0)

#####################################################################
#######################    Aestetics   ##############################
#####################################################################

hInteractingKE_Out.SetFillColor(kAzure-4)
hIncidentKE_Out   .SetFillColor(kAzure-4)
XS_Out            .SetFillColor(kAzure-4)
hInteractingKE_In.SetMarkerColor(kBlack)
hIncidentKE_In   .SetMarkerColor(kBlack)
XS_In            .SetMarkerColor(kBlack)
hInteractingKE_In.SetMarkerStyle(8)
hIncidentKE_In   .SetMarkerStyle(8)
XS_In            .SetMarkerStyle(8)
hInteractingKE_In.SetMarkerSize(0.5)
hIncidentKE_In   .SetMarkerSize(0.5)
XS_In            .SetMarkerSize(0.5)

hInteractingKE_Out.SetTitle("Raw Candidate Interacting;Kinetic Energy [MeV]; N_{Interacting} per 50 MeV")
hIncidentKE_Out   .SetTitle("Raw Candidate Incident;Kinetic Energy [MeV]; N_{Incident} per 50 MeV")
XS_Out            .SetTitle("Raw Cross Section; Kinetic Energy [MeV]; #sigma_{TOT} per 50 MeV [barn]")

hInteractingKE_Out.GetYaxis().SetTitleOffset(1.6)
hIncidentKE_Out   .GetYaxis().SetTitleOffset(1.6)
XS_Out            .GetYaxis().SetTitleOffset(1.2)


p1 = TCanvas("cHistos1","cHistos",600,600)
p1.SetGrid()
p1.SetLeftMargin(0.12)
hInteractingKE_Out.GetXaxis().SetRangeUser(0,1200.)
hInteractingKE_Out.GetYaxis().SetRangeUser(0,3000.)
hInteractingKE_Out.Draw("pe2")
hInteractingKE_In.Draw("hist p same")

legendInt = TLegend(.54,.75,.90,.90);
legendInt.AddEntry(hInteractingKE_Out,"Data Stat Only");
legendInt.Draw("same")
p1.Update()
p1.SaveAs(noRootFileName+"_Int.png")

p2 = TCanvas("cHistos2","cHistos",600,600)
p2.SetGrid()
p2.SetLeftMargin(0.12)
hIncidentKE_Out.GetXaxis().SetRangeUser(0,1200.)
hIncidentKE_Out.GetYaxis().SetRangeUser(0,400000.)
hIncidentKE_Out.Draw("pe2")
hIncidentKE_In.Draw("hist p same")
legendInc = TLegend(.54,.75,.90,.90);
legendInc.AddEntry(hIncidentKE_Out,"Data Stat Only");
legendInc.Draw("same")
p2.Update()
p2.SaveAs(noRootFileName+"_Inc.png")

cXS = TCanvas("cXS","cXS",600,600)
cXS.SetGrid()
XS_Out.GetXaxis().SetRangeUser(0,1200.)
XS_Out.GetYaxis().SetRangeUser(0,4.)
XS_Out.Draw("pe2")
XS_In.Draw("hist p same")
legendXS = TLegend(.54,.52,.84,.70);
legendXS.AddEntry(XS_Out,"Data Stat Only");
legendXS.Draw("same")
cXS.Update()
cXS.SaveAs(noRootFileName+".png")

#####################################################################
#######################    Save to File   ###########################
#####################################################################


outFile = TFile(outFileName,"recreate")
outFile.cd()

hInteractingKE_In  .Write("hInteractingKE_In" ,TObject.kWriteDelete)  
hIncidentKE_In     .Write("hIncidentKE_In"    ,TObject.kWriteDelete)  
XS_In              .Write("XS_In"             ,TObject.kWriteDelete)  
hInteractingKE_Out .Write("hInteractingKE_Out",TObject.kWriteDelete)  
hIncidentKE_Out    .Write("hIncidentKE_Out"   ,TObject.kWriteDelete)  
XS_Out             .Write("XS_Out"            ,TObject.kWriteDelete)  


outFile.Write()
outFile.Close()

raw_input()

