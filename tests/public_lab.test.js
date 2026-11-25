const assert=require("node:assert/strict"),lab=require("../web/lab.js"),finance=require("../core/finance.js"),starter=require("../core/starter.js"),sales=require("../core/sales.js"),forecast=require("../core/forecast.js");
const run=(kind,input)=>lab.evaluate(finance,starter,sales,forecast,kind,input);
const checks=[
["price",()=>assert.equal(run("price",{cost:"60",margin:"40"}).price_cents,"10000")],
["invalid margin",()=>assert.throws(()=>run("price",{cost:"60",margin:"100"}))],
["monthly result",()=>assert.equal(run("monthly",{price:"100",variable:"40",fixed:"2000",quantity:"100",fee:"5",target:"1000"}).result_cents,"350000")],
["break-even",()=>assert.equal(run("monthly",{price:"100",variable:"40",fixed:"2000",quantity:"100",fee:"5",target:"1000"}).break_even_units,"37")],
["infeasible break-even",()=>assert.equal(run("monthly",{price:"10",variable:"20",fixed:"2000",quantity:"10",fee:"0",target:"0"}).break_even_units,null)],
["invalid tool",()=>assert.throws(()=>run("invalid",{}))],
...starter.list().map(x=>[x.id+" reconciles",()=>{const r=run("scenario",{scenario:x.id});assert.equal(r.months.length,9);assert.equal(r.future.length,3);assert.equal(r.orders,27);assert.equal(BigInt(r.result_cents),BigInt(r.revenue_cents)-BigInt(r.cost_cents));assert.ok(r.csv.startsWith("date,revenue,cost\n"));}]),
["invalid scenario",()=>assert.throws(()=>run("scenario",{scenario:"constructor"}))]
];for(const [name,fn] of checks){fn();console.log("PASS "+name)}console.log(checks.length+" public lab checks passed");
