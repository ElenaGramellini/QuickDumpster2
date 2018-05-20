from ROOT import *
import ROOT as root
import numpy as np
import argparse
import os

gStyle.SetOptStat(0)

########################################################################
########################    MC Part   ##################################
########################################################################
changeMu = 1. 
changeE  = 1. 

#pionInBeam60A = 0.688           # 68.8% pions
muonInBeam60A  = 0.046*changeMu  #  4.6% muons
elecInBeam60A  = 0.266*changeE   # 26.6% electrons

pionInBeam60A = 1. - muonInBeam60A - elecInBeam60A


# Electron to Pion and Muon to Pion Ratio
elecScale = elecInBeam60A/pionInBeam60A
muonScale = muonInBeam60A/pionInBeam60A

checkFileName = "bkgFiles/BkgSub_1.0muons_1.0electrons_60A.root"
checkFile     = TFile.Open(checkFileName)
move_XS_60A   = checkFile.Get("move_XS_60A")


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



#Scale according to beam composition, both interacting and incident plots
elecMC_Int.Scale(elecScale)
elecMC_Inc.Scale(elecScale)
muonMC_Int.Scale(muonScale)
muonMC_Inc.Scale(muonScale)



# Staggered plots by hand
totHisto_Int = pionMC_Int.Clone("totHisto_Int")
totHisto_Inc = pionMC_Inc.Clone("totHisto_Inc")
for i in xrange(pionMC_Int.GetSize()):
    totHisto_Int.SetBinContent(i, muonMC_Int.GetBinContent(i)+elecMC_Int.GetBinContent(i)+ pionMC_Int.GetBinContent(i) + secoMC_Int.GetBinContent(i))
    totHisto_Inc.SetBinContent(i, muonMC_Inc.GetBinContent(i)+elecMC_Inc.GetBinContent(i)+ pionMC_Inc.GetBinContent(i) + secoMC_Inc.GetBinContent(i))
    totHisto_Int.SetBinError(i, TMath.Sqrt(muonMC_Int.GetBinContent(i)+elecMC_Int.GetBinContent(i)+ pionMC_Int.GetBinContent(i) + secoMC_Int.GetBinContent(i)))
    totHisto_Inc.SetBinError(i, TMath.Sqrt(muonMC_Inc.GetBinContent(i)+elecMC_Inc.GetBinContent(i)+ pionMC_Inc.GetBinContent(i) + secoMC_Inc.GetBinContent(i)))

pionMC_Int.Divide(pionMC_Inc)   
pionMC_Int.Multiply(totHisto_Inc)   
pionMC_Int.Divide(totHisto_Int)   
pionMC_Int.SetFillColor(kWhite)



## Check Staggered Plots Make Sense
c0 = TCanvas("c0","c0",600,600)
p1c0 = c0.cd(1)
p1c0.SetGrid()
move_XS_60A.Draw("pe")
pionMC_Int.Draw("histosame")


raw_input()

