
"use strict";
// Desktop access capability stays in this tab's sessionStorage; never sent in a URL.
let localToken = "";
try {
 const fragment = /^#access=([0-9a-f]{64})$/.exec(location.hash);
 if (fragment) {
  localToken = fragment[1];
  try { sessionStorage.setItem("lilium-access",localToken); } catch {}
  history.replaceState(null,"",location.pathname+location.search);
 } else {
  const saved = sessionStorage.getItem("lilium-access");
  if (/^[0-9a-f]{64}$/.test(saved||"")) localToken=saved;
 }
} catch {}
async function localFetch(url, options={}) {
 if (typeof url!=="string"||!url.startsWith("/api/")) throw Error("Rota local inválida.");
 const headers=new Headers(options.headers||{});
 if(localToken)headers.set("X-Lilium-Session",localToken);
 const response=await fetch(url,{...options,headers,cache:"no-store",redirect:"error",credentials:"omit"});
 if(response.status===403){
  const data=await response.clone().json().catch(()=>null);
  if(data?.error?.code==="session_required"){
   localToken="";
   try{sessionStorage.removeItem("lilium-access");}catch{}
   const notice=document.getElementById("session-notice");
   if(notice){notice.hidden=false;notice.textContent="Sessão local inválida ou encerrada. Abra o link privado exibido pelo Lilium Desktop.";}
   throw Error("Sessão inválida. Abra o link privado do Lilium Desktop.");
  }
 }
 return response;
}
const $=id=>document.getElementById(id);const sample="date,revenue,cost\n2026-01-01,10000,6000\n2026-02-01,11200,7440\n2026-03-01,12000,7800";const money=x=>new Intl.NumberFormat('pt-BR',{style:'currency',currency:'BRL'}).format(x/100);const pct=x=>x===null?'N/A':x.replace('.',',')+'%';let last=null,rev=0,selectedFile=null,lastPayload=null,lastQuality=null;function reset(){rev++;last=null;lastPayload=null;lastQuality=null;currentView=null;$('margin-target').value='';$('chart-mode').value='comparison';$('overview-empty').hidden=false;$('quality').hidden=true;$('save').hidden=true;$('results').hidden=true;$('status').textContent='';}let currentView=null;function show(data){for(const id of ['from','to']){const select=$(id);select.replaceChildren();const all=document.createElement('option');all.value='';all.textContent=id==='from'?'Início':'Fim';select.append(all);for(const m of data.months){const o=document.createElement('option');o.value=m.month;o.textContent=m.month;select.append(o)}}renderPeriod(data,'','');$('overview-empty').hidden=true;$('results').hidden=false;}
function renderPeriod(data,from,to){const view=LiliumDashboard.selectPeriod(data,from,to);currentView=view;$('metrics').replaceChildren();for(const [name,value] of [['Receita',money(view.totals.revenue_cents)],['Custos',money(view.totals.cost_cents)],['Resultado',money(view.totals.result_cents)],['Margem',pct(view.totals.margin_pct)]]){const box=document.createElement('div');box.className='kpi';const label=document.createElement('span');label.textContent=name;const strong=document.createElement('strong');strong.textContent=view.months.length?value:'—';box.append(label,strong);$('metrics').append(box)}$('rows').replaceChildren();for(const m of view.months){const tr=document.createElement('tr');for(const v of [m.month,money(m.revenue_cents),money(m.cost_cents),money(m.result_cents),pct(m.margin_pct)]){const td=document.createElement('td');td.textContent=v;tr.append(td)}$('rows').append(tr)}renderDataChart();renderMarginTarget();$('period-note').textContent=view.months.length?view.months.length+' meses com registros. O filtro não altera nem limita o histórico salvo.':'Nenhum mês com registros no intervalo.';$('export-csv').disabled=!view.months.length;}
function renderMarginTarget(){
 const raw=$('margin-target').value.trim(),out=$('margin-target-status');
 if(!raw){out.textContent='Defina uma meta opcional para o período.';return;}
 if(!currentView){out.textContent='Sem análise disponível.';return;}
 try{const x=LiliumDashboard.marginTarget(currentView,raw);out.textContent=x.status==='unavailable'?'Margem indisponível para este período.':(x.status==='met'?'Meta atingida':'Abaixo da meta')+' · diferença: '+x.gap.replace('.',',')+' p.p.';}catch(e){out.textContent=e.message;}
}
function renderDataChart(){
 if(!currentView)return;
 const mode=$('chart-mode').value,chart=LiliumDashboard.chartSeries(currentView.months,mode);
 $('chart-heading').textContent=mode==='result'?'Resultado mensal (magnitude e sinal)':'Receita e custos por mês';
 const legend=$('chart-legend');legend.className='legend'+(mode==='result'?' result':'');legend.replaceChildren();
 for(const name of mode==='result'?['Resultado não negativo','Resultado negativo']:['Receita','Custos']){const label=document.createElement('span');label.textContent=name;legend.append(label);}
 $('bars').replaceChildren();
 for(const r of chart.rows){const row=document.createElement('div');row.className='bar-row';const label=document.createElement('small');label.textContent=r.month;const pair=document.createElement('div');pair.className='bar-pair';for(const v of r.values){const track=document.createElement('div');track.className='bar-track';const bar=document.createElement('div');bar.className='bar '+v.kind;bar.style.width=(100*Math.abs(v.value)/chart.scale)+'%';track.title=money(v.value);track.append(bar);pair.append(track);}row.append(label,pair);$('bars').append(row);}
}
$('margin-target').addEventListener('input',renderMarginTarget);
$('chart-mode').addEventListener('change',renderDataChart);
$('apply').onclick=()=>{if(!last)return;try{renderPeriod(last,$('from').value,$('to').value)}catch{$('period-note').textContent='Período inválido. O início deve ser anterior ou igual ao fim.';}};$('clear').onclick=()=>{if(!last)return;$('from').value=$('to').value='';renderPeriod(last,'','');};
$('export-csv').onclick=()=>{if(!currentView||!currentView.months.length)return;const url=URL.createObjectURL(new Blob([LiliumDashboard.exportMonthly(currentView)],{type:'text/csv;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download='lilium-monthly.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};const XLSX='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
function payload(){return selectedFile?{body:selectedFile,type:selectedFile.name.toLowerCase().endsWith('.xlsx')?XLSX:'text/csv'}:{body:$('csv').value,type:'text/csv; charset=utf-8'};}
function showQuality(q){lastQuality=q;$('quality-summary').textContent=q.rows+' linhas · '+q.valid_rows+' válidas · '+q.invalid_rows+' inválidas · '+q.possible_duplicates+' possíveis duplicatas · '+q.zero_revenue_rows+' com receita zero.';$('quality-rows').replaceChildren();const labels={columns:'Número incorreto de colunas',date:'Data inválida',amount:'Valor monetário inválido',row_limit:'Linha vazia ou inválida',possible_duplicate:'Possível duplicata',zero_revenue:'Receita zero'};for(const i of q.issues){const tr=document.createElement('tr');for(const v of [i.row,i.severity==='error'?'Erro':'Alerta',labels[i.code]||i.code]){const td=document.createElement('td');td.textContent=v;tr.append(td)}$('quality-rows').append(tr)}$('quality-note').textContent=q.issues_truncated?'Exibindo os primeiros 100 apontamentos.':'';$('quality').hidden=false;}
$('quality-export').onclick=()=>{if(!lastQuality)return;const url=URL.createObjectURL(new Blob([JSON.stringify({schema_version:'1.0',kind:'lilium.quality',...lastQuality},null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='lilium-quality.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
async function run(onlyQuality=false){reset();const seq=rev,p=payload();const size=typeof p.body==='string'?new TextEncoder().encode(p.body).length:p.body.size;if(size>1048576){$('status').textContent='Limite de 1 MiB.';return;}$('run').disabled=$('check').disabled=true;try{const send=async url=>{const res=await localFetch(url,{method:'POST',headers:{'Content-Type':p.type},body:p.body});const data=await res.json();if(!res.ok)throw Error((data.error?.message||'Falha na validação.')+(data.error?.row?' Linha '+data.error.row:''));return data};const q=await send('/api/v1/quality');if(seq!==rev)return;showQuality(q);if(!q.can_analyze){$('status').textContent='Corrija as linhas inválidas antes de analisar.';return;}if(onlyQuality){$('status').textContent='Diagnóstico concluído.';return;}const data=await send('/api/v1/analyze');if(seq!==rev)return;last=data;lastPayload=p;show(data);$('save').hidden=false;$('overview').scrollIntoView({block:'start'});$('status').textContent=data.rows+' linhas válidas.';}catch(e){if(seq===rev)$('status').textContent=e.message||'Não foi possível acessar a API local.';}finally{$('run').disabled=$('check').disabled=false;}}
$('csv').addEventListener('input',reset);$('sample').onclick=()=>{selectedFile=null;$('file').value='';$('csv').disabled=false;$('csv').value=sample;$('source').textContent='Fonte: texto CSV.';reset()};$('file').onchange=()=>{reset();selectedFile=null;$('csv').disabled=false;$('csv').value='';const f=$('file').files[0];$('source').textContent='Fonte: texto CSV.';if(!f)return;if(!/\.(csv|xlsx)$/i.test(f.name)||f.size>1048576){$('file').value='';$('status').textContent='Escolha CSV ou XLSX de até 1 MiB.';return;}selectedFile=f;$('csv').disabled=true;$('source').textContent='Fonte: '+f.name;};$('run').onclick=()=>run(false);$('check').onclick=()=>run(true);$('export').onclick=()=>{if(!last)return;const url=URL.createObjectURL(new Blob([JSON.stringify(last,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='lilium-analysis.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)};$('csv').value=sample;
let historySeq=0, saving=false;
function historyMessage(data,fallback){return data?.error?.code==='history_corrupt'?'Histórico inconsistente. Preserve o banco local e procure suporte. Nenhum registro foi reparado automaticamente.':fallback;}
async function refreshHistory(){const seq=++historySeq;try{const res=await localFetch('/api/v1/history',{cache:'no-store'});const data=await res.json();if(seq!==historySeq)return;if(!res.ok)throw Error(historyMessage(data,'Histórico indisponível.'));$('history-rows').replaceChildren();for(const item of data.items){const tr=document.createElement('tr');for(const v of [new Date(item.created_at).toLocaleString('pt-BR'),item.rows,money(item.totals.result_cents)]){const td=document.createElement('td');td.textContent=v;tr.append(td)}const actions=document.createElement('td');for(const [label,handler] of [['Abrir',()=>openHistory(item.id)],['Excluir',()=>deleteHistory(item.id)]]){const b=document.createElement('button');b.textContent=label;b.style.margin='3px';b.addEventListener('click',handler);actions.append(b)}tr.append(actions);$('history-rows').append(tr)}$('history-status').textContent=data.items.length+' análises salvas.';}catch(e){if(seq===historySeq){$('history-rows').replaceChildren();$('history-status').textContent=e.message.startsWith('Histórico inconsistente.')?e.message:'Não foi possível consultar o histórico.';}}}
async function openHistory(id){reset();const seq=rev;try{const res=await localFetch('/api/v1/history/'+encodeURIComponent(id),{cache:'no-store'});const item=await res.json();if(seq!==rev)return;if(!res.ok)throw Error(historyMessage(item,'Não foi possível abrir a análise.'));last=item.analysis;show(last);$('overview').scrollIntoView({block:'start'});$('status').textContent='Análise salva aberta. O CSV original não foi armazenado.';}catch(e){if(seq===rev)$('status').textContent=e.message.startsWith('Histórico inconsistente.')?e.message:'Não foi possível abrir a análise.';}}
async function deleteHistory(id){if(!confirm('Excluir esta análise do histórico local?'))return;try{const res=await localFetch('/api/v1/history/'+encodeURIComponent(id),{method:'DELETE'});if(!res.ok)throw Error();reset();await refreshHistory();}catch{$('history-status').textContent='Não foi possível excluir a análise.';}}
$('save').onclick=async()=>{if(!last||!lastPayload||saving||$('save').hidden)return;saving=true;$('save').disabled=true;const seq=rev,p=lastPayload;try{const res=await localFetch('/api/v1/history',{method:'POST',headers:{'Content-Type':p.type},body:p.body});const data=await res.json();if(!res.ok)throw Error(data.error?.message||'Falha ao salvar.');if(seq===rev){$('save').hidden=true;$('status').textContent='Análise salva localmente.';}await refreshHistory();}catch(e){if(seq===rev)$('status').textContent=e.message;}finally{saving=false;$('save').disabled=false;}};
$('refresh').onclick=refreshHistory;refreshHistory();

let financeReport=null,managementReport=null;
const fmoney=v=>LiliumFinance.formatBRL(v), fpercent=v=>v===null?'N/A':v.replace('.',',')+'%', funits=v=>v===null?'Inviável nas premissas':BigInt(v).toLocaleString('pt-BR')+' un.';
function financeCards(id,items){const target=$(id);target.replaceChildren();for(const [name,value] of items){const card=document.createElement('div');card.className='kpi';const label=document.createElement('span');label.textContent=name;const strong=document.createElement('strong');strong.textContent=value;card.append(label,strong);target.append(card);}target.hidden=false;}
$('pricing-form').addEventListener('input',()=>{$('pricing-result').hidden=true;$('pricing-status').textContent='';});
$('pricing-form').addEventListener('submit',e=>{e.preventDefault();$('pricing-result').hidden=true;try{const p=LiliumFinance.pricing($('price-cost').value,$('price-margin').value);financeCards('pricing-result',[['Preço mínimo',fmoney(p.price_cents)],['Contribuição unitária',fmoney(p.contribution_cents)],['Margem efetiva',fpercent(p.margin_pct)]]);$('pricing-status').textContent='Preço arredondado para cima ao centavo.';}catch(err){$('pricing-status').textContent=err.message;}});
$('finance-form').addEventListener('input',()=>{clearScenarios();financeReport=null;$('finance-export').disabled=true;$('finance-result').hidden=true;$('finance-status').textContent='';});
$('finance-form').addEventListener('submit',e=>{e.preventDefault();clearScenarios();financeReport=null;$('finance-export').disabled=true;$('finance-result').hidden=true;try{const inputs=Object.fromEntries(['price','variable','fixed','quantity','fee','target'].map(k=>[k,$('sim-'+k).value.trim()]));const s=LiliumFinance.simulate(inputs);financeCards('finance-result',[['Receita simulada',fmoney(s.revenue_cents)],['Custos variáveis',fmoney(s.variable_cents)],['Taxas de venda',fmoney(s.fees_cents)],['Custos fixos',fmoney(s.fixed_cents)],['Resultado estimado',fmoney(s.result_cents)],['Margem de resultado',fpercent(s.result_margin_pct)],['Contribuição unitária',fmoney(s.unit_contribution_cents)],['Margem de contribuição',fpercent(s.contribution_margin_pct)],['Ponto de equilíbrio',funits(s.break_even_units)],['Vendas para atingir a meta',funits(s.target_units)]]);$('finance-status').textContent=BigInt(s.result_cents)<0n?'O cenário apresenta resultado negativo.':BigInt(s.result_cents)===0n?'Receitas e custos estimados se equilibram.':'Cenário com resultado positivo nas premissas informadas.';financeReport={schema_version:'1.0',kind:'single-product-monthly-simulation',currency:'BRL',inputs,results:s,assumptions:['Constant unit price and costs','Percentage fee rounded half-up per unit','Fixed monthly costs','Not a forecast or accounting statement']};$('finance-export').disabled=false;}catch(err){$('finance-status').textContent=err.message;}});
$('finance-export').onclick=()=>{if(!financeReport)return;const url=URL.createObjectURL(new Blob([JSON.stringify(financeReport,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='lilium-finance-scenario.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};

function clearScenarios(){
 if(financeReport?.scenarios){const {scenarios,...rest}=financeReport;financeReport=rest;}
 $('scenario-result').hidden=true;$('scenario-status').textContent='';
}
for(const id of ['scenario-low','scenario-high'])$(id).addEventListener('input',clearScenarios);
$('scenario-run').onclick=()=>{clearScenarios();try{
 if(!financeReport)throw Error('Calcule a simulação mensal primeiro.');
 const scenarios=LiliumFinance.compareScenarios(financeReport.inputs,$('scenario-low').value,$('scenario-high').value);
 financeReport={...financeReport,scenarios};
 financeCards('scenario-result',scenarios.map(x=>[x.label+' · '+x.quantity+' un.',fmoney(x.result_cents)]));
 $('scenario-status').textContent='Resultados hipotéticos; somente o volume varia.';
 }catch(e){$('scenario-status').textContent=e.message;}};
function clearManagement(){managementReport=null;$('management-result').hidden=true;$('management-export').disabled=true;$('management-status').textContent='';}
$('management-form').addEventListener('input',clearManagement);
$('management-form').addEventListener('submit',e=>{e.preventDefault();clearManagement();try{
 const input=Object.fromEntries(["revenue","deductions","cogs","expenses","other_income","other_expense","tax","opening","receipts","payments"].map(k=>[k,$('mgmt-'+k).value]));input.month=$('mgmt-month').value;
 const r=LiliumFinance.management(input),d=r.dre,c=r.cash;
 financeCards('management-result',[['Receita líquida',fmoney(d.net_revenue)],['Resultado bruto',fmoney(d.gross_profit)],['Resultado operacional',fmoney(d.operating_result)],['Resultado gerencial',fmoney(d.result)],['Margem líquida',fpercent(r.margin_pct)],['Saldo inicial de caixa',fmoney(c.opening)],['Entradas de caixa',fmoney(c.receipts)],['Saídas de caixa',fmoney(c.payments)],['Movimentação líquida',fmoney(c.flow)],['Saldo final de caixa',fmoney(c.closing)]]);
 managementReport=r;$('management-export').disabled=false;$('management-status').textContent='Mês '+r.month+' · DRE e caixa calculados separadamente.';
 }catch(e){$('management-status').textContent=e.message;}});
$('management-export').onclick=()=>{if(managementReport)stExport(managementReport,'lilium-management.json');};

let salesRows=null,salesView=null,salesRevision=0;
const salesSample="date,order_id,product,quantity,unit_price\n2026-01-05,A1,Café,2,25.00\n2026-01-05,A1,Bolo,1,10.00\n2026-02-01,A2,Café,3,25.00\n2026-02-02,A3,Chá,1,5.00";
function salesReset(){salesRevision++;salesRows=null;salesView=null;$('sales-results').hidden=true;$('sales-status').textContent='';}
$('sales-csv').addEventListener('input',()=>{salesReset();$('sales-file').value='';});
$('sales-sample').onclick=()=>{salesReset();$('sales-file').value='';$('sales-csv').value=salesSample;};
$('sales-file').onchange=async()=>{salesReset();const seq=salesRevision;const file=$('sales-file').files[0];if(!file)return;$('sales-csv').value='';if(file.size>1048576||!/\.csv$/i.test(file.name)){$('sales-status').textContent='Escolha CSV de até 1 MiB.';return;}$('sales-run').disabled=true;try{const bytes=await file.arrayBuffer();const str=new TextDecoder('utf-8',{fatal:true}).decode(bytes);if(seq===salesRevision)$('sales-csv').value=str;}catch{if(seq===salesRevision)$('sales-status').textContent='Não foi possível ler CSV UTF-8.';}finally{$('sales-run').disabled=false;}};
function salesFillTable(id,items){const body=$(id);body.replaceChildren();for(const x of items){const tr=document.createElement('tr');for(const v of [x.name,BigInt(x.quantity).toLocaleString('pt-BR'),fmoney(x.revenue_cents)]){const td=document.createElement('td');td.textContent=v;tr.append(td)}body.append(tr)}}
function salesRender(from='',to=''){const v=LiliumSales.summarize(salesRows,from,to);salesView=v;financeCards('sales-metrics',[['Receita bruta',fmoney(v.revenue_cents)],['Pedidos distintos',v.orders.toLocaleString('pt-BR')],['Unidades vendidas',BigInt(v.quantity).toLocaleString('pt-BR')],['Ticket médio',v.average_order_cents===null?'N/A':fmoney(v.average_order_cents)],['Produtos distintos',v.product_count.toLocaleString('pt-BR')],['Linhas de venda',v.rows.toLocaleString('pt-BR')]]);salesFillTable('sales-products',v.products);salesFillTable('sales-months',v.months);$('sales-bars').replaceChildren();const max=BigInt(v.products[0]?.revenue_cents||'0');for(const p of v.products.slice(0,10)){const wrapper=document.createElement('div');wrapper.style.margin='12px 0';const name=document.createElement('p');name.style.margin='0 0 3px';name.textContent=p.name+' · '+fmoney(p.revenue_cents);const track=document.createElement('div');track.className='bar-track';const bar=document.createElement('div');bar.className='bar';bar.style.width=(max?Number(BigInt(p.revenue_cents)*10000n/max)/100:0)+'%';track.append(bar);wrapper.append(name,track);$('sales-bars').append(wrapper)}$('sales-note').textContent=!v.rows?'Nenhuma venda no período.':v.possible_duplicate_rows?v.possible_duplicate_rows+' possíveis linhas duplicadas foram mantidas. Confira o arquivo original.':'Período analisado sem duplicatas exatas detectadas.';$('sales-results').hidden=false;$('sales-export').disabled=!v.rows;}
$('sales-run').onclick=()=>{salesReset();try{salesRows=LiliumSales.parse($('sales-csv').value);const months=LiliumSales.summarize(salesRows).months;for(const id of ['sales-from','sales-to']){const sel=$(id);sel.replaceChildren();const all=document.createElement('option');all.value='';all.textContent=id==='sales-from'?'Início':'Fim';sel.append(all);for(const m of months){const opt=document.createElement('option');opt.value=m.name;opt.textContent=m.name;sel.append(opt)}}salesRender();$('sales-status').textContent=salesRows.length+' linhas de venda validadas.';}catch(e){$('sales-status').textContent=e.message;}};
$('sales-filter').onclick=()=>{if(!salesRows)return;try{salesRender($('sales-from').value,$('sales-to').value);}catch(e){$('sales-note').textContent=e.message;}};
$('sales-clear').onclick=()=>{if(!salesRows)return;$('sales-from').value=$('sales-to').value='';salesRender();};
$('sales-export').onclick=()=>{if(!salesView||!salesView.rows)return;const u=URL.createObjectURL(new Blob([JSON.stringify(salesView,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=u;a.download='lilium-sales-analysis.json';a.click();setTimeout(()=>URL.revokeObjectURL(u),1000);};
$('sales-csv').value=salesSample;

let opsRows=null,opsView=null,opsRevision=0;
const opsSample="stage,planned_min,downtime_min,cycle_sec,total_units,good_units,rework_units,lead_min\nCorte,480,30,60,400,390,5,12\nMontagem,480,60,90,250,240,8,20\nEmbalagem,480,15,45,450,445,3,8";
const opsNumber=n=>n===null?'N/A':n.toLocaleString('pt-BR',{maximumFractionDigits:2});
const opsPct=n=>n===null?'N/A':opsNumber(n)+'%';
function opsReset(){opsRevision++;opsRows=null;opsView=null;$('ops-results').hidden=true;$('ops-status').textContent='';$('ops-reduction').value='0';$('ops-reduction-label').textContent='0%';}
$('ops-csv').addEventListener('input',()=>{opsReset();$('ops-file').value='';});
$('ops-sample').onclick=()=>{opsReset();$('ops-file').value='';$('ops-csv').value=opsSample;};
$('ops-file').onchange=async()=>{opsReset();const seq=opsRevision,f=$('ops-file').files[0];if(!f)return;$('ops-csv').value='';if(f.size>65536||!/\.csv$/i.test(f.name)){$('ops-status').textContent='Escolha CSV de até 64 KiB.';return;}$('ops-run').disabled=true;try{const raw=new TextDecoder('utf-8',{fatal:true}).decode(await f.arrayBuffer());if(seq===opsRevision)$('ops-csv').value=raw;}catch{if(seq===opsRevision)$('ops-status').textContent='Não foi possível ler CSV UTF-8.';}finally{$('ops-run').disabled=false;}};
function opsScenario(){
 if(!opsRows)return;
 const reduction=Number($('ops-reduction').value);opsView=LiliumOperations.summarize(opsRows,reduction);$('ops-reduction-label').textContent=reduction+'%';
 const s=opsView.scenario;
 financeCards('ops-scenario',[['Capacidade teórica simulada',opsNumber(s.capacity)+' un.'],['Capacidade adicional estimada','+'+opsNumber(s.additional_capacity)+' un.'],['Gargalo estimado',s.bottlenecks.join(', ')]]);
}
function opsRender(){
 opsScenario();const view=opsView;
 financeCards('ops-metrics',[['Etapas analisadas',opsNumber(view.stages.length)],['Capacidade teórica da linha',opsNumber(view.capacity)+' un.'],['Gargalo estimado',view.bottlenecks.join(', ')]]);
 $('ops-table').replaceChildren();$('ops-bars').replaceChildren();const max=Math.max(1,...view.stages.map(s=>s.capacity));
 for(const s of view.stages){
 const tr=document.createElement('tr');
 for(const v of [s.stage,opsNumber(s.run),opsNumber(s.planned_capacity),opsNumber(s.capacity),opsPct(s.availability_pct),opsPct(s.performance_pct),opsPct(s.quality_pct),opsPct(s.oee_pct),opsNumber(s.throughput_per_hour),opsNumber(s.nonconforming),opsNumber(s.rework)+' ('+opsPct(s.rework_pct)+')',opsNumber(s.lead)]){const td=document.createElement('td');td.textContent=v;tr.append(td)}
 $('ops-table').append(tr);const wrap=document.createElement('div');wrap.style.margin='10px 0';const label=document.createElement('p');label.textContent=s.stage+' · '+opsNumber(s.capacity)+' un.'+(view.bottlenecks.includes(s.stage)?' · gargalo estimado':'');const track=document.createElement('div');track.className='bar-track';const bar=document.createElement('div');bar.className='bar'+(view.bottlenecks.includes(s.stage)?' cost':'');bar.style.width=(s.capacity/max*100)+'%';track.append(bar);wrap.append(label,track);$('ops-bars').append(wrap);}
 const warnings=view.stages.filter(s=>s.warning).map(s=>s.stage);$('ops-warnings').textContent=warnings.length?'Revise ciclo ideal e produção: performance acima de 100% em '+warnings.join(', ')+'. OEE indisponível nessas etapas.':'Nenhuma performance acima de 100% detectada.';$('ops-results').hidden=false;
}
$('ops-run').onclick=()=>{opsReset();try{opsRows=LiliumOperations.parse($('ops-csv').value);opsRender();$('ops-status').textContent=opsRows.length+' etapas validadas.';}catch(e){$('ops-status').textContent=e.message;}};
$('ops-reduction').oninput=opsScenario;
$('ops-export').onclick=()=>{if(!opsView)return;const u=URL.createObjectURL(new Blob([JSON.stringify(opsView,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=u;a.download='lilium-operations-analysis.json';a.click();setTimeout(()=>URL.revokeObjectURL(u),1000);};
$('ops-csv').value=opsSample;

let strategyReport=null,actionReport=null;
const strategySample="objective,kr,baseline,target,actual,scenario,weight,due\nCrescimento,Receita,10000,15000,12500,14000,3,2026-12-31\nCrescimento,Ticket médio,50,70,60,66,2,2026-12-31\nEficiência,Retrabalho (%),10,5,7,6,2,2026-11-30";
const actionSample="action,impact,urgency,effort\nRevisar precificação,5,4,2\nPadronizar operações,4,5,3\nMelhorar exposição dos produtos,3,3,1";
const stNumber=n=>n.toLocaleString('pt-BR',{maximumFractionDigits:2});
const stPct=n=>stNumber(n)+'%';
function stReset(){strategyReport=null;$('strategy-results').hidden=true;$('strategy-status').textContent='';}
function actReset(){actionReport=null;$('actions-results').hidden=true;$('actions-status').textContent='';}
$('strategy-csv').addEventListener('input',stReset);$('strategy-date').addEventListener('input',stReset);
$('strategy-actions').addEventListener('input',actReset);
$('strategy-sample').onclick=()=>{stReset();$('strategy-csv').value=strategySample;$('strategy-date').value='2026-11-25';};
$('actions-sample').onclick=()=>{actReset();$('strategy-actions').value=actionSample;};
function stTable(id,rows){const body=$(id);body.replaceChildren();for(const values of rows){const tr=document.createElement('tr');for(const v of values){const td=document.createElement('td');td.textContent=v;tr.append(td)}body.append(tr)}}
function stExport(data,name){const u=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=u;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(u),1000);}
$('strategy-run').onclick=()=>{stReset();try{
 const view=LiliumStrategy.scoreGoals(LiliumStrategy.parseGoals($('strategy-csv').value),$('strategy-date').value);
 financeCards('strategy-metrics',[['Objetivos',stNumber(view.objective_count)],['Resultados-chave',stNumber(view.kr_count)],['Progresso ponderado',stPct(view.progress_pct)],['Cenário hipotético',stPct(view.scenario_progress_pct)],['Variação do cenário',stNumber(view.scenario_delta_pp)+' p.p.'],['KRs atingidos',stNumber(view.achieved)],['KRs vencidos não atingidos',stNumber(view.overdue)]]);
 const box=$('strategy-bars');box.replaceChildren();
 for(const o of view.objectives){const group=document.createElement('div');group.style.margin='12px 0';const title=document.createElement('p');title.textContent=o.objective;group.append(title);for(const [name,n,color] of [['Atual',o.progress_pct,'bar'],['Cenário',o.scenario_progress_pct,'bar cost']]){const label=document.createElement('small');label.textContent=name+' · '+stPct(n);const track=document.createElement('div');track.className='bar-track';const bar=document.createElement('div');bar.className=color;bar.style.width=n+'%';track.append(bar);group.append(label,track)}box.append(group)}
 const states={achieved:'Atingida',overdue:'Vencida',open:'Em aberto'};
 stTable('strategy-table',view.entries.map(g=>[g.objective,g.kr,stNumber(g.baseline),stNumber(g.target),stNumber(g.actual),stNumber(g.scenario),g.weight,stPct(g.raw_progress_pct),stPct(g.progress_pct),stPct(g.scenario_progress_pct),g.due,states[g.status]]));
 strategyReport=view;$('strategy-results').hidden=false;$('strategy-status').textContent=view.kr_count+' KRs avaliados na data informada.';
 }catch(e){$('strategy-status').textContent=e.message;}};
$('actions-run').onclick=()=>{actReset();try{const ranks=LiliumStrategy.rankActions($('strategy-actions').value);stTable('actions-table',ranks.map(x=>[x.action,x.impact,x.urgency,x.effort,stNumber(x.score)]));actionReport={schema_version:'1.0',method:'impact*urgency/effort',actions:ranks};$('actions-results').hidden=false;$('actions-status').textContent=ranks.length+' ações priorizadas.';}catch(e){$('actions-status').textContent=e.message;}};
$('strategy-export').onclick=()=>{if(strategyReport)stExport(strategyReport,'lilium-strategy-goals.json');};
$('actions-export').onclick=()=>{if(actionReport)stExport(actionReport,'lilium-strategy-actions.json');};
$('strategy-csv').value=strategySample;$('strategy-date').value='2026-11-25';$('strategy-actions').value=actionSample;

let executiveReport=null;
function repNode(tag,value){const node=document.createElement(tag);node.textContent=value;return node;}
function repReset(){executiveReport=null;$('reports-preview').hidden=true;for(const id of ['reports-json','reports-txt','reports-print'])$(id).disabled=true;$('reports-status').textContent='';}
$('reports-title').addEventListener('input',repReset);
for(const key of LiliumReports.MODULES)$('reports-'+key).addEventListener('change',repReset);
function repRender(report){
 const view=$('reports-preview');view.replaceChildren();
 view.append(repNode('small','LILIUM REPORTS · STRATEGY & GROWTH'),repNode('h3',report.title),repNode('p','Gerado em (UTC): '+report.generated_at));
 for(const section of report.sections){
  const block=document.createElement('article');
  block.append(repNode('h4',section.title),repNode('p',section.kind+' | '+section.scope));
  const dl=document.createElement('dl');
  for(const metric of section.metrics){const div=document.createElement('div');div.append(repNode('dt',metric.label),repNode('dd',metric.value));dl.append(div);}
  block.append(dl);
  if(section.details.length){const ul=document.createElement('ul');for(const detail of section.details)ul.append(repNode('li',detail.label+': '+detail.values.join(' | ')));block.append(ul);}
  for(const note of section.notes)block.append(repNode('p','Nota: '+note));
  view.append(block);
 }
 if(report.missing_sources.length)view.append(repNode('p','Fontes sem resultado: '+report.missing_sources.map(k=>LiliumReports.LABELS[k]).join(', ')));
 view.append(repNode('h4','Limitações'));for(const note of report.limitations)view.append(repNode('p',note));
 view.append(repNode('small','K&G Vision · Lilium'));view.hidden=false;
}
$('reports-generate').onclick=()=>{repReset();try{
 const sources={insights:currentView,finance:financeReport,sales:salesView,operations:opsView,strategy:strategyReport,actions:actionReport,management:managementReport};
 const selected=LiliumReports.MODULES.filter(k=>$('reports-'+k).checked);
 const report=LiliumReports.compose(sources,selected,{title:$('reports-title').value,generated_at:new Date().toISOString()});
 repRender(report);executiveReport=report;
 for(const id of ['reports-json','reports-txt','reports-print'])$(id).disabled=false;
 $('reports-status').textContent=report.sections.length+' seções incluídas; '+report.missing_sources.length+' fontes sem resultado. Fotografia da sessão no momento de geração.';
 }catch(e){$('reports-status').textContent=e.message;}};
function repDownload(content,type,name){const url=URL.createObjectURL(new Blob([content],{type}));const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
$('reports-json').onclick=()=>{if(executiveReport)repDownload(JSON.stringify(executiveReport,null,2),'application/json','lilium-executive-report.json');};
$('reports-txt').onclick=()=>{if(executiveReport)repDownload(LiliumReports.toText(executiveReport),'text/plain;charset=utf-8','lilium-executive-report.txt');};
$('reports-print').onclick=()=>{if(executiveReport)window.print();};

let forecastReport=null;
const forecastSample="month,value\n2026-01,10000\n2026-02,11200\n2026-03,12000\n2026-04,11500\n2026-05,13000\n2026-06,14200\n2026-07,13800\n2026-08,15000\n2026-09,15800";
function fcReset(){forecastReport=null;$('forecast-results').hidden=true;$('forecast-status').textContent='';}
for(const id of ['forecast-csv','forecast-horizon','forecast-unit','forecast-model'])$(id).addEventListener('input',fcReset);
$('forecast-sample').onclick=()=>{fcReset();$('forecast-csv').value=forecastSample;$('forecast-unit').value='BRL';};
$('forecast-insights').onclick=()=>{fcReset();if(!last){$('forecast-status').textContent='Calcule ou abra uma análise do Insights primeiro.';return;}try{
 const text='month,value\n'+last.months.map(m=>m.month+','+LiliumDashboard.decimal(m.revenue_cents)).join('\n');
 LiliumForecast.parse(text);$('forecast-csv').value=text;$('forecast-unit').value='BRL';$('forecast-status').textContent='Receita da análise completa carregada. Confira os meses antes de calcular.';
 }catch(e){$('forecast-status').textContent='Série do Insights não compatível: '+e.message;}};
function fcFormat(n,unit){if(n===null)return 'N/A';return new Intl.NumberFormat('pt-BR',unit==='BRL'?{style:'currency',currency:'BRL'}:{maximumFractionDigits:2}).format(n);}
$('forecast-run').onclick=()=>{fcReset();try{
 const unit=$('forecast-unit').value;
 const rows=LiliumForecast.parse($('forecast-csv').value);
 if(unit==='units'&&rows.some(r=>!Number.isInteger(r.value)))throw Error('Para quantidade vendida, use unidades históricas inteiras.');
 const view=LiliumForecast.analyze(rows,Number($('forecast-horizon').value),$('forecast-model').value);
 const f=n=>fcFormat(n,unit),chosen=view.comparison.find(m=>m.model===view.model);
 financeCards('forecast-metrics',[['Modelo utilizado',view.model_label],['Último valor observado',f(view.historical.at(-1).value)],['Próximo mês estimado',f(view.future[0].value)],['MAE histórico de 1 passo',f(chosen.mae)]]);
 $('forecast-validation').textContent='Validação temporal de um passo: '+view.validation.months+' meses ('+view.validation.from+' a '+view.validation.to+'). Menor MAE: '+LiliumForecast.LABELS[view.best_validation_model]+'. A seleção e avaliação usam os mesmos meses; não há teste independente.';
 stTable('forecast-comparison',view.comparison.map(m=>[m.label,f(m.mae),f(m.rmse),m.wape_pct===null?'N/A':stNumber(m.wape_pct)+'%',m.model===view.model?'Selecionado':'—']));
 stTable('forecast-future',view.future.map(m=>[m.month,f(m.value)]));
 const chart=$('forecast-chart');chart.replaceChildren();
 const values=[...view.historical.slice(-24).map(x=>({...x,estimated:false})),...view.future.map(x=>({...x,estimated:true}))];
 const max=Math.max(1,...values.map(x=>x.value));
 for(const x of values){const row=document.createElement('div');row.className='bar-row';const label=document.createElement('small');label.textContent=x.month;const pair=document.createElement('div');const track=document.createElement('div');track.className='bar-track';const bar=document.createElement('div');bar.className='bar'+(x.estimated?' cost':'');bar.style.width=(100*x.value/max)+'%';track.append(bar);const value=document.createElement('small');value.textContent=f(x.value)+(x.estimated?' · estimado':' · observado');pair.append(track,value);row.append(label,pair);chart.append(row);}
 const ul=$('forecast-limits');ul.replaceChildren();for(const note of view.limitations){const li=document.createElement('li');li.textContent=note;ul.append(li);}
 forecastReport={...view,unit};$('forecast-results').hidden=false;$('forecast-status').textContent=rows.length+' meses históricos validados; '+view.horizon+' meses estimados.';
 }catch(e){$('forecast-status').textContent=e.message;}};
$('forecast-export').onclick=()=>{if(forecastReport)stExport(forecastReport,'lilium-forecast.json');};
$('forecast-csv').value=forecastSample;

let flowQueue=[];
const flowSample="rule_id,metric,operator,threshold,action\nR1,insights.margin,lt,20,Revisar custos\nR2,finance.result,lt,0,Reavaliar cenário financeiro\nR3,sales.orders,lt,10,Investigar demanda\nR4,operations.capacity,lt,300,Revisar capacidade operacional\nR5,strategy.progress,lt,60,Revisar metas estratégicas\nR6,forecast.wape,gt,10,Revisar previsão";
const flowOps={lt:'<',lte:'≤',gt:'>',gte:'≥',eq:'='};
const flowStates={pending:'Aguardando aprovação',approved:'Aprovada — não executada',rejected:'Rejeitada',completed_manually:'Conclusão declarada'};
function flowFormat(key,value){if(value===null||value===undefined)return 'N/A';return LiliumFlow.METRICS[key].kind==='money'?fmoney(value):stNumber(value);}
function flowQueueRender(){
 financeCards('flow-summary',[['Pendentes',flowQueue.filter(q=>q.status==='pending').length],['Aprovadas',flowQueue.filter(q=>q.status==='approved').length],['Conclusões declaradas',flowQueue.filter(q=>q.status==='completed_manually').length],['Rejeitadas',flowQueue.filter(q=>q.status==='rejected').length]]);
 const target=$('flow-queue');target.replaceChildren();
 if(!flowQueue.length){target.append(repNode('p','Nenhuma proposta na sessão.'));return;}
 for(const q of flowQueue){
 const block=document.createElement('article');block.className='finance-block';block.append(repNode('h4',q.id+' · '+q.action),repNode('p',flowStates[q.status]),repNode('p',LiliumFlow.METRICS[q.metric].label+' '+flowOps[q.operator]+' '+flowFormat(q.metric,q.threshold)+' | Evidência: '+flowFormat(q.metric,q.evidence.value)+' · '+q.evidence.kind+' · '+q.evidence.scope),repNode('small','Criada em UTC: '+q.created_at));
 const row=document.createElement('div');row.className='actions';
 const options=q.status==='pending'?[['Aprovar proposta','approved'],['Rejeitar','rejected']]:q.status==='approved'?[['Declarar conclusão manual','completed_manually'],['Rejeitar','rejected']]:[];
 for(const [label,status] of options){const b=document.createElement('button');b.textContent=label;b.className='secondary';b.onclick=()=>{if(status==='completed_manually'&&!confirm('Você confirma que realizou esta ação manualmente? O aplicativo não executará nada.'))return;try{flowQueue=LiliumFlow.transition(flowQueue,q.id,status,new Date().toISOString());flowQueueRender();$('flow-queue-status').textContent=q.id+': '+flowStates[status]+'.';}catch(e){$('flow-queue-status').textContent=e.message;}};row.append(b)}
 block.append(row);target.append(block);
 }
}
$('flow-rules').addEventListener('input',()=>{$('flow-evaluation').replaceChildren();$('flow-status').textContent='';});
$('flow-sample').onclick=()=>{$('flow-rules').value=flowSample;$('flow-evaluation').replaceChildren();$('flow-status').textContent='';};
$('flow-run').onclick=()=>{$('flow-evaluation').replaceChildren();$('flow-status').textContent='';try{
 const rules=LiliumFlow.parse($('flow-rules').value),metrics=LiliumFlow.snapshot({insights:currentView,finance:financeReport,sales:salesView,operations:opsView,strategy:strategyReport,forecast:forecastReport}),results=LiliumFlow.evaluate(rules,metrics);
 const labels={matched:'Condição atendida',not_matched:'Não atendida',unavailable:'Fonte indisponível'};
 stTable('flow-evaluation',results.map(x=>[x.id,LiliumFlow.METRICS[x.metric].label,flowOps[x.op]+' '+flowFormat(x.metric,x.threshold),flowFormat(x.metric,x.evidence?.value),x.evidence?x.evidence.kind+' · '+x.evidence.scope:'—',labels[x.outcome]]));
 const result=LiliumFlow.enqueue(flowQueue,results,new Date().toISOString());flowQueue=result.queue;flowQueueRender();
 $('flow-status').textContent=result.added+' novas propostas; '+result.skipped+' repetidas ignoradas; '+result.full+' não adicionadas por limite; '+results.filter(x=>x.outcome==='unavailable').length+' regras sem dados.';
 }catch(e){$('flow-status').textContent=e.message;}};
$('flow-export').onclick=()=>stExport({schema_version:'1.0',mode:'local-human-review',exported_at:new Date().toISOString(),proposals:flowQueue,limitations:['No external execution','Manual completion is user-declared','Session event log is not tamper-proof']},'lilium-flow-queue.json');
$('flow-clear').onclick=()=>{if(flowQueue.length&&!confirm('Limpar todas as propostas e eventos desta sessão? Exporte antes se necessário.'))return;flowQueue=[];flowQueueRender();$('flow-queue-status').textContent='Fila vazia.';};
for(const [key,m] of Object.entries(LiliumFlow.METRICS))$('flow-metrics-list').append(repNode('li',key+' — '+m.label));
$('flow-rules').value=flowSample;flowQueueRender();

let connectData=null,connectPacket=null,connectRev=0,connectPackageRev=0;
const connectValidators={validDate:LiliumSales.validDate,sales:LiliumSales.parse,forecast:LiliumForecast.parse};
const connectNames={insights:'Insights',sales:'Sales',forecast:'Forecast',management:'DRE e caixa'};
function connectReset(){connectPacket=null;$('connect-result').hidden=true;$('connect-transfer-status').textContent='';}
function connectMapReset(){connectRev++;connectData=null;connectReset();$('connect-map').replaceChildren();$('connect-normalize').disabled=true;$('connect-status').textContent='';}
$('connect-raw').addEventListener('input',connectMapReset);$('connect-sep').addEventListener('change',connectMapReset);$('connect-target').addEventListener('change',connectMapReset);$('connect-decimal').addEventListener('change',connectReset);
$('connect-package').addEventListener('input',()=>{connectPackageRev++;connectReset();$('connect-package-status').textContent='';});
$('connect-sample').onclick=()=>{connectMapReset();$('connect-target').value='insights';$('connect-sep').value=';';$('connect-decimal').checked=true;$('connect-raw').value='Dia;Receita;Custo;Campo extra\n2026-01-01;100,50;60,25;ignorado\n2026-02-01;200,00;90,00;ignorado';$('connect-file').value='';};
async function connectLoadFile(file,textarea,status,version,isCurrent){
 if(!file)return;
 if(file.size>1048576){$(status).textContent='Arquivo acima de 1 MiB.';return;}
 try{const txt=new TextDecoder('utf-8',{fatal:true}).decode(await file.arrayBuffer());if(isCurrent(version)){$(textarea).value=txt;$(status).textContent='Arquivo carregado. Valide antes de usar.';}}catch{if(isCurrent(version))$(status).textContent='Não foi possível ler UTF-8.';}
}
$('connect-file').onchange=()=>{connectMapReset();$('connect-raw').value='';connectLoadFile($('connect-file').files[0],'connect-raw','connect-status',connectRev,v=>v===connectRev);};
$('connect-package-file').onchange=()=>{connectPackageRev++;connectReset();$('connect-package').value='';$('connect-package-status').textContent='';connectLoadFile($('connect-package-file').files[0],'connect-package','connect-package-status',connectPackageRev,v=>v===connectPackageRev);};
$('connect-read').onclick=()=>{connectMapReset();try{
 const sep=$('connect-sep').value;const data=LiliumConnect.parse($('connect-raw').value,sep==='tab'?'\t':sep);const target=$('connect-target').value;
 for(const field of LiliumConnect.SCHEMAS[target]){const label=document.createElement('label');label.append(repNode('span',field));const sel=document.createElement('select');sel.dataset.field=field;const empty=repNode('option','Selecione coluna');empty.value='';sel.append(empty);
 for(const h of data.headers){const opt=repNode('option',h);opt.value=h;sel.append(opt);}if(data.headers.includes(field))sel.value=field;sel.onchange=connectReset;label.append(sel);$('connect-map').append(label);}
 connectData=data;$('connect-normalize').disabled=false;$('connect-status').textContent=data.headers.length+' colunas · '+data.rows.length+' registros. Escolha os campos.';
 }catch(e){$('connect-status').textContent=e.message;}};
function connectRender(p){const data=LiliumConnect.parse(p.csv);financeCards('connect-metrics',[['Destino',connectNames[p.target]],['Registros',p.row_count],['Colunas',data.headers.length]]);const tr=document.createElement('tr');for(const h of data.headers){const th=repNode('th',h);th.scope='col';tr.append(th);}$('connect-head').replaceChildren(tr);stTable('connect-preview',data.rows.slice(0,10));connectPacket=p;$('connect-result').hidden=false;}
$('connect-normalize').onclick=()=>{connectReset();try{if(!connectData)throw Error('Leia os cabeçalhos primeiro.');const target=$('connect-target').value;const mapping=Object.fromEntries(Array.from($('connect-map').querySelectorAll('select')).map(x=>[x.dataset.field,x.value]));const csv=LiliumConnect.normalize(connectData,target,mapping,$('connect-decimal').checked);connectRender(LiliumConnect.make(csv,target,connectValidators));$('connect-status').textContent='Dados normalizados e validados para '+connectNames[target]+'.';}catch(e){$('connect-status').textContent=e.message;}};
$('connect-open').onclick=()=>{connectReset();try{connectRender(LiliumConnect.open($('connect-package').value,connectValidators));$('connect-package-status').textContent='Pacote validado.';}catch(e){$('connect-package-status').textContent=e.message;}};
$('connect-csv').onclick=()=>{if(connectPacket)repDownload(connectPacket.csv,'text/csv;charset=utf-8','lilium-'+connectPacket.target+'.csv');};
$('connect-json').onclick=()=>{if(!connectPacket)return;try{repDownload(LiliumConnect.serialize(connectPacket),'application/json','lilium-dataset.json');}catch(e){$('connect-transfer-status').textContent=e.message+' Exporte CSV.';}};
$('connect-apply').onclick=()=>{const p=connectPacket;if(!p||!confirm('Substituir a entrada e limpar os resultados atuais de '+connectNames[p.target]+'? Nenhuma análise será executada automaticamente.'))return;
 if(p.target==='insights'){selectedFile=null;$('file').value='';$('csv').disabled=false;$('csv').value=p.csv;reset();$('source').textContent='Fonte: Connect · CSV normalizado.';$('import').scrollIntoView({block:'start'});}
 else if(p.target==='sales'){salesReset();$('sales-file').value='';$('sales-csv').value=p.csv;$('sales').scrollIntoView({block:'start'});}
 else if(p.target==='forecast'){fcReset();$('forecast-csv').value=p.csv;$('forecast').scrollIntoView({block:'start'});}
 $('connect-transfer-status').textContent='Dados carregados em '+connectNames[p.target]+'. Confira as configurações e calcule manualmente.';
};
$('connect-sample').click();

let copilotResponse=null,chatTopic=null,chatEpoch=0,chatBusy=false;
const copilotDeps={reports:LiliumReports,flow:LiliumFlow};
const copilotSources=()=>({insights:currentView,finance:financeReport,sales:salesView,operations:opsView,strategy:strategyReport,forecast:forecastReport,management:managementReport});
const copilotLabels={insights:'Insights',finance:'Finance',sales:'Sales',operations:'Operations',strategy:'Strategy',forecast:'Forecast'};
function cpReset(){chatEpoch++;copilotResponse=null;$('copilot-results').hidden=true;$('copilot-export').disabled=true;$('copilot-status').textContent='';$('copilot-forward-status').textContent='';}
function cpDefaults(){cpReset();$('copilot-rules').value=[LiliumFlow.HEADER,...LiliumCopilot.DEFAULT_RULES.map(r=>r.join(','))].join('\n');}
for(const [key,label] of Object.entries(LiliumCopilot.TOPICS)){const o=repNode('option',label);o.value=key;$('copilot-topic').append(o);}
$('copilot-topic').onchange=cpReset;$('copilot-rules').oninput=cpReset;$('copilot-defaults').onclick=cpDefaults;
function cpRender(report){
 const view=$('copilot-answer');view.replaceChildren();
 view.append(repNode('small','LILIUM COPILOT · CONSULTA GUIADA'),repNode('h3',report.question),repNode('p','Consulta em UTC: '+report.generated_at));
 if(!report.sections.length&&report.topic!=='actions')view.append(repNode('p','Nenhuma análise disponível para este tópico. Calcule o módulo correspondente primeiro.'));
 for(const s of report.sections){
 const block=document.createElement('article');block.append(repNode('h4',s.title),repNode('p',s.kind+' · '+s.scope));
 const dl=document.createElement('dl');for(const m of s.metrics){const div=document.createElement('div');div.append(repNode('dt',m.label),repNode('dd',m.value));dl.append(div);}block.append(dl);
 if(s.details.length){const ul=document.createElement('ul');for(const x of s.details)ul.append(repNode('li',x.label+': '+x.values.join(' | ')));block.append(ul);}
 for(const note of s.notes)block.append(repNode('p',note));view.append(block);
 }
 if(report.missing_sources.length)view.append(repNode('p','Fontes sem resultado: '+report.missing_sources.map(k=>copilotLabels[k]).join(', ')));
 if(report.unavailable_metrics.length)view.append(repNode('p','Indicadores indisponíveis para regras: '+report.unavailable_metrics.map(k=>LiliumFlow.METRICS[k].label).join(', ')));
 view.append(repNode('h4','Limitações'));for(const note of report.limitations)view.append(repNode('p',note));
 const target=$('copilot-suggestions');target.replaceChildren();
 if(!report.suggestions.length)target.append(repNode('p','Nenhuma condição atendida entre as regras avaliadas com dados disponíveis. Isso não demonstra ausência de problemas.'));
 report.suggestions.forEach((s,i)=>{
 const block=document.createElement('article');block.className='finance-block';block.append(repNode('h4',s.action),repNode('p',LiliumFlow.METRICS[s.metric].label+' '+flowOps[s.op]+' '+flowFormat(s.metric,s.threshold)),repNode('p','Evidência: '+flowFormat(s.metric,s.evidence.value)+' · '+s.evidence.kind+' · '+s.evidence.scope));
 const b=repNode('button','Encaminhar ao Flow');b.className='secondary';b.onclick=()=>{if(copilotResponse!==report||!confirm('Criar proposta pendente no Flow? Nenhuma ação será executada.'))return;try{const result=LiliumCopilot.forward(flowQueue,report,i,copilotSources(),copilotDeps,new Date().toISOString(),$('copilot-rules').value);flowQueue=result.queue;flowQueueRender();$('copilot-forward-status').textContent=result.added?'Proposta pendente criada no Flow.':result.skipped?'Proposta idêntica já existe.':'Fila do Flow cheia.';}catch(e){$('copilot-forward-status').textContent=e.message;}};
 block.append(b);target.append(block);
 });
 $('copilot-results').hidden=false;
}
$('copilot-run').onclick=()=>{cpReset();try{const report=LiliumCopilot.explain($('copilot-topic').value,copilotSources(),copilotDeps,new Date().toISOString(),$('copilot-rules').value);cpRender(report);copilotResponse=report;$('copilot-export').disabled=false;$('copilot-status').textContent=report.sections.length+' fontes exibidas; '+report.evaluated_rules+' regras avaliadas; '+report.suggestions.length+' sugestões.';}catch(e){$('copilot-status').textContent=e.message;}};
function appendChat(question,topic,mode){
 const box=$('copilot-chat'),turn=document.createElement('article');
 turn.append(repNode('h4',question),repNode('p',LiliumCopilot.TOPICS[topic]+' · '+mode+' · veja os indicadores e sugestões abaixo.'));
 box.append(turn);while(box.children.length>8)box.firstElementChild.remove();
}
$('copilot-ask').onclick=async()=>{
 if(chatBusy)return;
 const question=$('copilot-question').value.trim(),status=$('copilot-chat-status');
 let topic;
 try{topic=LiliumCopilot.routeQuestion(question,chatTopic);}catch(e){status.textContent=e.message;return;}
 cpReset();const epoch=chatEpoch,initialSources=copilotSources();
 chatBusy=true;$('copilot-ask').disabled=true;
 let mode='roteamento por regras';
 try{
  if($('copilot-consent').checked){
   status.textContent='Consultando modelo local para identificar o tópico...';
   try{
    const res=await localFetch('/api/v1/copilot/route',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question,model:$('copilot-model').value,consent:true})});
    if(res.ok){const data=await res.json();const routed=LiliumCopilot.routedTopic(data.topic);if(routed){topic=routed;mode='tópico escolhido pelo modelo local';}else mode='modelo indisponível; regras locais';}
    else mode='modelo indisponível; regras locais';
   }catch{mode='modelo indisponível; regras locais';}
  }
  if(epoch!==chatEpoch)return;
  const sources=copilotSources();
  if(Object.keys(sources).some(k=>sources[k]!==initialSources[k])){status.textContent='Os indicadores mudaram. Pergunte novamente.';return;}
  if(!topic){status.textContent='Não identifiquei um tópico único. Escolha uma pergunta guiada ou reformule.';return;}
  const report=LiliumCopilot.explain(topic,sources,copilotDeps,new Date().toISOString(),$('copilot-rules').value);
  $('copilot-topic').value=topic;cpRender(report);copilotResponse=report;$('copilot-export').disabled=false;
  chatTopic=topic;appendChat(question,topic,mode);
  status.textContent=mode+' · resposta determinística · '+report.sections.length+' fontes; '+report.suggestions.length+' sugestões.';
  $('copilot-question').value='';
 }catch(e){if(epoch===chatEpoch)status.textContent=e.message||'Não foi possível consultar os indicadores.';}
 finally{chatBusy=false;$('copilot-ask').disabled=false;$('copilot-consent').checked=false;}
};
$('copilot-clear-chat').onclick=()=>{cpReset();chatTopic=null;$('copilot-chat').replaceChildren();$('copilot-question').value='';$('copilot-consent').checked=false;$('copilot-chat-status').textContent='Conversa local limpa.';};
$('copilot-export').onclick=()=>{if(copilotResponse)stExport(copilotResponse,'lilium-copilot-response.json');};
cpDefaults();
$('pilot-reset').onclick=()=>{if(confirm("Descartar os dados e resultados em memória? O histórico salvo será mantido."))location.reload();};


let backupBusy=false;
async function backupAction(fn){
 if(backupBusy)return;
 backupBusy=true;$('backup-export').disabled=$('backup-merge').disabled=$('backup-file').disabled=true;
 $('backup-status').textContent='Processando...';
 try{await fn();}catch(e){$('backup-status').textContent=e.message||'Falha no backup.';}
 finally{backupBusy=false;$('backup-export').disabled=$('backup-merge').disabled=$('backup-file').disabled=false;}
}
$('backup-export').onclick=()=>backupAction(async()=>{
 const res=await localFetch('/api/v1/backup',{cache:'no-store'});
 if(!res.ok)throw Error(historyMessage(await res.json().catch(()=>null),'Não foi possível exportar o histórico.'));
 const raw=await res.text();repDownload(raw,'application/json','lilium-history.json');
 $('backup-status').textContent='Backup gerado. Guarde o arquivo em local seguro.';
});
$('backup-merge').onclick=()=>{
 const file=$('backup-file').files[0];
 if(!file||file.size>16*1024*1024){$('backup-status').textContent='Selecione um backup JSON de até 16 MiB.';return;}
 if(!confirm('Adicionar análises deste arquivo ao histórico? Registros atuais não serão substituídos.'))return;
 backupAction(async()=>{
 const res=await localFetch('/api/v1/backup/merge',{method:'POST',headers:{'Content-Type':'application/json'},body:file});
 const data=await res.json();
 if(!res.ok)throw Error(historyMessage(data,data.error?.code==='backup_invalid'?'Backup inválido, conflito ou limite atingido. Nenhuma análise importada.':'Não foi possível recuperar o backup.'));
 $('backup-file').value='';await refreshHistory();
 $('backup-status').textContent=data.added+' análises recuperadas; '+data.skipped+' cópias idênticas ignoradas.';
 });
};


function markWorkspaceLocation(hash){
 const links=Array.from($('module-nav').querySelectorAll('a[href^="#"]'));
 const active=hash||'#overview';
 for(const a of links){
  if(a.getAttribute('href')===active)a.setAttribute('aria-current','location');
  else a.removeAttribute('aria-current');
 }
}
markWorkspaceLocation(location.hash);
window.addEventListener('hashchange',()=>markWorkspaceLocation(location.hash));
document.addEventListener('click',event=>{
 if(event.defaultPrevented||event.button!==0||event.altKey||event.ctrlKey||event.metaKey||event.shiftKey)return;
 const a=event.target.closest?.('a[href^="#"]');
 if(!a)return;
 const target=document.getElementById(a.getAttribute('href').slice(1));
 if(!target||target.hidden)return;
 // Keep the browser's native history and anchor behavior; focus the destination.
 if(target.hasAttribute('tabindex'))requestAnimationFrame(()=>target.focus({preventScroll:true}));
});


const starterTargets=['insights','sales','finance','operations','goals','actions','forecast'];
for(const item of LiliumStarter.list()){const opt=repNode('option',item.name);opt.value=item.id;$('starter-scenario').append(opt);}
function starterSelection(){const scenario=LiliumStarter.build($('starter-scenario').value);$('starter-focus').textContent='Exercício: '+scenario.focus;$('starter-status').textContent='';return scenario;}
$('starter-scenario').onchange=starterSelection;$('starter-target').onchange=starterSelection;starterSelection();
$('starter-load').onclick=()=>{
 const x=starterSelection(),target=$('starter-target').value,selected=target==='all'?starterTargets:[target];
 if(!selected.every(k=>starterTargets.includes(k)))return;
 if(saving||backupBusy||$('run').disabled||$('sales-run').disabled||$('ops-run').disabled){$('starter-status').textContent='Aguarde as operações em andamento.';return;}
 if(!confirm('Carregar '+x.name+'? As entradas e resultados selecionados serão substituídos. Relatórios e respostas do Copilot serão limpos. Histórico e fila Flow permanecem.'))return;
 for(const k of selected){
  if(k==='insights'){selectedFile=null;$('file').value='';$('csv').disabled=false;$('csv').value=x.insights;reset();$('source').textContent='Fonte: Starter Kit · '+x.name;}
  if(k==='sales'){salesReset();$('sales-file').value='';$('sales-csv').value=x.sales;}
  if(k==='finance'){for(const [key,value] of Object.entries(x.finance))$('sim-'+key).value=value;$('finance-form').dispatchEvent(new Event('input',{bubbles:true}));}
  if(k==='operations'){opsReset();$('ops-file').value='';$('ops-csv').value=x.operations;}
  if(k==='goals'){stReset();$('strategy-csv').value=x.goals;$('strategy-date').value=x.asOf;}
  if(k==='actions'){actReset();$('strategy-actions').value=x.actions;}
  if(k==='forecast'){fcReset();$('forecast-csv').value=x.forecast;$('forecast-unit').value='BRL';$('forecast-horizon').value='3';$('forecast-model').value='auto';}
 }
 repReset();cpReset();$('flow-evaluation').replaceChildren();$('flow-status').textContent='Dados alterados. Reavalie as regras; propostas anteriores permanecem na fila.';
 $('starter-status').textContent='Cenário '+x.name+' carregado em '+selected.length+' conjunto(s). Execute os cálculos manualmente. Confira os períodos e não misture cenários sem revisar as fontes.';
};
$('starter-export').onclick=()=>{
 const x=starterSelection(),k=$('starter-target').value;
 if(k==='all'){stExport({schema_version:'1.0',kind:'lilium.synthetic-exercise',...x},'lilium-'+x.id+'-starter.json');}
 else if(k==='finance')stExport({schema_version:'1.0',kind:'lilium.synthetic-finance',scenario:x.id,inputs:x.finance,notes:x.notes},'lilium-'+x.id+'-finance.json');
 else if(starterTargets.includes(k))repDownload(x[k],'text/csv;charset=utf-8','lilium-'+x.id+'-'+k+'.csv');
 $('starter-status').textContent='Modelo fictício preparado para download.';
};


function helpNormalize(value){return String(value).normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase('pt-BR').trim();}
function helpMatches(text,query){const words=helpNormalize(query).split(/\s+/).filter(Boolean),haystack=helpNormalize(text);return words.every(word=>haystack.includes(word));}
function filterHelp(){
 const query=$('help-search').value;
 const topics=Array.from($('help-topics').querySelectorAll('.help-topic'));
 let count=0;
 for(const topic of topics){const match=helpMatches(topic.textContent,query);topic.hidden=!match;if(match)count++;}
 $('help-empty').hidden=count!==0;
 $('help-status').textContent=count+' de '+topics.length+' tópicos disponíveis.';
}
$('help-search').addEventListener('input',filterHelp);
$('help-clear').onclick=()=>{$('help-search').value='';filterHelp();$('help-search').focus();};
$('help-download').onclick=()=>repDownload($('help-feedback').value,'text/plain;charset=utf-8','lilium-relato-suporte.txt');
filterHelp();

$('workspace-loading').hidden=true;
