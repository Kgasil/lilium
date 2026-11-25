const assert=require("node:assert/strict");
const s=require("../core/sales.js");
const csv=s.HEADER+"\n2026-01-05,A1,Cafe,2,25.00\n2026-01-05,A1,Bolo,1,10.00\n2026-02-01,A2,Cafe,3,25.00\n2026-02-02,A3,Cha,1,5.00";
const rows=s.parse(csv),r=s.summarize(rows);
const checks=[
["rows",()=>assert.equal(r.rows,4)],
["distinct orders",()=>assert.equal(r.orders,3)],
["revenue",()=>assert.equal(r.revenue_cents,"14000")],
["quantity",()=>assert.equal(r.quantity,"7")],
["ticket",()=>assert.equal(r.average_order_cents,"4667")],
["rank",()=>assert.equal(r.products[0].name,"Cafe")],
["rank value",()=>assert.equal(r.products[0].revenue_cents,"12500")],
["months",()=>assert.equal(r.months[0].revenue_cents,"6000")],
["filter",()=>assert.equal(s.summarize(rows,"2026-02","2026-02").revenue_cents,"8000")],
["empty",()=>assert.equal(s.summarize(rows,"2025-01","2025-02").average_order_cents,null)],
["inverted",()=>assert.throws(()=>s.summarize(rows,"2026-02","2026-01"))],
["invalid month",()=>assert.throws(()=>s.summarize(rows,"2026-13",""))],
["duplicate warning",()=>assert.equal(s.summarize(s.parse(csv+"\n2026-02-02,A3,Cha,1,5.0")).possible_duplicate_rows,1)],
["duplicate retained",()=>assert.equal(s.summarize(s.parse(csv+"\n2026-02-02,A3,Cha,1,5.0")).revenue_cents,"14500")],
["order date mismatch",()=>assert.throws(()=>s.parse(csv+"\n2026-02-03,A1,Cafe,1,1"))],
["invalid leap",()=>assert.equal(s.validDate("2026-02-29"),false)],
["valid leap",()=>assert.equal(s.validDate("2024-02-29"),true)],
["invalid date",()=>assert.throws(()=>s.parse(s.HEADER+"\n2026-04-31,A,X,1,2"))],
["fractional qty",()=>assert.throws(()=>s.parse(s.HEADER+"\n2026-01-01,A,X,1.5,2"))],
["zero qty",()=>assert.throws(()=>s.parse(s.HEADER+"\n2026-01-01,A,X,0,2"))],
["negative price",()=>assert.throws(()=>s.parse(s.HEADER+"\n2026-01-01,A,X,1,-2"))],
["precision",()=>assert.throws(()=>s.parse(s.HEADER+"\n2026-01-01,A,X,1,2.001"))],
["blank product",()=>assert.throws(()=>s.parse(s.HEADER+"\n2026-01-01,A,,1,2"))],
["quoted fields",()=>assert.throws(()=>s.parse(s.HEADER+'\n2026-01-01,A,"X",1,2'))],
["bom crlf",()=>assert.equal(s.parse("\uFEFF"+csv.replace(/\n/g,"\r\n")+"\r\n").length,4)],
["large exact",()=>assert.equal(s.summarize(s.parse(s.HEADER+"\n2026-01-01,A,X,1000000,999999999.99")).revenue_cents,"99999999999000000")],
["row cap",()=>assert.throws(()=>s.parse(s.HEADER+"\n"+"2026-01-01,A,X,1,2\n".repeat(10001)))],
["zero price",()=>assert.equal(s.summarize(s.parse(s.HEADER+"\n2026-01-01,A,X,1,0")).average_order_cents,"0")],
["size cap",()=>assert.throws(()=>s.parse("x".repeat(1048577)))],
["ties deterministic",()=>assert.equal(s.summarize(s.parse(s.HEADER+"\n2026-01-01,A,Z,1,2\n2026-01-01,A,A,1,2")).products[0].name,"A")]
];
for(const [name,run] of checks){run();console.log("PASS "+name);}
console.log(checks.length+" sales tests passed");
