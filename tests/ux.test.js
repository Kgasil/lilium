/* Structural accessibility checks and isolated navigation logic. Not a WCAG audit. */
const assert=require("node:assert/strict"),fs=require("node:fs"),path=require("node:path");
const load=p=>fs.readFileSync(path.join(__dirname,"..",p),"utf8");
const html=load("core/workspace.html"),js=load("core/workspace.js");
const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);
const nav=html.match(/<nav id="module-nav"[\s\S]*?<\/nav>/)[0];
const targets=[...nav.matchAll(/href="#([^"]+)"/g)].map(m=>m[1]);
const sections=[...html.matchAll(/<section id="([^"]+)"[^>]*aria-labelledby="([^"]+)"/g)];
const tables=[...html.matchAll(/<table>[\s\S]*?<\/table>/g)];
const checks=[
["skip link has focusable main target",()=>assert.ok(html.includes('class="skip-link" href="#main-content"')&&html.includes('<main id="main-content" tabindex="-1">'))],
["14 distinct module links",()=>assert.ok(targets.length===14&&new Set(targets).size===14&&targets.every(x=>ids.includes(x)))],
["four named navigation groups",()=>assert.equal((nav.match(/class="nav-label"/g)||[]).length,4)],
["section names and focus destinations",()=>assert.ok(sections.length===15&&sections.every(m=>m[2]===m[1]+"-heading"&&ids.includes(m[2])&&m[0].includes('tabindex="-1"')))],
["all tables have captions and scoped static headers",()=>assert.ok(tables.length===12&&tables.every(m=>m[0].includes('<caption class="sr-only">')&&!m[0].includes("<th>")))],
["all table scroll regions keyboard focusable",()=>assert.equal((html.match(/class="scroll" tabindex="0" role="region" aria-label="[^"]+"/g)||[]).length,12)],
["generated Connect headers scoped",()=>assert.ok(js.includes("th.scope='col'"))],
["six guided task shortcuts",()=>{const g=html.match(/<div class="quick-grid">[\s\S]*?<\/div>/)[0];assert.equal((g.match(/<a href="#/g)||[]).length,6);}],
["all status regions atomic",()=>assert.ok(!/role="status"(?! aria-atomic="true")/.test(html))],
["reduced motion preference respected",()=>assert.ok(html.includes("@media(prefers-reduced-motion:reduce)"))],
["current location updates and clears",()=>{
 const links=targets.map(id=>({href:"#"+id,current:null,getAttribute(){return this.href},setAttribute(k,v){this.current=v},removeAttribute(){this.current=null}}));
 const fn=js.slice(js.indexOf("function markWorkspaceLocation("),js.indexOf("markWorkspaceLocation(location.hash);"));
 const mark=new Function("$",fn+"\nreturn markWorkspaceLocation;")(()=>({querySelectorAll:()=>links}));
 mark("");assert.equal(links.filter(a=>a.current).map(a=>a.href).join(),"#getting-started");
 mark("#finance");assert.equal(links.filter(a=>a.current).map(a=>a.href).join(),"#finance");
 mark("#history");assert.equal(links.filter(a=>a.current).map(a=>a.href).join(),"#history");
 mark("#main-content");assert.equal(links.filter(a=>a.current).length,0);
}]
];
for(const [name,run] of checks){run();console.log("PASS "+name);}
console.log(checks.length+" UX structural/logic checks passed");
