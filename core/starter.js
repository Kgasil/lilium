/* Synthetic business exercises, not company data or market benchmarks. */
(function(root){
"use strict";
const catalog={
 retail:{name:"Comércio de bairro",products:["Caderno","Caneta","Mochila"],prices:[24,5,95],base:18,costPct:68,stages:["Separação","Conferência","Expedição"],fixed:1200,focus:"Margens e mix de produtos"},
 services:{name:"Prestação de serviços",products:["Consultoria inicial","Manutenção","Treinamento"],prices:[180,260,350],base:7,costPct:48,stages:["Triagem","Execução","Revisão"],fixed:900,focus:"Preço por serviço e capacidade de atendimento"},
 industry:{name:"Pequena indústria",products:["Suporte","Componente","Kit de montagem"],prices:[35,60,110],base:28,costPct:74,stages:["Corte","Montagem","Inspeção"],fixed:2200,focus:"Custos variáveis e gargalos"},
 restaurant:{name:"Restaurante",products:["Prato executivo","Bebida","Sobremesa"],prices:[32,8,14],base:40,costPct:72,stages:["Preparação","Finalização","Entrega"],fixed:1800,focus:"Ticket médio e capacidade de atendimento"},
 ecommerce:{name:"Loja virtual",products:["Organizador","Garrafa","Kit presente"],prices:[49,65,120],base:19,costPct:66,stages:["Separação","Embalagem","Despacho"],fixed:1500,focus:"Mix de produtos e taxas de venda"}
};
const list=()=>Object.entries(catalog).map(([id,x])=>({id,name:x.name,focus:x.focus}));
function csv(header,rows){return [header,...rows.map(r=>r.join(","))].join("\n");}
function build(id){
 if(!Object.hasOwn(catalog,id))throw Error("Cenário não disponível.");
 const x=catalog[id],insights=[],sales=[],forecast=[];
 for(let m=1;m<=9;m++){
  const month="2026-"+String(m).padStart(2,"0");
  let revenue=0;
  for(let j=0;j<3;j++){
   // One synthetic aggregate order per product/month; not individual customer purchases.
   const q=x.base+m*2+j*3,p=x.prices[j];
   sales.push([month+"-05","DEMO-"+m+"-"+(j+1),x.products[j],q,p.toFixed(2)]);
   revenue+=q*p;
  }
  const cost=revenue*x.costPct/100;
  insights.push([month+"-05",revenue.toFixed(2),cost.toFixed(2)]);
  forecast.push([month,revenue.toFixed(2)]);
 }
 const p=x.prices[0],variable=Math.round(p*x.costPct)/100;
 const operations=x.stages.map((name,i)=>[name,480,30+i*15,60+i*30,180-i*25,174-i*25,3,12+i*4]);
 return {id,name:x.name,focus:x.focus,asOf:"2026-09-30",insights:csv("date,revenue,cost",insights),sales:csv("date,order_id,product,quantity,unit_price",sales),forecast:csv("month,value",forecast),operations:csv("stage,planned_min,downtime_min,cycle_sec,total_units,good_units,rework_units,lead_min",operations),
 goals:csv("objective,kr,baseline,target,actual,scenario,weight,due",[
 ["Crescimento","Receita mensal",Number(forecast[0][1]),Number(forecast[8][1])+500,Number(forecast[8][1]),Number(forecast[8][1])+300,3,"2026-12-31"],
 ["Eficiência","Minutos parados",60,30,45,35,2,"2026-12-31"]]),
 actions:csv("action,impact,urgency,effort",[["Revisar custos",5,4,2],["Melhorar fluxo operacional",4,4,3],["Revisar oferta",3,3,2]]),
 finance:{price:p.toFixed(2),variable:variable.toFixed(2),fixed:String(x.fixed),quantity:String(x.base*5),fee:id==="ecommerce"?"12":"3",target:"500"},
 notes:["Dados totalmente fictícios. Não são referências de mercado.","Sales usa 27 pedidos sintéticos agregados por produto e mês; o ticket médio não representa compras individuais reais.","Insights e Forecast compartilham a receita mensal de Sales. Os custos são hipóteses proporcionais à receita.","Finance é uma simulação independente de um produto; Operations representa um exercício de etapas sequenciais comparáveis; Strategy contém metas hipotéticas."]};
}
const api={list,build};
if(typeof module!=="undefined"&&module.exports)module.exports=api;else root.LiliumStarter=Object.freeze(api);
})(typeof globalThis!=="undefined"?globalThis:this);
