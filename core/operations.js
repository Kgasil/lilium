/* Operational indicators for comparable sequential stages over one period.
   No external requests or storage. Ratios are estimates rounded for display. */
(function(root){
"use strict";
const HEADER="stage,planned_min,downtime_min,cycle_sec,total_units,good_units,rework_units,lead_min";
const MAX_STAGES=100,MAX_BYTES=65536;
function integer(s,min,max){if(!/^\d{1,9}$/.test(s))throw Error("Use números inteiros.");const n=Number(s);if(n<min||n>max)throw Error("Valor fora do intervalo "+min+"–"+max+".");return n;}
function parse(raw){
 if(typeof raw!=="string"||raw.length>MAX_BYTES||new BlobSize(raw).size>MAX_BYTES)throw Error("Limite de 64 KiB.");
 const lines=raw.replace(/^\uFEFF/,"").replace(/\r?\n$/,"").split(/\r?\n/);
 if(lines[0]?.trim().toLowerCase()!==HEADER)throw Error("Cabeçalho esperado: "+HEADER);
 if(lines.length<2||lines.length>MAX_STAGES+1)throw Error("Use 1 a 100 etapas.");
 const seen=new Set();
 return lines.slice(1).map((line,i)=>{try{
  const f=line.split(",").map(x=>x.trim());
  if(f.length!==8||f.some(x=>/["\u0000-\u001f\u007f]/.test(x)))throw Error("Use oito campos simples, sem aspas ou caracteres de controle.");
  const [stage,p,d,c,t,g,r,l]=f;
  if(!stage||stage.length>80||seen.has(stage))throw Error("Nome de etapa obrigatório e único (até 80 caracteres).");
  seen.add(stage);
  const planned=integer(p,1,1000000),downtime=integer(d,0,planned),cycle=integer(c,1,86400),total=integer(t,0,100000000),good=integer(g,0,total),rework=integer(r,0,total-good);
  if(downtime===planned&&total>0)throw Error("Produção positiva sem tempo de operação.");
  const lead=l===""?null:integer(l,0,1000000);
  if(total===0&&lead!==null)throw Error("Deixe lead time vazio quando não houver unidades processadas.");
  return {stage,planned,downtime,cycle,total,good,rework,lead};
 }catch(e){throw Error("Linha "+(i+2)+": "+e.message);}});
}
function BlobSize(s){let size=0;for(const c of s){const p=c.codePointAt(0);size+=p<128?1:p<2048?2:p<65536?3:4;}this.size=size;}
function pct(n,d){return d?100*n/d:null;}
function stageMetrics(s){
 const run=s.planned-s.downtime,plannedCapacity=Math.floor(s.planned*60/s.cycle),capacity=Math.floor(run*60/s.cycle);
 const availability=pct(run,s.planned),performance=pct(s.total*s.cycle,run*60),quality=pct(s.good,s.total);
 const inconsistent=performance!==null&&performance>100;
 return {...s,run,planned_capacity:plannedCapacity,capacity,
  availability_pct:availability,performance_pct:performance,quality_pct:quality,
  oee_pct:inconsistent||performance===null||quality===null?null:availability*performance*quality/10000,
  throughput_per_hour:run?s.total*60/run:null,rework_pct:pct(s.rework,s.total),
  nonconforming:s.total-s.good,other_nonconforming:s.total-s.good-s.rework,
  warning:inconsistent?"performance_above_100":null};
}
function summarize(rows,reduction=0){
 if(!Array.isArray(rows)||!rows.length)throw Error("Nenhuma etapa.");
 if(!Number.isInteger(reduction)||reduction<0||reduction>100)throw Error("Redução de parada deve ser inteira entre 0 e 100%.");
 const stages=rows.map(stageMetrics);
 const minimum=Math.min(...stages.map(x=>x.capacity));
 const scenario=stages.map(x=>{const recovered=Math.floor(x.downtime*reduction/100);return {stage:x.stage,recovered_minutes:recovered,capacity:Math.floor((x.run+recovered)*60/x.cycle)};});
 const improved=Math.min(...scenario.map(x=>x.capacity));
 return {schema_version:"1.0",model:"serial-single-period-theoretical-capacity",stages,capacity:minimum,
  bottlenecks:stages.filter(x=>x.capacity===minimum).map(x=>x.stage),
  scenario:{reduction_pct:reduction,capacity:improved,additional_capacity:improved-minimum,
  bottlenecks:scenario.filter(x=>x.capacity===improved).map(x=>x.stage),stages:scenario}};
}
const api={HEADER,parse,stageMetrics,summarize};
if(typeof module!=="undefined"&&module.exports)module.exports=api;else root.LiliumOperations=Object.freeze(api);
})(typeof globalThis!=="undefined"?globalThis:this);
