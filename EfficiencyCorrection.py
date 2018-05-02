from ROOT import *
import os
import math
import argparse


pionMCNoFilter_FileName = '/Volumes/Seagate/Elena/MCContamination/TrueAnaPions60A_NoFilter.root'
pionMC_FileName = '/Volumes/Seagate/Elena/MCContamination/XSHisto.root'


# Get Interacting and Incident plots Reco
pionMC_File  = TFile.Open(pionMC_FileName)
intTrue  = pionMC_File.Get("TrueXS/hInteractingKE")
incTrue  = pionMC_File.Get("TrueXS/hIncidentKE")
intReco  = pionMC_File.Get("RecoXS/hRecoInteractingKE")
incReco  = pionMC_File.Get("RecoXS/hRecoIncidentKE")



# Get Interacting and Incident plots for all true primary in TPC
pionMCNoFilter   = TFile.Open(pionMCNoFilter_FileName)
intTrueNoFilter  = pionMCNoFilter.Get("TrueXS/hInteractingKE")
incTrueNoFilter  = pionMCNoFilter.Get("TrueXS/hIncidentKE")

# Assign colors
intReco.SetLineColor(kRed)  
incReco.SetLineColor(kRed)  
intTrue.SetLineColor(kBlue)  
incTrue.SetLineColor(kBlue)
intTrueNoFilter.SetLineColor(kGreen-2)  
incTrueNoFilter.SetLineColor(kGreen-2)    

intReco.SetLineWidth(2)  
incReco.SetLineWidth(2)  
intTrue.SetLineWidth(2)  
incTrue.SetLineWidth(2)
intTrueNoFilter.SetLineWidth(2)  
incTrueNoFilter.SetLineWidth(2)    

legend = TLegend(.54,.52,.84,.70);
legend.AddEntry(intReco        ,"Reconstructed");
legend.AddEntry(intTrue        ,"True With Filters");
legend.AddEntry(intTrueNoFilter,"True No Filters");


# Comparison between plots
c60T1 = TCanvas("c60T1" ,"Interaction" ,200 ,10 ,700 ,700)
c60T1.cd()
c60T1.SetGrid()
intTrueNoFilter.SetTitle("Interacting Histogram; Interacting KE [MeV]; N Entries")
intTrueNoFilter.GetXaxis().SetRangeUser(0,1000)
intTrueNoFilter.Draw("histo")
intTrue.Draw("histosames")
intReco.Draw("histosames")
legend.Draw("same")
c60T1.Update()

c60T2 = TCanvas("c60T2" ,"Incident" ,200 ,10 ,700 ,700)
c60T2.cd()
c60T2.SetGrid()
incTrueNoFilter.SetTitle("Incident Histogram; Incitent KE [MeV]; N Entries")
incTrueNoFilter.GetXaxis().SetRangeUser(0,1000)
incTrueNoFilter.Draw("histo")
incTrue.Draw("histosames")
incReco.Draw("histosames")
legend.Draw("same")
c60T2.Update()

c60T3 = TCanvas("c60T3" ,"Cross Section" ,200 ,10 ,700 ,700)
c60T3.cd()
c60T3.SetGrid()
XSTrueNoFilter= intTrueNoFilter.Clone("XSTrueNoFilter")
XSTrue = intTrue.Clone("XSTrue")
XSReco = intReco.Clone("XSReco")
XSTrueNoFilter.Sumw2()
XSTrue.Sumw2()
XSReco.Sumw2()
XSTrueNoFilter.Scale(101.10968)
XSTrue.Scale(101.10968)
XSReco.Scale(101.10968)
XSTrueNoFilter.Divide(incTrueNoFilter)
XSTrue.Divide(incTrue)
XSReco.Divide(incReco)

XSTrueNoFilter.SetTitle("Cross Section; KE [MeV]; Cross Section [barn]")
XSTrueNoFilter.GetXaxis().SetRangeUser(0,1000)
XSTrueNoFilter.Draw("pe")
XSTrue.Draw("pesames")
XSReco.Draw("pesames")
legend.Draw("same")

c60T3.Update()


'''
# TPC Reco Efficiencies
c60 = TCanvas("c60" ,"TPC Reco Efficiency" ,200 ,10 ,1200 ,800)
c60.Divide(2,1) 
p3 = c60.cd(1)
p3.SetGrid()
intEff = intReco.Clone("intEff")
intEff.Divide(intTrue)
intEff.Sumw2()
intEff.Draw("")

p4 = c60.cd(2)
p4.SetGrid()
incEff = incReco.Clone("incEff")
incEff.Divide(incTrue)
incEff.Sumw2()
incEff.Draw("")
c60.Update()


# WC2TPC Match Efficiencies
cNoF = TCanvas("cNoF" ,"TPC Reco Efficiency" ,200 ,10 ,1200 ,800)
cNoF.Divide(2,2) 
pNoF1 = cNoF.cd(1)
pNoF1.SetGrid()
intTrueNoFilter.Draw("histo")
intReco.Draw("histosames")
legend.Draw("same")

pNoF2 = cNoF.cd(2)
pNoF2.SetGrid()
incTrueNoFilter.Draw("histo")
incReco.Draw("histosames")
legend.Draw("same")

pNoF3 = cNoF.cd(3)
pNoF3.SetGrid()
intEffNoFilter = intReco.Clone("intEffNoF")
intEffNoFilter.Divide(incTrueNoFilter)
intEffNoFilter.Sumw2()
intEffNoFilter.Draw("")

pNoF4 = cNoF.cd(4)
pNoF4.SetGrid()
incEffNoFilter = incReco.Clone("incEffNoF")
incEffNoFilter.Divide(incTrue)
incEffNoFilter.Sumw2()
incEffNoFilter.Draw("")
cNoF.Update()
'''

raw_input()  



