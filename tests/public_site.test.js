/* Isolated DOM contract smoke test of public laboratory. Not Chromium. */
const fs=require("node:fs"),path=require("node:path"),assert=require("node:assert/strict");
const load=p=>fs.readFileSync(path.join(__dirname,"..",p),"utf8");
const html=load("index.html"),js=load("web/lab.js");
const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);
const checks=[];
function check(name,fn){fn();checks.push(name);console.log("PASS "+name);}
check("unique IDs",()=>assert.equal(new Set(ids).size,ids.length));
check("local anchors",()=>assert.ok([...html.matchAll(/href="#([^"]+)"/g)].every(m=>ids.includes(m[1]))));
check("lab assets present and ordered",()=>{const assets=[...html.matchAll(/<script src="([^"]+)"/g)].map(m=>m[1]);assert.deepEqual(assets,["core/finance.js","core/starter.js","core/sales.js","core/forecast.js","core/connect.js","web/lab.js"]);assert.ok(assets.every(p=>load(p).length>0));});
check("bilingual lab and language event",()=>assert.ok(html.includes('data-en="Lab"')&&html.includes("dispatchEvent(new Event('lilium-language'))")));
check("input labels resolve",()=>assert.ok([...html.matchAll(/<label for="([^"]+)"/g)].every(m=>ids.includes(m[1]))));
function el(){return {children:[],value:"",disabled:false,textContent:"",events:{},replaceChildren(){this.children=[]},append(...items){this.children.push(...items)},addEventListener(k,fn){this.events[k]=fn}}}
const elements=Object.fromEntries(ids.map(id=>[id,el()]));
for(const m of html.matchAll(/<input id="([^"]+)"[^>]*value="([^"]*)"/g))elements[m[1]].value=m[2];
elements["lab-scenario"].value="retail";
const doc={documentElement:{lang:"pt-BR"},events:{},getElementById(id){return elements[id]},createElement:el,addEventListener(k,fn){this.events[k]=fn}};
const root={LiliumFinance:require("../core/finance.js"),LiliumStarter:require("../core/starter.js"),LiliumSales:require("../core/sales.js"),LiliumForecast:require("../core/forecast.js"),LiliumConnect:require("../core/connect.js")};
new Function("document","globalThis",js)(doc,root);
const val=id=>elements[id].children.map(x=>x.children[1].textContent);
check("pricing shown on initialization",()=>assert.ok(val("lab-price-result").includes("R$ 100,00")));
check("monthly result shown",()=>assert.ok(val("lab-monthly-result").includes("R$ 3.500,00")));
check("invalid input clears stale results",()=>{elements["lab-price-margin"].value="100";elements["lab-price-form"].events.input();assert.equal(elements["lab-price-result"].children.length,0);assert.ok(elements["lab-price-error"].textContent.length>0);});
check("valid input restores calculation",()=>{elements["lab-price-margin"].value="40";elements["lab-price-form"].events.input();assert.ok(val("lab-price-result").includes("R$ 100,00"));});
check("scenario switching changes revenue",()=>{const old=val("lab-scenario-result")[0];elements["lab-scenario"].value="restaurant";elements["lab-scenario"].events.change();assert.ok(old!==val("lab-scenario-result")[0]);assert.equal(elements["lab-download"].disabled,false);assert.equal(elements["lab-package"].disabled,false);});
check("English event refreshes dynamic labels",()=>{doc.documentElement.lang="en";doc.events["lilium-language"]();assert.equal(elements["lab-price-result"].children[0].children[0].textContent,"Estimated price");});
console.log(checks.length+" public site contract checks passed");
