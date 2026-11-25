const assert=require("node:assert/strict");
const f=require("../core/forecast.js");
const raw=f.HEADER+"\n2026-01,100\n2026-02,120\n2026-03,140\n2026-04,160\n2026-05,180\n2026-06,200";
const rows=f.parse(raw),r=f.analyze(rows,3);
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-8);
const checks=[
["six months",()=>assert.equal(rows.length,6)],
["three models",()=>assert.equal(r.comparison.length,3)],
["automatic trend",()=>assert.equal(r.model,"trend")],
["linear next",()=>near(r.future[0].value,220)],
["linear horizon",()=>near(r.future[2].value,260)],
["future dates",()=>assert.equal(r.future[2].month,"2026-09")],
["holdout count",()=>assert.equal(r.validation.months,2)],
["holdout start",()=>assert.equal(r.validation.from,"2026-05")],
["rolling no leakage",()=>near(r.comparison[0].pairs[0].predicted,160)],
["rolling second",()=>near(r.comparison[0].pairs[1].predicted,180)],
["naive MAE",()=>near(r.comparison[0].mae,20)],
["trend MAE",()=>near(r.comparison[2].mae,0)],
["RMSE",()=>near(f.metrics([{actual:0,predicted:3},{actual:0,predicted:4}]).rmse,Math.sqrt(12.5))],
["WAPE",()=>near(f.metrics([{actual:100,predicted:90}]).wape_pct,10)],
["zero WAPE",()=>assert.equal(f.metrics([{actual:0,predicted:1}]).wape_pct,null)],
["manual selection",()=>assert.equal(f.analyze(rows,2,"ma3").model,"ma3")],
["moving average",()=>near(f.predict([100,200,300],"ma3",1)[0],200)],
["recursive MA",()=>near(f.predict([100,200,300],"ma3",2)[1],700/3)],
["naive horizon",()=>near(f.predict([100,200,300],"naive",4)[3],300)],
["nonnegative trend",()=>near(f.predict([30,20,10],"trend",3)[2],0)],
["tie chooses naive",()=>assert.equal(f.analyze(rows.map(x=>({...x,value:0}))).model,"naive")],
["year rollover",()=>assert.equal(f.monthLabel(f.monthIndex("2026-12")+1),"2027-01")],
["calendar limit",()=>assert.throws(()=>f.analyze(rows.map((x,i)=>({...x,month:"9999-"+String(i+7).padStart(2,"0")})),1))],
["invalid month",()=>assert.throws(()=>f.parse(raw.replace("2026-06","2026-13")))],
["missing month",()=>assert.throws(()=>f.parse(raw.replace("2026-06","2026-07")))],
["duplicate month",()=>assert.throws(()=>f.parse(raw.replace("2026-06","2026-05")))],
["negative",()=>assert.throws(()=>f.parse(raw.replace(",200",",-1")))],
["precision",()=>assert.throws(()=>f.parse(raw.replace(",200",",1.001")))],
["too short",()=>assert.throws(()=>f.parse(raw.split("\n").slice(0,-1).join("\n")))],
["horizon bound",()=>assert.throws(()=>f.analyze(rows,13))],
["unknown model",()=>assert.throws(()=>f.analyze(rows,3,"x"))],
["BOM CRLF",()=>assert.equal(f.parse("\uFEFF"+raw.replace(/\n/g,"\r\n")+"\r\n").length,6)],
["direct NaN rejected",()=>assert.throws(()=>f.analyze(rows.map(x=>({...x,value:NaN}))))],
["source unchanged",()=>assert.equal(JSON.stringify(rows),JSON.stringify(f.parse(raw)))],
["holdout maximum",()=>assert.equal(f.analyze(Array.from({length:24},(_,i)=>({month:f.monthLabel(f.monthIndex("2024-01")+i),value:i}))).validation.months,6)],
["JSON safe",()=>assert.equal(JSON.parse(JSON.stringify(r)).future.length,3)]
];
for(const [name,run] of checks){run();console.log("PASS "+name);}
console.log(checks.length+" forecast tests passed");
