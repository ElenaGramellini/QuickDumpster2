from ROOT import *
import os
import math
import argparse


# Get BeamComposition: percentage of pions, muons and electrons in a 60A beam configuration
#                       The beam at 60A is 
#pionInBeam60A = 0.642  # 68.8% pions
#muonInBeam60A = 0.092  #  4.6% muons
#elecInBeam60A = 0.266  # 26.6% electrons


pionInBeam60A = 0.688  # 68.8% pions
muonInBeam60A = 0.046  #  4.6% muons
elecInBeam60A = 0.266  # 26.6% electrons


# Electron to Pion and Muon to Pion Ratio
elecScale = elecInBeam60A/pionInBeam60A
muonScale = muonInBeam60A/pionInBeam60A

pionMC_FileName = "/Volumes/Seagate/Elena/TPC/MC60A_Pions.root"
muonMC_FileName = "/Volumes/Seagate/Elena/TPC/MC60A_Muon.root"
elecMC_FileName = "/Volumes/Seagate/Elena/TPC/MC60A_Electron.root"



# Get Monte Carlo files
interactingPlotString = "RecoXS/hRecoInteractingKE"
incidentPlotString    = "RecoXS/hRecoIncidentKE"
pionMC_File   = TFile.Open(pionMC_FileName)
muonMC_File   = TFile.Open(muonMC_FileName)
elecMC_File   = TFile.Open(elecMC_FileName)



# Get Interacting and Incident plots
pionMC_Int  = pionMC_File.Get(interactingPlotString)
muonMC_Int  = muonMC_File.Get(interactingPlotString)
elecMC_Int  = elecMC_File.Get(interactingPlotString)
pionMC_Inc  = pionMC_File.Get(incidentPlotString)
muonMC_Inc  = muonMC_File.Get(incidentPlotString)
elecMC_Inc  = elecMC_File.Get(incidentPlotString)




# Let's assign a color scheme --> check color scheme is the same as G4Beamline
pionMC_Int.SetFillColor(9)
muonMC_Int.SetFillColor(41)
elecMC_Int.SetFillColor(40)    
pionMC_Inc.SetFillColor(9)    
muonMC_Inc.SetFillColor(41)
elecMC_Inc.SetFillColor(40)    

legend = TLegend(.54,.52,.84,.70);
legend.AddEntry(pionMC_Int,"MC 60A pions");
legend.AddEntry(muonMC_Int,"MC 60A muons");
legend.AddEntry(elecMC_Int,"MC 60A electrons");


#Scale according to beam composition, both interacting and incident plots
elecMC_Int.Scale(elecScale)
elecMC_Inc.Scale(elecScale)
muonMC_Int.Scale(muonScale)
muonMC_Inc.Scale(muonScale)

 


# Form staggered plots for incident
interactingStack60A = THStack("interactingStack60A", "Interacting Stack with Beam Weights; Interacting K.E. [MeV]; Entries per 50 MeV");
interactingStack60A.Add(muonMC_Int )
interactingStack60A.Add(elecMC_Int )
interactingStack60A.Add(pionMC_Int )

# Form staggered plots for incident
incidentStack60A = THStack("incidentStack60A", "Incident Stack with Beam Weights; Incident K.E. [MeV]; Entries per 50 MeV");
incidentStack60A.Add(muonMC_Inc )
incidentStack60A.Add(elecMC_Inc )
incidentStack60A.Add(pionMC_Inc )

# Staggered plots by hand
totHisto_Int = pionMC_Int.Clone("totHisto_Int")
totHisto_Inc = pionMC_Inc.Clone("totHisto_Inc")
for i in xrange(pionMC_Int.GetSize()):
    totHisto_Int.SetBinContent(i, muonMC_Int.GetBinContent(i)+elecMC_Int.GetBinContent(i)+ pionMC_Int.GetBinContent(i))
    totHisto_Inc.SetBinContent(i, muonMC_Inc.GetBinContent(i)+elecMC_Inc.GetBinContent(i)+ pionMC_Inc.GetBinContent(i))


#PionMuE Cross Section
cRecoPiMuEXS = TCanvas("cRecoPiMuEXS" ,"#pi/#mu/e Reconstructed Cross Section" ,200 ,10 ,900 ,900)
cRecoPiMuEXS.Divide(2,2) 
PiMuEXS = totHisto_Int.Clone("MC_PiMuERecoXS")
PiMuEXS.Sumw2()
PiMuEXS.Divide(totHisto_Inc)
PiMuEXS.Scale(101.10968) 
PiMuEXS.SetTitle("#pi/#mu/e MC Reconstructed Cross Section; K.E. [MeV]; Total Hadronic Cross Section per 50 MeV [barn]")
PiMuEXS.Draw("pe")

