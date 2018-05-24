from ROOT import *
import ROOT as root
import numpy as np
import argparse
import os

outFileName = "Eff_Correction.root"

########################################################################
########################    MC Part   ##################################
########################################################################
# Get Monte Carlo files
kaonMC_FileName = "/Volumes/Seagate/Elena/TPC/Kaons/MCKaons_WithDK.root"
kaonMC_File   = TFile.Open(kaonMC_FileName)
# Get Interacting and Incident plot
kaonMC_Int    = kaonMC_File.Get("RecoXSKaonOnly/hRecoInteractingKE")
kaonMC_IntDK  = kaonMC_File.Get("RecoXSKaonOnly/hRecoInteractingKE_DK")
kaonMC_Inc    = kaonMC_File.Get("RecoXSKaonOnly/hRecoIncidentKE")

kaonMC_Int.Add(kaonMC_IntDK,-1)


# Get TruthMC
kaonMC_FileNameTrue = "/Volumes/Seagate/Elena/TPC/Kaons/MCKaon_Picky.root"
kaonTrue_45 = TFile.Open(kaonMC_FileNameTrue)
kaonTrue_45_Int  = kaonTrue_45.Get("TrueXS08/hInteractingKE")
kaonTrue_45_Inc  = kaonTrue_45.Get("TrueXS08/hIncidentKE")
kaonTrue_45_XS = kaonTrue_45_Int.Clone("XS45Deg")
kaonTrue_45_XS.Scale(101.)
kaonTrue_45_XS.Divide(kaonTrue_45_Inc)

kaonTrue_All = TFile.Open(kaonMC_FileName)
kaonTrue_All_Int  = kaonTrue_All.Get("TrueXS/hInteractingKE")
kaonTrue_All_Inc  = kaonTrue_All.Get("TrueXS/hIncidentKE")


###############################################################################

eff_Corr_45_Int = kaonMC_Int.Clone("eff_Corr_45_Int")
eff_Corr_45_Int.Sumw2()
kaonTrue_45_Int.Sumw2()
eff_Corr_45_Int.Divide(kaonTrue_45_Int)   

eff_Corr_45_Inc = kaonMC_Inc.Clone("eff_Corr_45_Inc")
eff_Corr_45_Inc.Sumw2()
kaonTrue_45_Inc.Sumw2()
eff_Corr_45_Inc.Divide(kaonTrue_45_Inc)   

moveXS_45 = eff_Corr_45_Inc.Clone("move_XS_45")
moveXS_45.Divide(eff_Corr_45_Int)   

eff_Corr_45_Int .SetFillColor(kWhite) 
eff_Corr_45_Inc .SetFillColor(kWhite) 
moveXS_45       .SetFillColor(kWhite) 

eff_Corr_45_Int .SetLineColor(kRed) 
eff_Corr_45_Inc .SetLineColor(kRed) 
moveXS_45       .SetLineColor(kRed) 

###############################################################################


eff_Corr_All_Int = kaonMC_Int.Clone("eff_Corr_All_Int")
eff_Corr_All_Int.Sumw2()
kaonTrue_All_Int.Sumw2()
eff_Corr_All_Int.Divide(kaonTrue_All_Int)   

eff_Corr_All_Inc = kaonMC_Inc.Clone("eff_Corr_All_Inc")
eff_Corr_All_Inc.Sumw2()
kaonTrue_All_Inc.Sumw2()
eff_Corr_All_Inc.Divide(kaonTrue_All_Inc)   

moveXS_All = eff_Corr_All_Inc.Clone("move_XS_All")
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
kaonTrue_45_XS.Write()

outFile.Write()
outFile.Close()

raw_input()

