const assert=require("node:assert/strict"),c=require("../core/copilot.js"),flow=require("../core/flow.js"),reports=require("../core/reports.js");
const deps={flow,reports},at="2026-11-25T12:00:00.000Z";
const insights={from:"2026-01",to:"2026-02",months:[{month:"2026-01",revenue_cents:10000,cost_cents:8500,result_cents:1500}],totals:{revenue_cents:10000,cost_cents:8500,result_cents:1500,margin_pct:"15.00"}};
const sales={period:{from:"2026-03",to:"2026-03"},rows:2,revenue_cents:"25000",orders:2,quantity:"5",average_order_cents:"12500",possible_duplicate_rows:0,products:[]};
const forecast={unit:"BRL",model:"trend",model_label:"Tendência linear",horizon:3,validation:{from:"2026-08",to:"2026-09"},comparison:[{model:"trend",mae:100,wape_pct:null}],future:[{month:"2026-10",value:1200}]};
const sources={insights,sales,forecast};
const ask=(topic="overview",data=sources,raw)=>c.explain(topic,data,deps,at,raw);
const r=ask(),one=ask("insights");
const checks=[
["guided mode",()=>assert.equal(r.mode,"deterministic-guided")],
["three available sources",()=>assert.equal(r.sections.length,3)],
["missing sources",()=>assert.ok(r.missing_sources.includes("finance"))],
["exact source revenue",()=>assert.equal(r.sections[0].metrics[0].value,"R$ 100,00")],
["independent period",()=>assert.ok(r.sections[1].scope.includes("2026-03"))],
["selected question",()=>assert.equal(one.sections.length,1)],
["unknown topic rejected",()=>assert.throws(()=>ask("constructor"))],
["no invented figures",()=>assert.equal(ask("finance",{}).sections.length,0)],
["missing finance",()=>assert.equal(ask("finance",{}).missing_sources[0],"finance")],
["forecast kind",()=>assert.equal(ask("forecast").sections[0].kind,"estimativa estatística")],
["undefined WAPE",()=>assert.equal(ask("forecast").sections[0].metrics[3].value,"N/A")],
["missing WAPE",()=>assert.ok(ask("forecast").unavailable_metrics.includes("forecast.wape"))],
["two matched rules",()=>assert.equal(r.suggestions.length,2)],
["scope retained",()=>assert.ok(one.suggestions[0].evidence.scope.includes("2026-01"))],
["threshold retained",()=>assert.equal(one.suggestions[0].threshold,20)],
["unmatched not proposed",()=>assert.equal(ask("insights",{insights:{...insights,totals:{...insights.totals,margin_pct:"40"}}}).suggestions.length,0)],
["actions view",()=>assert.equal(ask("actions").sections.length,0)],
["custom threshold",()=>assert.equal(ask("insights",sources,flow.HEADER+"\nA,insights.margin,lt,10,Revisar").suggestions.length,0)],
["invalid rules rejected",()=>assert.throws(()=>ask("overview",sources,"bad"))],
["invalid time rejected",()=>assert.throws(()=>c.explain("overview",sources,deps,"bad"))],
["forward pending",()=>assert.equal(c.forward([],one,0,sources,deps,at).queue[0].status,"pending")],
["forward evidence",()=>assert.equal(c.forward([],one,0,sources,deps,at).queue[0].evidence.value,15)],
["dedup",()=>assert.equal(c.forward(c.forward([],one,0,sources,deps,at).queue,one,0,sources,deps,at).skipped,1)],
["changed evidence rejected",()=>assert.throws(()=>c.forward([],one,0,{insights:{...insights,totals:{...insights.totals,margin_pct:"16"}}},deps,at))],
["changed rule rejected",()=>assert.throws(()=>c.forward([],one,0,sources,deps,at,flow.HEADER+"\nC_MARGIN,insights.margin,lt,19,Revisar composição dos custos e margem"))],
["missing current source rejected",()=>assert.throws(()=>c.forward([],one,0,{},deps,at))],
["bad index",()=>assert.throws(()=>c.forward([],one,4,sources,deps,at))],
["JSON safe",()=>assert.equal(JSON.parse(JSON.stringify(r)).topic,"overview")],
["snapshot unchanged",()=>{const copy=JSON.parse(JSON.stringify(sources));const result=ask("overview",copy);copy.insights.totals.revenue_cents=1;assert.equal(result.sections[0].metrics[0].value,"R$ 100,00");}],
["no cross totals",()=>assert.ok(r.limitations.some(x=>x.includes("Não soma receitas")))]
];
for(const [name,run] of checks){run();console.log("PASS "+name);}
console.log(checks.length+" copilot tests passed");
