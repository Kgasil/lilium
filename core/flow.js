/* Local rule evaluation and human-reviewed task proposals. Never executes actions. */
(function(root){
"use strict";
const HEADER="rule_id,metric,operator,threshold,action";
const METRICS={
 "insights.margin":{label:"Insights · margem (%)",kind:"number"},
 "finance.result":{label:"Finance · resultado simulado (R$)",kind:"money"},
 "sales.orders":{label:"Sales · pedidos distintos",kind:"number"},
 "operations.capacity":{label:"Operations · capacidade teórica (un.)",kind:"number"},
 "strategy.progress":{label:"Strategy · progresso ponderado (%)",kind:"number"},
 "forecast.wape":{label:"Forecast · WAPE histórico (%)",kind:"number"}
};
const OPS=["lt","lte","gt","gte","eq"],MAX_QUEUE=200;
function decimal(s){if(!/^-?\d{1,12}(?:\.\d{1,2})?$/.test(s))throw Error("Limite: 12 dígitos inteiros e 2 decimais, com ponto decimal.");const neg=s.startsWith("-"),[a,b=""]=s.replace(/^-/,"").split(".");return (neg?-1n:1n)*(BigInt(a)*100n+BigInt((b+"00").slice(0,2)));}
function parse(raw){
 if(typeof raw!=="string"||raw.length>32768)throw Error("Limite de 32.768 caracteres.");
 const lines=raw.replace(/^\uFEFF/,"").replace(/\r?\n$/,"").split(/\r?\n/);
 if(lines[0]?.trim().toLowerCase()!==HEADER)throw Error("Cabeçalho esperado: "+HEADER);
 if(lines.length<2||lines.length>51)throw Error("Use 1 a 50 regras.");
 const seen=new Set();
 return lines.slice(1).map((line,i)=>{try{
 const f=line.split(",").map(x=>x.trim());
 if(f.length!==5||f.some(v=>!v||/["\u0000-\u001f\u007f]/.test(v)))throw Error("Cinco campos obrigatórios; sem aspas ou vírgulas internas.");
 const [id,metric,op,threshold,action]=f;
 if(!/^[A-Za-z0-9_-]{1,40}$/.test(id)||seen.has(id))throw Error("ID único de até 40 caracteres (letras ASCII, números, _ ou -).");
 if(!Object.hasOwn(METRICS,metric)||!OPS.includes(op))throw Error("Indicador ou operador não suportado.");
 if(action.length>180)throw Error("Ação de até 180 caracteres.");
 const cents=decimal(threshold);seen.add(id);
 return {id,metric,op,threshold:METRICS[metric].kind==="money"?String(cents):Number(cents)/100,action};
 }catch(e){throw Error("Linha "+(i+2)+": "+e.message);}});
}
function snapshot(s){
 const i=s.insights,f=s.finance?.results,a=s.sales,o=s.operations,t=s.strategy,p=s.forecast;
 const finite=x=>x===null||x===undefined||!Number.isFinite(Number(x))?null:Number(x);
 return {
 "insights.margin":{value:i?.months?.length?finite(i.totals.margin_pct):null,scope:i?"Filtro "+(i.from||"início")+" a "+(i.to||"fim"):"Sem fonte",kind:"dados informados"},
 "finance.result":{value:f?.result_cents??null,scope:"Um mês hipotético; produto único",kind:"simulação"},
 "sales.orders":{value:a?.rows?finite(a.orders):null,scope:a?"Filtro "+(a.period.from||"início")+" a "+(a.period.to||"fim"):"Sem fonte",kind:"dados informados"},
 "operations.capacity":{value:o?finite(o.capacity):null,scope:"Etapas sequenciais; período informado",kind:"capacidade teórica"},
 "strategy.progress":{value:t?finite(t.progress_pct):null,scope:t?"Avaliação em "+t.as_of:"Sem fonte",kind:"metas informadas"},
 "forecast.wape":{value:p?finite(p.comparison.find(m=>m.model===p.model)?.wape_pct):null,scope:p?"Validação de um passo "+p.validation.from+" a "+p.validation.to:"Sem fonte",kind:"erro histórico de previsão"}
 };
}
function compare(a,b,op){switch(op){case "lt":return a<b;case "lte":return a<=b;case "gt":return a>b;case "gte":return a>=b;case "eq":return a===b;default:throw Error("Operador inválido.");}}
function evaluate(rules,metrics){
 return rules.map(r=>{
 const m=metrics[r.metric];
 if(!m||m.value===null||m.value===undefined)return {...r,outcome:"unavailable",evidence:null};
 const isMoney=METRICS[r.metric].kind==="money";
 // Percentages and counts compare at displayed precision; currency compares exact cents.
 const value=isMoney?String(BigInt(m.value)):Math.round(m.value*100)/100;
 const a=isMoney?BigInt(value):value,b=isMoney?BigInt(r.threshold):r.threshold;
 return {...r,outcome:compare(a,b,r.op)?"matched":"not_matched",evidence:{value,scope:m.scope,kind:m.kind}};
 });
}
function timestamp(t){if(typeof t!=="string"||!Number.isFinite(Date.parse(t))||new Date(t).toISOString()!==t)throw Error("Data UTC inválida.");return t;}
function enqueue(queue,results,at){
 timestamp(at);const next=queue.slice(),known=new Set(next.map(x=>x.signature));
 let added=0,skipped=0,full=0;
 for(const r of results){if(r.outcome!=="matched")continue;
 const signature=JSON.stringify([r.id,r.metric,r.op,r.threshold,r.action,r.evidence.value,r.evidence.scope,r.evidence.kind]);
 if(known.has(signature)){skipped++;continue;}
 if(next.length>=MAX_QUEUE){full++;continue;}
 next.push({id:"P"+String(next.length+1).padStart(3,"0"),signature,rule_id:r.id,metric:r.metric,operator:r.op,threshold:r.threshold,action:r.action,evidence:{...r.evidence},status:"pending",created_at:at,events:[{status:"pending",at}]});
 known.add(signature);added++;
 }return {queue:next,added,skipped,full};
}
function transition(queue,id,status,at){
 timestamp(at);const old=queue.find(x=>x.id===id);if(!old)throw Error("Proposta não encontrada.");
 const allowed={pending:["approved","rejected"],approved:["completed_manually","rejected"]};
 if(!allowed[old.status]?.includes(status))throw Error("Transição não permitida.");
 if(at<old.events.at(-1).at)throw Error("Data anterior ao último evento.");
 return queue.map(x=>x.id===id?{...x,status,events:[...x.events,{status,at}]}:x);
}
const api={HEADER,METRICS,OPS,parse,snapshot,evaluate,enqueue,transition};
if(typeof module!=="undefined"&&module.exports)module.exports=api;else root.LiliumFlow=Object.freeze(api);
})(typeof globalThis!=="undefined"?globalThis:this);
