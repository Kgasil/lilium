/* Restricted sales CSV. Exact integer-cent arithmetic; no network or storage. */
(function(root){
"use strict";
const HEADER="date,order_id,product,quantity,unit_price", MAX_BYTES=1048576, MAX_ROWS=10000;
function fail(row,message){throw Error("Linha "+row+": "+message);}
function bytes(s){let n=0;for(const c of s){const p=c.codePointAt(0);n+=p<128?1:p<2048?2:p<65536?3:4;if(n>MAX_BYTES)break;}return n;}
function validDate(s){const m=/^(\d{4})-(\d{2})-(\d{2})$/.exec(s);if(!m)return false;const y=Number(m[1]),mo=Number(m[2]),d=Number(m[3]);if(y<1||mo<1||mo>12)return false;const leap=y%4===0&&(y%100!==0||y%400===0);return d>=1&&d<=[31,leap?29:28,31,30,31,30,31,31,30,31,30,31][mo-1];}
function parse(raw){
 if(typeof raw!=="string"||bytes(raw)>MAX_BYTES)throw Error("CSV de até 1 MiB.");
 const lines=raw.replace(/^\uFEFF/,"").replace(/\r?\n$/,"").split(/\r?\n/);
 if(lines[0]?.trim().toLowerCase()!==HEADER)fail(1,"Cabeçalho esperado: "+HEADER);
 if(lines.length<2||lines.length>MAX_ROWS+1)throw Error("Use de 1 a 10.000 linhas de dados.");
 const rows=[],orders=new Map();
 for(let i=1;i<lines.length;i++){
  const fields=lines[i].split(",").map(x=>x.trim());
  if(fields.length!==5||fields.some(x=>/["\u0000-\u001f\u007f]/.test(x)))fail(i+1,"Use cinco campos simples, sem aspas ou caracteres de controle.");
  const [date,order,product,q,p]=fields;
  if(!validDate(date))fail(i+1,"Data inválida (AAAA-MM-DD).");
  if(!order||order.length>80||!product||product.length>120)fail(i+1,"Pedido e produto obrigatórios (80/120 caracteres).");
  if(!/^\d{1,7}$/.test(q)||BigInt(q)<1n||BigInt(q)>1000000n)fail(i+1,"Quantidade inteira de 1 a 1.000.000.");
  if(!/^\d{1,9}(?:\.\d{1,2})?$/.test(p))fail(i+1,"Preço não negativo, até 9 dígitos inteiros e 2 decimais, com ponto decimal.");
  if(orders.has(order)&&orders.get(order)!==date)fail(i+1,"O mesmo pedido deve ter uma única data.");
  orders.set(order,date);
  const [a,b=""]=p.split("."),quantity=BigInt(q),price=BigInt(a)*100n+BigInt((b+"00").slice(0,2));
  rows.push({date,order,product,quantity,price});
 }return rows;
}
function summarize(rows,from="",to=""){
 const valid=x=>/^\d{4}-(0[1-9]|1[0-2])$/.test(x);
 if((from&&!valid(from))||(to&&!valid(to))||(from&&to&&from>to))throw Error("Período inválido.");
 const selected=rows.filter(x=>(!from||x.date.slice(0,7)>=from)&&(!to||x.date.slice(0,7)<=to));
 let revenue=0n,units=0n,duplicates=0;const orders=new Set(),products=new Map(),months=new Map(),seen=new Set();
 function add(map,key,q,r){const a=map.get(key)||{quantity:0n,revenue:0n};a.quantity+=q;a.revenue+=r;map.set(key,a);}
 for(const x of selected){const r=x.quantity*x.price;revenue+=r;units+=x.quantity;orders.add(x.order);add(products,x.product,x.quantity,r);add(months,x.date.slice(0,7),x.quantity,r);const sig=JSON.stringify([x.date,x.order,x.product,String(x.quantity),String(x.price)]);if(seen.has(sig))duplicates++;seen.add(sig);}
 const count=BigInt(orders.size), cmp=(a,b)=>a<b?-1:a>b?1:0;
 const rank=[...products].sort((a,b)=>a[1].revenue===b[1].revenue?cmp(a[0],b[0]):a[1].revenue>b[1].revenue?-1:1);
 const pack=([name,x])=>({name,quantity:String(x.quantity),revenue_cents:String(x.revenue)});
 return {schema_version:"1.0",currency:"BRL",period:{from,to},rows:selected.length,orders:orders.size,quantity:String(units),revenue_cents:String(revenue),average_order_cents:count?String((2n*revenue+count)/(2n*count)):null,product_count:products.size,possible_duplicate_rows:duplicates,products:rank.map(pack),months:[...months].sort((a,b)=>cmp(a[0],b[0])).map(pack)};
}
const api={parse,summarize,validDate,HEADER};
if(typeof module!=="undefined"&&module.exports)module.exports=api;else root.LiliumSales=Object.freeze(api);
})(typeof globalThis!=="undefined"?globalThis:this);
