'use strict';
const BANK = window.QUESTION_BANK || [];
const BY_ID = new Map(BANK.map(q => [q.id,q]));
const FULL = 30, LIMIT = 80, STORAGE = 'usmanov-informatika-v2', WHO = 'usmanov-informatika-who';
const LAN = !!window.LAN_MODE;
const NAMES = ['',
'Informatika fani. Axborot haqida tushuncha','Axborotning ko‘rinishlari, xususiyatlari va turlari','Axborotlar ustida bajariladigan amallar','Axborotlarni kodlash','Axborotlarning kompyuterda tasvirlanishi','Axborot miqdori, o‘lchash, birliklari va uzatish tezligi','Grafik axborotni ikki belgi yordamida kodlash','Hisoblash texnikasining rivojlanish tarixi','Kompyuter haqida umumiy ma’lumot','Asosiy plata','Protsessor','Tezkor xotira qurilmasi (TXQ)','Tovush, video va tarmoq platalari','Qattiq disk (ing. HDD)','Quvvat bloki','Monitor va klaviatura','Axborot tashuvchi vositalar','Printer va plotter','Sichqoncha, skaner, web-kamera','Kompyuterdan foydalanishda sanitariya-gigiyena talablari','Sanoq sistemalari haqida asosiy tushunchalar','Ikkilik sanoq sistemasi ustida amallar','Sakkizlik sanoq sistemasi ustida amallar','O‘n oltilik sanoq sistemasi ustida amallar','Ikkilik, sakkizlik va o‘n oltilik sanoq sistemalari orasidagi munosabatlar','Turli sanoq sistemalari va ular ustida amallar','Rim sanoq sistemalari ustida amallar','Mantiqiy amallar haqida tushuncha','Mantiqiy ko‘paytirish amali','Mantiqiy qo‘shish amali','Mantiqiy inkor amali','Aralash mantiqiy amallar','Yechimlar sonini aniqlash','Rostlik jadvali yordamida natijani aniqlash','Mantiqiy amallar va matematika','Mantiqiy amallar va informatika','Mantiqiy sxema','Kompyuterlarning dasturiy ta’minoti haqida umumiy tushuncha','Interfeys','Operatsion sistema tushunchasi','Operatsion sistemani tashkil etuvchi dasturlar va qobiq-dasturlar','Fayllar va kataloglar','Kompyuterning tashqi xotirasi bilan ishlash','Windows operatsion sistemasi haqida umumiy tushuncha','Windowsning ish stoli','Sichqoncha va u bilan ishlash','“Mening kompyuterim” sistema katalogi','Windows yo‘lboshlovchisi','Masalalar paneli','Windowsda oynalar bilan ishlash','Windows muhitida ishlash','Klaviatura bilan ishlash','Dasturiy ta’minot va mantiqiy amallar','MS Word interfeysi','Matn yozish va matnlarni tahrirlash','Matn qismidan nusxa olish va ko‘chirib o‘tkazish','Ma’lumotni xotirada saqlash va xotiradan chaqirish. WORD muharriridan chiqish','Asboblar paneli','Fayl va Pravka menyulari','Tahrirlash (Format) menyusi','Servis va Jadval menyulari','Word 2003 dasturida menyulardagi buyruqlarning joylashuvi','Elektron jadvalning vazifalari va imkoniyatlari','Excel interfeysi va ishchi kitob oynasi elementlari','Fayllar va ishchi kitoblar bilan ishlash. Ma’lumotlar kiritish va tahrir qilish','Formulalar hosil qilish va qo‘llash','Joriy ishchi jadvaldan tashqarida joylashgan kataklarga murojaat qilish','Formulalarga doir misollar','Adreslar va ularga doir misollar','Funksiyalar va ularning turlari','Matematik funksiyalar ustida amallar','Matn ko‘rinishidagi funksiyalar ustida amallar','Statistik funksiyalar ustida amallar','Mantiqiy kategoriyaga tegishli funksiyalar ustida amallar','Sana va vaqt kategoriyasiga tegishli funksiyalar ustida amallar','Elektron jadvallar ustida asosiy amallar','Diagrammalar yasash asoslari','Paint dasturi','Axborot texnologiyalari haqida tushuncha','Tarmoqlarning tasnifi va ularni qo‘llash xususiyatlari','Tarmoqning dasturiy ta’minoti','Internet va uning rivojlanish tarixi','Protokollar. IP adres va domenlar','Internetning asosiy xizmat turlari','WWW Xalqaro axborot tarmog‘i','Elektron pochta','Internetga ulanish','Internetga ulanish turlari','Veb-sahifalarni ko‘rish vositasi. Internet Explorer','Internetda axborot qidiruv tizimlari','Internetning afzalliklari va kamchiliklari','Internet tizimida turli vazifalarni bajaruvchi kichik dasturlar','HTML haqida tushuncha','Web-sahifaga matn kiritish','Shrift o‘lchami, rangi va web-sahifa foni','Web-sahifada grafika','Web-sahifaga ro‘yxat joylashtirish','Web-sahifaga jadval joylashtirish','Web-sahifada «o‘tish» (gipermurojaat)','Formalar','Interaktiv web-sahifalar','Kompyuter virusi va antivirus dasturlar','Arxivatorlar va fayllarni arxivlash','Model va uning turlari','Algoritm tushunchasi','Algoritmning asosiy xossalari','Algoritmni tasvirlash usullari','Algoritmning asosiy turlari','Dastur va dasturlash tillari','Dasturlash tillari tarixidan qisqacha ma’lumot','Turbo Paskal 7.0 integrallashgan muhiti','Paskal dasturlash tili alifbosi va tuzilishi','O‘zgarmas va o‘zgaruvchi miqdorlar','Jadval ko‘rinishidagi miqdorlar','Standart funksiyalar va protseduralar','Algebraik ifodalar','O‘zlashtirish va ma’lumotlarni ekranga chiqarish operatori','Ma’lumotlarni xotiraga muloqot usulida kiritish operatori','Matn holatida ekran bilan ishlash','O‘tish operatori','Tarmoqlanish operatori','Tarmoqlanish operatori va mantiqiy amallar','Tanlash operatori','Parametrli takrorlash operatori','Shart bo‘yicha takrorlash operatorlari','Belgi va satrli miqdorlar bilan ishlash','Paskalda ekranni grafik holatiga o‘tkazish','Paskalda shakllar chizish imkoniyatlari','Fayllar bilan ishlash. Protsedura va funksiyalar'
];
const CHAPTERS = [
 [1,8,'1-bob. Informatika. Axborot va EHM haqida boshlang‘ich tushuncha'],
 [9,20,'2-bob. Kompyuterning asosiy va qo‘shimcha qurilmalari'],
 [21,27,'3-bob. Sanoq sistemalari va ular ustida amallar'],
 [28,37,'4-bob. Mantiqiy amallar'],
 [38,43,'5-bob. Kompyuterning dasturiy ta’minoti'],
 [44,53,'6-bob. Windows XP operatsion sistemasi'],
 [54,62,'7-bob. Microsoft Office Word 2003'],
 [63,77,'8-bob. Microsoft Office Excel 2003'],
 [78,78,'9-bob. Paint dasturi'],
 [79,92,'10-bob. Axborot texnologiyalari'],
 [93,101,'11-bob. HTML'],
 [102,103,'12-bob. Viruslar, antivirus dasturlari va arxivatorlar'],
 [104,108,'13-bob. Model va algoritmlar'],
 [109,129,'14-bob. Turbo Paskal 7.0 dasturlash tili']
];
let state = null, topic = -1, filter = 'all', storageOK = true, timerHandle = null, progressHandle = null, starting = false;
const app = document.getElementById('app');
const esc = v => String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const groupName = q => NAMES[q.section] || (q.section + '-§');
const pool = n => n<0 ? BANK : BANK.filter(q=>q.section===n);
const size = () => state ? state.ids.length : FULL;
const askCount = () => { const n = pool(topic).length; return topic<0 ? Math.min(FULL, n) : Math.min(FULL, n); };
function shuffle(items) { const a=[...items]; for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];} return a; }
function save(){try{localStorage.setItem(STORAGE,JSON.stringify(state));}catch{storageOK=false;}}
function load(){try{const s=JSON.parse(localStorage.getItem(STORAGE));if(!s)return;
 const n=s.ids&&s.ids.length; if(!Array.isArray(s.ids)||n<1||n>FULL||new Set(s.ids).size!==n||s.ids.some(id=>!BY_ID.has(id)))return;
 if(!Array.isArray(s.answers)||s.answers.length!==n||s.answers.some((v,i)=>v!==null&&!BY_ID.get(s.ids[i]).options.includes(v)))return;
 if(!Number.isInteger(s.current)||s.current<0||s.current>=n||!Array.isArray(s.marked)||s.marked.length!==n||!s.marked.every(v=>typeof v==='boolean'))return;
 if(!Number.isFinite(s.started)||typeof s.done!=='boolean')return;
 if(LAN&&(typeof s.session!=='string'||(s.done&&!s.keys)))return;
 state=s;
 }catch{storageOK=false;}}
