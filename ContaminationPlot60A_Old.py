from ROOT import *
import os
import math
import argparse


# Get BeamComposition
pionInBeam60A = 0.688
muonInBeam60A = 0.0046 #this is incorrect, needs to be 0.046
elecInBeam60A = 0.264

elecScale = elecInBeam60A/pionInBeam60A
muonScale = muonInBeam60A/pionInBeam60A

pionMC_FileName = "RecoPionMC_60A.root"
muonMC_FileName = "RecoMuonMC_60A.root"
elecMC_FileName = "RecoElectronMC_60A.root"

# Get Monte Carlo files
interactingPlotString = "RecoXS/hRecoInteractingKE"
incidentPlotString    = "RecoXS/hRecoIncidentKE"
pionMC_File  = TFile.Open(pionMC_FileName)
muonMC_File  = TFile.Open(muonMC_FileName)
elecMC_File  = TFile.Open(elecMC_FileName)


# Get Interacting and Incident plots
pionMC_Int  = pionMC_File.Get(interactingPlotString)
muonMC_Int  = muonMC_File.Get(interactingPlotString)
elecMC_Int  = elecMC_File.Get(interactingPlotString)
pionMC_Inc  = pionMC_File.Get(incidentPlotString)
muonMC_Inc  = muonMC_File.Get(incidentPlotString)
elecMC_Inc  = elecMC_File.Get(incidentPlotString)


pionMC_Int.SetFillColor(kBlue)
muonMC_Int.SetFillColor(kYellow)
elecMC_Int.SetFillColor(kRed)    
pionMC_Inc.SetFillColor(kBlue)    
muonMC_Inc.SetFillColor(kYellow)
elecMC_Inc.SetFillColor(kRed)    


#Scale according to beam composition
elecMC_Int.Scale(elecScale)
elecMC_Inc.Scale(elecScale)
muonMC_Int.Scale(muonScale)
muonMC_Inc.Scale(muonScale)



incidentStack60A = THStack("incidentStack60A", "Incident Stack with Beam Weights; Incident K.E. [MeV]; Entries per 50 MeV");
incidentStack60A.Add(muonMC_Inc )
incidentStack60A.Add(elecMC_Inc )
incidentStack60A.Add(pionMC_Inc )


interactingStack60A = THStack("interactingStack60A", "Interacting Stack with Beam Weights; Interacting K.E. [MeV]; Entries per 50 MeV");
interactingStack60A.Add(muonMC_Int )
interactingStack60A.Add(elecMC_Int )
interactingStack60A.Add(pionMC_Int )



#MC 60A
c60 = TCanvas("c60" ,"Plots Overlay" ,200 ,10 ,1200 ,600)
c60.Divide(2,1) 
c60.cd(1)
pionMC_Int.Draw("histo")
elecMC_Int.Draw("samehisto")
muonMC_Int.Draw("samehisto")
c60.cd(2)
pionMC_Inc.Draw("histo")
elecMC_Inc.Draw("samehisto")
muonMC_Inc.Draw("samehisto")



c60EC = TCanvas("c60S" ,"Electron Content" ,200 ,10 ,1200 ,600)
c60EC.Divide(2,1) 
c60EC.cd(1)
interactingStack60A.Draw("histo")
c60EC.cd(2)
incidentStack60A.Draw("histo")

totHisto_Int = pionMC_Int.Clone("totHisto_Int")
totHisto_Inc = pionMC_Inc.Clone("totHisto_Inc")
for i in xrange(pionMC_Int.GetSize()):
    totHisto_Int.SetBinContent(i, muonMC_Int.GetBinContent(i)+elecMC_Int.GetBinContent(i)+ pionMC_Int.GetBinContent(i))
    totHisto_Inc.SetBinContent(i, muonMC_Inc.GetBinContent(i)+elecMC_Inc.GetBinContent(i)+ pionMC_Inc.GetBinContent(i))



c60Electron = TCanvas("c60Electron" ,"Electron Contributions" ,200 ,10 ,1200 ,600)
c60Electron.Divide(2,1) 
c60Electron.cd(1)
electronNum_Int = elecMC_Int.Clone("electronNum_Int")
totHisto_Int.Sumw2()
electronNum_Int.Divide(totHisto_Int)
electronNum_Int.Draw("pe")
c60Electron.cd(2)
totHisto_Inc.Sumw2()
electronNum_Inc = elecMC_Inc.Clone("electronNum_Inc")
electronNum_Inc.Divide(totHisto_Inc)
electronNum_Inc.Draw("pe")

c60Muon = TCanvas("c60Muon" ,"Muon Contributions" ,200 ,10 ,1200 ,600)
c60Muon.Divide(2,1) 
c60Muon.cd(1)
totHisto_Int.Sumw2()
muonNum_Int = muonMC_Int.Clone("muonNum_Int")
muonNum_Int.Divide(totHisto_Int)
muonNum_Int.Draw("pe")
c60Muon.cd(2)
totHisto_Inc.Sumw2()
muonNum_Inc = muonMC_Inc.Clone("muonNum_Inc")
muonNum_Inc.Divide(totHisto_Inc)
muonNum_Inc.Draw("pe")


c60XCheck = TCanvas("c60XCheck" ,"XCheck Contributions" ,200 ,10 ,1200 ,600)
c60XCheck.Divide(2,1) 
c60XCheck.cd(1)
totHisto_Int.Draw("")
c60XCheck.cd(2)
totHisto_Inc.Draw("")


c60XS = TCanvas("c60XS" ,"XS Contributions" ,200 ,10 ,600 ,600)
c60XS.cd()
totHisto_Int.Sumw2()
totHisto_Inc.Sumw2()
stackNum = totHisto_Int.Clone("stackNum")
stackNum.Sumw2()
stackNum.Divide(totHisto_Inc)
pionNum  = pionMC_Int.Clone("pionNum")
pionNum.Sumw2()
pionMC_Inc.Sumw2()
pionNum.Divide(pionMC_Inc)
pionNum.Sumw2()
XSstack = stackNum.Clone("XSstack")
XSstack.Sumw2()
XSstack.Divide(pionNum)
XSstack.Sumw2()
XSstack.Draw("pe")
c60XS.Update()


raw_input()  



