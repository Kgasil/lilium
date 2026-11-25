const assert=require("node:assert/strict");
const s=require("../core/strategy.js");
const csv=s.GOALS+"\nCrescer,Receita,100,200,150,180,2,2026-12-31\nCrescer,Custo,100,50,75,60,1,2026-11-01\nQualidade,Erros,10,0,0,0,1,2026-11-01";
const goals=s.parseGoals(csv),r=s.scoreGoals(goals,"2026-11-25");
const one=line=>s.parseGoals(s.GOALS+"\n"+line);
const checks=[
["three KRs",()=>assert.equal(r.kr_count,3)],
["two objectives",()=>assert.equal(r.objective_count,2)],
["increase",()=>assert.equal(r.entries[0].progress_pct,50)],
["decrease",()=>assert.equal(r.entries[1].progress_pct,50)],
["achieved",()=>assert.equal(r.achieved,1)],
["overdue",()=>assert.equal(r.overdue,1)],
["weighted progress",()=>assert.equal(r.progress_pct,62.5)],
["scenario",()=>assert.equal(r.scenario_progress_pct,85)],
["scenario delta",()=>assert.equal(r.scenario_delta_pp,22.5)],
["objective score",()=>assert.equal(r.objectives[0].progress_pct,50)],
["deadline inclusive",()=>assert.equal(s.scoreGoals(goals,"2026-11-01").overdue,0)],
["overachieved clamped",()=>assert.equal(s.scoreGoals(one("O,K,0,10,20,30,1,2026-12-31"),"2026-11-25").progress_pct,100)],
["regression clamped",()=>assert.equal(s.scoreGoals(one("O,K,0,10,-1,0,1,2026-12-31"),"2026-11-25").progress_pct,0)],
["raw regression retained",()=>assert.equal(s.scoreGoals(one("O,K,0,10,-1,0,1,2026-12-31"),"2026-11-25").entries[0].raw_progress_pct,-10)],
["negative baseline",()=>assert.equal(s.scoreGoals(one("O,K,-100,0,-50,0,1,2026-12-31"),"2026-11-25").progress_pct,50)],
["decimal precision",()=>assert.equal(s.scoreGoals(one("O,K,0.10,0.30,0.20,0.25,1,2026-12-31"),"2026-11-25").progress_pct,50)],
["same target rejected",()=>assert.throws(()=>one("O,K,1,1,1,1,1,2026-12-31"))],
["bad weight",()=>assert.throws(()=>one("O,K,0,1,0,1,0,2026-12-31"))],
["bad date",()=>assert.throws(()=>one("O,K,0,1,0,1,1,2026-02-29"))],
["bad as-of",()=>assert.throws(()=>s.scoreGoals(goals,"2026-13-01"))],
["leap date",()=>assert.equal(s.date("2024-02-29"),true)],
["duplicate KR",()=>assert.throws(()=>s.parseGoals(csv+"\nCrescer,Receita,0,1,0,1,1,2026-12-31"))],
["bad precision",()=>assert.throws(()=>one("O,K,0,1,0.001,1,1,2026-12-31"))],
["blank field",()=>assert.throws(()=>one("O,,0,1,0,1,1,2026-12-31"))],
["BOM CRLF",()=>assert.equal(s.parseGoals("\uFEFF"+csv.replace(/\n/g,"\r\n")+"\r\n").length,3)],
["rank first",()=>assert.equal(s.rankActions(s.ACTIONS+"\nA,5,5,2\nB,4,4,1")[0].action,"B")],
["rank score",()=>assert.equal(s.rankActions(s.ACTIONS+"\nA,5,5,2")[0].score,12.5)],
["rank ties",()=>assert.equal(s.rankActions(s.ACTIONS+"\nZ,2,2,1\nA,4,1,1")[0].action,"A")],
["bad effort",()=>assert.throws(()=>s.rankActions(s.ACTIONS+"\nA,5,5,0"))],
["bad impact",()=>assert.throws(()=>s.rankActions(s.ACTIONS+"\nA,6,5,1"))],
["duplicate action",()=>assert.throws(()=>s.rankActions(s.ACTIONS+"\nA,1,1,1\nA,2,2,2"))],
["row cap",()=>assert.throws(()=>s.rankActions(s.ACTIONS+"\n"+Array.from({length:101},(_,i)=>i+",1,1,1").join("\n")))],
["length cap",()=>assert.throws(()=>s.parseGoals("x".repeat(65537)))],
["input unchanged",()=>assert.equal(JSON.stringify(goals),JSON.stringify(s.parseGoals(csv)))]
];
for(const [name,run] of checks){run();console.log("PASS "+name);}
console.log(checks.length+" strategy tests passed");