#PionOnly Cross Section
cRecoPionOnlyXS = TCanvas("cRecoPionOnlyXS" ,"#pi/#mu/e Reconstructed Cross Section" ,200 ,10 ,900 ,900)
cRecoPionOnlyXS.Divide(2,2) 
PionOnlyXS = pionMC_Int.Clone("MC_PionOnlyRecoXS")
PionOnlyXS.Sumw2()
PionOnlyXS.Divide(pionMC_Inc)
PionOnlyXS.Scale(101.10968) 
PionOnlyXS.SetTitle("#pi MC Reconstructed Cross Section; K.E. [MeV]; Total Hadronic Cross Section per 50 MeV [barn]")
PionOnlyXS.Draw("pe")


#PionContent
cPion60A = TCanvas("cPion60A" ,"Plots Overlay" ,200 ,10 ,900 ,900)
cPion60A.Divide(2,2) 
p1 = cPion60A.cd(1)
p1.SetGrid()
pionContent_Int = pionMC_Int.Clone("pionContent_Int")
pionContent_Int.Sumw2()
pionContent_Int.Divide(totHisto_Int)
pionContent_Int.Draw("")
p2 = cPion60A.cd(2)
p2.SetGrid()
pionContent_Inc = pionMC_Inc.Clone("pionContent_Inc")
pionContent_Inc.Sumw2()
pionContent_Inc.Divide(totHisto_Inc)
pionContent_Inc.Draw("")
cPion60A.SetGrid()
cPion60A.Update()


##Plot Staggered plots
p3 = cPion60A.cd(3)
p3.SetGrid()
interactingStack60A.Draw("histo")
legend.Draw("same")
p4 = cPion60A.cd(4)
p4.SetGrid()
incidentStack60A.Draw("histo")
legend.Draw("same")
cPion60A.Update()

outFile = TFile("BackGroundCorrectionPions60A.root","recreate")
outFile.cd()
pionContent_Int.Write("backgroundCorrection_Int",TObject.kWriteDelete)
pionContent_Inc.Write("backgroundCorrection_Inc",TObject.kWriteDelete)
PiMuEXS.Write()
PionOnlyXS.Write()
outFile.Write()
outFile.Close()

raw_input()  





