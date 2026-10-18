"use strict";
window.TAX_DATA={
year:2025,
currency:"USD",
sources:[
{name:"IRS: tasas y tramos federales de 2025",url:"https://www.irs.gov/filing/federal-income-tax-rates-and-brackets"},
{name:"IRS: Publicación 501, dependientes y deducción estándar",url:"https://www.irs.gov/publications/p501"},
{name:"IRS: información para presentar la declaración",url:"https://www.irs.gov/filing"},
{name:"IRS: crédito por ingreso del trabajo",url:"https://www.irs.gov/credits-deductions/individuals/earned-income-tax-credit-eitc"},
{name:"IRS: crédito tributario por hijos",url:"https://www.irs.gov/credits-deductions/individuals/child-tax-credit"},
{name:"IRS: trabajo por cuenta propia",url:"https://www.irs.gov/businesses/small-businesses-self-employed/self-employed-individuals-tax-center"}
],
standardDeduction:{single:15750,marriedJoint:31500,marriedSeparate:15750,headOfHousehold:23625,qualifyingSurvivingSpouse:31500},
additionalStandardDeduction:{single:2000,marriedJointPerEligible:1600,marriedSeparate:1600,headOfHousehold:2000,qualifyingSurvivingSpouse:1600},
brackets:{
single:[[11925,.10],[48475,.12],[103350,.22],[197300,.24],[250525,.32],[626350,.35],[Infinity,.37]],
marriedJoint:[[23850,.10],[96950,.12],[206700,.22],[394600,.24],[501050,.32],[751600,.35],[Infinity,.37]],
marriedSeparate:[[11925,.10],[48475,.12],[103350,.22],[197300,.24],[250525,.32],[375800,.35],[Infinity,.37]],
headOfHousehold:[[17000,.10],[64850,.12],[103350,.22],[197300,.24],[250500,.32],[626350,.35],[Infinity,.37]],
qualifyingSurvivingSpouse:[[23850,.10],[96950,.12],[206700,.22],[394600,.24],[501050,.32],[751600,.35],[Infinity,.37]]
},
filingStatuses:[
{value:"single",label:{es:"Soltero/a",en:"Single"}},
{value:"marriedJoint",label:{es:"Casado/a y declaramos juntos",en:"Married filing jointly"}},
{value:"marriedSeparate",label:{es:"Casado/a y declaramos por separado",en:"Married filing separately"}},
{value:"headOfHousehold",label:{es:"Cabeza de familia (hay requisitos)",en:"Head of household (eligibility rules apply)"}},
{value:"qualifyingSurvivingSpouse",label:{es:"Cónyuge sobreviviente que cumple los requisitos",en:"Qualifying surviving spouse"}}
],
money(n){return new Intl.NumberFormat("en-US",{style:"currency",currency:"USD",maximumFractionDigits:2}).format(Number(n)||0)}
};
