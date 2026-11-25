/* Explicit, local OKR tracking and prioritization. Scores are planning aids, not forecasts. */
(function(root){
"use strict";
const GOALS="objective,kr,baseline,target,actual,scenario,weight,due";
const ACTIONS="action,impact,urgency,effort";
function date(s){const m=/^(\d{4})-(\d{2})-(\d{2})$/.exec(s);if(!m)return false;const y=+m[1],mo=+m[2],d=+m[3];return y>0&&mo>=1&&mo<=12&&d>=1&&d<=[31,y%4===0&&(y%100!==0||y%400===0)?29:28,31,30,31,30,31,31,30,31,30,31][mo-1];}
function rows(raw,header,count,max){
 if(typeof raw!=="string"||raw.length>65536)throw Error("Limite de 65.536 caracteres.");
 const lines=raw.replace(/^\uFEFF/,"").replace(/\r?\n$/,"").split(/\r?\n/);
 if(lines[0]?.trim().toLowerCase()!==header)throw Error("Cabeçalho esperado: "+header);
 if(lines.length<2||lines.length>max+1)throw Error("Use 1 a "+max+" registros.");
 return lines.slice(1).map((line,i)=>{const a=line.split(",").map(x=>x.trim());if(a.length!==count||a.some(v=>!v||/["\u0000-\u001f\u007f]/.test(v)))throw Error("Linha "+(i+2)+": campos obrigatórios, sem aspas ou caracteres de controle.");return a;});
}
function label(s){if(s.length>100)throw Error("Nome de até 100 caracteres.");return s;}
function decimal(s){if(!/^-?\d{1,9}(?:\.\d{1,2})?$/.test(s))throw Error("Valor numérico com até 9 dígitos e 2 decimais (ponto decimal).");const sign=s.startsWith("-")?-1:1;const [a,b=""]=s.replace(/^-/,"").split(".");return sign*(Number(a)*100+Number((b+"00").slice(0,2)));}
function scale(s,max){if(!/^\d{1,2}$/.test(s)||+s<1||+s>max)throw Error("Escala inteira de 1 a "+max+".");return +s;}
function parseGoals(raw){
 const seen=new Set();return rows(raw,GOALS,8,100).map((a,i)=>{try{
 const [objective,kr,b,t,v,s,w,due]=a;label(objective);label(kr);const key=JSON.stringify([objective,kr]);if(seen.has(key))throw Error("KR repetido no mesmo objetivo.");seen.add(key);
 const baseline=decimal(b),target=decimal(t),actual=decimal(v),scenario=decimal(s),weight=scale(w,10);
 if(baseline===target)throw Error("Meta deve ser diferente da linha de base.");if(!date(due))throw Error("Prazo inválido (AAAA-MM-DD).");
 return {objective,kr,baseline,target,actual,scenario,weight,due};
 }catch(e){throw Error("Linha "+(i+2)+": "+e.message);}});
}
function rawProgress(b,t,v){return (v-b)/(t-b)*100;}
function clamp(x){return Math.max(0,Math.min(100,x));}
function scoreGoals(goals,asOf){
 if(!date(asOf))throw Error("Informe uma data de avaliação válida.");
 if(!goals.length)throw Error("Nenhuma meta.");
 const entries=goals.map(g=>{const raw=rawProgress(g.baseline,g.target,g.actual),sim=rawProgress(g.baseline,g.target,g.scenario);return {objective:g.objective,kr:g.kr,baseline:g.baseline/100,target:g.target/100,actual:g.actual/100,scenario:g.scenario/100,weight:g.weight,due:g.due,direction:g.target>g.baseline?"increase":"decrease",raw_progress_pct:raw,progress_pct:clamp(raw),scenario_progress_pct:clamp(sim),status:raw>=100?"achieved":asOf>g.due?"overdue":"open"};});
 const by=new Map();
 for(const g of entries){const x=by.get(g.objective)||{objective:g.objective,weight:0,current:0,scenario:0,kr_count:0,achieved:0,overdue:0};x.weight+=g.weight;x.current+=g.progress_pct*g.weight;x.scenario+=g.scenario_progress_pct*g.weight;x.kr_count++;x.achieved+=Number(g.status==="achieved");x.overdue+=Number(g.status==="overdue");by.set(g.objective,x);}
 const objectives=[...by.values()].map(x=>({objective:x.objective,weight:x.weight,kr_count:x.kr_count,achieved:x.achieved,overdue:x.overdue,progress_pct:x.current/x.weight,scenario_progress_pct:x.scenario/x.weight}));
 const weight=entries.reduce((n,g)=>n+g.weight,0);
 const current=entries.reduce((n,g)=>n+g.progress_pct*g.weight,0)/weight;
 const scenario=entries.reduce((n,g)=>n+g.scenario_progress_pct*g.weight,0)/weight;
 return {schema_version:"1.0",as_of:asOf,kr_count:entries.length,objective_count:objectives.length,achieved:entries.filter(g=>g.status==="achieved").length,overdue:entries.filter(g=>g.status==="overdue").length,progress_pct:current,scenario_progress_pct:scenario,scenario_delta_pp:scenario-current,objectives,entries};
}
function rankActions(raw){
 const seen=new Set();return rows(raw,ACTIONS,4,100).map((a,i)=>{try{
 const [action,b,c,d]=a;label(action);if(seen.has(action))throw Error("Ação repetida.");seen.add(action);
 const impact=scale(b,5),urgency=scale(c,5),effort=scale(d,5);return {action,impact,urgency,effort,score:impact*urgency/effort};
 }catch(e){throw Error("Linha "+(i+2)+": "+e.message);}}).sort((a,b)=>b.impact*b.urgency*a.effort-a.impact*a.urgency*b.effort||(a.action<b.action?-1:a.action>b.action?1:0));
}
const api={GOALS,ACTIONS,parseGoals,scoreGoals,rankActions,date};
if(typeof module!=="undefined"&&module.exports)module.exports=api;else root.LiliumStrategy=Object.freeze(api);
})(typeof globalThis!=="undefined"?globalThis:this);
