from ROOT import *
import os
import math
import argparse




backgroundCorrection_FileName = 'BackGroundCorrectionPions60A.root'
backgroundCorrection_File = TFile.Open(backgroundCorrection_FileName)
backgroundCorrection_Int  = backgroundCorrection_File.Get("backgroundCorrection_Int")
backgroundCorrection_Inc  = backgroundCorrection_File.Get("backgroundCorrection_Inc")
XS_MC = backgroundCorrection_File.Get("MC_PionOnlyRecoXS")
XS_MC.SetLineColor(kRed)
XS_MC.SetFillColor(0)

efficiencyCorrection_FileName = 'EfficiencyCorrectionPions60A.root'
efficiencyCorrection_File = TFile.Open(efficiencyCorrection_FileName)
efficiencyCorrection_Int  = efficiencyCorrection_File.Get("multEffCorr_Int_NoFilt")
efficiencyCorrection_Inc  = efficiencyCorrection_File.Get("multEffCorr_Inc_NoFilt")
trueXS  = efficiencyCorrection_File.Get("XSTrueNoFilter")


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

legend = TLegend(.54,.52,.84,.70);
legend.AddEntry(recoData_Int   ,"Reconstructed Data");
legend.AddEntry(bkgSubData_Int ,"Data Background Subtracted");
legend.AddEntry(effCorrData_Int,"Efficiency Corrected");


# All the Cross Section in One Plot
cSummary = TCanvas("cSummary" ,"All Cross Sections" ,40 ,40 ,1800 ,600)
cSummary.Divide(3,1)
p1 = cSummary.cd(1)
p1.SetGrid()
recoData_Int.Draw("pe")
bkgSubData_Int.Draw("pesame")
effCorrData_Int.Draw("pesame")
legend.Draw("same")

p2 = cSummary.cd(2)
p2.SetGrid()
recoData_Inc.Draw("pe")
bkgSubData_Inc.Draw("pesame")
effCorrData_Inc.Draw("pesame")


p3 = cSummary.cd(3)
p3.SetGrid()
rawXS.Draw("pe")
bkgSubXS.Draw("pesame")
effCorrXS.Draw("pesame")
trueXS.Draw("pesamehisto")
cSummary.Update()

cXS = TCanvas("cXS" ,"All Cross Sections" ,40 ,40 ,600 ,600)
cXS.cd()
cXS.SetGrid()
rawXS.Draw("pe")
bkgSubXS.Draw("pesame")
XS_MC.Draw("samehisto")
effCorrXS.Draw("pesame")
trueXS.Draw("samehisto")


legend2 = TLegend(.54,.52,.84,.70);
legend2.AddEntry(rawXS,"Data Raw");
legend2.AddEntry(bkgSubXS,"Data Bkg Sub");
legend2.AddEntry(XS_MC,"Pion Only MC");
legend2.AddEntry(effCorrXS,"Data Efficiency Corrected");
legend2.AddEntry(trueXS,"True MC");
legend2.Draw("same")

cXSApples = TCanvas("cXSApples" ,"All Cross Sections" ,40 ,40 ,600 ,600)
cXSApples.cd()
cXSApples.SetGrid()
#rawXS.Draw("pe")
#bkgSubXS.Draw("pesame")
XS_MC.Draw("samehisto")
effCorrXS.Draw("pesame")
trueXS.Draw("samehisto")
legend2.Draw("same")
cXSApples.Update()



cXSOranges = TCanvas("cXSOranges" ,"All Cross Sections" ,40 ,40 ,600 ,600)
cXSOranges.cd()
cXSOranges.SetGrid()
rawXS.Draw("pe")
bkgSubXS.Draw("pesame")
XS_MC.Draw("samehisto")
#effCorrXS.Draw("pesame")
#trueXS.Draw("samehisto")
legend2.Draw("same")
cXSOranges.Update()
cXS.Update()


outFile = TFile("DataCorrected.root","recreate")
outFile.cd()

bkgSubXS.Write("pionXS_DataBkgSub"       ,TObject.kWriteDelete)
effCorrXS.Write("pionXS_DataBkgSubEffCorr",TObject.kWriteDelete)


outFile.Write()
outFile.Close()



raw_input()  



