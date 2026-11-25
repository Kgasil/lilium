/* Deterministic local calculators; monetary inputs are integer cents. */
(function(root){
"use strict";
function cents(s){s=String(s).trim().replace(",",".");if(!/^\d{1,9}(?:\.\d{1,2})?$/.test(s))throw new Error("Informe um valor não negativo com até duas casas decimais.");const [a,b=""]=s.split(".");return Number(a)*100+Number((b+"00").slice(0,2));}
function percentBps(s){const x=cents(s);if(x>=10000)throw new Error("A margem desejada deve ser menor que 100%.");return x;}
function profit(revenue,cost){const r=cents(revenue),c=cents(cost);return {result:r-c,margin:r===0?null:(r-c)/r*100};}
function pricing(cost,margin){const c=cents(cost),m=percentBps(margin);const price=Number((BigInt(c)*10000n+BigInt(9999-m))/BigInt(10000-m));return {price,contribution:price-c,actualMargin:price===0?null:(price-c)/price*100};}
function breakeven(fixed,price,variable){const f=cents(fixed),p=cents(price),v=cents(variable),contribution=p-v;if(contribution<=0)return {units:null,contribution};const units=Math.ceil(f/contribution);return {units,contribution};}
const api={cents,profit,pricing,breakeven};if(typeof module!=="undefined"&&module.exports)module.exports=api;else root.LiliumMath=Object.freeze(api);
})(typeof globalThis!=="undefined"?globalThis:this);