function who(){try{return JSON.parse(localStorage.getItem(WHO))||{};}catch{return {};}}
function saveWho(ism,sinf){try{localStorage.setItem(WHO,JSON.stringify({ism,sinf}));}catch{}}
function stopProgress(){clearInterval(progressHandle);progressHandle=null;}
function keyOf(id){if(state?.keys?.[id])return state.keys[id];const q=BY_ID.get(id);return q&&q.answer?q.answer:'';}
function count(){return state.answers.filter(a=>a!==null).length;}
function clock(s){s=Math.max(0,Math.floor(s));return `${String(Math.floor(s/60)).padStart(2,'0')}:${String(s%60).padStart(2,'0')}`;}
function elapsed(){return Math.max(0,Math.floor(((state.done?state.finished:Date.now())-state.started)/1000));}
function left(){return Math.max(0,LIMIT-elapsed());}
function timeText(){return clock(state?.done?Math.min(LIMIT,elapsed()):left());}
function tick(){const t=document.getElementById('timer');if(!t||!state||state.done)return;const remain=left();t.textContent=clock(remain);t.classList.toggle('urgent',remain>0&&remain<=10);if(remain<=0&&!holdTimer)timeUp();}
function topFocus(){window.scrollTo({top:0,behavior:'instant'});const h=app.querySelector('h2,h1');if(h){h.tabIndex=-1;h.focus({preventScroll:true});}}
function home(){clearInterval(timerHandle);stopProgress();const person=who();app.innerHTML=`
 <div class="home-heading"><div><span class="eyebrow">INFORMATIKA TEST MAYDONI</span><h2>Bilimingizni sinab ko‘ring.</h2></div><span class="quiet">1 daqiqa 20 soniya. 30 tagacha savol.</span></div>
 ${state&&!state.done?`<div class="resume"><div><strong>Tugallanmagan testingiz bor</strong><p>${count()} / ${size()} ta javob belgilangan. To‘xtagan joyingizdan davom eting.</p></div><button class="button primary" data-action="resume">Davom etish →</button></div>`:''}
 <div class="hero-grid"><section class="hero"><span class="eyebrow">KITOBDAN — AMALIYOTGA</span><h1>Informatikadan<br><span>30 ta savol.</span></h1><p>M. Usmanovning informatika testlari asosida mashq qiling. Javoblarni tanlang, natijani esa test oxirida bilib oling.</p><div class="hero-bottom"><div class="number-row"><div><strong>30</strong><small>tasodifiy savol</small></div><div><strong>${BANK.length.toLocaleString('en-US').replace(',',' ')}</strong><small>savollar bazasida</small></div><div><strong>129</strong><small>kitobdagi mavzu</small></div></div><div class="hero-symbol" aria-hidden="true">{ }</div></div></section>
 <section class="start-card"><span class="eyebrow">TAYYORMISIZ?</span><h2>Kichik qadam.<br>Aniq natija.</h2><ol class="steps"><li><span class="step-num">01</span>${askCount()} ta savol tanlanadi</li><li><span class="step-num">02</span>Har savolga bitta javob belgilang</li><li><span class="step-num">03</span>Vaqt 1:20 dan teskari sanaydi</li></ol>${LAN?`<div class="who-fields"><label>Ism familiya<input id="student-name" maxlength="80" autocomplete="name" value="${esc(person.ism||'')}" placeholder="Masalan, Ali Valiyev"></label><label>Sinf<input id="student-class" maxlength="20" autocomplete="off" value="${esc(person.sinf||'')}" placeholder="Masalan, 9-A"></label></div>`:''}<button class="button primary" data-action="start" ${askCount()<1?'disabled':''}>Testni boshlash <span>↗</span></button><p class="quiet">${askCount()<1?'Bu mavzuda savol ajratilmagan.':topic<0?'1 daqiqa 20 soniya · 30 tagacha savol':'1 daqiqa 20 soniya · '+askCount()+' ta savol'}</p></section></div>
 <section class="topics"><div class="section-title"><h3>Qaysi mavzuda mashq qilamiz?</h3><span class="quiet">Tanlangan: ${topic<0?'barcha mavzular':esc(topic+'-§. '+NAMES[topic])}</span></div><button class="topic ${topic<0?'active':''}" data-topic="-1" aria-pressed="${topic<0}">Barcha mavzular <span>${BANK.length}</span></button>${CHAPTERS.map(([a,b,name])=>`<h4 class="chapter">${esc(name)}</h4><div class="topic-list">${Array.from({length:b-a+1},(_,k)=>a+k).map(s=>`<button class="topic ${topic===s?'active':''}" data-topic="${s}" aria-pressed="${topic===s}" ${pool(s).length?'':'disabled'}>${s}-§. ${esc(NAMES[s])}<span>${pool(s).length}</span></button>`).join('')}</div>`).join('')}</section>
 <details class="source-note"><summary>Savollar manbasi va baholash haqida</summary><p>Manba: M. Usmanov, «Informatikadan mavzulashtirilgan testlar to‘plami», «Navro‘z», 2018. Yuklangan PDFdan ${BANK.length} ta savol ajratilgan. Savollar va variantlar asl sahifadan olingan rasmlarda ko‘rsatiladi. Har bir natijada PDF sahifasi, paragraf va kitobdagi savol raqami beriladi.</p><p>Bu kitobning to‘liq raqamli nusxasi emas: savol chegarasi, variantlari yoki javob kaliti avtomatik ajratishda noaniq chiqqan savollar bazaga kiritilmagan. Baholash kitobning javoblar kaliti bo‘yicha amalga oshiriladi; kitobdagi xatolar alohida ilmiy tahrirdan o‘tkazilmagan. Windows XP, Office 2003 va Turbo Paskal savollari aynan shu eski versiyalarga tegishli.</p><p>${LAN?'Ism va sinf test yakunida o‘qituvchi kompyuteriga yuboriladi. Javob kaliti o‘quvchi kompyuterida ochilmaydi; ballni o‘qituvchi kompyuteridagi dastur hisoblaydi. Tugallanmagan test shu brauzerda saqlanadi.':'Test holati faqat shu brauzerda saqlanadi. Natijalar umumiy o‘qituvchi bazasiga yuborilmaydi. Bu mustaqil mashq uchun mo‘ljallangan sayt.'}</p></details>
 ${state&&state.done?'<p><button class="button secondary" data-action="result">Oxirgi natijani ko‘rish →</button></p>':''}`;
}
async function start(){const n=askCount();if(starting||n<1)return;
 let ism='',sinf='';
 if(LAN){ism=(document.getElementById('student-name')?.value||'').trim();sinf=(document.getElementById('student-class')?.value||'').trim();
  if(ism.length<2){window.alert('Ism familiyangizni kiriting.');document.getElementById('student-name')?.focus();return;}
  saveWho(ism,sinf);}
 if(state&&!state.done&&!window.confirm(`Joriy tugallanmagan test o‘rniga yangi ${n} ta savol tanlansinmi?`))return;
 starting=true;
 try{let ids,session=null;
  if(LAN){const r=await fetch('/api/boshlash',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({ism,sinf,section:topic,mavzu:topic<0?'Barcha mavzular':topic+'-§. '+NAMES[topic]})});
   const data=await r.json().catch(()=>null);
   if(!r.ok||!data||!Array.isArray(data.ids)||data.ids.length<1||data.ids.length>FULL||new Set(data.ids).size!==data.ids.length||data.ids.some(id=>!BY_ID.has(id))||typeof data.session!=='string'){window.alert((data&&data.xato)||'Testni ochib bo‘lmadi. O‘qituvchi kompyuteridagi dastur ishlayotganini tekshiring.');return;}
   ids=data.ids;session=data.session;}
  else ids=shuffle(pool(topic)).slice(0,n).map(q=>q.id);
  state={ids,answers:Array(ids.length).fill(null),marked:Array(ids.length).fill(false),current:0,started:Date.now(),finished:null,done:false,topic,ism,sinf,session};save();quiz();topFocus();
 }catch{window.alert('O‘qituvchi kompyuteriga ulanib bo‘lmadi.');}
 finally{starting=false;}}
