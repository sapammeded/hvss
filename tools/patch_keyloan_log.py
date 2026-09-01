from pathlib import Path

p = Path('hvss2.html')
s = p.read_text(encoding='utf-8')

if 'id="keylogPage"' in s:
    print('Key Loan Log already present; nothing to do.')
    raise SystemExit(0)

old_tab = '<button type="button" class="tab" data-page="key">Key Loan</button>'
new_tab = old_tab + '\n  <button type="button" class="tab" data-page="keylogPage">Key Loan Log</button>'
if old_tab not in s:
    raise SystemExit('TAB marker not found')
s = s.replace(old_tab, new_tab, 1)

marker = '<section class="page" id="history">'
if marker not in s:
    raise SystemExit('HISTORY marker not found')

section = r'''<section class="page" id="keylogPage">
 <div class="card">
  <div class="head"><div><h2>Key Loan Log</h2><div class="muted">Riwayat Key Loan dari CENTRAL / Google Spreadsheet</div></div><div class="actions no-print" style="margin:0"><button type="button" class="btn primary" id="keyLogLoad">Ambil Data CENTRAL</button><button type="button" class="btn dark" id="keyLogExcel">Export Excel</button><button type="button" class="btn success" id="keyLogPdf">Export PDF</button></div></div>
  <div class="notice">Pencarian mengambil data terbaru dari CENTRAL. Data lama tetap dapat dicari selama record masih ada di Spreadsheet, termasuk data bertahun-tahun lalu.</div>
  <div class="formgrid"><div class="field"><label>Dari Tanggal</label><input id="keyLogFrom" type="date"></div><div class="field"><label>Sampai Tanggal</label><input id="keyLogTo" type="date"></div><div class="field"><label>Nama Peminjam</label><input id="keyLogBorrower" placeholder="Semua peminjam"></div><div class="field"><label>Nama / Nomor Kunci</label><input id="keyLogKey" placeholder="Semua kunci"></div></div>
  <div class="actions"><button type="button" class="btn secondary" id="keyLogFilter">Terapkan Filter</button><button type="button" class="btn secondary" id="keyLogClear">Reset Filter</button></div>
  <div class="muted" id="keyLogStatus" style="margin-top:10px">Belum mengambil data CENTRAL.</div>
 </div>
 <div class="card"><div class="head"><h2>Riwayat Transaksi</h2><div class="muted" id="keyLogCount">0 transaksi</div></div><div class="tablewrap"><table class="table"><thead><tr><th>No</th><th>Date Out</th><th>Time Out</th><th>Peminjam</th><th>Divisi</th><th>Security OUT</th><th>Key</th><th>No. Kunci</th><th>Date In</th><th>Time In</th><th>Pengembali</th><th>Security IN</th><th>Status</th></tr></thead><tbody id="keyLogBody"><tr><td colspan="13" class="empty">Tekan “Ambil Data CENTRAL” untuk mengambil history.</td></tr></tbody></table></div></div>
 </div>
</section>

'''
s = s.replace(marker, section + marker, 1)

