const assert=require("node:assert/strict");
const f=require("../core/finance.js");
const sample={price:"100",variable:"40",fixed:"2000",quantity:"100",fee:"5",target:"1000"};
const sim=(v={})=>f.simulate({...sample,...v});
const tests=[
["monthly revenue",()=>assert.equal(sim().revenue_cents,"1000000")],
["variable cost",()=>assert.equal(sim().variable_cents,"400000")],
["fee",()=>assert.equal(sim().fees_cents,"50000")],
["monthly result",()=>assert.equal(sim().result_cents,"350000")],
["margin",()=>assert.equal(sim().result_margin_pct,"35.00")],
["contribution",()=>assert.equal(sim().unit_contribution_cents,"5500")],
["contribution margin",()=>assert.equal(sim().contribution_margin_pct,"55.00")],
["break even ceil",()=>assert.equal(sim().break_even_units,"37")],
["target ceil",()=>assert.equal(sim().target_units,"55")],
["negative result",()=>assert.equal(sim({quantity:"0"}).result_cents,"-200000")],
["zero revenue",()=>assert.equal(sim({price:"0"}).result_margin_pct,null)],
["no viable contribution",()=>assert.equal(sim({variable:"100"}).break_even_units,null)],
["zero contribution and fixed costs",()=>assert.equal(sim({variable:"95",fixed:"0"}).break_even_units,"0")],
["fee half up",()=>assert.equal(sim({price:"0.10",fee:"5",quantity:"1"}).fees_cents,"1")],
["price target",()=>assert.equal(f.pricing("60","40").price_cents,"10000")],
["price rounds up",()=>assert.equal(f.pricing("1","33.33").price_cents,"150")],
["zero pricing",()=>assert.equal(f.pricing("0","50").margin_pct,null)],
["reject 100 percent",()=>assert.throws(()=>f.pricing("5","100"))],
["reject negative",()=>assert.throws(()=>sim({fixed:"-1"}))],
["reject fractional quantity",()=>assert.throws(()=>sim({quantity:"2.5"}))],
["reject quantity over limit",()=>assert.throws(()=>sim({quantity:"1000001"}))],
["reject precision",()=>assert.throws(()=>sim({price:"1.001"}))],
["comma decimal",()=>assert.equal(f.cents("1,25"),125n)],
["large values exact",()=>assert.equal(sim({price:"999999999.99",quantity:"1000000"}).revenue_cents,"99999999999000000")],
["BRL exact",()=>assert.equal(f.formatBRL("-123456789012345678"),"−R$ 1.234.567.890.123.456,78")]
];
for(const [name,run] of tests){run();console.log("PASS "+name);}
console.log(tests.length+" finance tests passed");