function scan(q,lazy=false){return `<div class="scan" data-question="${esc(q.id)}"><img src="${esc(q.image)}" width="${q.width}" height="${q.height}" ${lazy?'loading="lazy"':''} decoding="async" alt="${esc(groupName(q))}. Kitobdagi ${q.number}-savol va ${q.options.join(', ')} variantlari. PDF ${q.page}-sahifa."><div class="image-error" hidden role="status"><p>Rasm yuklanmadi. Qayta yuklab ko‘ring.</p><button class="button secondary" data-action="retry-image">↻ Qayta yuklash</button></div></div>`;}
function retryImage(img){
 const q=BY_ID.get(img.closest('.scan').dataset.question);if(!q)return;
 img.hidden=false;img.parentElement.querySelector('.image-error').hidden=true;
 const attempt=Number(img.dataset.attempt||0)+1;img.dataset.attempt=attempt;
 img.src=q.image.startsWith('data:')?q.image:q.image+'?v=2&retry='+attempt+'&t='+Date.now();
}
app.addEventListener('error',e=>{
 const img=e.target;if(img.tagName!=='IMG'||!img.closest('.scan'))return;
 if(Number(img.dataset.attempt||0)<2&&!img.src.startsWith('data:')){
  setTimeout(()=>{if(img.isConnected)retryImage(img);},700);return;
 }
 img.hidden=true;img.parentElement.querySelector('.image-error').hidden=false;
},true);
app.addEventListener('load',e=>{
 const img=e.target;if(img.tagName==='IMG'&&img.closest('.scan')){
 img.hidden=false;img.parentElement.querySelector('.image-error').hidden=true;
 }
},true);

