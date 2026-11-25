const assert=require("node:assert/strict");
const o=require("../core/operations.js");
const sample=o.HEADER+"\nCorte,480,30,60,400,390,5,12\nMontagem,480,60,90,250,240,8,20\nEmbalagem,480,15,45,450,445,3,8";
const rows=o.parse(sample),r=o.summarize(rows,50),a=r.stages[0];
const one=(line)=>o.parse(o.HEADER+"\n"+line);
const checks=[
["parse",()=>assert.equal(rows.length,3)],
["planned capacity",()=>assert.equal(a.planned_capacity,480)],
["effective capacity",()=>assert.equal(a.capacity,450)],
["availability",()=>assert.equal(a.availability_pct,93.75)],
["performance",()=>assert.ok(Math.abs(a.performance_pct-88.8888888889)<1e-8)],
["quality",()=>assert.equal(a.quality_pct,97.5)],
["OEE",()=>assert.ok(Math.abs(a.oee_pct-81.25)<1e-9)],
["throughput",()=>assert.ok(Math.abs(a.throughput_per_hour-53.3333333333)<1e-8)],
["lead time",()=>assert.equal(a.lead,12)],
["rework",()=>assert.equal(a.rework_pct,1.25)],
["nonconforming",()=>assert.equal(a.nonconforming,10)],
["other nonconforming",()=>assert.equal(a.other_nonconforming,5)],
["bottleneck",()=>assert.equal(r.bottlenecks[0],"Montagem")],
["serial capacity",()=>assert.equal(r.capacity,280)],
["scenario",()=>assert.equal(r.scenario.capacity,300)],
["scenario gain",()=>assert.equal(r.scenario.additional_capacity,20)],
["zero reduction",()=>assert.equal(o.summarize(rows,0).scenario.additional_capacity,0)],
["full reduction",()=>assert.equal(o.summarize(rows,100).scenario.capacity,320)],
["invalid reduction",()=>assert.throws(()=>o.summarize(rows,101))],
["ties",()=>assert.equal(o.summarize(o.parse(o.HEADER+"\nA,60,0,60,10,10,0,1\nB,60,0,60,10,10,0,1")).bottlenecks.length,2)],
["no output",()=>assert.equal(o.summarize(one("A,60,60,60,0,0,0,")).stages[0].oee_pct,null)],
["zero runtime",()=>assert.equal(o.summarize(one("A,60,60,60,0,0,0,")).stages[0].throughput_per_hour,null)],
["above ideal",()=>assert.equal(o.summarize(one("A,60,0,60,61,61,0,1")).stages[0].warning,"performance_above_100")],
["above ideal no OEE",()=>assert.equal(o.summarize(one("A,60,0,60,61,61,0,1")).stages[0].oee_pct,null)],
["downtime bounds",()=>assert.throws(()=>one("A,60,61,60,1,1,0,1"))],
["good bounds",()=>assert.throws(()=>one("A,60,0,60,1,2,0,1"))],
["rework bounds",()=>assert.throws(()=>one("A,60,0,60,3,2,2,1"))],
["runtime consistency",()=>assert.throws(()=>one("A,60,60,60,1,1,0,1"))],
["no measured lead",()=>assert.equal(one("A,60,0,60,1,1,0,")[0].lead,null)],
["lead without output",()=>assert.throws(()=>one("A,60,0,60,0,0,0,2"))],
["duplicate names",()=>assert.throws(()=>o.parse(o.HEADER+"\nA,60,0,60,1,1,0,1\nA,60,0,60,1,1,0,1"))],
["invalid cycle",()=>assert.throws(()=>one("A,60,0,0,1,1,0,1"))],
["size cap",()=>assert.throws(()=>o.parse("x".repeat(65537)))],
["row cap",()=>assert.throws(()=>o.parse(o.HEADER+"\n"+Array.from({length:101},(_,i)=>i+",60,0,60,1,1,0,1").join("\n")))],
["source unchanged",()=>assert.equal(JSON.stringify(rows),JSON.stringify(o.parse(sample)))]
];
for(const [name,run] of checks){run();console.log("PASS "+name);}
console.log(checks.length+" operations tests passed");
