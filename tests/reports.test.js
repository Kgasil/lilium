const assert=require("node:assert/strict");
const R=require("../core/reports.js");
const meta={title:"Relatório de teste",generated_at:"2026-11-25T12:00:00.000Z"};
const sources={
 insights:{from:"2026-01",to:"2026-02",months:[{month:"2026-01",revenue_cents:10000,cost_cents:6000,result_cents:4000}],totals:{revenue_cents:10000,cost_cents:6000,result_cents:4000,margin_pct:"40.00"}},
 finance:{inputs:{price:"100",quantity:"10"},results:{revenue_cents:"100000",variable_cents:"40000",fees_cents:"5000",fixed_cents:"20000",result_cents:"35000",result_margin_pct:"35.00",break_even_units:"4"}},
 sales:{period:{from:"2026-03",to:"2026-03"},revenue_cents:"25000",orders:2,quantity:"5",average_order_cents:"12500",possible_duplicate_rows:1,products:[{name:"Café",quantity:"5",revenue_cents:"25000"}]},
 operations:{stages:[{stage:"A",oee_pct:null,capacity:100,warning:"performance_above_100"}],capacity:100,bottlenecks:["A"],scenario:{reduction_pct:50,capacity:120}},
 strategy:{as_of:"2026-11-25",objective_count:1,kr_count:2,progress_pct:50,scenario_progress_pct:70,achieved:0,overdue:1,objectives:[{objective:"Crescer",progress_pct:50,scenario_progress_pct:70}]},
 actions:{actions:[{action:"Revisar preço",score:10,impact:5,urgency:4,effort:2}]}
};
const build=(keys=R.MODULES,data=sources,m=meta)=>R.compose(data,keys,m);
const report=build(),txt=R.toText(report);
const checks=[
["all six sections",()=>assert.equal(report.sections.length,6)],
["stable order",()=>assert.equal(build(["sales","insights"]).sections[0].source,"insights")],
["deduplicate selection",()=>assert.equal(build(["sales","sales"]).sections.length,1)],
["selected only",()=>assert.equal(build(["sales"]).sections[0].source,"sales")],
["missing source",()=>assert.equal(build(["sales","strategy"],{sales:sources.sales}).missing_sources[0],"strategy")],
["all missing rejected",()=>assert.throws(()=>build(["sales"],{}))],
["empty selection",()=>assert.throws(()=>build([]))],
["unknown source",()=>assert.throws(()=>build(["x"]))],
["empty title",()=>assert.throws(()=>build(["sales"],sources,{...meta,title:" "}))],
["long title",()=>assert.throws(()=>build(["sales"],sources,{...meta,title:"x".repeat(101)}))],
["bad timestamp",()=>assert.throws(()=>build(["sales"],sources,{...meta,generated_at:"bad"}))],
["insights period",()=>assert.ok(report.sections[0].scope.includes("2026-01"))],
["sales period independent",()=>assert.ok(report.sections[2].scope.includes("2026-03"))],
["finance simulation labeled",()=>assert.equal(report.sections[1].kind,"simulação")],
["financial assumptions retained",()=>assert.ok(report.sections[1].details.some(d=>d.label==="Quantidade (un.)"&&d.values[0]==="10"))],
["duplicate count",()=>assert.equal(report.sections[2].metrics.find(x=>x.label==="Possíveis duplicatas").value,"1")],
["OEE warning",()=>assert.ok(txt.includes("Revisar performance"))],
["hypothetical distinction",()=>assert.ok(txt.includes("cenário hipotético"))],
["priority method",()=>assert.ok(txt.includes("impacto × urgência ÷ esforço"))],
["no cross-module totals",()=>assert.ok(report.limitations.some(x=>x.includes("Não consolida somas")))],
["exact negative money",()=>assert.equal(R.money("-123456789012345678"),"−R$ 1.234.567.890.123.456,78")],
["null money",()=>assert.equal(R.money(null),"N/A")],
["JSON safe",()=>assert.equal(JSON.parse(JSON.stringify(report)).sections.length,6)],
["snapshot independent",()=>{const copy=JSON.parse(JSON.stringify(sources));const r=build(["sales"],copy);copy.sales.revenue_cents="0";assert.equal(r.sections[0].metrics[0].value,"R$ 250,00");}],
["empty insights",()=>assert.equal(build(["insights"],{insights:{from:"",to:"",months:[]}}).sections[0].metrics.length,0)],
["missing text",()=>assert.ok(R.toText(build(["sales","actions"],{sales:sources.sales})).includes("Fontes sem resultado: Prioridades"))],
["user text treated literally",()=>assert.ok(R.toText(build(["actions"],{actions:{actions:[{action:"<script>x</script>",score:1,impact:1,urgency:1,effort:1}]}})).includes("<script>x</script>"))]
];
for(const [name,run] of checks){run();console.log("PASS "+name);}
console.log(checks.length+" reports tests passed");
