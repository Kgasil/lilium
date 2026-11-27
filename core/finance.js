/* Local, deterministic business simulations. All money is BigInt cents internally.
   Public results use decimal strings of integer cents (JSON safe). */
(function(root){
"use strict";
function cents(value){
  const s=String(value).trim().replace(",",".");
  if(!/^\d{1,9}(?:\.\d{1,2})?$/.test(s))throw Error("Use um valor não negativo, com até 9 dígitos inteiros e 2 decimais.");
  const [a,b=""]=s.split(".");
  return BigInt(a)*100n+BigInt((b+"00").slice(0,2));
}
function percent(value){
  const b=cents(value);
  if(b>=10000n)throw Error("O percentual deve ser menor que 100%.");
  return b;
}
function units(value){
  const s=String(value).trim();
  if(!/^\d{1,7}$/.test(s)||BigInt(s)>1000000n)throw Error("Informe uma quantidade inteira de 0 a 1.000.000.");
  return BigInt(s);
}
function ceil(n,d){return (n+d-1n)/d;}
function ratio(n,d){
  if(d===0n)return null;
  const a=n<0n?-n:n;
  const rounded=(a*20000n+d)/(2n*d);
  return (n<0n&&rounded!==0n?"-":"")+(rounded/100n)+"."+(rounded%100n).toString().padStart(2,"0");
}
function pricing(cost,target){
  const c=cents(cost),m=percent(target);
  const price=ceil(c*10000n,10000n-m);
  return {price_cents:String(price),contribution_cents:String(price-c),margin_pct:ratio(price-c,price)};
}
function simulate(input){
  const p=cents(input.price),v=cents(input.variable),f=cents(input.fixed),q=units(input.quantity),fee=percent(input.fee),target=cents(input.target);
  // Percentage fee rounded half-up per unit; total fees follow this assumption.
  const perFee=(p*fee+5000n)/10000n;
  const contribution=p-v-perFee;
  const revenue=p*q,variable=v*q,fees=perFee*q;
  const result=revenue-variable-fees-f;
  return {revenue_cents:String(revenue),variable_cents:String(variable),fees_cents:String(fees),
    fixed_cents:String(f),result_cents:String(result),unit_contribution_cents:String(contribution),
    result_margin_pct:ratio(result,revenue),contribution_margin_pct:ratio(contribution,p),
    break_even_units:contribution>0n?String(ceil(f,contribution)):f===0n&&contribution===0n?"0":null,
    target_units:contribution>0n?String(ceil(f+target,contribution)):f===0n&&target===0n&&contribution===0n?"0":null,
    quantity:String(q),target_cents:String(target)};
}
function formatBRL(value){
  const n=BigInt(value),a=n<0n?-n:n;
  return (n<0n?"−":"")+"R$ "+(a/100n).toLocaleString("pt-BR")+","+(a%100n).toString().padStart(2,"0");
}
function management(input){
 const month=String(input.month||"");
 if(!/^[0-9]{4}-(0[1-9]|1[0-2])$/.test(month)||month.startsWith("0000"))throw Error("Informe um mês válido.");
 const keys=["revenue","deductions","cogs","expenses","other_income","other_expense","tax","opening","receipts","payments"];
 const v=Object.fromEntries(keys.map(k=>[k,cents(input[k])]));
 const net=v.revenue-v.deductions;
 const gross=net-v.cogs,operating=gross-v.expenses,preTax=operating+v.other_income-v.other_expense;
 const result=preTax-v.tax,flow=v.receipts-v.payments,closing=v.opening+flow;
 const pack=o=>Object.fromEntries(Object.entries(o).map(([k,n])=>[k,String(n)]));
 return {schema_version:"1.0",kind:"management-inputs",month,currency:"BRL",
  dre:pack({revenue:v.revenue,deductions:v.deductions,net_revenue:net,cogs:v.cogs,gross_profit:gross,expenses:v.expenses,operating_result:operating,other_income:v.other_income,other_expense:v.other_expense,pre_tax:preTax,tax:v.tax,result}),
  cash:pack({opening:v.opening,receipts:v.receipts,payments:v.payments,flow,closing}),
  margin_pct:net>0n?ratio(result,net):null,
  notes:["DRE gerencial simplificada, não demonstração contábil oficial.","Recebimentos e pagamentos informados separadamente; não reconciliados com a DRE.","Saldo inicial informado não negativo; saldo final pode ser negativo."]};
}
function compareScenarios(input,low,high){
 const b=units(input.quantity),l=units(low),h=units(high);
 if(l>b||h<b)throw Error("Quantidade reduzida ≤ base ≤ ampliada.");
 return [{label:"Reduzido",quantity:l},{label:"Base",quantity:b},{label:"Ampliado",quantity:h}].map(x=>({label:x.label,...simulate({...input,quantity:String(x.quantity)})}));
}
const api={cents,percent,units,pricing,simulate,formatBRL,management,compareScenarios};
if(typeof module!=="undefined"&&module.exports)module.exports=api;else root.LiliumFinance=Object.freeze(api);
})(typeof globalThis!=="undefined"?globalThis:this);
