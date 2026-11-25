/* Local data interchange. No network, credentials or execution. */
(function(root){
"use strict";
const SCHEMAS={insights:["date","revenue","cost"],sales:["date","order_id","product","quantity","unit_price"],forecast:["month","value"]};
const LIMIT=1048576;
function size(s){let n=0;for(const c of s){const p=c.codePointAt(0);n+=p<128?1:p<2048?2:p<65536?3:4;if(n>LIMIT)break;}return n;}
function text(s){if(typeof s!=="string"||size(s)>LIMIT)throw Error("Limite de 1 MiB em UTF-8.");return s;}
function schema(target){if(!Object.hasOwn(SCHEMAS,target))throw Error("Destino não suportado.");return SCHEMAS[target];}
function parse(raw,delimiter=","){
 if(![",",";","\t"].includes(delimiter))throw Error("Separador inválido.");
 const lines=text(raw).replace(/^\uFEFF/,"").replace(/\r?\n$/,"").split(/\r?\n/);
 if(lines.length<2||lines.length>10001)throw Error("Use 1 a 10.000 linhas de dados.");
 const cells=(line,i)=>{if(/["\u0000-\u0008\u000b-\u001f\u007f]/.test(line)||(delimiter!=="\t"&&line.includes("\t")))throw Error("Linha "+i+": formato simples sem aspas ou controles.");return line.split(delimiter).map(v=>v.trim());};
 const headers=cells(lines[0],1);
 if(headers.length>50||headers.some(x=>!x||x.length>100)||new Set(headers).size!==headers.length)throw Error("Cabeçalhos únicos e não vazios; até 50 colunas e 100 caracteres por nome.");
 const rows=lines.slice(1).map((line,i)=>{const a=cells(line,i+2);if(a.length!==headers.length)throw Error("Linha "+(i+2)+": número de colunas diferente do cabeçalho.");return a;});
 return {headers,rows};
}
function normalize(data,target,mapping,decimalComma=false){
 const fields=schema(target);
 if(!mapping||Object.keys(mapping).length!==fields.length)throw Error("Mapeie todas as colunas obrigatórias.");
 const indexes=fields.map(f=>{if(!Object.hasOwn(mapping,f))throw Error("Coluna não mapeada: "+f);const i=data.headers.indexOf(mapping[f]);if(i<0)throw Error("Coluna de origem ausente: "+f);return i;});
 if(new Set(indexes).size!==indexes.length)throw Error("Cada campo precisa de uma coluna de origem diferente.");
 const numeric=new Set(["revenue","cost","quantity","unit_price","value"]);
 const rows=data.rows.map((row,i)=>indexes.map((idx,j)=>{let v=row[idx];if(decimalComma&&numeric.has(fields[j]))v=v.replace(",",".");if(!v||/[,"\r\n\t]/.test(v))throw Error("Linha "+(i+2)+": valor ausente ou incompatível em "+fields[j]+".");return v;}).join(","));
 return text([fields.join(","),...rows].join("\n"));
}
function validate(csv,target,validators){
 const fields=schema(target),d=parse(csv,",");
 if(d.headers.join(",")!==fields.join(","))throw Error("Cabeçalho incompatível com o destino.");
 if(target==="insights"){
  for(let i=0;i<d.rows.length;i++){const [date,r,c]=d.rows[i];if(!validators.validDate(date)||![r,c].every(v=>/^\d{1,9}(?:\.\d{1,2})?$/.test(v)))throw Error("Linha "+(i+2)+": data ou valor monetário inválido.");}
 }else if(target==="sales")validators.sales(csv);else validators.forecast(csv);
 return d.rows.length;
}
function make(csv,target,validators){
 const count=validate(csv,target,validators);
 return {schema_version:"1.0",kind:"lilium.dataset",target,encoding:"utf-8",format:"csv",row_count:count,csv};
}
function open(raw,validators){
 let p;try{p=JSON.parse(text(raw));}catch{throw Error("Pacote JSON inválido ou acima de 1 MiB.");}
 const keys=["schema_version","kind","target","encoding","format","row_count","csv"];
 if(!p||typeof p!=="object"||Array.isArray(p)||Object.keys(p).length!==keys.length||keys.some(k=>!Object.hasOwn(p,k))||p.schema_version!=="1.0"||p.kind!=="lilium.dataset"||p.encoding!=="utf-8"||p.format!=="csv")throw Error("Contrato de pacote não suportado.");
 const canonical=make(p.csv,p.target,validators);
 if(p.row_count!==canonical.row_count)throw Error("Contagem de registros incompatível.");
 return canonical;
}
function serialize(p){return text(JSON.stringify(p,null,2));}
const api={SCHEMAS,parse,normalize,validate,make,open,serialize};
if(typeof module!=="undefined"&&module.exports)module.exports=api;else root.LiliumConnect=Object.freeze(api);
})(typeof globalThis!=="undefined"?globalThis:this);
