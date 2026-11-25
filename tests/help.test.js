/* Offline Help Center search and content checks; no real browser. */
const assert=require("node:assert/strict"),fs=require("node:fs"),path=require("node:path");
const read=p=>fs.readFileSync(path.join(__dirname,"..",p),"utf8");
const html=read("core/workspace.html"),js=read("core/workspace.js");
const help=html.match(/<section id="help"[\s\S]*?<\/section>/)[0];
const topics=[...help.matchAll(/<details class="help-details help-topic">([\s\S]*?)<\/details>/g)].map(m=>m[1]);
const code=js.slice(js.indexOf("function helpNormalize("),js.indexOf("function filterHelp("));
const match=new Function(code+"\nreturn helpMatches;")();
const checks=[
["15 local guides",()=>assert.equal(topics.length,15)],
["blank search shows all",()=>assert.equal(topics.filter(x=>match(x,"   ")).length,15)],
["accent-insensitive search",()=>assert.ok(match("Previsão e solução","previsao SOLUCAO"))],
["all search words required",()=>assert.ok(!match("Margem e receita","margem inexistente"))],
["whitespace normalized",()=>assert.ok(match("Margem de contribuição","  margem   contribuicao "))],
["no matches for nonsense",()=>assert.equal(topics.filter(x=>match(x,"xyz987654321")).length,0)],
["backup query finds history",()=>assert.ok(topics.some(x=>match(x,"backup")&&x.includes('href="#history"')))],
["all guides link to real sections",()=>assert.ok(topics.every(x=>{const id=x.match(/href="#([^"]+)"/)?.[1];return id&&html.includes('<section id="'+id+'"');}))],
["all guides have summaries",()=>assert.ok(topics.every(x=>x.includes("<summary>")&&x.includes("</summary>")))],
["labeled search and live status",()=>assert.ok(help.includes('for="help-search"')&&help.includes('id="help-status" role="status" aria-atomic="true"'))],
["feedback template is read-only and excludes secrets",()=>assert.ok(help.includes('id="help-feedback" readonly')&&help.includes("Não inclua dados reais, tokens ou caminhos pessoais."))],
["no external help links",()=>assert.ok(!/href="https?:/.test(help))],
["local download",()=>assert.ok(js.includes("repDownload($('help-feedback').value,'text/plain;charset=utf-8','lilium-relato-suporte.txt')"))]
];
for(const [name,run] of checks){run();console.log("PASS "+name);}
console.log(checks.length+" Help Center checks passed");
