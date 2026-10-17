"use strict";
window.TAX_DATA = Object.freeze({
year:2025,
standardDeduction:{single:15750,mfj:31500,mfs:15750,hoh:23625,qss:31500},
brackets:{
single:[[11925,.10],[48475,.12],[103350,.22],[197300,.24],[250525,.32],[626350,.35],[Infinity,.37]],
mfj:[[23850,.10],[96950,.12],[206700,.22],[394600,.24],[501050,.32],[751600,.35],[Infinity,.37]],
mfs:[[11925,.10],[48475,.12],[103350,.22],[197300,.24],[250525,.32],[375800,.35],[Infinity,.37]],
hoh:[[17000,.10],[64850,.12],[103350,.22],[197300,.24],[250500,.32],[626350,.35],[Infinity,.37]],
qss:[[23850,.10],[96950,.12],[206700,.22],[394600,.24],[501050,.32],[751600,.35],[Infinity,.37]]
},
capitalGains:{
single:{zero:48350,fifteen:533400},
mfj:{zero:96700,fifteen:600050},
mfs:{zero:48350,fifteen:300000},
hoh:{zero:64750,fifteen:566700},
qss:{zero:96700,fifteen:600050}
},
eitc:{
investmentLimit:11950,
maxCredit:[649,4328,7152,8046],
agiLimitSingle:[19104,50434,57310,61555],
agiLimitJoint:[26214,57554,64430,68675],
phaseIn:[.0765,.34,.40,.45],
phaseOut:[.0765,.1598,.2106,.2106],
phaseInEnd:[8490,12730,17880,17880],
phaseOutStartSingle:[10620,23350,23350,23350],
phaseOutStartJoint:[17630,30470,30470,30470]
},
ctc:{
perChild:2200,otherDependent:500,actcMax:1700,
phaseoutStart:{single:200000,hoh:200000,mfs:200000,mfj:400000,qss:400000},
phaseoutPer1000:50,earnedIncomeThreshold:2500,actcRate:.15
},
schedule1a:{
tipsMax:25000,tipsMagLimit:{single:150000,mfj:300000,hoh:150000,qss:300000,mfs:0},tipsPhaseoutPer1000:1000,
overtimeMax:{single:12500,mfj:25000,hoh:12500,qss:25000,mfs:0},overtimeMagLimit:{single:150000,mfj:300000,hoh:150000,qss:300000,mfs:0},overtimePhaseoutPer1000:1000,
vehicleInterestMax:10000,vehicleMagLimit:{single:100000,mfj:200000,hoh:100000,qss:200000,mfs:0},vehiclePhaseoutPer1000:200,
seniorMax:6000,seniorMagLimit:{single:75000,mfj:150000,hoh:75000,qss:150000,mfs:0},seniorPhaseoutRate:.06,
ageDateCutoff:"1961-01-02"
},
selfEmployment:{netEarningsFactor:.9235,socialSecurityRate:.124,medicareRate:.029,socialSecurityWageBase:176100,halfTaxDeductionRate:.5},
additionalTaxes:{
niitRate:.038,niitThreshold:{single:200000,mfj:250000,mfs:125000,hoh:200000,qss:250000},
additionalMedicareRate:.009,additionalMedicareThreshold:{single:200000,mfj:250000,mfs:125000,hoh:200000,qss:250000}
},
additionalStandardDeduction:{unmarried:2000,married:1600},
sources:[
{title:"Form 1040 and instructions, 2025",url:"https://www.irs.gov/instructions/i1040gi"},
{title:"2025 EITC tables and limits",url:"https://www.irs.gov/credits-deductions/individuals/earned-income-tax-credit/earned-income-and-earned-income-tax-credit-eitc-tables"},
{title:"Schedule 8812, 2025",url:"https://www.irs.gov/instructions/i1040s8"},
{title:"Schedule C, 2025",url:"https://www.irs.gov/instructions/i1040sc"},
{title:"Schedule SE, 2025",url:"https://www.irs.gov/instructions/i1040sse"},
{title:"Schedule D, 2025",url:"https://www.irs.gov/instructions/i1040sd"},
{title:"Schedule A, 2025",url:"https://www.irs.gov/instructions/i1040sca"},
{title:"About Form 1040",url:"https://www.irs.gov/forms-pubs/about-form-1040"},
{title:"Schedule 1-A information",url:"https://www.irs.gov/newsroom/schedule-1-a-additional-deductions-what-to-know-about-the-new-form"}
],
forms:[
{form:"Form 1040",es:"Declaración individual federal",en:"U.S. Individual Income Tax Return",url:"https://www.irs.gov/pub/irs-pdf/f1040.pdf",lines:"1a wages; 2b taxable interest; 3a qualified dividends; 3b ordinary dividends; 4-6 retirement/Social Security; 7a capital gain or loss; 8 additional income; 9 total income; 10 adjustments; 11a/11b AGI; 12 deduction; 13a QBI; 13b Schedule 1-A; 14 deductions; 15 taxable income; 16 tax; 19 CTC/ODC; 20 Schedule 3 credits; 23 additional taxes; 24 total tax; 25 withholding; 26 estimated payments; 27 EITC; 28 ACTC; 33 total payments; 34 overpayment; 37 amount owed."},
{form:"Schedule 1",es:"Ingresos adicionales y ajustes",en:"Additional Income and Adjustments to Income",url:"https://www.irs.gov/pub/irs-pdf/f1040s1.pdf",lines:"Part I additional income; Part II adjustments to income."},
{form:"Schedule 1-A",es:"Deducciones adicionales de 2025",en:"Additional Deductions",url:"https://www.irs.gov/pub/irs-pdf/f1040s1a.pdf",lines:"Deductions for qualified tips, qualified overtime, qualified passenger vehicle loan interest, and enhanced senior deduction; total flows to Form 1040 line 13b."},
{form:"Schedule 2",es:"Impuestos adicionales",en:"Additional Taxes",url:"https://www.irs.gov/pub/irs-pdf/f1040s2.pdf",lines:"Includes additional taxes such as self-employment tax and other taxes that flow to Form 1040 line 23."},
{form:"Schedule 3",es:"Créditos y pagos adicionales",en:"Additional Credits and Payments",url:"https://www.irs.gov/pub/irs-pdf/f1040s3.pdf",lines:"Certain nonrefundable credits and additional payments; generally flows to Form 1040 lines 20 and 31."},
{form:"Schedule C",es:"Ganancias o pérdidas del negocio",en:"Profit or Loss From Business",url:"https://www.irs.gov/pub/irs-pdf/f1040sc.pdf",lines:"Business gross receipts, returns/allowances, expenses, and net profit/loss; net profit generally flows to Schedule 1."},
{form:"Schedule SE",es:"Impuesto de trabajo por cuenta propia",en:"Self-Employment Tax",url:"https://www.irs.gov/pub/irs-pdf/f1040sse.pdf",lines:"Calculates self-employment tax; tax generally flows to Schedule 2 and half-tax deduction to Schedule 1."},
{form:"Schedule A",es:"Deducciones detalladas",en:"Itemized Deductions",url:"https://www.irs.gov/pub/irs-pdf/f1040sa.pdf",lines:"Itemized deductions compared with the standard deduction; Form 1040 line 12."},
{form:"Schedule D",es:"Ganancias y pérdidas de capital",en:"Capital Gains and Losses",url:"https://www.irs.gov/pub/irs-pdf/f1040sd.pdf",lines:"Net short-term and long-term gains/losses; Form 1040 line 7a; special tax worksheet may apply."},
{form:"Schedule 8812",es:"Crédito tributario por hijos y otros dependientes",en:"Credits for Qualifying Children and Other Dependents",url:"https://www.irs.gov/pub/irs-pdf/f1040s8.pdf",lines:"Calculates CTC, ODC and ACTC; Form 1040 lines 19 and 28."},
{form:"Schedule EIC",es:"Información de hijos calificados para EITC",en:"Earned Income Credit",url:"https://www.irs.gov/pub/irs-pdf/f1040seic.pdf",lines:"Required in applicable cases with qualifying children; Form 1040 line 27."}
]
});
