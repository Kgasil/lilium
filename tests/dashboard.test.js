const assert=require("node:assert/strict");
const api=require("../core/dashboard.js");
const m=(month,r,c)=>({month,revenue_cents:r,cost_cents:c,result_cents:r-c,margin_pct:api.margin(r,c)});
const data={months:[m("2026-01",1000000,600000),m("2026-02",1120000,744000),m("2026-03",1200000,780000)]};
const checks=[
["full totals",()=>assert.deepEqual(api.selectPeriod(data).totals,{revenue_cents:3320000,cost_cents:2124000,result_cents:1196000,margin_pct:"36.02"})],
["inclusive range",()=>assert.equal(api.selectPeriod(data,"2026-02","2026-03").totals.result_cents,796000)],
["single month",()=>assert.equal(api.selectPeriod(data,"2026-02","2026-02").months.length,1)],
["no records",()=>assert.equal(api.selectPeriod(data,"2025-01","2025-12").months.length,0)],
["zero margin unavailable",()=>assert.equal(api.margin(0,50),null)],
["negative margin",()=>assert.equal(api.margin(100,125),"-25.00")],
["half up positive",()=>assert.equal(api.margin(20000,19999),"0.01")],
["half up negative",()=>assert.equal(api.margin(20000,20001),"-0.01")],
["invalid range",()=>assert.throws(()=>api.selectPeriod(data,"2026-03","2026-01"))],
["invalid month",()=>assert.throws(()=>api.selectPeriod(data,"2026-13",""))],
["decimal exact",()=>assert.equal(api.decimal(-5),"-0.05")],
["CSV filtered",()=>assert.equal(api.exportMonthly(api.selectPeriod(data,"2026-02","2026-02")),"month,revenue_brl,cost_brl,result_brl,margin_pct\r\n2026-02,11200.00,7440.00,3760.00,33.57\r\n")],
["chart scale",()=>assert.equal(api.chartScale(data.months),1200000)],
["source unchanged",()=>{const old=JSON.stringify(data);api.selectPeriod(data,"2026-02","2026-02");assert.equal(JSON.stringify(data),old)}]
];
for(const [name,run] of checks){run();console.log("PASS "+name);}
console.log(checks.length+" dashboard tests passed");
