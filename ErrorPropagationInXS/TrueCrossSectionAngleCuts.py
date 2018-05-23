from ROOT import *
import os
import math
import argparse

gStyle.SetOptStat(0);




# Truth 100 A
noAngleCutFile100A   = TFile.Open("/Volumes/Seagate/Elena/TPC/AngleCut_100A_histo.root")
File_0083_100A       = TFile.Open("/Volumes/Seagate/Elena/TPC/AngleCut_0.08334_new_histo.root")

noAngleCut_Int100A          = noAngleCutFile100A   .Get("TrueXS/hInteractingKE")
noAngleCut_Inc100A          = noAngleCutFile100A   .Get("TrueXS/hIncidentKE") 
noAngleCut_Int_0083_100A    = File_0083_100A       .Get("AngleCutTrueXS083/hInteractingKE")
noAngleCut_Inc_0083_100A    = File_0083_100A       .Get("AngleCutTrueXS083/hIncidentKE")



# Truth 60 A
noAngleCutFile   = TFile.Open("/Volumes/Seagate/Elena/TPC/TruePionGen60A.root")
angleCutFile0083 = TFile.Open("/Volumes/Seagate/Elena/TPC/AngleCut_0.08334_histo_60A.root")


# Get Interacting and Incident plots
interactingName = "AngleCutTrueXS/hInteractingKE"
incidentName = "AngleCutTrueXS/hIncidentKE"

noAngleCut_Int    = noAngleCutFile   .Get("TrueXS/hInteractingKE")
angleCut_Int_0083 = angleCutFile0083 .Get(interactingName)


noAngleCut_Inc    = noAngleCutFile   .Get("TrueXS/hIncidentKE")
angleCut_Inc_0083 = angleCutFile0083 .Get(incidentName)


'''
cP = TCanvas("cP" ,"cP" ,200 ,10 ,600 ,600)
noAngleCut_Int100A.Draw("pe")
noAngleCut_Int.Draw("pe")

cP2 = TCanvas("cP2" ,"cP2" ,200 ,10 ,600 ,600)
noAngleCut_Inc100A.Draw("")
noAngleCut_Inc.Draw("same")

cPC = TCanvas("cPC" ,"cPC" ,200 ,10 ,600 ,600)
noAngleCut_Int100A.Divide(noAngleCut_Inc100A)
noAngleCut_Int100A.Scale(101)

noAngleCut_Int.Divide(noAngleCut_Inc)
noAngleCut_Int.Scale(101)

noAngleCut_Int100A.Draw("histo")
noAngleCut_Int.Draw("samehisto")
'''

cPNoCuts = TCanvas("cPNoCuts" ,"cPNoCuts" ,200 ,10 ,600 ,600)
cPNoCuts.SetGrid()
noAngleCut_Int100A.Add(noAngleCut_Int)
noAngleCut_Inc100A.Add(noAngleCut_Inc)
noAngleCut_Int_0083_100A.Add(angleCut_Int_0083)
noAngleCut_Inc_0083_100A.Add(angleCut_Inc_0083)

noAngleCut_Int100A.SetLineColor(kGreen-2)
noAngleCut_Int_0083_100A.SetLineColor(kBlue)

noAngleCut_Int100A.Divide(noAngleCut_Inc100A)
noAngleCut_Int100A.Scale(101)
noAngleCut_Int100A.SetTitle("Geant4 (#pi^{-},Ar) True Cross Section; Kinetic Energy [MeV];  (#pi^{-},Ar) True Cross Section [barn]")
noAngleCut_Int100A.GetYaxis().SetTitleOffset(1.3)
noAngleCut_Int100A.Draw("histo][")
noAngleCut_Int_0083_100A.Divide(noAngleCut_Inc_0083_100A)
noAngleCut_Int_0083_100A.Scale(101)
noAngleCut_Int_0083_100A.Draw("histosame][")



for i in xrange(4):
    noAngleCut_Int100A.SetBinContent(i,0)
    noAngleCut_Int_0083_100A.SetBinContent(i,0)


#for i in xrange(20,30):
#    noAngleCut_Int100A.SetBinContent(i,0)
#    noAngleCut_Int_0079_100A.SetBinContent(i,0)
#    noAngleCut_Int_0083_100A.SetBinContent(i,0)
#    noAngleCut_Int_0157_100A.SetBinContent(i,0)



legend = TLegend(.54,.52,.84,.70)
legend.AddEntry(noAngleCut_Int100A  ,"All Angles")
legend.AddEntry(noAngleCut_Int_0083_100A,"Angles > 5.0 Deg")


legend.Draw("same")




raw_input()  