function quiz(){if(!state||state.done)return home();const i=state.current,q=BY_ID.get(state.ids[i]);app.innerHTML=`
 <div class="quiz-heading"><div><span class="eyebrow">${esc(groupName(q))}</span><h2>Shoshilmang. O‘ylab javob bering.</h2></div><div><div class="timer ${left()<=10?'urgent':''}" id="timer">${timeText()}</div><span class="quiet" style="font-size:10px">qolgan vaqt</span></div></div>
 <div class="quiz-layout"><section class="question-card"><div class="question-top"><div class="question-count">${i+1}-savol <span>/ ${size()}</span></div><button class="flag ${state.marked[i]?'on':''}" data-action="flag" aria-pressed="${state.marked[i]}">${state.marked[i]?'★ Belgilangan':'☆ Keyin ko‘raman'}</button></div><p class="question-source">${q.section}-§ · Kitobdagi ${q.number}-savol · PDF ${q.page}-sahifa</p>${scan(q)}<div class="image-tools"><button class="button ghost" data-action="zoom">⊕ Rasmni kattalashtirish</button></div><fieldset><legend class="answer-prompt">Rasmdagi variantlardan birini tanlang:</legend><div class="answers" style="grid-template-columns:repeat(${q.options.length},1fr)">${q.options.map(a=>`<label class="answer"><input type="radio" name="answer" value="${a}" ${state.answers[i]===a?'checked':''}><span>${a}</span><span class="answer-text">variant</span></label>`).join('')}</div></fieldset><div style="min-height:34px"><button class="button ghost" data-action="clear" ${state.answers[i]===null?'disabled':''}>Tanlovni tozalash</button></div><div class="question-actions"><button class="button secondary" data-action="prev" ${i===0?'disabled':''}>← Oldingi</button>${i===size()-1?'<button class="button primary" data-action="finish">Testni yakunlash ↗</button>':'<button class="button primary" data-action="next">Keyingi →</button>'}</div></section>
 <aside class="navigator"><h3>Savollar xaritasi</h3><p class="quiet" id="answered" aria-live="polite">${count()} / ${size()} ta javob belgilangan</p><div class="progress"><div style="width:${count()/size()*100}%"></div></div><div class="nav-grid">${state.ids.map((id,n)=>`<button class="nav-num ${state.answers[n]!==null?'answered':''} ${i===n?'current':''} ${state.marked[n]?'marked':''}" data-goto="${n}" aria-label="${n+1}-savol${state.answers[n]!==null?', javob belgilangan':''}${state.marked[n]?', keyin ko‘rish uchun belgilangan':''}" ${i===n?'aria-current="step"':''}>${n+1}</button>`).join('')}</div><div class="legend"><span><i></i>Javob berilgan</span><span><i class="mark-dot"></i>Keyin ko‘rish</span></div><button class="button secondary" data-action="finish">Testni yakunlash</button><p class="auto-save">${storageOK?(LAN?'✓ Jarayon saqlanadi. Natija yakunda o‘qituvchiga yuboriladi.':'✓ Jarayon avtomatik saqlanadi'):'Saqlash imkoni yo‘q. Sahifani yopmang.'}</p></aside></div>`;
 clearInterval(timerHandle);stopProgress();
 if(left()<=0&&!holdTimer){timeUp();return;}
 timerHandle=setInterval(tick,1000);
 if(LAN&&state.session){reportProgress();progressHandle=setInterval(reportProgress,15000);}
}
function reportProgress(){if(!LAN||!state||state.done||!state.session)return;
 fetch('/api/jarayon',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({session:state.session,javob:count(),savol:state.current+1})}).catch(()=>{});}
