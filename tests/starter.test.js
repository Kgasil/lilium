const assert=require("node:assert/strict"),s=require("../core/starter.js"),sales=require("../core/sales.js"),ops=require("../core/operations.js"),strategy=require("../core/strategy.js"),forecast=require("../core/forecast.js"),finance=require("../core/finance.js"),connect=require("../core/connect.js");
let count=0;function check(name,fn){fn();count++;console.log("PASS "+name);}
check("five unique scenarios",()=>assert.equal(new Set(s.list().map(x=>x.id)).size,5));
check("unknown scenario rejected",()=>assert.throws(()=>s.build("constructor")));
for(const item of s.list()){
 const x=s.build(item.id);
 check(item.id+" deterministic",()=>assert.deepEqual(s.build(item.id),x));
 check(item.id+" revenue consistent",()=>{
  const v=sales.summarize(sales.parse(x.sales)),f=forecast.parse(x.forecast);
  assert.equal(v.orders,27);assert.equal(v.months.length,9);
  const i=connect.parse(x.insights).rows;
  for(let n=0;n<9;n++){assert.equal(v.months[n].revenue_cents,String(Math.round(f[n].value*100)));assert.equal(Number(i[n][1]),f[n].value);}
 });
 check(item.id+" Insights contract",()=>assert.equal(connect.make(x.insights,"insights",{validDate:sales.validDate,sales:sales.parse,forecast:forecast.parse}).row_count,9));
 check(item.id+" operations",()=>assert.equal(ops.summarize(ops.parse(x.operations)).stages.length,3));
 check(item.id+" goals",()=>assert.equal(strategy.scoreGoals(strategy.parseGoals(x.goals),x.asOf).kr_count,2));
 check(item.id+" actions",()=>assert.equal(strategy.rankActions(x.actions).length,3));
 check(item.id+" forecast",()=>assert.equal(forecast.analyze(forecast.parse(x.forecast),3).future.length,3));
 check(item.id+" finance",()=>assert.ok(typeof finance.simulate(x.finance).result_cents==="string"));
 check(item.id+" fresh objects",()=>{x.finance.price="0";assert.ok(s.build(item.id).finance.price!=="0");});
}
console.log(count+" starter tests passed");
