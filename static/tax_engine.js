"use strict";
window.TAX_ENGINE = (() => {
const D=window.TAX_DATA;
const n=v=>Number.isFinite(Number(v))?Number(v):0;
const money=v=>Math.round((n(v)+Number.EPSILON)*100)/100;
const nonneg=v=>Math.max(0,n(v));
const roundDollar=v=>Math.round(n(v));
const sum=(...v)=>v.reduce((a,b)=>a+n(b),0);
const statusOf=s=>D.brackets[s]?s:"single";
function progressiveTax(income,status){
 let x=Math.max(0,n(income)),lower=0,tax=0;
 for(const [upper,rate] of D.brackets[statusOf(status)]){
  const portion=Math.max(0,Math.min(x,upper)-lower);
  tax+=portion*rate;if(x<=upper)break;lower=upper;
 }
 return money(tax);
}
function ordinaryTaxWithCapital(taxable,qualifiedDividends,longTermGain,status){
 const st=statusOf(status),br=D.brackets[st];
 const ordinary=Math.max(0,n(taxable)),pref=Math.min(ordinary,Math.max(0,n(qualifiedDividends))+Math.max(0,n(longTermGain)));
 const ordinaryBase=Math.max(0,ordinary-pref),thresholds=D.capitalGains[st];
 const ordinaryOnStack=progressiveTax(ordinaryBase,st);
 let prefTax=0,remaining=pref,base=ordinaryBase;
 const zeroRoom=Math.max(0,thresholds.zero-base);
 const zero=Math.min(remaining,zeroRoom);remaining-=zero;base+=zero;
 const fifteenRoom=Math.max(0,thresholds.fifteen-base);
 const fifteen=Math.min(remaining,fifteenRoom);remaining-=fifteen;
 prefTax=fifteen*.15+remaining*.20;
 return {tax:money(ordinaryOnStack+prefTax),ordinaryBase:money(ordinaryBase),preferential:money(pref),zeroRate:money(zero),fifteenRate:money(fifteen),twentyRate:money(remaining)};
}
function selfEmploymentTax(netProfit,w2SocialSecurityWages=0){
 const net=nonneg(netProfit)*D.selfEmployment.netEarningsFactor;
 const ssRoom=Math.max(0,D.selfEmployment.socialSecurityWageBase-nonneg(w2SocialSecurityWages));
 const ss=Math.min(net,ssRoom)*D.selfEmployment.socialSecurityRate;
 const medicare=net*D.selfEmployment.medicareRate;
 const total=money(ss+medicare);
 return {netEarnings:money(net),socialSecurity:money(ss),medicare:money(medicare),tax:total,halfDeduction:money(total*D.selfEmployment.halfTaxDeductionRate)};
}
function creditPhaseout(amount,magi,threshold,per1000){
 const excess=Math.max(0,n(magi)-n(threshold));
 return Math.max(0,n(amount)-Math.ceil(excess/1000)*n(per1000));
}
function schedule1A(i,status,magi){
 const s=statusOf(status),p=D.schedule1a,eligibleJoint=s==="mfj"||s==="qss";
 const jointAllowed=(s!=="mfs");
 const ssOk=i.validSsn==="yes";
 const tipsLimit=p.tipsMagLimit[s]||0,overLimit=p.overtimeMagLimit[s]||0;
 let tips=0,overtime=0,vehicle=0,senior=0;
 const tipsAllowed=jointAllowed&&ssOk&&tipsLimit>0;
 const overtimeAllowed=jointAllowed&&ssOk&&overLimit>0;
 if(tipsAllowed)tips=creditPhaseout(Math.min(nonneg(i.qualifiedTips),p.tipsMax),magi,tipsLimit,p.tipsPhaseoutPer1000);
 if(overtimeAllowed)overtime=creditPhaseout(Math.min(nonneg(i.qualifiedOvertime),p.overtimeMax[s]||0),magi,overLimit,p.overtimePhaseoutPer1000);
 const vehicleLimit=p.vehicleMagLimit[s]||0;
 if(jointAllowed&&vehicleLimit>0&&i.vehicleVinKnown==="yes")vehicle=creditPhaseout(Math.min(nonneg(i.carLoanInterest),p.vehicleInterestMax),magi,vehicleLimit,p.vehiclePhaseoutPer1000);
 const seniorLimit=p.seniorMagLimit[s]||0;
 if(jointAllowed&&seniorLimit>0&&i.seniorDeductionEligible==="yes"&&ssOk){
  const eligibleAge=(n(i.age)>=65)||(s==="mfj"&&n(i.spouseAge)>=65);
  const count=(n(i.age)>=65?1:0)+(s==="mfj"&&n(i.spouseAge)>=65?1:0);
  if(eligibleAge)senior=Math.max(0,count*p.seniorMax-Math.max(0,magi-seniorLimit)*p.seniorPhaseoutRate);
 }
 return {tips:money(tips),overtime:money(overtime),vehicleInterest:money(vehicle),senior:money(senior),total:money(tips+overtime+vehicle+senior),
 flags:{tipsEligible:tipsAllowed,overtimeEligible:overtimeAllowed,vehicleEligible:jointAllowed&&vehicleLimit>0&&i.vehicleVinKnown==="yes",seniorEligible:senior>0}};
}
function eitcCredit(income,children,status){
 const s=statusOf(status),c=Math.min(3,Math.max(0,Math.floor(n(children))));
 const max=D.eitc.maxCredit[c],rate=D.eitc.phaseIn[c],outRate=D.eitc.phaseOut[c];
 const phaseEnd=D.eitc.phaseInEnd[c],outStart=s==="mfj"?D.eitc.phaseOutStartJoint[c]:D.eitc.phaseOutStartSingle[c];
 const agiLimit=s==="mfj"?D.eitc.agiLimitJoint[c]:D.eitc.agiLimitSingle[c];
 const x=nonneg(income);
 let value;
 if(x<phaseEnd)value=x*rate;
 else if(x<=outStart)value=max;
 else value=Math.max(0,max-(x-outStart)*outRate);
 return {amount:money(Math.min(max,value)),max,eligibleIncomeLimit:agiLimit};
}
function earnedIncomeCredit(i,agi,status){
 const c=Math.min(3,Math.max(0,Math.floor(n(i.eitcChildren))));
 const earned=nonneg(i.eitcEarnedIncome)>0?nonneg(i.eitcEarnedIncome):sum(i.wages,i.qualifiedTips,i.qualifiedOvertime,Math.max(0,n(i.businessReceipts)-n(i.returns)-n(i.businessExpenses)));
 const earnedCalc=eitcCredit(earned,c,status),agiCalc=eitcCredit(agi,c,status);
 const maxAgi=status==="mfj"?D.eitc.agiLimitJoint[c]:D.eitc.agiLimitSingle[c];
 const invest=nonneg(i.investmentIncome);
 const joint=status==="mfj";
 const statusAllowed=status!=="mfs";
 let amount=Math.min(earnedCalc.amount,agiCalc.amount);
 if(agi>maxAgi||invest>D.eitc.investmentLimit||!statusAllowed||i.validSsn!=="yes")amount=0;
 if(c===0&&n(i.age)<25||c===0&&n(i.age)>64)amount=0;
 return {amount:money(amount),earnedIncome:money(earned),agi:money(agi),children:c,investmentIncome:money(invest),maxAgi,investmentLimit:D.eitc.investmentLimit,method:"Estimación por tasas y límites publicados; confirmar en EIC Worksheet y tabla EITC 2025.",joint};
}
function childTaxCredit(i,agi,taxBeforeCredits){
 const s=statusOf(i.filingStatus),eligibleSsn=i.validSsn==="yes";
 const children=Math.max(0,Math.floor(n(i.qualifyingChildren))),other=Math.max(0,Math.floor(n(i.otherDependents)));
 const threshold=D.ctc.phaseoutStart[s];
 const raw=children*D.ctc.perChild+other*D.ctc.otherDependent;
 const phase=Math.ceil(Math.max(0,agi-threshold)/1000)*D.ctc.phaseoutPer1000;
 const allowed=eligibleSsn?Math.max(0,raw-phase):0;
 const nonrefundable=Math.min(nonneg(taxBeforeCredits),allowed);
 const unused=Math.max(0,allowed-nonrefundable);
 const earned=nonneg(i.wages)+nonneg(i.eitcEarnedIncome)+Math.max(0,n(i.businessReceipts)-n(i.returns)-n(i.businessExpenses));
 const refundableBase=Math.floor(Math.max(0,earned-D.ctc.earnedIncomeThreshold)*D.ctc.actcRate);
 const actc=eligibleSsn?Math.min(D.ctc.actcMax*children,unused,refundableBase):0;
 return {raw:money(raw),phaseout:money(phase),allowed:money(allowed),nonrefundable:money(nonrefundable),odcIncluded:money(other*D.ctc.otherDependent),actc:money(actc),children,other,ssnOk:eligibleSsn};
}
function capitalGainSummary(i){
 const short=n(i.shortGain),long=sum(i.longGain,i.capitalDistributions);
 return {short:money(short),long:money(long),net:money(short+long),qualifiedDividends:money(Math.min(nonneg(i.qualifiedDividends),nonneg(i.ordinaryDividends))),longTermPositive:money(Math.max(0,long))};
}
function readInput(form){
 const o={};new FormData(form).forEach((v,k)=>o[k]=v);
 for(const [k,v] of Object.entries(o))if(v!==""&&v!==undefined&&k!=="filingStatus"&&k!=="blind"&&k!=="spouseBlind"&&k!=="validSsn"&&k!=="paidHome"&&k!=="halfSe"&&k!=="vehicleVinKnown"&&k!=="seniorDeductionEligible")o[k]=n(v);
 return o;
}
function calculate(i){
 const warnings=[],notes=[];
 const status=statusOf(i.filingStatus),businessProfit=money(n(i.businessReceipts)-n(i.returns)-n(i.businessExpenses));
 const se=selfEmploymentTax(Math.max(0,businessProfit),0);
 const wages=nonneg(i.wages),interest=nonneg(i.interest),dividends=nonneg(i.ordinaryDividends);
 const cap=capitalGainSummary(i);
 const socialSecurityTaxable=0;
 if(nonneg(i.socialSecurity)>0)warnings.push("El ingreso tributable de Seguro Social no se calculó automáticamente. Usa la hoja oficial de beneficios tributables del IRS.");
 const otherIncome=sum(i.unemployment,i.pension,i.otherIncome,Math.max(0,businessProfit),cap.net,interest,dividends,socialSecurityTaxable);
 const totalIncome=money(wages+otherIncome);
 const adjustments=nonneg(i.adjustments)+se.halfDeduction;
 const agi=money(Math.max(0,totalIncome-adjustments));
 const extraDeduction= schedule1A(i,status,agi);
 const standard=D.standardDeduction[status];
 const ageCount=(n(i.age)>=65?1:0)+(status==="mfj"&&n(i.spouseAge)>=65?1:0);
 const blindCount=(i.blind==="yes"?1:0)+(status==="mfj"&&i.spouseBlind==="yes"?1:0);
 const addStandard=ageCount*D.additionalStandardDeduction[status==="mfj"||status==="mfs"? "married":"unmarried"]+blindCount*D.additionalStandardDeduction[status==="mfj"||status==="mfs"?"married":"unmarried"];
 const deduction=Math.max(standard+addStandard,nonneg(i.itemized));
 const qbi=0;
 const taxable=money(Math.max(0,agi-deduction-qbi-extraDeduction.total));
 const capTax=ordinaryTaxWithCapital(taxable,cap.qualifiedDividends,cap.longTermPositive,status);
 const incomeTax=capTax.tax;
 const seTax=se.tax;
 const medicareThreshold=D.additionalTaxes.additionalMedicareThreshold[status];
 const addMedicare=money(Math.max(0,nonneg(i.medicareWages)+se.netEarnings-medicareThreshold)*D.additionalTaxes.additionalMedicareRate);
 const niitThreshold=D.additionalTaxes.niitThreshold[status];
 const niit=money(Math.min(nonneg(i.netInvestment),Math.max(0,agi-niitThreshold))*D.additionalTaxes.niitRate);
 const totalOtherTaxes=money(nonneg(i.otherTaxes)+seTax+addMedicare+niit);
 const child=childTaxCredit(i,agi,incomeTax);
 const careCredit=0;
 const otherNonrefundable=nonneg(i.otherCredits);
 const credits=money(child.nonrefundable+otherNonrefundable+careCredit);
 const taxAfterCredits=money(Math.max(0,incomeTax-credits));
 const eitc=earnedIncomeCredit(i,agi,status);
 const totalPayments=money(nonneg(i.withheld)+nonneg(i.otherWithheld)+nonneg(i.estimatedPayments)+eitc.amount+child.actc);
 const totalTax=money(taxAfterCredits+totalOtherTaxes);
 const net=money(totalPayments-totalTax);
 if(status==="hoh"&&i.paidHome!=="yes")warnings.push("Head of household: confirma que cumples todos los requisitos de persona no casada/considerada no casada, persona calificada y costo del hogar.");
 if(status==="qss")warnings.push("Qualifying surviving spouse: confirma año de fallecimiento, hijo calificado y los requisitos específicos del estado civil.");
 if(status==="mfs")warnings.push("Married filing separately: puede limitar créditos, deducciones y beneficios; comprueba cada regla aplicable.");
 if(i.validSsn!=="yes")warnings.push("No se confirmó el requisito de SSN. EITC, CTC/ACTC y deducciones de Schedule 1-A pueden no estar disponibles.");
 if(n(i.qualifiedDividends)>n(i.ordinaryDividends))warnings.push("Los dividendos calificados superan los dividendos ordinarios: revisa los importes del Form 1099-DIV.");
 if(n(i.businessReceipts)>0||n(i.businessExpenses)>0)warnings.push("Negocio: revisa Schedule C, inventario, depreciación, millaje, uso del hogar, pérdidas y otros requisitos. El motor no decide qué gasto es deducible.");
 if(n(i.businessReceipts)>0&&businessProfit<0)warnings.push("La pérdida del negocio puede estar sujeta a límites, reglas de riesgo, actividad pasiva o reglas de pérdidas excesivas no calculadas aquí.");
 if(n(i.qualifiedTips)>0&&extraDeduction.tips===0)warnings.push("No se calculó deducción por propinas. Revisa SSN, estado civil, MAGI y requisitos de propinas calificadas.");
 if(n(i.qualifiedOvertime)>0&&extraDeduction.overtime===0)warnings.push("No se calculó deducción por horas extra. Confirma que sea compensación calificada según la ley y que la documentación lo respalde.");
 if(n(i.carLoanInterest)>0&&i.vehicleVinKnown!=="yes")warnings.push("No se concedió la deducción de interés de vehículo porque no se confirmó el VIN y la elegibilidad.");
 if(i.seniorDeductionEligible==="unknown")warnings.push("La deducción mejorada para personas mayores requiere confirmar edad, SSN, MAGI y estado civil.");
 if(n(i.childCare)>0)warnings.push("Gastos de cuidado: no se calculó el crédito. Revisa Form 2441, personas calificadas, límites y gastos laborales.");
 if(n(i.education)>0)warnings.push("Educación: no se calculó el crédito. Revisa Form 8863, institución, matrícula elegible, límites de ingresos y años anteriores.");
 if(n(i.netInvestment)>0||agi>niitThreshold)notes.push("NIIT: la cifra mostrada es una estimación basada en los datos introducidos. Confirma Form 8960 y los componentes del ingreso neto de inversión.");
 if(n(i.medicareWages)>medicareThreshold)notes.push("Impuesto adicional de Medicare: verifica Form 8959, salarios sujetos a Medicare, umbral por estado civil y posible impuesto de trabajo independiente.");
 warnings.push("No se calcularon AMT, crédito tributario extranjero, ingreso extranjero, QBI, ingreso tributable de Seguro Social, pérdidas arrastradas ni todos los impuestos especiales.");
 warnings.push("El EITC se estima con límites y tasas generales; antes de usarlo en una declaración, confirma el EIC Worksheet y la tabla EITC oficial de 2025.");
 warnings.push("El CTC/ACTC es una estimación. Confirma edad, parentesco, residencia, manutención, SSN válido, reglas de custodia y el Schedule 8812 oficial.");
 const refund=Math.max(0,net),owed=Math.max(0,-net);
 return {
year:D.year,status,inputs:i,summary:{wages,otherIncome,totalIncome,adjustments,agi,standardDeduction:money(standard+addStandard),itemizedDeduction:money(nonneg(i.itemized)),deductionUsed:money(deduction),schedule1ADeduction:extraDeduction.total,taxableIncome:taxable,incomeTax,capitalGainTaxBreakdown:capTax,seTax,halfSeDeduction:se.halfDeduction,additionalMedicare:addMedicare,niit,otherTaxes:totalOtherTaxes,ctc:child.nonrefundable,actc:child.actc,eitc:eitc.amount,otherCredits:otherNonrefundable,totalTax,payments:totalPayments,refund,owed},
details:{businessProfit,capitalGains:cap,schedule1A:extraDeduction,eitc,childCredit:child,selfEmployment:se,capitalGainTax:capTax,notes},
warnings:[...warnings,...notes],
mapping:D.forms
};
}
return {calculate,readInput,progressiveTax,ordinaryTaxWithCapital,selfEmploymentTax,earnedIncomeCredit,childTaxCredit,schedule1A,money};
})();
