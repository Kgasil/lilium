/* Lilium public lab: deterministic browser-only examples. */
(function(root){
"use strict";
function evaluate(finance,starter,sales,forecast,kind,input){
 if(kind==="price")return finance.pricing(input.cost,input.margin);
 if(kind==="monthly")return finance.simulate(input);
 if(kind==="scenario"){
  const x=starter.build(input.scenario);
  const s=sales.summarize(sales.parse(x.sales));
  const f=forecast.analyze(forecast.parse(x.forecast),3);
  const cost=x.insights.split("\n").slice(1).reduce((sum,row)=>sum+finance.cents(row.split(",")[2]),0n);
  const revenue=BigInt(s.revenue_cents);
  return {name:x.name,revenue_cents:String(revenue),cost_cents:String(cost),result_cents:String(revenue-cost),orders:s.orders,months:s.months,future:f.future,model:f.model_label,csv:x.insights};
 }
 throw Error("Unknown tool");
}
const api={evaluate};
if(typeof module!=="undefined"&&module.exports){module.exports=api;return;}
const $=id=>document.getElementById(id),deps=[root.LiliumFinance,root.LiliumStarter,root.LiliumSales,root.LiliumForecast];
const lang=()=>document.documentElement.lang==="en"?"en":"pt";
const tr=(pt,en)=>lang()==="en"?en:pt;
const fmt=v=>root.LiliumFinance.formatBRL(v);
const pct=v=>v===null?tr("Indisponível","Unavailable"):v.replace(".",lang()==="en"?".":",")+"%";
const units=v=>v===null?tr("Inviável nas premissas","Not feasible under assumptions"):BigInt(v).toLocaleString(lang()==="en"?"en-US":"pt-BR");
function output(id,items){
 const el=$(id);el.replaceChildren();
 for(const [label,value] of items){const row=document.createElement("div"),dt=document.createElement("dt"),dd=document.createElement("dd");dt.textContent=label;dd.textContent=value;row.append(dt,dd);el.append(row);}
}
let current=null;
function run(){
 for(const [kind,fields] of [["price",["cost","margin"]],["monthly",["price","variable","fixed","quantity","fee","target"]]]){
  const id="lab-"+kind;$(id+"-error").textContent="";
  try{
   const values=Object.fromEntries(fields.map(k=>[k,$(id+"-"+k).value]));
   const r=evaluate(...deps,kind,values);
   output(id+"-result",kind==="price"?[[tr("Preço estimado","Estimated price"),fmt(r.price_cents)],[tr("Contribuição unitária","Unit contribution"),fmt(r.contribution_cents)],[tr("Margem de contribuição","Contribution margin"),pct(r.margin_pct)]]:[[tr("Receita simulada","Simulated revenue"),fmt(r.revenue_cents)],[tr("Resultado mensal","Monthly result"),fmt(r.result_cents)],[tr("Margem do resultado","Result margin"),pct(r.result_margin_pct)],[tr("Ponto de equilíbrio (un.)","Break-even (units)"),units(r.break_even_units)],[tr("Vendas para atingir a meta (un.)","Units to reach target"),units(r.target_units)]]);
  }catch(e){$(id+"-result").replaceChildren();$(id+"-error").textContent=tr("Revise os valores: números não negativos, até 2 decimais; quantidade inteira e percentual menor que 100%.","Check values: nonnegative, up to 2 decimals; integer quantity and percentage below 100%.");}
 }
 try{
  current=evaluate(...deps,"scenario",{scenario:$("lab-scenario").value});
  output("lab-scenario-result",[[tr("Receita · 9 meses","Revenue · 9 months"),fmt(current.revenue_cents)],[tr("Custos estimados","Estimated costs"),fmt(current.cost_cents)],[tr("Resultado","Result"),fmt(current.result_cents)],[tr("Pedidos agregados fictícios","Synthetic aggregate orders"),String(current.orders)],[tr("Próximo mês estimado","Next-month estimate"),new Intl.NumberFormat(lang()==="en"?"en-US":"pt-BR",{style:"currency",currency:"BRL"}).format(current.future[0].value)]]);
  $("lab-download").disabled=false;
 }catch(e){current=null;$("lab-scenario-result").replaceChildren();$("lab-download").disabled=true;}
}
for(const id of ["lab-price-form","lab-monthly-form"])$(id).addEventListener("submit",e=>{e.preventDefault();run();});
for(const id of ["lab-price-form","lab-monthly-form"])$(id).addEventListener("input",run);
$("lab-scenario").addEventListener("change",run);
$("lab-download").addEventListener("click",()=>{if(!current)return;const url=URL.createObjectURL(new Blob([current.csv],{type:"text/csv;charset=utf-8"}));const a=document.createElement("a");a.href=url;a.download="lilium-"+$("lab-scenario").value+"-sample.csv";a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
document.addEventListener("lilium-language",run);
run();
})(typeof globalThis!=="undefined"?globalThis:this);
