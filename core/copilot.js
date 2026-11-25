/* Guided deterministic assistant. No language model, external calls, or autonomous execution. */
(function(root){
"use strict";
const TOPICS={overview:"Resumo empresarial",insights:"Como estão receitas e custos?",finance:"O que indica a simulação financeira?",sales:"Como estão as vendas?",operations:"Onde está o gargalo estimado?",strategy:"Como estão as metas?",forecast:"O que indica a previsão?",actions:"Quais ações merecem revisão?"};
const DEFAULT_RULES=[
 ["C_MARGIN","insights.margin","lt","20","Revisar composição dos custos e margem"],
 ["C_RESULT","finance.result","lt","0","Reavaliar premissas do cenário financeiro"],
 ["C_ORDERS","sales.orders","lt","10","Investigar volume de pedidos no período"],
 ["C_CAPACITY","operations.capacity","lt","300","Verificar capacidade e gargalo na operação"],
 ["C_GOALS","strategy.progress","lt","60","Revisar andamento dos resultados-chave"],
 ["C_ERROR","forecast.wape","gt","10","Reavaliar modelo e histórico da previsão"]
];
const LIMITS=["Assistente determinístico com perguntas predefinidas; não é IA generativa.","Dados e períodos podem ser independentes. Não soma receitas entre módulos nem verifica a origem dos dados.","Os limites de alerta são exemplos configuráveis, não referências universais. Nenhuma ação é executada."];
const number=n=>n===null||n===undefined?"N/A":Number(n).toLocaleString("pt-BR",{maximumFractionDigits:2});
function rules(flow,raw){return flow.parse(raw===undefined?[flow.HEADER,...DEFAULT_RULES.map(r=>r.join(","))].join("\n"):raw);}
function checkTime(t){if(typeof t!=="string"||!Number.isFinite(Date.parse(t))||new Date(t).toISOString()!==t)throw Error("Data UTC inválida.");}
function explain(topic,sources,deps,at,ruleText){
 if(!Object.hasOwn(TOPICS,topic))throw Error("Pergunta não suportada. Escolha um tópico disponível.");
 checkTime(at);
 const {reports,flow}=deps;
 const selected=topic==="overview"?["insights","finance","sales","operations","strategy"]:topic==="actions"?[]:topic==="forecast"?[]:[topic];
 const sections=[],missing=[];
 for(const k of selected){
  if(sources[k]==null){missing.push(k);continue;}
  const r=reports.compose(sources,[k],{title:TOPICS[topic],generated_at:at});
  const s=r.sections[0];
  // Keep original source, scope, data kind and precomputed metrics. Do not combine totals.
  sections.push({source:s.source,title:s.title,scope:s.scope,kind:s.kind,metrics:s.metrics,notes:s.notes,details:s.details.slice(0,5)});
 }
 if(topic==="overview"||topic==="forecast"){
  const f=sources.forecast;
  if(!f)missing.push("forecast");
  else{
   const fmt=v=>f.unit==="BRL"?new Intl.NumberFormat("pt-BR",{style:"currency",currency:"BRL"}).format(v):number(v)+" un.";
   const chosen=f.comparison.find(m=>m.model===f.model);
   sections.push({source:"forecast",title:"Forecast",kind:"estimativa estatística",scope:"Validação "+f.validation.from+" a "+f.validation.to+"; horizonte "+f.horizon+" meses",metrics:[
    {label:"Modelo",value:f.model_label},{label:"Próximo mês estimado",value:f.future[0].month+" · "+fmt(f.future[0].value)},{label:"MAE histórico de um passo",value:fmt(chosen.mae)},{label:"WAPE histórico",value:chosen.wape_pct===null?"N/A":number(chosen.wape_pct)+"%"}
   ],notes:["Estimativa pontual, sem garantia de resultado ou intervalo de confiança. O erro mede um passo, não o horizonte completo."],details:[]});
  }
 }
 const rs=rules(flow,ruleText);
 const snapshot=flow.snapshot(sources);
 const checked=flow.evaluate(rs,snapshot).filter(r=>topic==="overview"||topic==="actions"||r.metric.split(".")[0]===topic);
 const suggestions=checked.filter(r=>r.outcome==="matched");
 const unavailable=checked.filter(r=>r.outcome==="unavailable").map(r=>r.metric);
 return {schema_version:"1.0",mode:"deterministic-guided",topic,question:TOPICS[topic],generated_at:at,sections,missing_sources:missing,
  suggestions,unavailable_metrics:[...new Set(unavailable)],evaluated_rules:checked.length,limitations:LIMITS.slice()};
}
function forward(queue,report,index,currentSources,deps,at,ruleText){
 checkTime(at);
 if(!report||!Number.isInteger(index)||index<0||index>=report.suggestions.length)throw Error("Sugestão inválida.");
 const old=report.suggestions[index];
 const fresh=deps.flow.evaluate(rules(deps.flow,ruleText),deps.flow.snapshot(currentSources)).find(r=>r.id===old.id);
 if(!fresh||fresh.outcome!=="matched"||JSON.stringify(fresh)!==JSON.stringify(old))throw Error("A regra ou evidência mudou. Gere uma nova resposta antes de encaminhar.");
 return deps.flow.enqueue(queue,[fresh],at);
}
const api={TOPICS,DEFAULT_RULES,explain,forward};
if(typeof module!=="undefined"&&module.exports)module.exports=api;else root.LiliumCopilot=Object.freeze(api);
})(typeof globalThis!=="undefined"?globalThis:this);