async function submitResult(){const r=await fetch('/api/natija',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({session:state.session,javoblar:state.answers})});
 const data=await r.json().catch(()=>null);if(!r.ok||!data?.kalit)throw Error((data&&data.xato)||'yuborilmadi');return data;}
let timing=false,holdTimer=false;
async function timeUp(){if(!state||state.done||timing)return;timing=true;clearInterval(timerHandle);
 const close=()=>{state.done=true;state.finished=Date.now();save();filter='all';result();topFocus();timing=false;};
 if(!LAN){close();return;}
 app.innerHTML='<p class="loading">Vaqt tugadi. Natija yuborilmoqda…</p>';
 try{const data=await submitResult();state.keys=data.kalit;state.score={correct:data.togri,wrong:data.notogri,empty:data.javobsiz};close();}
 catch(err){timing=false;holdTimer=true;window.alert(err.message&&err.message!=='yuborilmadi'?err.message:'Natija yuborilmadi. Tugmani bosib yana yakunlang.');quiz();}}
function finish(){if(!state||state.done)return;const missing=size()-count(),marked=state.marked.filter(Boolean).length;document.getElementById('confirm-text').textContent=`${missing?`${missing} ta savol javobsiz qoldi. Javobsiz savollar uchun ball berilmaydi. `:`Barcha ${size()} ta savolga javob belgilangan. `}${marked?`${marked} ta savol keyin ko‘rish uchun belgilangan. `:''}Yakunlagach javoblarni o‘zgartirib bo‘lmaydi.`;document.getElementById('confirm').showModal();}
function stats(){if(state.score&&Number.isInteger(state.score.correct))return state.score;let correct=0,empty=0;state.ids.forEach((id,i)=>{if(state.answers[i]===null)empty++;else if(state.answers[i]===keyOf(id))correct++;});return {correct,empty,wrong:size()-correct-empty};}
function result(){if(!state?.done)return;clearInterval(timerHandle);stopProgress();const s=stats(),total=size(),pct=Math.round(s.correct/total*100);app.innerHTML=`
 <div class="home-heading"><div><span class="eyebrow">TEST YAKUNLANDI</span><h2>Natijangiz bilan tanishing.</h2></div><span class="quiet">${LAN?'Natija o‘qituvchi kompyuteriga yuborildi':'Kitobning javoblar kaliti bo‘yicha'}</span></div>
 <section class="result-hero"><div class="score">${pct}%<small>${s.correct} / ${total} ball</small></div><div><span class="eyebrow">${pct>=80?'YAXSHI NATIJA':pct>=50?'MASHQNI DAVOM ETTIRING':'HAR BIR MASHQ — YANGI BILIM'}</span><h1>${pct>=80?'Bilimingiz mustahkamlanmoqda.':'Keyingi urinish — yangi imkoniyat.'}</h1><p>Javoblaringizni tekshiring, so‘ng yana mashq qiling.</p></div></section>
 <div class="result-stats"><div class="stat"><strong>${s.correct}</strong><span>To‘g‘ri javob</span></div><div class="stat"><strong>${s.wrong}</strong><span>Noto‘g‘ri javob</span></div><div class="stat"><strong>${s.empty}</strong><span>Javobsiz savol</span></div><div class="stat"><strong>${timeText()}</strong><span>Sarflangan vaqt</span></div></div>
 <div class="result-toolbar"><div><h3 style="margin-bottom:10px">Javoblar tahlili</h3><div class="filters">${[['all','Barchasi'],['wrong','Xato va javobsiz'],['correct','To‘g‘ri']].map(([v,label])=>`<button class="topic ${filter===v?'active':''}" data-filter="${v}" aria-pressed="${filter===v}">${label}</button>`).join('')}</div></div><div style="display:flex;gap:9px"><button class="button secondary" data-action="home">Bosh sahifa</button><button class="button primary" data-action="restart">Yangi test ↗</button></div></div>
 <div id="reviews">${state.ids.map((id,i)=>{const q=BY_ID.get(id),a=state.answers[i],key=keyOf(id),ok=a!==null&&a===key;if(filter==='correct'&&!ok||filter==='wrong'&&ok)return '';return `<details class="review-card"><summary><span class="review-label"><strong>${i+1}-savol · ${esc(groupName(q))}</strong><small>${q.section}-§ · Kitobdagi ${q.number}-savol · PDF ${q.page}-sahifa</small></span><span class="status ${a===null?'empty':ok?'':'wrong'}">${a===null?'Javobsiz':ok?'To‘g‘ri':'Noto‘g‘ri'}</span></summary><div class="review-body">${scan(q,true)}<div class="review-answers"><span>Sizning javobingiz: <b class="${ok?'':'bad'}">${a||'Belgilanmagan'}</b></span><span>Kitob kaliti bo‘yicha: <strong>${key||'—'}</strong></span></div></div></details>`;}).join('')||'<p class="empty-message">Bu guruhda savollar yo‘q.</p>'}</div><p class="source-note">Har bir to‘g‘ri javob — 1 ball. Maksimal natija — ${total} ball. To‘g‘ri javoblar kitobning kalitidan olingan.${LAN&&state.ism?` ${esc(state.ism)}${state.sinf?' · '+esc(state.sinf):''} natijasi o‘qituvchi kompyuterida saqlanadi.`:''}</p>`;}
