import { STORAGE_KEY, INITIAL_STATE, readState, moveNote, replyTo } from './model.mjs';

const $ = (selector, root = document) => root.querySelector(selector);
const desktop = $('#desktop');
const workspace = $('#workspace');
const windows = new Map();
let depth = 20;
let activeWindow = null;
let state = { ...INITIAL_STATE, notes: [], trash: [] };
let storageBlocked = false;
let storageMessage = '';
let mode = 'idle';
let preview = false;
let busy = false;
let turn = 0;
let timers = [];
let toastTimer;
let localVoices = [];
let conversation = [{ who: 'Mack', text: 'A familiar desktop. A new little personality. What shall we try first?' }];
try { state = readState(localStorage.getItem(STORAGE_KEY)); }
catch (error) { storageBlocked = true; storageMessage = 'Saved notes could not be opened. The original data has been left untouched; this session will not overwrite it.'; }

function node(tag, className, text) {
  const item = document.createElement(tag);
  if (className) item.className = className;
  if (text !== undefined) item.textContent = text;
  return item;
}
function button(text, action, className = 'classic-button') {
  const item = node('button', className, text);
  item.type = 'button'; item.addEventListener('click', action); return item;
}
function toast(text) {
  const item = $('#toast'); item.textContent = text; item.hidden = false;
  clearTimeout(toastTimer); toastTimer = setTimeout(() => { item.hidden = true; }, 5500);
}
function persist(next) {
  if (storageBlocked) { toast(storageMessage); return false; }
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(next)); state = next; return true; }
  catch { toast('This browser could not save the change. Your existing notes have been kept.'); return false; }
}
function icon(name) {
  const art = node('span', 'icon-art'); art.setAttribute('aria-hidden', 'true');
  const drawings = {
    disk: '<path fill="#eee" d="M7 8h30v28H7z"/><path fill="#b5b5b5" d="M7 29h30v7H7z"/><path fill="white" d="M10 11h24v15H10z"/><path d="M14 14h16v9H14zM11 32h16M31 32h2"/>',
    memory: '<path fill="#e5dca0" d="M5 13h15l3-5h10l5 7v24H5z"/><path fill="#fff6bc" d="M5 16h33v23H5z"/><path d="M12 23h18M12 28h15M12 33h11"/>',
    controls: '<path fill="#eee" d="M5 8h34v30H5z"/><path fill="#c8c8c8" d="M5 8h34v6H5z"/><path d="M11 20h22M11 28h22"/><path fill="white" d="M17 17h5v6h-5zM26 25h5v6h-5z"/>',
    trash: '<path fill="#e6e6e6" d="M12 12h22l-2 27H14z"/><path fill="#bbb" d="M10 9h26v5H10zM18 5h10v4H18z"/><path d="M18 18v16M23 18v16M28 18v16"/>',
    readme: '<path fill="#fffff2" d="M10 4h19l8 8v28H10z"/><path fill="#bbb" d="M29 4v9h8"/><path d="M16 20h15M16 25h15M16 30h12"/>',
    mack: '<path fill="#eee" d="M9 3h27v31H9zM7 35h31v6H7z"/><path fill="#c3d4e0" d="M13 7h19v17H13z"/><path d="M17 12v3M27 12v3M21 12v7h3M17 20l3 2h5l3-2M25 29h7"/>',
    note: '<path fill="#fff6ae" d="M7 5h31v27l-8 8H7z"/><path fill="#d5c979" d="M30 32h8l-8 8z"/><path d="M13 14h19M13 20h19M13 26h13"/>'
  };
  art.innerHTML = '<svg viewBox="0 0 44 44" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="#292b32" stroke-width="1.4" stroke-linejoin="miter">' + (drawings[name] || drawings.mack) + '</svg>';
  return art;
}
function face() {
  const item = node('div', 'mack-face'); item.setAttribute('aria-hidden', 'true');
  item.innerHTML = '<svg viewBox="0 0 72 82" xmlns="http://www.w3.org/2000/svg"><path fill="#ecece5" stroke="currentColor" stroke-width="2" d="M11 3h50v62H11zM8 69h56v9H8z"/><path fill="#dbe5e9" stroke="currentColor" stroke-width="2" d="M16 9h40v40H16z"/><g class="face-eyes" fill="currentColor"><path d="M24 22h3v7h-3zM45 22h3v7h-3z"/></g><path fill="none" stroke="currentColor" stroke-width="2" d="M35 22v13h5"/><path class="face-mouth-rest" fill="none" stroke="currentColor" stroke-width="2" d="M25 38v3h5v2h13v-2h5v-3"/><path class="face-mouth-speaking" fill="currentColor" d="M27 38h19v7H27z"/><path fill="currentColor" d="M37 56h15v2H37zM17 55h3v3h-3zM16 72h40v2H16z"/></svg>';
  return item;
}
function desktopIcon(label, image, action) {
  const item = button('', action, 'desktop-icon'); item.append(icon(image), node('span','icon-label',label)); return item;
}
function clamp(value, min, max) { return Math.max(min, Math.min(value, Math.max(min,max))); }
function fit(win) {
  const box = workspace.getBoundingClientRect();
  win.style.left = clamp(parseFloat(win.style.left) || 0, 6, box.width-win.offsetWidth-6) + 'px';
  win.style.top = clamp(parseFloat(win.style.top) || 0, 6, box.height-win.offsetHeight-6) + 'px';
}
function focusWindow(win) {
  windows.forEach((w) => w.classList.toggle('active', w===win));
  win.style.zIndex = ++depth; activeWindow = win;
}
function closeWindow(id) {
  const win = windows.get(id); if (!win) return;
  win.remove(); windows.delete(id);
  if (activeWindow===win) {
    activeWindow = [...windows.values()].sort((a,b) => Number(b.style.zIndex)-Number(a.style.zIndex))[0] || null;
    if (activeWindow) focusWindow(activeWindow);
  }
}
function zoomWindow(win) {
  if (win.dataset.zoomed === 'true') {
    const old = JSON.parse(win.dataset.previous); Object.assign(win.style,old); win.dataset.zoomed='false';
  } else {
    win.dataset.previous=JSON.stringify({left:win.style.left,top:win.style.top,width:win.style.width,height:win.style.height});
    Object.assign(win.style,{left:'6px',top:'6px',width:(workspace.clientWidth-12)+'px',height:(workspace.clientHeight-12)+'px'}); win.dataset.zoomed='true';
  }
  win.classList.remove('collapsed'); fit(win);
}
function makeWindow(id, title, width, contents, options={}) {
  if (windows.has(id)) { const existing=windows.get(id); existing.classList.remove('collapsed'); focusWindow(existing); fit(existing); return existing; }
  const win=node('section','window'); win.dataset.window=id; win.setAttribute('role','region'); win.setAttribute('aria-label',title);
  win.style.width=width+'px';
  win.style.left=(options.x ?? Math.max(15,(workspace.clientWidth-Math.min(width,workspace.clientWidth-24))/2-45+windows.size*18))+'px';
  win.style.top=(options.y ?? Math.max(16,Math.min(100,workspace.clientHeight*.15)+windows.size*20))+'px';
  const bar=node('header','title-bar');
  const close=button('',()=>closeWindow(id),'window-control close'); close.setAttribute('aria-label','Close '+title);
  const collapse=button('',()=>{win.classList.toggle('collapsed');fit(win);},'window-control collapse'); collapse.setAttribute('aria-label','Collapse '+title);
  const zoom=button('',()=>zoomWindow(win),'window-control zoom'); zoom.setAttribute('aria-label','Zoom '+title);
  bar.append(close,node('span','title-lines'),node('h2','',title),node('span','title-lines'),zoom,collapse);
  const body=node('div','window-content'); body.append(contents);
  const foot=node('footer','window-foot');
  const resize=button('',()=>{},'resize-glyph'); resize.setAttribute('aria-label','Resize '+title); resize.title='Drag to resize; arrow keys also work';
  resize.style.cssText='border:0;padding:0;cursor:nwse-resize;touch-action:none';
  foot.append(node('span','',options.foot || ''),resize);
  win.append(bar,body,foot); $('#windows').append(win); windows.set(id,win); focusWindow(win); fit(win);
  win.addEventListener('pointerdown',()=>focusWindow(win));
  win.addEventListener('focusin',()=>{if(activeWindow!==win)focusWindow(win);});
  bar.addEventListener('dblclick',(event)=>{if(!event.target.closest('button'))zoomWindow(win);});
  let drag=null;
  bar.addEventListener('pointerdown',(event)=>{
    if(event.target.closest('button')||event.button!==0)return;
    drag={x:event.clientX,y:event.clientY,left:win.offsetLeft,top:win.offsetTop};
    bar.setPointerCapture(event.pointerId); event.preventDefault();
  });
  bar.addEventListener('pointermove',(event)=>{
    if(!drag)return;
    win.style.left=clamp(drag.left+event.clientX-drag.x,6,workspace.clientWidth-win.offsetWidth-6)+'px';
    win.style.top=clamp(drag.top+event.clientY-drag.y,6,workspace.clientHeight-28)+'px';
  });
  bar.addEventListener('lostpointercapture',()=>{drag=null;});
  bar.addEventListener('pointerup',()=>{drag=null;fit(win);});
  let size=null;
  const setSize=(width,height)=>{
    win.style.width=clamp(width,Math.min(300,workspace.clientWidth-24),workspace.clientWidth-win.offsetLeft-6)+'px';
    win.style.height=clamp(height,100,workspace.clientHeight-win.offsetTop-6)+'px';
  };
  resize.addEventListener('pointerdown',(event)=>{size={x:event.clientX,y:event.clientY,w:win.offsetWidth,h:win.offsetHeight};resize.setPointerCapture(event.pointerId);event.preventDefault();});
  resize.addEventListener('pointermove',(event)=>{if(size)setSize(size.w+event.clientX-size.x,size.h+event.clientY-size.y);});
  resize.addEventListener('lostpointercapture',()=>{size=null;});
  resize.addEventListener('pointerup',()=>{size=null;});
  resize.addEventListener('keydown',(event)=>{const delta={ArrowLeft:[-10,0],ArrowRight:[10,0],ArrowUp:[0,-10],ArrowDown:[0,10]}[event.key];if(delta){event.preventDefault();setSize(win.offsetWidth+delta[0],win.offsetHeight+delta[1]);}});
  return win;
}

