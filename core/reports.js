/* Executive report composition from current, already calculated module results.
   No AI, no network, no persistence. Sources are not reconciled or added together. */
(function(root){
"use strict";
const MODULES=["insights","finance","sales","operations","strategy","actions"];
const LABELS={insights:"Insights",finance:"Finance",sales:"Sales",operations:"Operations",strategy:"Strategy",actions:"Prioridades"};
const number=n=>n===null||n===undefined?"N/A":Number(n).toLocaleString("pt-BR",{maximumFractionDigits:2});
function money(value){
 if(value===null||value===undefined)return "N/A";
 const n=BigInt(value),a=n<0n?-n:n;
 return (n<0n?"−":"")+"R$ "+(a/100n).toLocaleString("pt-BR")+","+(a%100n).toString().padStart(2,"0");
}
const pct=n=>n===null||n===undefined?"N/A":number(n)+"%";
const bounds=(from,to)=>"Filtro: "+(from||"início dos dados")+" a "+(to||"fim dos dados");
const item=(label,value)=>({label,value:String(value)});
function section(id,scope,kind,metrics,notes,details=[]){return {source:id,title:LABELS[id],scope,kind,metrics,notes,details};}
function build(id,d){
 switch(id){
 case "insights": {
  if(!d.months.length)return section(id,bounds(d.from,d.to),"dados informados",[],["Nenhum mês com registros no filtro."]);
  const t=d.totals;
  return section(id,bounds(d.from,d.to),"dados informados",[
   item("Receita",money(t.revenue_cents)),item("Custos",money(t.cost_cents)),item("Resultado",money(t.result_cents)),item("Margem",pct(t.margin_pct))
  ],["Resultado considera somente os custos informados; não é necessariamente lucro contábil."],d.months.map(m=>({label:m.month,values:[money(m.revenue_cents),money(m.cost_cents),money(m.result_cents)]})));
 }
 case "finance": {
  const t=d.results;
  return section(id,"Um mês hipotético; produto único","simulação",[
   item("Receita simulada",money(t.revenue_cents)),item("Custos variáveis",money(t.variable_cents)),item("Taxas",money(t.fees_cents)),item("Custos fixos",money(t.fixed_cents)),item("Resultado simulado",money(t.result_cents)),item("Margem",pct(t.result_margin_pct)),item("Ponto de equilíbrio",t.break_even_units===null?"Inviável":BigInt(t.break_even_units).toLocaleString("pt-BR")+" un.")
  ],["Preços e custos constantes; taxa arredondada por unidade. Não representa vendas realizadas ou previsão."],Object.entries(d.inputs).map(([key,value])=>({label:({price:"Preço unitário (R$)",variable:"Custo variável unitário (R$)",fixed:"Custo fixo (R$)",quantity:"Quantidade (un.)",fee:"Taxa (%)",target:"Meta de resultado (R$)"})[key]||key,values:[String(value)]})));
 }
 case "sales":
  return section(id,bounds(d.period.from,d.period.to),"dados informados",[
   item("Receita bruta",money(d.revenue_cents)),item("Pedidos distintos",number(d.orders)),item("Unidades vendidas",BigInt(d.quantity).toLocaleString("pt-BR")),item("Ticket médio",money(d.average_order_cents)),item("Possíveis duplicatas",number(d.possible_duplicate_rows))
  ],["Receita bruta não desconta devoluções, tributos ou taxas. Duplicatas possíveis são mantidas. Não somar com Insights."],d.products.slice(0,10).map(p=>({label:p.name,values:[BigInt(p.quantity).toLocaleString("pt-BR")+" un.",money(p.revenue_cents)]})));
 case "operations":
  return section(id,"Período operacional informado, sem data vinculada","estimativa e dados informados",[
   item("Etapas",number(d.stages.length)),item("Capacidade teórica",number(d.capacity)+" un."),item("Gargalo estimado",d.bottlenecks.join(", ")),item("Redução hipotética de paradas",pct(d.scenario.reduction_pct)),item("Capacidade simulada",number(d.scenario.capacity)+" un.")
  ],["Capacidade teórica de etapas sequenciais; cenário não garante ganho real. OEE indisponível se inconsistente ou sem denominador."],d.stages.map(s=>({label:s.stage,values:["OEE: "+pct(s.oee_pct),"Capacidade: "+number(s.capacity)+" un.",...(s.warning?["Revisar performance acima de 100%"]:[])]})));
 case "strategy":
  return section(id,"Avaliação em "+d.as_of,"metas informadas e cenário hipotético",[
   item("Objetivos",number(d.objective_count)),item("Resultados-chave",number(d.kr_count)),item("Progresso ponderado",pct(d.progress_pct)),item("Cenário hipotético",pct(d.scenario_progress_pct)),item("KRs atingidos",number(d.achieved)),item("KRs vencidos não atingidos",number(d.overdue))
  ],["Progresso ponderado limitado a 0–100% por KR; cenário não é previsão."],d.objectives.map(o=>({label:o.objective,values:["Atual: "+pct(o.progress_pct),"Cenário: "+pct(o.scenario_progress_pct)]})));
 case "actions":
  return section(id,"Avaliações subjetivas informadas, sem data vinculada","priorização",[
   item("Ações avaliadas",number(d.actions.length))
  ],["Pontuação = impacto × urgência ÷ esforço; decisão final humana."],d.actions.slice(0,10).map(a=>({label:a.action,values:["Pontuação: "+number(a.score),"Impacto: "+a.impact,"Urgência: "+a.urgency,"Esforço: "+a.effort]})));
 default:throw Error("Fonte não suportada.");
 }
}
function compose(sources,selected,metadata){
 if(!Array.isArray(selected)||!selected.length)throw Error("Selecione ao menos uma fonte.");
 if(selected.some(k=>!MODULES.includes(k)))throw Error("Fonte não suportada.");
 const title=String(metadata.title||"").trim(),date=String(metadata.generated_at||"");
 if(!title||title.length>100||/[\u0000-\u001f\u007f]/.test(title))throw Error("Título obrigatório de até 100 caracteres.");
 if(!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/.test(date)||!Number.isFinite(Date.parse(date)))throw Error("Data de geração inválida.");
 const keys=MODULES.filter(k=>selected.includes(k));
 const sections=[],missing=[];
 for(const k of keys){if(sources[k]==null)missing.push(k);else sections.push(build(k,sources[k]));}
 if(!sections.length)throw Error("Nenhuma fonte selecionada tem resultado calculado.");
 return {schema_version:"1.0",title,generated_at:date,currency:"BRL",sections,missing_sources:missing,
  limitations:["Relatório instantâneo dos resultados disponíveis na sessão. Não verifica os dados originais.","As fontes podem corresponder a períodos e conjuntos de dados diferentes. Não consolida somas entre módulos.","Simulações e cenários hipotéticos não são resultados realizados. Sem IA, auditoria ou validação contábil."]};
}
function toText(report){
 const lines=["LILIUM REPORTS | STRATEGY & GROWTH",report.title,"Gerado em (UTC): "+report.generated_at,""];
 for(const s of report.sections){lines.push(s.title.toUpperCase()+" ["+s.source+"]",s.kind+" | "+s.scope);for(const x of s.metrics)lines.push(x.label+": "+x.value);for(const x of s.details)lines.push("• "+x.label+": "+x.values.join(" | "));for(const x of s.notes)lines.push("Nota: "+x);lines.push("");}
 if(report.missing_sources.length)lines.push("Fontes sem resultado: "+report.missing_sources.map(k=>LABELS[k]).join(", "),"");
 lines.push("LIMITAÇÕES",...report.limitations,"","K&G Vision · Lilium");
 return lines.join("\n");
}
const api={MODULES,LABELS,compose,toText,money};
if(typeof module!=="undefined"&&module.exports)module.exports=api;else root.LiliumReports=Object.freeze(api);
})(typeof globalThis!=="undefined"?globalThis:this);