script = r'''<script id="HVSS_KEY_LOAN_LOG">
(function(){"use strict";
function e(v){return String(v==null?"":v).replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[m]))}
function d(v){return String(v==null?"":v).trim().slice(0,10)}
function n(v){return String(v==null?"":v).trim().toLowerCase()}
function all(){const x=window.HVSS_DB||{};return Array.isArray(x.keys)?x.keys.slice():[]}
function filtered(){const f=document.getElementById("keyLogFrom").value||"",t=document.getElementById("keyLogTo").value||"",b=n(document.getElementById("keyLogBorrower").value),k=n(document.getElementById("keyLogKey").value);return all().filter(x=>{const ds=[d(x.outDate),d(x.inDate)].filter(Boolean);return ds.some(z=>(!f||z>=f)&&(!t||z<=t))&&(!b||n(x.borrower).includes(b))&&(!k||(n(x.keyName).includes(k)||n(x.keyNumber).includes(k)))}).sort((a,b)=>(d(b.outDate)+String(b.outTime||"")).localeCompare(d(a.outDate)+String(a.outTime||"")))}
function render(){const r=filtered();document.getElementById("keyLogCount").textContent=r.length+" transaksi";document.getElementById("keyLogBody").innerHTML=r.length?r.map((x,i)=>`<tr><td>${i+1}</td><td>${e(x.outDate)}</td><td>${e(x.outTime)}</td><td>${e(x.borrower)}</td><td>${e(x.division)}</td><td>${e(x.security||x.outSecurity)}</td><td>${e(x.keyName)}</td><td>${e(x.keyNumber)}</td><td>${e(x.inDate)}</td><td>${e(x.inTime)}</td><td>${e(x.returner)}</td><td>${e(x.inSecurity||x.securityIn)}</td><td><span class="badge ${x.inDate?"in":"out"}">${x.inDate?"RETURNED":"KEY OUT"}</span></td></tr>`).join(""):'<tr><td colspan="13" class="empty">Tidak ada transaksi sesuai filter.</td></tr>';return r}
async function load(){const b=document.getElementById("keyLogLoad"),s=document.getElementById("keyLogStatus");b.disabled=true;s.textContent="Mengambil data terbaru dari CENTRAL...";try{if(!window.HVSS_CENTRAL_PULL)throw Error("CENTRAL belum siap");const r=await window.HVSS_CENTRAL_PULL();s.textContent="✓ CENTRAL LOADED • "+((r&&r.keys)||[]).length+" transaksi Key Loan tersedia.";render()}catch(x){s.textContent="✕ "+(x.message||x);alert("Key Loan Log gagal mengambil CENTRAL: "+(x.message||x))}finally{b.disabled=false}}
function rows(){return filtered().map((x,i)=>[i+1,x.outDate||"",x.outTime||"",x.borrower||"",x.division||"",x.security||x.outSecurity||"",x.keyName||"",x.keyNumber||"",x.inDate||"",x.inTime||"",x.returner||"",x.inSecurity||x.securityIn||"",x.inDate?"RETURNED":"KEY OUT"])}
function excel(){if(!window.XLSX)return alert("Excel engine belum siap. Refresh halaman.");const a=[["No","Date Out","Time Out","Peminjam","Divisi","Security OUT","Nama Kunci","Key Number","Date In","Time In","Pengembali","Security IN","Status"]].concat(rows()),w=XLSX.utils.aoa_to_sheet(a),b=XLSX.utils.book_new();XLSX.utils.book_append_sheet(b,w,"Key Loan Log");XLSX.writeFile(b,"HVSS_Key_Loan_Log.xlsx")}
function pdf(){const r=filtered();if(!r.length)return alert("Tidak ada data Key Loan sesuai filter.");if(!window.jspdf||!window.jspdf.jsPDF)return alert("PDF engine belum siap. Refresh halaman.");const x=new window.jspdf.jsPDF({orientation:"landscape",unit:"mm",format:"a4"});x.setFontSize(15);x.text("HVSS KEY LOAN LOG",14,15);x.setFontSize(8);x.text("Total: "+r.length,14,21);x.autoTable({startY:25,head:[["NO","DATE OUT","TIME OUT","PEMINJAM","DIVISI","SECURITY OUT","KEY","NO. KUNCI","DATE IN","TIME IN","PENGEMBALI","SECURITY IN","STATUS"]],body:rows(),theme:"grid",styles:{fontSize:7,cellPadding:2,overflow:"linebreak"},headStyles:{fontStyle:"bold",fontSize:7},margin:{left:10,right:10,bottom:15}});x.save("HVSS_Key_Loan_Log.pdf")}
function init(){document.getElementById("keyLogLoad").onclick=load;document.getElementById("keyLogFilter").onclick=render;document.getElementById("keyLogClear").onclick=()=>{["keyLogFrom","keyLogTo","keyLogBorrower","keyLogKey"].forEach(i=>document.getElementById(i).value="");render()};document.getElementById("keyLogExcel").onclick=excel;document.getElementById("keyLogPdf").onclick=pdf;["keyLogFrom","keyLogTo","keyLogBorrower","keyLogKey"].forEach(i=>document.getElementById(i).addEventListener("change",render));render()}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();
</script>
'''
s = s.replace('</body>', script + '</body>', 1)
p.write_text(s, encoding='utf-8')
print('Patched hvss2.html')
