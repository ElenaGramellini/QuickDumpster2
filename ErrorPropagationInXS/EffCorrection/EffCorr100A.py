from ROOT import *
import ROOT as root
import numpy as np
import argparse
import os

outFileName = "Eff_Correction_100A.root"

########################################################################
########################    MC Part   ##################################
########################################################################
# Get Monte Carlo files
pionMC_FileName = "/Volumes/Seagate/Elena/TPC/MC100A_Pions.root"
pionMC_File   = TFile.Open(pionMC_FileName)
# Get Interacting and Incident plot
pionMC_Int  = pionMC_File.Get("RecoXSPionOnly/hRecoInteractingKE")
pionMC_Inc  = pionMC_File.Get("RecoXSPionOnly/hRecoIncidentKE")


# Get Truth
pionTrue_45_FileName = "/Volumes/Seagate/Elena/TPC/AngleCut_0.08334_new_histo.root"
pionTrue_45 = TFile.Open(pionTrue_45_FileName)
pionTrue_45_Int  = pionTrue_45.Get("AngleCutTrueXS083/hInteractingKE")
pionTrue_45_Inc  = pionTrue_45.Get("AngleCutTrueXS083/hIncidentKE")


pionTrue_All_FileName = "/Volumes/Seagate/Elena/TPC/AngleCut_100A_histo.root"
pionTrue_All = TFile.Open(pionTrue_All_FileName)
pionTrue_All_Int  = pionTrue_All.Get("TrueXS/hInteractingKE")
pionTrue_All_Inc  = pionTrue_All.Get("TrueXS/hIncidentKE")


###############################################################################

eff_Corr_45_Int = pionMC_Int.Clone("eff_Corr_45_Int_100A")
eff_Corr_45_Int.Sumw2()
pionTrue_45_Int.Sumw2()
eff_Corr_45_Int.Divide(pionTrue_45_Int)   

eff_Corr_45_Inc = pionMC_Inc.Clone("eff_Corr_45_Inc_100A")
eff_Corr_45_Inc.Sumw2()
pionTrue_45_Inc.Sumw2()
eff_Corr_45_Inc.Divide(pionTrue_45_Inc)   

moveXS_45 = eff_Corr_45_Inc.Clone("move_XS_45_100A")
moveXS_45.Divide(eff_Corr_45_Int)   

eff_Corr_45_Int .SetFillColor(kWhite) 
eff_Corr_45_Inc .SetFillColor(kWhite) 
moveXS_45       .SetFillColor(kWhite) 

eff_Corr_45_Int .SetLineColor(kRed) 
eff_Corr_45_Inc .SetLineColor(kRed) 
moveXS_45       .SetLineColor(kRed) 

###############################################################################


eff_Corr_All_Int = pionMC_Int.Clone("eff_Corr_All_Int_100A")
eff_Corr_All_Int.Sumw2()
pionTrue_All_Int.Sumw2()
eff_Corr_All_Int.Divide(pionTrue_All_Int)   

eff_Corr_All_Inc = pionMC_Inc.Clone("eff_Corr_All_Inc_100A")
eff_Corr_All_Inc.Sumw2()
pionTrue_All_Inc.Sumw2()
eff_Corr_All_Inc.Divide(pionTrue_All_Inc)   

moveXS_All = eff_Corr_All_Inc.Clone("move_XS_All_100A")
moveXS_All.Divide(eff_Corr_All_Int)   

eff_Corr_All_Int .SetFillColor(kWhite) 
eff_Corr_All_Inc .SetFillColor(kWhite) 
moveXS_All       .SetFillColor(kWhite) 

###############################################################################

## Check Staggered Plots Make Sense
c0 = TCanvas("c0","c0",1200,600)
c0.Divide(2,1)
p1c0 = c0.cd(1)
p1c0.SetGrid()
eff_Corr_All_Int.Draw("pe")
eff_Corr_45_Int.Draw("pesame")

p2c0 = c0.cd(2)
p2c0.SetGrid()
c0.Update()
eff_Corr_All_Inc.Draw("pe")
eff_Corr_45_Inc.Draw("pesame")
                           
## Check Staggered Plots Make Sense
c0C = TCanvas("c0C","c0C",1200,600)
c0C.Divide(2,1)
p1c0C = c0C.cd(1)
p1c0C.SetGrid()
p1c0C.Update()

p2c0C = c0C.cd(2)
p2c0C.SetGrid()
moveXS_All.Draw("pe")
moveXS_45.Draw("pesame")
c0C.Update()
     
                                


#####################################################################
#######################    Save to File   ###########################
#####################################################################


outFile = TFile(outFileName,"recreate")
outFile.cd()

eff_Corr_All_Int .Write() 
eff_Corr_All_Inc .Write() 
moveXS_All       .Write() 

eff_Corr_45_Int .Write() 
eff_Corr_45_Inc .Write() 
moveXS_45       .Write() 

outFile.Write()
outFile.Close()

raw_input()