'''
#Plot Overlaid plots
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
c60.SetGrid()
c60.Update()


# Understand the electron contribution to the interacting and incident plots
# i.e. the percentage of each bin in the staggered plot which is due to the electrons
# for each bin: get the electron only plot and divide by 

c60Electron = TCanvas("c60Electron" ,"Electron Contributions" ,200 ,10 ,1200 ,600)
c60Electron.Divide(2,1) 
p3 = c60Electron.cd(1)
p3.SetGrid()
electronNum_Int = elecMC_Int.Clone("electronNum_Int")
totHisto_Int.Sumw2()
electronNum_Int.SetTitle("Relative Electron Contribution to the staggered plot; Electron Interacting KE [MeV]; Percentage to the Staggered plot")
electronNum_Int.GetYaxis().SetRangeUser(0,0.5)
electronNum_Int.GetYaxis().SetTitleOffset(1.5)
electronNum_Int.Divide(totHisto_Int)
electronNum_Int.Draw("pe")
p4 = c60Electron.cd(2)
p4.SetGrid()
totHisto_Inc.Sumw2()
electronNum_Inc = elecMC_Inc.Clone("electronNum_Inc")
electronNum_Inc.Divide(totHisto_Inc)
electronNum_Inc.SetTitle("Relative Electron Contribution to the staggered plot; Electron Incident KE [MeV]; Percentage to the Staggered plot")
electronNum_Inc.GetYaxis().SetRangeUser(0,0.5)
electronNum_Inc.GetYaxis().SetTitleOffset(1.5)
electronNum_Inc.Draw("pe")


## Understanding the muon contributions
c60Muon = TCanvas("c60Muon" ,"Muon Contributions" ,200 ,10 ,1200 ,600)
c60Muon.Divide(2,1) 
pM1 = c60Muon.cd(1)
pM1.SetGrid()
totHisto_Int.Sumw2()
muonNum_Int = muonMC_Int.Clone("muonNum_Int")
muonNum_Int.Divide(totHisto_Int)
muonNum_Int.Draw("pe")
muonNum_Int.SetTitle("Relative Muon Contribution to the staggered plot; Muon Interacting KE [MeV]; Percentage to the Staggered plot")
muonNum_Int.GetYaxis().SetRangeUser(0,0.4)
muonNum_Int.GetYaxis().SetTitleOffset(1.5)
pM2 = c60Muon.cd(2)
pM2.SetGrid()
totHisto_Inc.Sumw2()
muonNum_Inc = muonMC_Inc.Clone("muonNum_Inc")
muonNum_Inc.Divide(totHisto_Inc)
muonNum_Inc.SetTitle("Relative Muon Contribution to the staggered plot; Muon Incident KE [MeV]; Percentage to the Staggered plot")
muonNum_Inc.GetYaxis().SetRangeUser(0,0.4)
muonNum_Inc.GetYaxis().SetTitleOffset(1.5)
muonNum_Inc.Draw("pe")



c60XCheck = TCanvas("c60XCheck" ,"XCheck Contributions" ,200 ,10 ,1200 ,600)
c60XCheck.Divide(2,1) 
c60XCheck.cd(1)
totHisto_Int.Draw("")
c60XCheck.cd(2)
totHisto_Inc.Draw("")


c60XS = TCanvas("c60XS" ,"XS Contributions" ,200 ,10 ,600 ,600)
c60XS.cd()
c60XS.SetGrid()
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
XSstack.SetTitle("Relative Contribution to the XS; Kinetic Energy [MeV]; XS with Contaminants / XS Pions Only ")
XSstack.Divide(pionNum)
XSstack.Sumw2()
XSstack.GetYaxis().SetRangeUser(0.5,1.5)
XSstack.GetXaxis().SetRangeUser(0.,1000)
XSstack.Draw("pe")
c60XS.Update()


#Electrons
c60XSE = TCanvas("c60XSE" ,"XSE Contributions" ,200 ,10 ,600 ,600)
c60XSE.cd()
c60XSE.SetGrid()
# Staggered plots by hand
totHistoE_Int = pionMC_Int.Clone("totHisto_Int")
totHistoE_Inc = pionMC_Inc.Clone("totHisto_Inc")
for i in xrange(pionMC_Int.GetSize()):
    totHistoE_Int.SetBinContent(i, elecMC_Int.GetBinContent(i)+ pionMC_Int.GetBinContent(i))
    totHistoE_Inc.SetBinContent(i, elecMC_Inc.GetBinContent(i)+ pionMC_Inc.GetBinContent(i))
totHistoE_Int.Sumw2()
totHistoE_Inc.Sumw2()
stackNumE = totHistoE_Int.Clone("stackNum")
stackNumE.Sumw2()
stackNumE.Divide(totHistoE_Inc)


XSEstack = stackNumE.Clone("XSEstack")
XSEstack.Sumw2()
XSEstack.SetTitle("Relative Contribution to the XS; Kinetic Energy [MeV]; XS with Electrons / XS Pions Only ")
XSEstack.Divide(pionNum)
XSEstack.Sumw2()
XSEstack.GetYaxis().SetRangeUser(0.5,1.5)
XSEstack.GetXaxis().SetRangeUser(0.,1000)
XSEstack.Draw("pe")
c60XSE.Update()


#Muons
c60XSM = TCanvas("c60XSM" ,"XSM Contributions" ,200 ,10 ,600 ,600)
c60XSM.cd()
c60XSM.SetGrid()
# Staggered plots by hand
totHistoM_Int = pionMC_Int.Clone("totHisto_Int")
totHistoM_Inc = pionMC_Inc.Clone("totHisto_Inc")
for i in xrange(pionMC_Int.GetSize()):
    totHistoM_Int.SetBinContent(i, muonMC_Int.GetBinContent(i)+ pionMC_Int.GetBinContent(i))
    totHistoM_Inc.SetBinContent(i, muonMC_Inc.GetBinContent(i)+ pionMC_Inc.GetBinContent(i))
totHistoM_Int.Sumw2()
totHistoM_Inc.Sumw2()
stackNumM = totHistoM_Int.Clone("stackNumM")
stackNumM.Sumw2()
stackNumM.Divide(totHistoM_Inc)


XSMstack = stackNumM.Clone("XSMstack")
XSMstack.Sumw2()
XSMstack.SetTitle("Relative Contribution to the XS; Kinetic Energy [MeV]; XS with Muons / XS Pions Only ")
XSMstack.Divide(pionNum)
XSMstack.Sumw2()
XSMstack.GetYaxis().SetRangeUser(0.5,1.5)
XSMstack.GetXaxis().SetRangeUser(0.,1000)
XSMstack.Draw("pe")
c60XSM.Update()
'''

## Final Plots I want out:
# backgroundCorrection_Int
# backgroundCorrection_Inc
# 
#fileName = "OutEl"+str(muonInBeam60A)+".root"
#fileOut = TFile(fileName,"recreate")
#fileOut.Add(XSMstack)
#fileOut.Write()
#fileOut.Close()
raw_input()  



