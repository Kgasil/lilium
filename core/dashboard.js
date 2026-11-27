/* Pure dashboard functions. No browser, network or storage dependencies. */
(function(root){
"use strict";
function margin(revenue,cost){
  if(revenue===0)return null;
  const result=BigInt(revenue)-BigInt(cost),den=BigInt(revenue);
  const magnitude=result<0n?-result:result;
  const rounded=(magnitude*10000n*2n+den)/(den*2n);
  return (result<0n?"-":"")+(rounded/100n).toString()+"."+(rounded%100n).toString().padStart(2,"0");
}
function selectPeriod(data,from="",to=""){
  const valid=x=>/^\d{4}-(0[1-9]|1[0-2])$/.test(x);
  if((from&&!valid(from))||(to&&!valid(to))||(from&&to&&from>to))throw Error("Invalid period");
  const months=data.months.filter(m=>(!from||m.month>=from)&&(!to||m.month<=to));
  let revenue=0,cost=0;
  for(const m of months){revenue+=m.revenue_cents;cost+=m.cost_cents;}
  return {from,to,months,totals:{revenue_cents:revenue,cost_cents:cost,result_cents:revenue-cost,margin_pct:margin(revenue,cost)}};
}
function decimal(cents){
  const n=BigInt(cents),a=n<0n?-n:n;
  return (n<0n?"-":"")+(a/100n).toString()+"."+(a%100n).toString().padStart(2,"0");
}
function exportMonthly(view){
  return ["month,revenue_brl,cost_brl,result_brl,margin_pct",...view.months.map(m=>[m.month,decimal(m.revenue_cents),decimal(m.cost_cents),decimal(m.result_cents),m.margin_pct??""].join(","))].join("\r\n")+"\r\n";
}
function chartScale(months){return Math.max(1,...months.flatMap(m=>[m.revenue_cents,m.cost_cents]));}
function marginTarget(view,raw){
  if(typeof raw!=="string"||!/^\d{1,3}(?:[.,]\d{1,2})?$/.test(raw.trim()))throw Error("Informe uma meta de 0 a 100%, com até duas casas decimais.");
  const [a,b=""]=raw.trim().replace(",",".").split(".");
  const target=BigInt(a)*100n+BigInt((b+"00").slice(0,2));
  if(target>10000n)throw Error("A meta deve estar entre 0 e 100%.");
  if(!view.months.length||view.totals.margin_pct===null)return {status:"unavailable",gap:null};
  const actual=BigInt(view.totals.margin_pct.replace(".",""));
  return {status:actual>=target?"met":"below",gap:decimal(actual-target)};
}
function chartSeries(months,mode="comparison"){
  if(!["comparison","result"].includes(mode))throw Error("Invalid chart mode");
  const rows=months.slice(-24).map(m=>({month:m.month,values:mode==="result"?[{value:m.result_cents,kind:m.result_cents<0?"loss":"gain"}]:[{value:m.revenue_cents,kind:"revenue"},{value:m.cost_cents,kind:"cost"}]}));
  return {rows,scale:Math.max(1,...rows.flatMap(r=>r.values.map(v=>Math.abs(v.value))))};
}
const api={margin,selectPeriod,decimal,exportMonthly,chartScale,marginTarget,chartSeries};
if(typeof module!=="undefined"&&module.exports)module.exports=api;else root.LiliumDashboard=Object.freeze(api);
})(typeof globalThis!=="undefined"?globalThis:this);
