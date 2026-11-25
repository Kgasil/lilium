/* Monthly nonnegative time-series baselines. No network, AI or persistence.
   Model selection uses rolling-origin one-step validation on the same recent months. */
(function(root){
"use strict";
const HEADER="month,value";
const MODELS=["naive","ma3","trend"];
const LABELS={naive:"Último valor",ma3:"Média móvel (3 meses)",trend:"Tendência linear"};
function monthIndex(s){
 const m=/^(\d{4})-(0[1-9]|1[0-2])$/.exec(s);
 if(!m||+m[1]<1)throw Error("Mês inválido (AAAA-MM).");
 return (+m[1]-1)*12+(+m[2]-1);
}
function monthLabel(i){
 if(!Number.isInteger(i)||i<0||i>=9999*12)throw Error("Horizonte excede o calendário suportado.");
 return String(Math.floor(i/12)+1).padStart(4,"0")+"-"+String(i%12+1).padStart(2,"0");
}
function parse(raw){
 if(typeof raw!=="string"||raw.length>16384)throw Error("Limite de 16.384 caracteres.");
 const lines=raw.replace(/^\uFEFF/,"").replace(/\r?\n$/,"").split(/\r?\n/);
 if(lines[0]?.trim().toLowerCase()!==HEADER)throw Error("Cabeçalho esperado: "+HEADER);
 if(lines.length<7||lines.length>121)throw Error("Informe de 6 a 120 meses consecutivos.");
 const rows=[];
 for(let i=1;i<lines.length;i++){try{
  const f=lines[i].split(",").map(x=>x.trim());
  if(f.length!==2)throw Error("Use duas colunas simples.");
  const [month,v]=f,idx=monthIndex(month);
  if(rows.length&&idx!==monthIndex(rows.at(-1).month)+1)throw Error("Meses devem ser consecutivos, únicos e em ordem crescente.");
  if(!/^\d{1,9}(?:\.\d{1,2})?$/.test(v))throw Error("Valor não negativo, até 9 dígitos inteiros e 2 decimais, com ponto decimal.");
  rows.push({month,value:Number(v)});
 }catch(e){throw Error("Linha "+(i+1)+": "+e.message);}}
 return rows;
}
function fittedTrend(y){
 const n=y.length,xMean=(n-1)/2,yMean=y.reduce((a,b)=>a+b,0)/n;
 let xy=0,xx=0;for(let i=0;i<n;i++){xy+=(i-xMean)*(y[i]-yMean);xx+=(i-xMean)**2;}
 const slope=xx?xy/xx:0;
 return {intercept:yMean-slope*xMean,slope};
}
function predict(y,model,h){
 if(!MODELS.includes(model))throw Error("Modelo inválido.");
 const output=[],work=y.slice(),trend=model==="trend"?fittedTrend(y):null;
 for(let i=0;i<h;i++){
  const v=model==="naive"?work.at(-1):model==="ma3"?work.slice(-3).reduce((a,b)=>a+b,0)/3:trend.intercept+trend.slope*(y.length+i);
  const next=Math.max(0,v);
  output.push(next);work.push(next);
 }
 return output;
}
function metrics(pairs){
 let abs=0,sq=0,total=0;
 for(const p of pairs){const e=p.predicted-p.actual;abs+=Math.abs(e);sq+=e*e;total+=Math.abs(p.actual);}
 return {mae:abs/pairs.length,rmse:Math.sqrt(sq/pairs.length),wape_pct:total?abs/total*100:null};
}
function analyze(rows,horizon=3,requested="auto"){
 if(!Number.isInteger(horizon)||horizon<1||horizon>12)throw Error("Horizonte inteiro entre 1 e 12 meses.");
 if(requested!=="auto"&&!MODELS.includes(requested))throw Error("Modelo inválido.");
 // Revalidate public rows to keep direct callers within the same constraints.
 if(!Array.isArray(rows)||rows.length<6||rows.length>120)throw Error("Informe de 6 a 120 meses consecutivos.");
 for(let i=0;i<rows.length;i++){
  const row=rows[i];const idx=monthIndex(row.month);
  if(!Number.isFinite(row.value)||row.value<0||row.value>999999999.99||(i&&idx!==monthIndex(rows[i-1].month)+1))throw Error("Série mensal inválida.");
 }
 const last=monthIndex(rows.at(-1).month);monthLabel(last+horizon);
 const y=rows.map(r=>r.value),holdout=Math.min(6,Math.floor(y.length/3)),start=y.length-holdout;
 const comparison=MODELS.map(model=>{
  const pairs=[];for(let i=start;i<y.length;i++)pairs.push({month:rows[i].month,actual:y[i],predicted:predict(y.slice(0,i),model,1)[0]});
  return {model,label:LABELS[model],...metrics(pairs),pairs};
 });
 const best=comparison.reduce((a,b)=>b.mae<a.mae?b:a),model=requested==="auto"?best.model:requested;
 const future=predict(y,model,horizon).map((value,i)=>({month:monthLabel(last+i+1),value}));
 return {schema_version:"1.0",model,model_label:LABELS[model],selection:requested,best_validation_model:best.model,
  historical:rows.map(r=>({...r})),horizon,validation:{method:"rolling-origin-one-step",months:holdout,from:rows[start].month,to:rows.at(-1).month},
  comparison,future,limitations:["Valores mensais não negativos; meses ausentes devem ser corrigidos na origem.","Validação de um passo à frente; não mede erro do horizonte completo. A escolha automática usa os mesmos meses de validação e pode ser otimista.","Previsões pontuais sem intervalos de confiança, sazonalidade ou variáveis externas; não são garantias."]};
}
const api={HEADER,MODELS,LABELS,parse,analyze,predict,metrics,monthIndex,monthLabel};
if(typeof module!=="undefined"&&module.exports)module.exports=api;else root.LiliumForecast=Object.freeze(api);
})(typeof globalThis!=="undefined"?globalThis:this);
