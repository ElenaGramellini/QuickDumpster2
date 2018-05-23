from ROOT import *
import ROOT as root
import numpy as np
from array import array

gStyle.SetOptStat(0)

'''
inFileName          = "../StatOnly/XSRaw_StatOnlyUnc_Data60A.root"
f                   = root.TFile(inFileName)
XS_Stat             = f.Get("XS_Out")
XS_Stat.SetBinContent(3,-100)
XS_Stat.SetBinError(3,0)



inFileNameSys          = "../Systematics/XSRaw_SysOnlyUnc_SystematicsEnergy60A.root"
fSys                  = root.TFile(inFileNameSys)
XS_SysMax             = fSys.Get("XS_ErrMax")
XS_SysMin             = fSys.Get("XS_ErrMin")


inFileNameBkg          = "../BkgSub/BkgSubWithBuoundaries_60A.root"
fBkg                  = root.TFile(inFileNameBkg)
XS_BkgSub             = fBkg.Get("XS_BkgSub60A")
XS_BkgMax             = fBkg.Get("XS_BkgSub_Max60A")
XS_BkgMin             = fBkg.Get("XS_BkgSub_Min60A")


inFileNameEff          = "../EffCorrection/Eff_Correction_60A_WithBoundaries.root"
fEff                  = root.TFile(inFileNameEff)
XS_Eff                = fEff.Get("XS_Eff")
XS_EffMax             = fEff.Get("XS_Eff_Max")
XS_EffMin             = fEff.Get("XS_Eff_Min")
'''

inFileNameEff_60A     = "../EffCorrection/Eff_Correction_60A.root"
fEff_60A              = root.TFile(inFileNameEff_60A)
eff_Corr_45_Int_60A   = fEff_60A.Get("eff_Corr_45_Int_60A")
eff_Corr_45_Inc_60A   = fEff_60A.Get("eff_Corr_45_Inc_60A")


inFileNameEff_100A     = "../EffCorrection/Eff_Correction_100A.root"
fEff_100A              = root.TFile(inFileNameEff_100A)
eff_Corr_45_Int_100A   = fEff_100A.Get("eff_Corr_45_Int_100A")
eff_Corr_45_Inc_100A   = fEff_100A.Get("eff_Corr_45_Inc_100A")


eff_Corr_45_Int_60A_C = eff_Corr_45_Int_60A.Clone("eff_Corr_45_Int_60A_C")
eff_Corr_45_Inc_60A_C = eff_Corr_45_Inc_60A.Clone("eff_Corr_45_Inc_60A_C")

eff_Corr_45_Int_60A_C.Add(eff_Corr_45_Int_100A)
eff_Corr_45_Inc_60A_C.Add(eff_Corr_45_Inc_100A)


eff_Corr_45_Int_60A_C.Scale(101.)
eff_Corr_45_Int_60A_C.Sumw2()
eff_Corr_45_Int_60A_C.Divide(eff_Corr_45_Inc_60A_C)
eff_Corr_45_Int_60A_C.Draw("pe")


#eff_Corr_45_Int_60A.Scale(101.)
#eff_Corr_45_Int_60A.Sumw2()
#eff_Corr_45_Int_60A.Divide(eff_Corr_45_Inc_60A)
#eff_Corr_45_Int_60A.SetLineColor(kBlue)
#eff_Corr_45_Int_60A.Draw("pesame")

#eff_Corr_45_Int_100A.Scale(101.)
#eff_Corr_45_Int_100A.Sumw2()
#eff_Corr_45_Int_100A.SetLineColor(kBlack)
#eff_Corr_45_Int_100A.Divide(eff_Corr_45_Inc_100A)
#eff_Corr_45_Int_100A.Draw("pesame")

raw_input()

