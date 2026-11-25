const assert=require("node:assert/strict"),c=require("../core/connect.js"),s=require("../core/sales.js"),f=require("../core/forecast.js");
const v={validDate:s.validDate,sales:s.parse,forecast:f.parse};
const raw="Dia;Receita;Custo;Cliente\n2026-01-01;100,50;60,25;IGNORAR";
const data=c.parse(raw,";"),map={date:"Dia",revenue:"Receita",cost:"Custo"};
const csv=c.normalize(data,"insights",map,true),p=c.make(csv,"insights",v);
const checks=[
["headers",()=>assert.equal(data.headers.length,4)],
["decimal comma",()=>assert.equal(csv,"date,revenue,cost\n2026-01-01,100.50,60.25")],
["unused column discarded",()=>assert.ok(!csv.includes("IGNORAR"))],
["row count",()=>assert.equal(p.row_count,1)],
["roundtrip",()=>assert.deepEqual(c.open(c.serialize(p),v),p)],
["reordered mapping",()=>assert.equal(c.normalize(c.parse("C,D,R\n60,2026-01-01,100"),"insights",{date:"D",revenue:"R",cost:"C"}),"date,revenue,cost\n2026-01-01,100,60")],
["tab separator",()=>assert.equal(c.parse("A\tB\n1\t2","\t").rows[0][1],"2")],
["BOM CRLF",()=>assert.equal(c.parse("\uFEFFa,b\r\n1,2\r\n").rows.length,1)],
["duplicate headers",()=>assert.throws(()=>c.parse("A,A\n1,2"))],
["uneven row",()=>assert.throws(()=>c.parse("A,B\n1"))],
["quoted fields rejected",()=>assert.throws(()=>c.parse('A,B\n"1",2'))],
["unknown destination",()=>assert.throws(()=>c.make(csv,"constructor",v))],
["duplicate mapping",()=>assert.throws(()=>c.normalize(data,"insights",{date:"Dia",revenue:"Receita",cost:"Receita"}))],
["missing mapping",()=>assert.throws(()=>c.normalize(data,"insights",{date:"Dia",revenue:"Receita"}))],
["absent header",()=>assert.throws(()=>c.normalize(data,"insights",{...map,cost:"X"}))],
["no implicit decimal conversion",()=>assert.throws(()=>c.normalize(data,"insights",map))],
["invalid date",()=>assert.throws(()=>c.make("date,revenue,cost\n2026-02-30,1,2","insights",v))],
["negative money",()=>assert.throws(()=>c.make("date,revenue,cost\n2026-01-01,-1,2","insights",v))],
["wrong header",()=>assert.throws(()=>c.make("x,y,z\n1,2,3","insights",v))],
["sales contract",()=>assert.equal(c.make(s.HEADER+"\n2026-01-01,A,Café,2,10","sales",v).row_count,1)],
["sales rejects invalid",()=>assert.throws(()=>c.make(s.HEADER+"\n2026-01-01,A,Café,0,10","sales",v))],
["forecast contract",()=>assert.equal(c.make(f.HEADER+"\n"+Array.from({length:6},(_,i)=>"2026-0"+(i+1)+",100").join("\n"),"forecast",v).row_count,6)],
["forecast gap",()=>assert.throws(()=>c.make(f.HEADER+"\n2026-01,1\n2026-03,2","forecast",v))],
["invalid JSON",()=>assert.throws(()=>c.open("{",v))],
["wrong version",()=>assert.throws(()=>c.open(JSON.stringify({...p,schema_version:"2"}),v))],
["tampered row count",()=>assert.throws(()=>c.open(JSON.stringify({...p,row_count:2}),v))],
["extra property",()=>assert.throws(()=>c.open(JSON.stringify({...p,command:"run"}),v))],
["tampered dataset",()=>assert.throws(()=>c.open(JSON.stringify({...p,csv:"bad"}),v))],
["size limit",()=>assert.throws(()=>c.parse("é".repeat(524289)))],
["row limit",()=>assert.throws(()=>c.parse("x\n"+"1\n".repeat(10001)))],
["source unchanged",()=>assert.equal(data.rows[0][1],"100,50")]
];
for(const [name,run] of checks){run();console.log("PASS "+name);}
console.log(checks.length+" connect tests passed");