app.addEventListener('click',e=>{const b=e.target.closest('button');if(!b||b.disabled)return;
 if(b.dataset.topic!==undefined){topic=Number(b.dataset.topic);home();return;}
 if(b.dataset.goto!==undefined){state.current=Number(b.dataset.goto);save();quiz();topFocus();return;}
 if(b.dataset.filter){filter=b.dataset.filter;result();return;}
 switch(b.dataset.action){case 'retry-image':retryImage(b.closest('.scan').querySelector('img'));break;case 'start':start();break;case 'resume':quiz();topFocus();break;case 'home':home();topFocus();break;case 'result':filter='all';result();topFocus();break;case 'restart':topic=Number.isInteger(state.topic)?state.topic:-1;start();break;case 'prev':case 'next':state.current+=b.dataset.action==='next'?1:-1;save();quiz();topFocus();break;case 'clear':state.answers[state.current]=null;save();quiz();break;case 'flag':state.marked[state.current]=!state.marked[state.current];save();quiz();break;case 'finish':finish();break;case 'zoom':{const scan=app.querySelector('.scan');scan.classList.toggle('zoom');b.textContent=scan.classList.contains('zoom')?'⊖ Asl o‘lchamga qaytarish':'⊕ Rasmni kattalashtirish';break;}}
});
app.addEventListener('change',e=>{if(e.target.name==='answer'&&state&&!state.done){state.answers[state.current]=e.target.value;save();const focus=e.target.value;quiz();app.querySelector(`input[value="${focus}"]`).focus({preventScroll:true});}});
document.getElementById('confirm').addEventListener('close',async e=>{if(e.target.returnValue!=='finish'||!state||state.done)return;
 if(!LAN){state.done=true;state.finished=Date.now();save();filter='all';result();topFocus();return;}
 app.innerHTML='<p class="loading">Natija o‘qituvchi kompyuteriga yuborilmoqda…</p>';
 try{const data=await submitResult();state.done=true;state.finished=Date.now();state.keys=data.kalit;state.score={correct:data.togri,wrong:data.notogri,empty:data.javobsiz};save();filter='all';result();topFocus();}
 catch(err){window.alert(err.message&&err.message!=='yuborilmadi'?err.message:'Natija yuborilmadi. Tarmoqni tekshirib, yana yakunlang.');quiz();}});
