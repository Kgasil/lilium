const assert=require("node:assert/strict");
const f=require("../core/flow.js");
const raw=f.HEADER+"\nR1,insights.margin,lt,20,Revisar custos\nR2,finance.result,lt,0,Reavaliar cenário\nR3,sales.orders,gte,5,Revisar demanda\nR4,forecast.wape,gt,10,Revisar modelo";
const rules=f.parse(raw),at="2026-11-25T12:00:00.000Z",later="2026-11-25T13:00:00.000Z";
const m=f.snapshot({insights:{months:[{}],from:"2026-01",to:"2026-02",totals:{margin_pct:"19.99"}},finance:{results:{result_cents:"-1"}},sales:{rows:5,orders:5,period:{from:"",to:""}},forecast:null});
const r=f.evaluate(rules,m),q=f.enqueue([],r,at);
const one=line=>f.parse(f.HEADER+"\n"+line);
const checks=[
["parse",()=>assert.equal(rules.length,4)],
["money cents",()=>assert.equal(rules[1].threshold,"0")],
["margin match",()=>assert.equal(r[0].outcome,"matched")],
["negative money",()=>assert.equal(r[1].outcome,"matched")],
["gte inclusive",()=>assert.equal(r[2].outcome,"matched")],
["missing unavailable",()=>assert.equal(r[3].outcome,"unavailable")],
["scope",()=>assert.ok(r[0].evidence.scope.includes("2026-01"))],
["simulation label",()=>assert.equal(r[1].evidence.kind,"simulação")],
["queue",()=>assert.equal(q.queue.length,3)],
["pending",()=>assert.equal(q.queue[0].status,"pending")],
["dedup",()=>assert.equal(f.enqueue(q.queue,r,later).skipped,3)],
["no mutation",()=>assert.equal(q.queue[0].events.length,1)],
["approve",()=>assert.equal(f.transition(q.queue,"P001","approved",later)[0].status,"approved")],
["reject",()=>assert.equal(f.transition(q.queue,"P001","rejected",later)[0].status,"rejected")],
["manual completion",()=>assert.equal(f.transition(f.transition(q.queue,"P001","approved",later),"P001","completed_manually",later)[0].status,"completed_manually")],
["cannot bypass approval",()=>assert.throws(()=>f.transition(q.queue,"P001","completed_manually",later))],
["terminal rejection",()=>assert.throws(()=>f.transition(f.transition(q.queue,"P001","rejected",later),"P001","approved",later))],
["unknown proposal",()=>assert.throws(()=>f.transition(q.queue,"X","approved",later))],
["backdated",()=>assert.throws(()=>f.transition(q.queue,"P001","approved","2025-01-01T00:00:00.000Z"))],
["invalid timestamp",()=>assert.throws(()=>f.enqueue([],r,"bad"))],
["unknown metric",()=>assert.throws(()=>one("R,constructor,eq,0,A"))],
["unknown operator",()=>assert.throws(()=>one("R,sales.orders,eval,0,A"))],
["duplicate rules",()=>assert.throws(()=>f.parse(raw+"\nR1,sales.orders,eq,1,A"))],
["precision",()=>assert.throws(()=>one("R,sales.orders,eq,1.001,A"))],
["large exact comparison",()=>assert.equal(f.evaluate(one("R,finance.result,gt,999999999999.99,A"),{"finance.result":{value:"999999999999999999",scope:"x",kind:"simulação"}})[0].outcome,"matched")],
["not matched",()=>assert.equal(f.evaluate(one("R,sales.orders,gt,5,A"),m)[0].outcome,"not_matched")],
["empty insights unavailable",()=>assert.equal(f.snapshot({insights:{months:[],totals:{margin_pct:"0"}}})["insights.margin"].value,null)],
["forecast selected model",()=>assert.equal(f.snapshot({forecast:{model:"b",comparison:[{model:"a",wape_pct:2},{model:"b",wape_pct:4}],validation:{from:"x",to:"y"}}})["forecast.wape"].value,4)],
["null forecast error",()=>assert.equal(f.snapshot({forecast:{model:"a",comparison:[{model:"a",wape_pct:null}],validation:{from:"x",to:"y"}}})["forecast.wape"].value,null)],
["queue limit",()=>assert.equal(f.enqueue(Array.from({length:200},(_,i)=>({signature:String(i)})),r,at).full,3)],
["changed evidence new proposal",()=>assert.equal(f.enqueue(q.queue,[{...r[0],evidence:{...r[0].evidence,value:18}}],later).added,1)],
["JSON safe",()=>assert.equal(JSON.parse(JSON.stringify(q.queue)).length,3)],
["BOM CRLF",()=>assert.equal(f.parse("\uFEFF"+raw.replace(/\n/g,"\r\n")+"\r\n").length,4)]
];
for(const [name,run] of checks){run();console.log("PASS "+name);}
console.log(checks.length+" flow tests passed");
