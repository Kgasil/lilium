/* Static integration guard; run with node tests/workspace.test.js. Not a browser test. */
const assert=require("node:assert/strict");
const fs=require("node:fs"),path=require("node:path");
const load=name=>fs.readFileSync(path.join(__dirname,"..",name),"utf8");
const html=load("core/workspace.html"),js=load("core/workspace.js"),api=load("core/api.py"),build=load("desktop/build_windows.py");
const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);
const scripts=[...html.matchAll(/<script src="([^"]+)"/g)].map(m=>m[1]);
const checks=[
 ["controller parses",()=>assert.doesNotThrow(()=>new Function(js))],
 ["unique ids",()=>assert.equal(new Set(ids).size,ids.length)],
 ["literal DOM references resolve",()=>assert.ok([...js.matchAll(/\$\('([^']+)'\)/g)].every(m=>ids.includes(m[1])))],
 ["local navigation anchors resolve",()=>assert.ok([...html.matchAll(/href="#([^"]+)"/g)].every(m=>ids.includes(m[1])))],
 ["no inline script",()=>assert.ok(!/<script\b(?![^>]*\bsrc=)[^>]*>/i.test(html))],
 ["no inline event handler",()=>assert.ok(!/<[^>]+\son\w+\s*=/i.test(html))],
 ["only local script sources",()=>assert.ok(scripts.length===12&&scripts.every(s=>/^\/assets\/[a-z]+\.js$/.test(s)))],
 ["controller last",()=>assert.equal(scripts.at(-1),"/assets/workspace.js")],
 ["all assets have routes",()=>assert.ok(scripts.every(s=>api.includes('"'+s+'"')))],
 ["CSP blocks inline scripts",()=>assert.ok(api.includes("script-src 'self';"))],
 ["build includes JS files",()=>assert.ok(build.includes('glob("*.js")'))],
 ["startup fallback",()=>assert.ok(ids.includes("workspace-loading")&&js.includes("$('workspace-loading').hidden=true"))]
];
for(const [name,run] of checks){run();console.log("PASS "+name);}
console.log(checks.length+" static workspace checks passed");