load();
if(LAN){const pill=document.querySelector('.header-pill');if(pill)pill.innerHTML='<i></i> Lokal tarmoq';}
if(BANK.length<FULL)app.innerHTML='<p class="empty-message">Savollar bazasi yuklanmadi. bank.js fayli index.html bilan bir papkada ekanini tekshiring.</p>';
else home();
document.querySelector('.brand')?.addEventListener('click',e=>{if(location.protocol==='file:'||location.pathname.endsWith('index.html')||location.pathname==='/'||location.pathname===''){e.preventDefault();home();topFocus();}});
// Optional agent access uses the same answers and navigation as the interface.
if(document.modelContext?.registerTool){
 const tools=[{
  name:'get_test_progress',description:'Read the current test progress. Correct answers are returned only after the test is finished.',inputSchema:{type:'object',properties:{},additionalProperties:false},annotations:{readOnlyHint:true},
  execute(){return state?{finished:state.done,question:state.current+1,answered:count(),total:size(),...(state.done?{score:stats()}: {})}:{started:false,total:FULL};}
 },{
  name:'select_test_answers',description:'Select or clear answers in the active test and display the last updated question. Does not finish the test.',inputSchema:{type:'object',properties:{answers:{type:'array',minItems:1,maxItems:30,items:{type:'object',properties:{question:{type:'integer',minimum:1,maximum:30},answer:{type:['string','null'],enum:['A','B','C','D','E',null]}},required:['question','answer'],additionalProperties:false}}},required:['answers'],additionalProperties:false},annotations:{readOnlyHint:false},
  execute(input){if(!state||state.done)throw Error('No active test');if(!input||!Array.isArray(input.answers)||!input.answers.length||input.answers.length>30)throw Error('Invalid answers');
   for(const a of input.answers){if(!a||!Number.isInteger(a.question)||a.question<1||a.question>size()||(a.answer!==null&&!BY_ID.get(state.ids[a.question-1]).options.includes(a.answer)))throw Error('Invalid answer');}
   for(const a of input.answers)state.answers[a.question-1]=a.answer;
   state.current=input.answers[input.answers.length-1].question-1;save();quiz();return {answered:count(),total:size(),question:state.current+1};}
 }];
 for(const tool of tools){try{Promise.resolve(document.modelContext.registerTool(tool)).catch(()=>{});}catch{}}
}
