from ROOT import *
import os
import math
import argparse




backgroundCorrection_FileName = 'BackGroundCorrectionPions60A.root'
backgroundCorrection_File = TFile.Open(backgroundCorrection_FileName)
backgroundCorrection_Int  = backgroundCorrection_File.Get("backgroundCorrection_Int")
backgroundCorrection_Inc  = backgroundCorrection_File.Get("backgroundCorrection_Inc")

efficiencyCorrection_FileName = 'EfficiencyCorrectionPions60A.root'
efficiencyCorrection_File = TFile.Open(efficiencyCorrection_FileName)
efficiencyCorrection_Int  = efficiencyCorrection_File.Get("effCorr_Int_NoFilt")
efficiencyCorrection_Inc  = efficiencyCorrection_File.Get("effCorr_Inc_NoFilt")


pionData_FileName = '/Volumes/Seagate/Elena/TPC/Data60A.root'


###################################################################
####################       Raw Data       #########################
###################################################################
# Get Interacting and Incident plots Reco
pionData_File  = TFile.Open(pionData_FileName)
recoData_Int   = pionData_File.Get("RecoXS/hRecoInteractingKE")
recoData_Inc   = pionData_File.Get("RecoXS/hRecoIncidentKE")
# Assign colors
recoData_Int.SetLineColor(kBlack)  
recoData_Inc.SetLineColor(kBlack)  
recoData_Int.SetMarkerSize(0.5)  
recoData_Inc.SetMarkerSize(0.5)  
recoData_Int.SetMarkerStyle(21)  
recoData_Inc.SetMarkerStyle(21)  
recoData_Int.SetLineWidth(2)  
recoData_Inc.SetLineWidth(2)  

#legend = TLegend(.54,.52,.84,.70);
#legend.AddEntry(recoData_Int   ,"Reconstructed Data");



# Comparison between plots
cRaw = TCanvas("cRaw" ,"Uncorrected Interacting and Incindent" ,0 ,0 ,1800 ,600)
cRaw.Divide(3,1)
pRaw1 = cRaw.cd(1)
pRaw1.SetGrid()
recoData_Int.Draw("pe")

pRaw2 = cRaw.cd(2)
pRaw2.SetGrid()
recoData_Inc.Draw("pe")
cRaw.Update()

pRaw3 = cRaw.cd(3)
pRaw3.SetGrid()
rawXS = recoData_Int.Clone("rawXS")
rawXS.Sumw2()
rawXS.Divide(recoData_Inc)
rawXS.Scale(101.10968)
rawXS.Draw("pe")

cRaw.Update()



######################################################################
####################       BkgSub Data       #########################
######################################################################
# Background Subtracted Interacting Plot
cBkgSub = TCanvas("cBkgSub" ,"Background Subtracted Interacting and Incindent" ,0 ,0 ,1800 ,600)
cBkgSub.Divide(3,1)
pBkgSub1 = cBkgSub.cd(1)
pBkgSub1.SetGrid()
bkgSubData_Int = recoData_Int.Clone("bkgSubData_Int")
bkgSubData_Int.Multiply(backgroundCorrection_Int)
bkgSubData_Int.SetMarkerColor(kBlue)
bkgSubData_Int.SetLineColor(kBlue)
bkgSubData_Int.Draw("pe")

# Background Subtracted Incident Plot
pBkgSub2 = cBkgSub.cd(2)
pBkgSub2.SetGrid()
bkgSubData_Inc = recoData_Inc.Clone("bkgSubData_Inc")
bkgSubData_Inc.Multiply(backgroundCorrection_Inc)
bkgSubData_Inc.SetMarkerColor(kBlue)
bkgSubData_Inc.SetLineColor(kBlue)
bkgSubData_Inc.Draw("pe")

# Background Subtracted Cross Section
pBkgSub3 = cBkgSub.cd(3)
pBkgSub3.SetGrid()
bkgSubXS = bkgSubData_Int.Clone("bkgSubXS")
bkgSubXS.Divide(bkgSubData_Inc)
bkgSubXS.Scale(101.10968)
bkgSubXS.Draw("pe")

cBkgSub.Update()


######################################################################
##############    Efficiency Correction Data       ###################
######################################################################
# Get Interacting and Incident plots Reco
'''
efficiencyCorrection_Int = recoData_Int.Clone("efficiencyCorrection_Int")
efficiencyCorrection_Inc = recoData_Inc.Clone("efficiencyCorrection_Inc")
for i in xrange(efficiencyCorrection_Int.GetSize()):
    efficiencyCorrection_Int.SetBinContent(i, 1)
    efficiencyCorrection_Int.SetBinError(i, 0.01)
    if i < 6 :
        efficiencyCorrection_Inc.SetBinContent(i, 2)
        efficiencyCorrection_Inc.SetBinError(i, 0.01)
    else:
        efficiencyCorrection_Inc.SetBinContent(i, 0.5)
        efficiencyCorrection_Inc.SetBinError(i, 0.01)
'''


# Efficiency Corrected Interacting Plot
cEffCorrected = TCanvas("cEffCorrected" ,"Efficiency Corrected Interacting and Incindent" ,0 ,0 ,1800 ,600)
cEffCorrected.Divide(3,1)
pEffCorrected1 = cEffCorrected.cd(1)
pEffCorrected1.SetGrid()
effCorrData_Int = bkgSubData_Int.Clone("effCorrData_Int")
effCorrData_Int.Multiply(efficiencyCorrection_Int)
effCorrData_Int.SetMarkerColor(kRed)
effCorrData_Int.SetLineColor(kRed)
effCorrData_Int.Draw("pe")

# Efficiency Corrected Incident Plot
pEffCorrected2 = cEffCorrected.cd(2)
pEffCorrected2.SetGrid()
effCorrData_Inc = bkgSubData_Inc.Clone("effCorrData_Inc")
effCorrData_Inc.Multiply(efficiencyCorrection_Inc)
effCorrData_Inc.SetMarkerColor(kRed)
effCorrData_Inc.SetLineColor(kRed)
effCorrData_Inc.Draw("pe")

# Efficiency Corrected Cross Section
pEffCorrected3 = cEffCorrected.cd(3)
pEffCorrected3.SetGrid()
effCorrXS = effCorrData_Int.Clone("effCorrXS")
effCorrXS.Divide(effCorrData_Inc)
effCorrXS.Scale(101.10968)
effCorrXS.Draw("pe")

cEffCorrected.Update()




# All the Cross Section in One Plot
cSummary = TCanvas("cSummary" ,"All Cross Sections" ,40 ,40 ,1800 ,600)
cSummary.Divide(3,1)
p1 = cSummary.cd(1)
p1.SetGrid()
recoData_Int.Draw("pe")
#bkgSubData_Int.Draw("pesame")
effCorrData_Int.Draw("pesame")

p2 = cSummary.cd(2)
p2.SetGrid()
recoData_Inc.Draw("pe")
#bkgSubData_Inc.Draw("pesame")
effCorrData_Inc.Draw("pesame")

p3 = cSummary.cd(3)
p3.SetGrid()
rawXS.Draw("pe")
#bkgSubXS.Draw("pesame")
effCorrXS.Draw("pesame")
cSummary.Update()


raw_input()  



