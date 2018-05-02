from ROOT import *
import os
import math
import argparse



pionData_FileName = '/Volumes/Seagate/Elena/DataTPC/temp60A.root'

# Get Interacting and Incident plots Reco
pionData_File  = TFile.Open(pionData_FileName)
intReco  = pionData_File.Get("RecoXS/hRecoInteractingKE")
incReco  = pionData_File.Get("RecoXS/hRecoIncidentKE")



# Assign colors
intReco.SetLineColor(kRed)  
incReco.SetLineColor(kRed)  
intReco.SetLineWidth(2)  
incReco.SetLineWidth(2)  

#legend = TLegend(.54,.52,.84,.70);
#legend.AddEntry(intReco        ,"Reconstructed");
#legend.AddEntry(intTrue        ,"True With Filters");
#legend.AddEntry(intTrueNoFilter,"True No Filters");


# Comparison between plots
c60T1 = TCanvas("c60T1" ,"Interaction" ,200 ,10 ,700 ,700)
c60T1.cd()
c60T1.SetGrid()
intReco.Draw("pe")
c60T1.Update()

c60T2 = TCanvas("c60T2" ,"Incident" ,200 ,10 ,700 ,700)
c60T2.cd()
c60T2.SetGrid()
incReco.Draw("pe")
c60T2.Update()

c60T3 = TCanvas("c60T3" ,"Cross Section" ,200 ,10 ,700 ,700)
c60T3.cd()
c60T3.SetGrid()
XSReco = intReco.Clone("XSReco")
XSReco.Sumw2()
XSReco.Scale(101.10968)
XSReco.Divide(incReco)
XSReco.Draw("pe")

c60T3.Update()



raw_input()  



