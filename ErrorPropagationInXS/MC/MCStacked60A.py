from ROOT import *
import ROOT as root
import numpy as np
import argparse
import os

gStyle.SetOptStat(0)
#def calculateXSPlot(InteractingHisto, IncidentHisto, Name  ):
#    XS =  InteractingHisto.Clone(Name)
#    XS.Scale(101.10968)
#    XS.Divide(IncidentHisto)
#    return XS

#####################################################################
###################    Find Data Integral   #########################
#####################################################################


parser = argparse.ArgumentParser()
parser.add_argument("fileName"       , nargs='?', default = "/Volumes/Seagate/Elena/TPC/Data60A.root"  , type = str, help="insert fileName")
parser.add_argument("interactingName", nargs='?', default = "RecoXS/hRecoInteractingKE", type = str, help="interacting plot name")
parser.add_argument("incidentName"   , nargs='?', default = "RecoXS/hRecoIncidentKE"   , type = str, help="incident plot name")
args    = parser.parse_args()
inFileName           = args.fileName
hInteractingKE_Name  = args.interactingName
hIncidentKE_Name     = args.incidentName

inFileNameNoPath = os.path.basename(os.path.normpath(inFileName))
outFileName = "MC_Staggered_" + inFileNameNoPath
noRootFileName = outFileName[:-5]
print noRootFileName


fData = root.TFile(inFileName)
hInteractingKE_In  = fData.Get(hInteractingKE_Name)
hIncidentKE_In     = fData.Get(hIncidentKE_Name)

hInteractingKE_In_Integral = 0
hIncidentKE_In_Integral    = 0

for i in xrange(3,hInteractingKE_In.GetSize()):
    hInteractingKE_In_Integral += hInteractingKE_In.GetBinContent(i)
    hIncidentKE_In_Integral    += hIncidentKE_In   .GetBinContent(i)


print hInteractingKE_In_Integral, hIncidentKE_In_Integral

########################################################################
########################    MC Part   ##################################
########################################################################

pionInBeam60A = 0.688  # 68.8% pions
muonInBeam60A = 0.046  #  4.6% muons
elecInBeam60A = 0.266  # 26.6% electrons

# Electron to Pion and Muon to Pion Ratio
elecScale = elecInBeam60A/pionInBeam60A
muonScale = muonInBeam60A/pionInBeam60A


pionMC_FileName = "/Volumes/Seagate/Elena/TPC/XSMCPionWithSecondaries60A_histo.root"
muonMC_FileName = "/Volumes/Seagate/Elena/TPC/MC60A_Muon.root"
elecMC_FileName = "/Volumes/Seagate/Elena/TPC/MC60A_Electron.root"


# Get Monte Carlo files
interactingPlotString = "RecoXS/hRecoInteractingKE"
incidentPlotString    = "RecoXS/hRecoIncidentKE"
pionMC_File   = TFile.Open(pionMC_FileName)
muonMC_File   = TFile.Open(muonMC_FileName)
elecMC_File   = TFile.Open(elecMC_FileName)


# Get Interacting and Incident plots
pionMC_Int  = pionMC_File.Get("RecoXSPionOnly/hRecoInteractingKE")
secoMC_Int  = pionMC_File.Get("RecoXSSec/hRecoInteractingKE")
muonMC_Int  = muonMC_File.Get(interactingPlotString)
elecMC_Int  = elecMC_File.Get(interactingPlotString)
pionMC_Inc  = pionMC_File.Get("RecoXSPionOnly/hRecoIncidentKE")
secoMC_Inc  = pionMC_File.Get("RecoXSSec/hRecoIncidentKE")
muonMC_Inc  = muonMC_File.Get(incidentPlotString)
elecMC_Inc  = elecMC_File.Get(incidentPlotString)




# Let's assign a color scheme
pionMC_Int.SetFillColor(9)
secoMC_Int.SetFillColor(kRed-2)
muonMC_Int.SetFillColor(41)
elecMC_Int.SetFillColor(40)    
pionMC_Inc.SetFillColor(9)    
secoMC_Inc.SetFillColor(kRed-2)
muonMC_Inc.SetFillColor(41)
elecMC_Inc.SetFillColor(40)   



legend = TLegend(.54,.52,.84,.70);
legend.AddEntry(pionMC_Int,"MC 60A pions");
legend.AddEntry(secoMC_Int,"MC 60A secondaries");
legend.AddEntry(muonMC_Int,"MC 60A muons");
legend.AddEntry(elecMC_Int,"MC 60A electrons");


#Scale according to beam composition, both interacting and incident plots
elecMC_Int.Scale(elecScale)
elecMC_Inc.Scale(elecScale)
muonMC_Int.Scale(muonScale)
muonMC_Inc.Scale(muonScale)


# Form staggered plots for incident
interactingStack60A = THStack("interactingStack60A", "Interacting MC #pi/#mu/e; Interacting K.E. [MeV]; Entries per 50 MeV");
interactingStack60A.Add(elecMC_Int )
interactingStack60A.Add(muonMC_Int )
interactingStack60A.Add(secoMC_Int )
interactingStack60A.Add(pionMC_Int )

# Form staggered plots for incident
incidentStack60A = THStack("incidentStack60A", "Incident MC #pi/#mu/e; Incident K.E. [MeV]; Entries per 50 MeV");
incidentStack60A.Add(elecMC_Inc )
incidentStack60A.Add(muonMC_Inc )
incidentStack60A.Add(secoMC_Inc )
incidentStack60A.Add(pionMC_Inc )

# Staggered plots by hand