const stateText={idle:'Mack is ready',listening:'Listening',thinking:'Thinking',speaking:'Speaking',resting:'Resting',fault:'Connection unavailable'};
function setMode(next, isPreview=false) {
  mode=next; preview=isPreview; desktop.dataset.state=mode;
  $('#status-label').textContent=stateText[mode]+(preview?' · preview':'');
  const line=$('#mack-state');
  if(line)line.textContent=preview?'Expression preview — '+stateText[mode].toLowerCase()+'. No microphone or AI is connected.':(mode==='thinking'?'Choosing a local demo reply…':mode==='speaking'?'Reading the reply aloud.':mode==='resting'?'Taking a little desktop nap. Send a message to wake me.':'Local conversation preview · no AI service connected');
  const fault=$('#fault-banner'); if(fault)fault.hidden=mode!=='fault';
  const input=$('#message-input'); if(input)input.disabled=busy;
  const send=$('#send-message'); if(send)send.disabled=busy;
  document.querySelectorAll('[data-preview-state]').forEach((b)=>b.setAttribute('aria-pressed',String(preview && b.dataset.previewState===mode)));
}
function stopCurrent() {
  turn++; timers.forEach(clearTimeout); timers=[]; busy=false;
  if('speechSynthesis' in window)window.speechSynthesis.cancel();
}
function previewState(next) { stopCurrent(); openMack(); setMode(next,true); }
function renderConversation() {
  const log=$('#conversation'); if(!log)return; log.replaceChildren();
  conversation.forEach(({who,text})=>{
    const row=node('div','message '+(who==='You'?'user':'assistant'));
    row.append(node('span','speaker',who),node('p','',text)); log.append(row);
  });
  log.scrollTop=log.scrollHeight;
}
function refreshVoices() { localVoices=('speechSynthesis' in window)?window.speechSynthesis.getVoices().filter((voice)=>voice.localService):[]; }
if('speechSynthesis' in window){ refreshVoices();window.speechSynthesis.addEventListener('voiceschanged',refreshVoices); }
function speak(text, token) {
  refreshVoices();
  if(!state.voice || !localVoices.length) { setMode('idle'); if(state.voice)toast('No local browser voice is available. You can keep chatting by typing.'); return; }
  const speech=new SpeechSynthesisUtterance(text.slice(0,2500));
  speech.voice=localVoices.find((v)=>v.lang.startsWith('en')&&/Samantha|Daniel|Alex/.test(v.name)) || localVoices.find((v)=>v.lang.startsWith('en')) || localVoices[0];
  speech.rate=.94;
  speech.onstart=()=>{if(token===turn)setMode('speaking');};
  speech.onend=()=>{if(token===turn)setMode('idle');};
  speech.onerror=()=>{if(token===turn){setMode('idle');toast('Voice playback was unavailable. The reply is here to read.');}};
  window.speechSynthesis.speak(speech);
  timers.push(setTimeout(()=>{if(token===turn&&mode==='speaking'){window.speechSynthesis.cancel();setMode('idle');}},30000));
}
function sendMessage(value) {
  const text=value.trim().slice(0,2000); if(!text||busy)return;
  stopCurrent(); const token=turn; busy=true;
  conversation.push({who:'You',text}); if(conversation.length>80)conversation=conversation.slice(-80);
  openMack(); $('#message-input').value=''; renderConversation(); setMode('thinking');
  timers.push(setTimeout(()=>{
    if(token!==turn)return;
    const result=replyTo(text,state.notes);
    if(result.note){
      if(state.notes.length>=100)result.text='My notebook has 100 notes. Move an old note to Trash before saving another.';
      else if(persist({...state,notes:[{id:crypto.randomUUID(),text:result.note,created:new Date().toISOString()},...state.notes]}))refreshNotes();
      else result.text='I could not save that note in this browser. Your existing notes have not changed.';
    }
    conversation.push({who:'Mack',text:result.text});busy=false;renderConversation();setMode('idle');speak(result.text,token);
    $('#message-input')?.focus();
  },650));
}
function openMack() {
  if(windows.has('mack')){const win=windows.get('mack');win.classList.remove('collapsed');focusWindow(win);return;}
  const content=node('div','mack-content');
  const welcome=node('div','welcome'); const greeting=node('div'); greeting.append(node('h1','','Hello, Bill.'),node('p','','I’m Mack. A small computer with a little more on its mind.'));
  welcome.append(face(),greeting);
  const log=node('div','conversation');log.id='conversation';log.setAttribute('role','log');log.setAttribute('aria-live','polite');log.setAttribute('aria-label','Conversation with Mack');
  const line=node('div','state-line');line.append(node('span','status-dot'));const lineText=node('span');lineText.id='mack-state';line.append(lineText);
  const suggestions=node('div','suggestions');
  [['Say hello','Hello, Mack'],['What can you do?','What can you do?'],['Remember a note',null]].forEach(([label,prompt])=>suggestions.append(button(label,()=>prompt?sendMessage(prompt):openNewNote(),'suggestion')));
  const fault=node('div','fault-banner');fault.id='fault-banner';fault.hidden=true;fault.append(node('p','','This is the disconnected expression. The demo remains available; no AI connection has been attempted.'),button('Return to desktop',()=>{stopCurrent();setMode('idle');},'classic-button small'));
  const form=node('form','composer');form.setAttribute('aria-label','Talk to Mack');
  const input=node('input');input.id='message-input';input.type='text';input.maxLength=2000;input.placeholder='Say something to Mack…';input.autocomplete='off';input.setAttribute('aria-label','Message to Mack');
  const send=node('button','classic-button primary','Send');send.id='send-message';send.type='submit';
  form.append(input,send);form.addEventListener('submit',(event)=>{event.preventDefault();sendMessage(input.value);});
  content.append(welcome,log,line,suggestions,fault,form);
  makeWindow('mack','Mack',560,content,{foot:'M.A.C. Model 04 · Desktop Preview 0.1'});renderConversation();setMode(mode,preview);
}
function openAbout() {
  const content=node('div','panel');const hero=node('div','about-header');const words=node('div');words.append(node('h3','','M.A.C. Model 04'),node('p','','Mobile Autonomous Computer'));hero.append(face(),words);
  const table=node('table','spec-table');
  [['Known as','Mack'],['System','Mack Desktop Preview 0.1'],['Personality','Classic Macintosh. Curious companion.'],['Conversation','Local, scripted responses'],['Memories','Saved in this browser on this Mac'],['Body','Four legs planned · hardware disconnected']].forEach(([key,value])=>{const row=node('tr');row.append(node('th','',key),node('td','',value));table.append(row);});
  content.append(hero,table,node('p','','A little Mac brought to life. This is the first working shell for the RayCue conversion, inspired by the Platinum desktop.'),node('p','fine-print','Original interface and icons. This preview does not run Mac OS 9 or vintage applications.'));
  makeWindow('about','About This Computer',440,content);
}
function openDisk() {
  const content=node('div');const meta=node('div','finder-meta');meta.append(node('span','','5 items'),node('span','','Mackintosh HD'));
  const items=node('div','finder-items');
  [['Mack','mack',openMack],['Memories','memory',openMemories],['Control Panels','controls',openControls],['Read Me','readme',openHelp],['About Mack','mack',openAbout]].forEach(([label,image,action])=>items.append(desktopIcon(label,image,action)));
  content.append(meta,items);makeWindow('disk','Mackintosh HD',460,content);
}
function addNote(text) {
  if(!text.trim()){toast('Write a note first.');return false;}
  if(state.notes.length>=100){toast('Your notebook has 100 notes. Move one to Trash to make room.');return false;}
  const saved=persist({...state,notes:[{id:crypto.randomUUID(),text:text.trim().slice(0,2000),created:new Date().toISOString()},...state.notes]});
  if(saved){refreshNotes();toast('Saved in Memories on this browser.');}return saved;
}
function openNewNote() {
  const content=node('form','note-editor'); const area=node('textarea');area.maxLength=2000;area.placeholder='Something worth remembering…';area.setAttribute('aria-label','New memory');
  const actions=node('div','panel-actions');const save=node('button','classic-button primary','Save note');save.type='submit';actions.append(button('Cancel',()=>closeWindow('new-note')),save);
  content.append(area,node('p','fine-print','Stored only in this browser. Nothing is sent to an AI service.'),actions);
  content.addEventListener('submit',(event)=>{event.preventDefault();if(addNote(area.value)){closeWindow('new-note');openMemories();}});
  makeWindow('new-note','New Note',350,content);$('textarea',windows.get('new-note')).focus();
}
function noteList(destination) {
  const panel=node('div','notes-list');panel.dataset.notesList=destination;
  if(storageBlocked){panel.append(node('p','empty-state',storageMessage));return panel;}
  const count=state[destination].length;
  const toolbar=node('div','notes-toolbar');toolbar.append(node('span','',count+(destination==='notes'?' saved note':' note')+(count===1?'':'s')+(destination==='trash'?' in Trash':'')));
  if(destination==='notes')toolbar.append(button('New note',openNewNote,'classic-button small'));
  panel.append(toolbar);const list=node('div','trash-list');
  if(!state[destination].length)list.append(node('p','empty-state',destination==='notes'?'An empty notebook. A good place to begin.':'The Trash is empty. Removed notes appear here until you restore them.'));
  state[destination].forEach((note)=>{
    const row=node('div','note-row');row.append(node('p','',note.text),button(destination==='notes'?'Move to Trash':'Restore',()=>{
      const target=destination==='notes'?'trash':'notes';const next=moveNote(state,note.id,target);
      if(next===state){toast('That destination is full. Your note has not moved.');return;}
      if(persist(next)){refreshNotes();toast(destination==='notes'?'Moved to Trash. You can restore it there.':'Restored to Memories.');}
    },'classic-button small'));list.append(row);
  });panel.append(list,node('div','window-note','Notes stay in this browser. Refreshing keeps them; clearing site data removes them.'));return panel;
}
function refreshNotes() { document.querySelectorAll('[data-notes-list]').forEach((list)=>list.replaceWith(noteList(list.dataset.notesList))); }
function openMemories(){makeWindow('memories','Memories',420,noteList('notes'));}
function openTrash(){makeWindow('trash','Trash',410,noteList('trash'));}
function toggleVoice() {
  refreshVoices();
  if(!state.voice&&!localVoices.length){toast('This browser has no local voice available. Try Mack in Safari or Chrome, or keep voice off.');return;}
  if(persist({...state,voice:!state.voice})){
    if(!state.voice){if(mode==='speaking')stopCurrent();window.speechSynthesis?.cancel();if(mode==='speaking')setMode('idle');}
    updateVoiceControls();
  }
}
function updateVoiceControls(){
  const control=$('#sound-control');control.textContent=state.voice?'Voice on':'Voice off';control.setAttribute('aria-pressed',String(state.voice));control.setAttribute('aria-label',state.voice?'Turn off Mack’s voice':'Turn on Mack’s voice');
  const check=$('#voice-check');if(check)check.checked=state.voice;
}
function openControls() {
  const panel=node('div','panel');panel.append(node('h3','','Desktop appearance'));
  const swatches=node('div','swatches');
  [['periwinkle','#929bbb'],['sage','#8b9d92'],['graphite','#7e8594'],['classic','#979797']].forEach(([name,color])=>{
    const swatch=button('',()=>{if(persist({...state,pattern:name})){desktop.dataset.pattern=name;swatches.querySelectorAll('button').forEach((b)=>b.setAttribute('aria-pressed',String(b===swatch)));}},'swatch');swatch.style.background=color;swatch.title=name;swatch.setAttribute('aria-label',name+' desktop');swatch.setAttribute('aria-pressed',String(state.pattern===name));swatches.append(swatch);
  });panel.append(swatches,node('hr'),node('h3','','Mack’s voice'));
  const label=node('label');const check=node('input');check.type='checkbox';check.id='voice-check';check.checked=state.voice;check.addEventListener('change',()=>{toggleVoice();updateVoiceControls();});label.append(check,document.createTextNode('Read Mack’s replies aloud'));
  panel.append(label,node('p','fine-print','Uses a local voice supplied by your browser when available. Off by default. There is no microphone capture.'),node('hr'),node('h3','','Try Mack’s expressions'),node('p','','These buttons preview screen states. They do not start a microphone, AI service, or robot.'));
  const states=node('div','state-buttons');
  [['idle','Ready'],['listening','Listening'],['thinking','Thinking'],['speaking','Speaking'],['resting','Resting'],['fault','Disconnected']].forEach(([name,label])=>{const b=button(label,()=>previewState(name),'classic-button small');b.dataset.previewState=name;b.setAttribute('aria-pressed','false');states.append(b);});
  panel.append(states);const actions=node('div','panel-actions');actions.append(button('Reset expression',()=>{stopCurrent();setMode('idle');}));panel.append(actions);
  makeWindow('controls','Control Panels',390,panel);setMode(mode,preview);
}
function openHelp() {
  const panel=node('div','panel');panel.append(node('h3','','Welcome to Mack.'),node('p','','A small desktop to get acquainted with. Click an icon once to open it. Drag a title bar to move a window.'));
  const list=node('ul','help-list');['Talk to Mack: say hello, ask the time, or try “Remember that I like jazz.”','Memories: save notes, move them to Trash, and restore them. Notes persist in this browser.','Control Panels: change the wallpaper, enable an available local voice, or preview expressions.','Window controls: close on the left, zoom and collapse on the right. Drag the bottom corner to resize.','Press Escape to close a menu or stop the current reply or expression preview.'].forEach((text)=>list.append(node('li','',text)));
  panel.append(list,node('hr'),node('p','','Conversation is scripted in this first preview. It has no live AI, microphone capture, file access, or robot connection. Conversation text resets when you reload; saved notes stay.'),node('p','fine-print','Mack is a new interface inspired by classic Mac OS. It does not include Apple system software, ROMs, sounds, or fonts.'));
  makeWindow('help','Read Me',470,panel);
}
function arrangeWindows(){windows.forEach((win,id)=>{const i=[...windows.keys()].indexOf(id);win.classList.remove('collapsed');Object.assign(win.style,{left:18+i*24+'px',top:18+i*24+'px',height:''});fit(win);});}
function newConversation(){stopCurrent();conversation=[{who:'Mack',text:'A fresh conversation. Your saved notes are still in Memories.'}];openMack();renderConversation();setMode('idle');}
function closeMenus(){document.querySelectorAll('.dropdown').forEach((menu)=>menu.hidden=true);document.querySelectorAll('.menu-trigger').forEach((b)=>b.setAttribute('aria-expanded','false'));}
function buildMenus(){
  const items=[
    ['Mack menu',[['About This Computer…',openAbout],null,['Mack',openMack],['Control Panels…',openControls],['Memories',openMemories]]],
    ['File',[['New Note',openNewNote],['Open Mackintosh HD',openDisk],null,['Close Window',()=>{if(activeWindow)closeWindow(activeWindow.dataset.window);}]]],
    ['Edit',[['New Conversation',newConversation],['Show Saved Notes',openMemories]]],
    ['View',[['Arrange Windows',arrangeWindows],['Desktop Appearance…',openControls]]],
    ['Special',[['Take a Nap',()=>{stopCurrent();openMack();setMode('resting');}],['Wake Mack',()=>{stopCurrent();openMack();setMode('idle');}],null,['Try Expressions…',openControls]]],
    ['Help',[['Mack Help',openHelp],['About This Preview',openAbout]]]
  ];
  items.forEach(([name,entries],i)=>{
    const wrap=node('div','menu-wrap');const trigger=button(i===0?'':name,()=>{},'menu-trigger'+(i===0?' brand-trigger':''));
    trigger.setAttribute('aria-label',name);trigger.setAttribute('aria-haspopup','menu');trigger.setAttribute('aria-expanded','false');
    if(i===0)trigger.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"><path d="M3 20V4h5l4 7 4-7h5v16h-5v-8l-4 6-4-6v8z" fill="#3b477a"/><path d="M3 4h5v3H3z" fill="#6b9a63"/><path d="M3 7h5v3H3z" fill="#dfca68"/><path d="M3 10h5v3H3z" fill="#ce8551"/><path d="M3 13h5v3H3z" fill="#b55c68"/><path d="M3 16h5v4H3z" fill="#8171a2"/></svg>';
    const menu=node('div','dropdown');menu.hidden=true;menu.setAttribute('role','menu');
    entries.forEach((entry)=>{if(!entry){menu.append(node('hr'));return;}const b=button(entry[0],()=>{closeMenus();entry[1]();},'');b.setAttribute('role','menuitem');menu.append(b);});
    trigger.addEventListener('click',()=>{const opening=menu.hidden;closeMenus();menu.hidden=!opening;trigger.setAttribute('aria-expanded',String(opening));});
    trigger.addEventListener('keydown',(event)=>{if(event.key==='ArrowDown'){event.preventDefault();closeMenus();menu.hidden=false;trigger.setAttribute('aria-expanded','true');menu.querySelector('button')?.focus();}});
    menu.addEventListener('keydown',(event)=>{
      const buttons=[...menu.querySelectorAll('button')];const index=buttons.indexOf(document.activeElement);
      if(event.key==='ArrowDown'||event.key==='ArrowUp'){event.preventDefault();buttons[(index+(event.key==='ArrowDown'?1:-1)+buttons.length)%buttons.length].focus();}
      if(event.key==='Escape'){event.preventDefault();closeMenus();trigger.focus();}
    });wrap.append(trigger,menu);$('#menus').append(wrap);
  });
}
desktop.dataset.pattern=state.pattern;
buildMenus();
[['Mackintosh HD','disk',openDisk],['Memories','memory',openMemories],['Control Panels','controls',openControls],['Trash','trash',openTrash]].forEach(([label,image,action])=>$('#desktop-icons').append(desktopIcon(label,image,action)));
document.addEventListener('pointerdown',(event)=>{if(!event.target.closest('.menu-wrap'))closeMenus();});
document.addEventListener('keydown',(event)=>{
  if(event.key==='Escape'){closeMenus();stopCurrent();setMode('idle');}
});
window.addEventListener('resize',()=>windows.forEach(fit));
window.addEventListener('pagehide',()=>stopCurrent());
window.addEventListener('storage',(event)=>{
  if(event.key!==STORAGE_KEY&&event.key!==null)return;
  try{state=readState(event.newValue);storageBlocked=false;desktop.dataset.pattern=state.pattern;refreshNotes();updateVoiceControls();toast('Saved notes and preferences updated from another Mack tab.');}
  catch{storageBlocked=true;storageMessage='Another tab saved data this preview cannot read. Reload after checking that tab. Existing data will not be overwritten.';toast(storageMessage);}
});
$('#status-control').addEventListener('click',openControls);$('#sound-control').addEventListener('click',toggleVoice);
function updateClock(){const now=new Date();$('#clock').textContent=now.toLocaleTimeString([],{hour:'numeric',minute:'2-digit'});$('#clock').dateTime=now.toISOString();}
updateClock();setInterval(updateClock,15000);updateVoiceControls();openMack();
if(storageMessage)setTimeout(()=>toast(storageMessage),500);
