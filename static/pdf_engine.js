"use strict";
window.TAX_PDF = (() => {
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const usd=(v,lang)=>new Intl.NumberFormat(lang==="es"?"es-US":"en-US",{style:"currency",currency:"USD"}).format(Number(v)||0);
function printGuide(r,lang="es"){
 const w=window.open("","_blank");
 if(!w){alert(lang==="es"?"El navegador bloqueó la ventana. Permite ventanas emergentes para generar la guía.":"The browser blocked the window. Allow pop-ups to generate the guide.");return}
 const es=lang==="es",s=r.summary,d=r.details;
 const title=es?"Guía educativa de impuestos federales — 2025":"Educational federal tax guide — 2025";
 const label=(es?a=>a.es:a=>a.en);
 const items=[
 [es?"Ingresos totales estimados":"Estimated total income",s.totalIncome],
 [es?"Ingreso bruto ajustado (AGI)":"Adjusted gross income (AGI)",s.agi],
 [es?"Deducción utilizada":"Deduction used",s.deductionUsed],
 [es?"Deducción Schedule 1-A":"Schedule 1-A deduction",s.schedule1ADeduction],
 [es?"Ingreso imponible estimado":"Estimated taxable income",s.taxableIncome],
 [es?"Impuesto federal sobre ingresos estimado":"Estimated federal income tax",s.incomeTax],
 [es?"Impuesto de trabajo por cuenta propia":"Self-employment tax",s.seTax],
 [es?"Créditos no reembolsables estimados":"Estimated nonrefundable credits",s.ctc+s.otherCredits],
 [es?"EITC estimado":"Estimated EITC",s.eitc],
 [es?"Crédito adicional por hijos (ACTC)":"Additional Child Tax Credit (ACTC)",s.actc],
 [es?"Retenciones y pagos totales":"Total withholding and payments",s.payments],
 [es?"Impuestos totales estimados":"Estimated total taxes",s.totalTax],
 [es?"Reembolso estimado":"Estimated refund",s.refund],
 [es?"Posible saldo a pagar":"Possible amount owed",s.owed]
 ];
 const resultRows=items.map(([a,b])=>`<tr><th>${esc(a)}</th><td>${esc(usd(b,lang))}</td></tr>`).join("");
 const warnings=r.warnings.map(x=>`<li>${esc(x)}</li>`).join("")||`<li>${es?"No hay advertencias adicionales.":"No additional warnings."}</li>`;
 const formRows=r.mapping.map(f=>`<tr><td><strong>${esc(f.form)}</strong><br>${esc(label(f))}</td><td>${esc(f.lines)}</td><td><a href="${esc(f.url)}" target="_blank" rel="noopener noreferrer">${es?"Abrir PDF oficial":"Open official PDF"}</a></td></tr>`).join("");
 const sourceRows=window.TAX_DATA.sources.map(x=>`<li><a href="${esc(x.url)}" target="_blank" rel="noopener noreferrer">${esc(x.title)}</a></li>`).join("");
 const explanations=es?`
 <h2>Cómo leer el resultado</h2>
 <ul>
 <li><b>Ingresos totales:</b> suma estimada de los ingresos introducidos. El tratamiento fiscal de ciertos ingresos puede necesitar hojas oficiales adicionales.</li>
 <li><b>AGI:</b> ingresos totales menos los ajustes que este cálculo reconoce. El AGI influye en la elegibilidad de muchos créditos y deducciones.</li>
 <li><b>Deducción utilizada:</b> compara la deducción estándar aproximada con las deducciones detalladas introducidas. La deducción adicional por edad o ceguera se incorpora según las respuestas.</li>
 <li><b>Schedule 1-A:</b> suma estimada de deducciones por propinas calificadas, horas extra calificadas, intereses de vehículo elegibles y deducción senior, tras límites iniciales. Confirma los requisitos en las instrucciones oficiales.</li>
 <li><b>Ingreso imponible e impuesto:</b> el impuesto se estima aplicando tramos progresivos y tasas preferenciales a ganancias de capital a largo plazo/dividendos calificados. Las hojas oficiales pueden exigir otros ajustes.</li>
 <li><b>EITC y créditos por hijos:</b> son estimaciones sujetas a requisitos de edad, parentesco, residencia, ingresos, SSN y otras condiciones. Revisa las hojas oficiales antes de usar una cifra en una declaración.</li>
 <li><b>Reembolso o saldo:</b> compara los pagos y créditos reembolsables estimados con los impuestos calculados. No es una garantía de lo que emitirá o cobrará el IRS.</li>
 </ul>`:`
 <h2>How to read the result</h2>
 <ul>
 <li><b>Total income:</b> estimated total of entered income. Some income types require additional official worksheets.</li>
 <li><b>AGI:</b> total income minus the adjustments recognized by this calculation. AGI affects eligibility for many credits and deductions.</li>
 <li><b>Deduction used:</b> compares the estimated standard deduction with the itemized deductions entered. Additional age/blindness amounts are included based on your answers.</li>
 <li><b>Schedule 1-A:</b> estimated deductions for qualified tips, qualified overtime, eligible vehicle interest, and the senior deduction after initial limits. Confirm all requirements in official instructions.</li>
 <li><b>Taxable income and tax:</b> estimated using progressive brackets and preferential rates for long-term capital gains/qualified dividends. Official worksheets may require additional adjustments.</li>
 <li><b>EITC and child credits:</b> estimates subject to age, relationship, residence, income, SSN, and other requirements. Review official worksheets before using an amount on a return.</li>
 <li><b>Refund or balance due:</b> compares estimated payments and refundable credits with calculated taxes. It does not guarantee what the IRS will pay or collect.</li>
 </ul>`;
 const html=`<!doctype html><html lang="${es?"es":"en"}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(title)}</title>
 <style>body{font:14px Arial,sans-serif;color:#202b32;max-width:950px;margin:25px auto;padding:0 18px;line-height:1.45}h1{font-size:24px}h2{font-size:18px;margin-top:24px;border-bottom:1px solid #ccd5da;padding-bottom:5px}.banner{border:2px solid #9c2525;padding:12px;font-weight:bold;color:#8b2020;margin:18px 0}table{width:100%;border-collapse:collapse;margin:12px 0}td,th{border:1px solid #cbd4da;padding:8px;text-align:left;vertical-align:top}td:nth-child(2){font-variant-numeric:tabular-nums}a{color:#075b89;overflow-wrap:anywhere}li{margin:7px 0}.small{font-size:12px;color:#485965}.buttons{margin:15px 0}button{padding:10px 14px;margin-right:8px;font-size:14px}@media print{.buttons{display:none}body{margin:0;max-width:none;padding:0}a{color:#000;text-decoration:underline}tr{break-inside:avoid}h2{break-after:avoid}}</style></head><body>
 <div class="buttons"><button onclick="window.print()">${es?"Imprimir / Guardar como PDF":"Print / Save as PDF"}</button><button onclick="window.close()">${es?"Cerrar":"Close"}</button></div>
 <h1>${esc(title)}</h1><p>${es?"Preparada localmente en tu navegador a partir de los importes introducidos.":"Generated locally in your browser from the amounts entered."}</p>
 <div class="banner">${es?"EJEMPLO EDUCATIVO — NO ES UNA DECLARACIÓN PRESENTADA AL IRS. LAS CIFRAS SON ESTIMACIONES Y REQUIEREN VERIFICACIÓN.":"EDUCATIONAL GUIDE — NOT A RETURN FILED WITH THE IRS. FIGURES ARE ESTIMATES AND REQUIRE VERIFICATION."}</div>
 <p><b>${es?"Estado civil seleccionado:":"Selected filing status:"}</b> ${esc(r.status)}<br><b>${es?"Año fiscal:":"Tax year:"}</b> ${r.year}</p>
 <h2>${es?"Resumen del resultado":"Result summary"}</h2><table><tbody>${resultRows}</tbody></table>
 ${explanations}
 <h2>${es?"Cálculos intermedios":"Intermediate calculations"}</h2>
 <table><tbody>
 <tr><th>${es?"Ganancia/pérdida estimada de Schedule C":"Estimated Schedule C profit/loss"}</th><td>${usd(d.businessProfit,lang)}</td></tr>
 <tr><th>${es?"Impuesto de Seguro Social por trabajo independiente":"Self-employment Social Security tax"}</th><td>${usd(d.selfEmployment.socialSecurity,lang)}</td></tr>
 <tr><th>${es?"Impuesto de Medicare por trabajo independiente":"Self-employment Medicare tax"}</th><td>${usd(d.selfEmployment.medicare,lang)}</td></tr>
 <tr><th>${es?"Deducción estimada de la mitad del impuesto SE":"Estimated deduction for half of SE tax"}</th><td>${usd(d.selfEmployment.halfDeduction,lang)}</td></tr>
 <tr><th>${es?"Propinas deducibles estimadas":"Estimated tips deduction"}</th><td>${usd(d.schedule1A.tips,lang)}</td></tr>
 <tr><th>${es?"Horas extra deducibles estimadas":"Estimated overtime deduction"}</th><td>${usd(d.schedule1A.overtime,lang)}</td></tr>
 <tr><th>${es?"Interés de vehículo deducible estimado":"Estimated vehicle interest deduction"}</th><td>${usd(d.schedule1A.vehicleInterest,lang)}</td></tr>
 <tr><th>${es?"Deducción senior estimada":"Estimated senior deduction"}</th><td>${usd(d.schedule1A.senior,lang)}</td></tr>
 <tr><th>${es?"Ganancia neta de capital":"Net capital gain"}</th><td>${usd(d.capitalGains.net,lang)}</td></tr>
 </tbody></table>
 <h2>${es?"Advertencias que debes revisar":"Warnings to review"}</h2><ul>${warnings}</ul>
 <h2>${es?"Correspondencia inicial con los formularios originales":"Initial mapping to original forms"}</h2>
 <p>${es?"La correspondencia que sigue es una orientación para localizar líneas y formularios. No significa que la aplicación haya rellenado los PDF originales. Abre los formularios oficiales, verifica las instrucciones del año 2025 y completa los originales de forma independiente.":"The mapping below is a guide to locating forms and lines. It does not mean that the app has filled the original PDFs. Open the official forms, verify the 2025 instructions, and complete the originals independently."}</p>
 <table><thead><tr><th>${es?"Formulario":"Form"}</th><th>${es?"Uso y correspondencia":"Purpose and mapping"}</th><th>${es?"Documento":"Document"}</th></tr></thead><tbody>${formRows}</tbody></table>
 <h2>${es?"Fuentes oficiales":"Official sources"}</h2><ul>${sourceRows}</ul>
 <h2>${es?"Privacidad y límites":"Privacy and limitations"}</h2>
 <p>${es?"Los cálculos se ejecutaron en este navegador; esta guía se generó en una ventana local. No se transmitió esta información al servidor de la aplicación. La guía no borra copias que puedas guardar, imprimir o capturar en tu dispositivo. No se presenta ni transmite una declaración al IRS.":"Calculations ran in this browser; this guide was generated in a local window. This information was not transmitted to the app server. The guide cannot erase copies you save, print, or capture on your device. No return is filed or transmitted to the IRS."}</p>
 <p class="small">${es?"La IA, si se añade, solo puede explicar fuentes y señalar dudas. El motor determinista y las instrucciones oficiales controlan los cálculos. Esta guía no sustituye al IRS ni a un contador cualificado.":"If AI is added, it can only explain sources and flag uncertainties. The deterministic engine and official instructions govern calculations. This guide does not replace the IRS or a qualified tax professional."}</p>
 <p class="small">${new Date().toLocaleDateString(es?"es-US":"en-US")}</p>
 <script>window.addEventListener('load',()=>setTimeout(()=>window.print(),500));<\/script>
 </body></html>`;
 w.document.open();w.document.write(html);w.document.close();
 return true;
}
return {printGuide};
})();