hInteractingKE_MC_Integral = 0
hIncidentKE_MC_Integral    = 0
totHisto_Int = pionMC_Int.Clone("totHisto_Int")
totHisto_Inc = pionMC_Inc.Clone("totHisto_Inc")
for i in xrange(pionMC_Int.GetSize()):
    totHisto_Int.SetBinContent(i, muonMC_Int.GetBinContent(i)+elecMC_Int.GetBinContent(i)+ pionMC_Int.GetBinContent(i) + secoMC_Int.GetBinContent(i))
    totHisto_Inc.SetBinContent(i, muonMC_Inc.GetBinContent(i)+elecMC_Inc.GetBinContent(i)+ pionMC_Inc.GetBinContent(i) + secoMC_Inc.GetBinContent(i))
    if i > 2:
        #print totHisto_Int.GetXaxis().GetBinCenter(i)
        hInteractingKE_MC_Integral += totHisto_Int.GetBinContent(i)
        hIncidentKE_MC_Integral    += totHisto_Inc.GetBinContent(i)

xsMC = totHisto_Int.Clone("xsMC")
xsMC.Scale(101.10968)
xsMC.Divide(totHisto_Inc)   


xsPiOnly = pionMC_Int.Clone("xsPiOnly")
xsPiOnly.Scale(101.10968)
xsPiOnly.Divide(pionMC_Inc)   

## Check Staggered Plots Make Sense
c0 = TCanvas("c0","c0",1200,600)
c0.Divide(2,1)
p1c0 = c0.cd(1)
p1c0.SetGrid()
interactingStack60A.Draw("histo")
totHisto_Int.Draw("samepe")

p2c0 = c0.cd(2)
p2c0.SetGrid()
incidentStack60A.Draw("histo")
totHisto_Inc.Draw("samepe")
c0.Update()

print hInteractingKE_In_Integral, hIncidentKE_In_Integral
print hInteractingKE_MC_Integral, hIncidentKE_MC_Integral

scaleFactor_Int = float(hInteractingKE_In_Integral)/float(hInteractingKE_MC_Integral)
scaleFactor_Inc = float(hIncidentKE_In_Integral   )/float(hIncidentKE_MC_Integral)


pionMC_IntC = pionMC_Int.Clone("pionMC_IntC")
pionMC_IncC = pionMC_Inc.Clone("pionMC_IncC")
secoMC_IntC = secoMC_Int.Clone("secoMC_IntC")
secoMC_IncC = secoMC_Inc.Clone("secoMC_IncC")
elecMC_IntC = elecMC_Int.Clone("elecMC_IntC")
elecMC_IncC = elecMC_Inc.Clone("elecMC_IncC")
muonMC_IntC = muonMC_Int.Clone("muonMC_IntC")
muonMC_IncC = muonMC_Inc.Clone("muonMC_IncC")


pionMC_IntC.Scale(scaleFactor_Int)
pionMC_IncC.Scale(scaleFactor_Inc)
secoMC_IntC.Scale(scaleFactor_Int)
secoMC_IncC.Scale(scaleFactor_Inc)
elecMC_IntC.Scale(scaleFactor_Int)
elecMC_IncC.Scale(scaleFactor_Inc)
muonMC_IntC.Scale(scaleFactor_Int)
muonMC_IncC.Scale(scaleFactor_Inc)

interactingStack60AC = THStack("interactingStack60AC", "Interacting MC #pi/#mu/e; Interacting K.E. [MeV]; Entries per 50 MeV");
interactingStack60AC.Add(elecMC_IntC )
interactingStack60AC.Add(muonMC_IntC )
interactingStack60AC.Add(secoMC_IntC )
interactingStack60AC.Add(pionMC_IntC )
                                   
# Form staggered plots for incident
incidentStack60AC = THStack("incidentStack60AC", "Incident MC #pi/#mu/e; Incident K.E. [MeV]; Entries per 50 MeV");
incidentStack60AC.Add(elecMC_IncC )
incidentStack60AC.Add(muonMC_IncC )
incidentStack60AC.Add(secoMC_IncC )
incidentStack60AC.Add(pionMC_IncC )
                           
## Check Staggered Plots Make Sense
c0C = TCanvas("c0C","c0C",1200,600)
c0C.Divide(2,1)
p1c0C = c0C.cd(1)
p1c0C.SetGrid()
interactingStack60AC.Draw("histo")
hInteractingKE_In.Draw("pesame")
p1c0C.Update()

p2c0C = c0C.cd(2)
p2c0C.SetGrid()
incidentStack60AC.Draw("histo")
hIncidentKE_In.Draw("pesame")
c0C.Update()
     
                                


#####################################################################
#######################    Save to File   ###########################
#####################################################################


outFile = TFile(outFileName,"recreate")
outFile.cd()

pionMC_IntC.Write("pionMC_Int60A",TObject.kWriteDelete)
pionMC_IncC.Write("pionMC_Inc60A",TObject.kWriteDelete)
secoMC_IntC.Write("secoMC_Int60A",TObject.kWriteDelete)
secoMC_IncC.Write("secoMC_Inc60A",TObject.kWriteDelete)
elecMC_IntC.Write("elecMC_Int60A",TObject.kWriteDelete)
elecMC_IncC.Write("elecMC_Inc60A",TObject.kWriteDelete)
muonMC_IntC.Write("muonMC_Int60A",TObject.kWriteDelete)
muonMC_IncC.Write("muonMC_Inc60A",TObject.kWriteDelete)

xsMC.Write("XS_60A",TObject.kWriteDelete)
xsPiOnly.Write("XS_60APiOnly",TObject.kWriteDelete)
interactingStack60AC.Write("interactingStack60A",TObject.kWriteDelete)
incidentStack60AC   .Write("incidentStack60A"   ,TObject.kWriteDelete)



outFile.Write()
outFile.Close()

raw_input()

