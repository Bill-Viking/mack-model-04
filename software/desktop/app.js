import { STORAGE_KEY, INITIAL_STATE, readState } from './model.mjs';
import { connect, api, speechAudio, transcribeAudio } from './service.mjs';
import { DEFAULT_DELIVERY, AUDITION, readDelivery, chooseVoice, speechChunks } from './voice.mjs';

import { Microphone, LiveTranscript } from './listening.mjs';

const $ = (selector, root = document) => root.querySelector(selector);
const desktop = $('#desktop');
const workspace = $('#workspace');
const windows = new Map();
const windowSizes = new ResizeObserver((entries)=>entries.forEach(({target})=>fit(target)));
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
let conversation = [];
let connected = false;
let health = { ready: false, model: '', models: [], message: 'Connecting to local AI…' };
let request = null;
const PREFS_KEY = 'mack.desktop.preferences.v2';
let legacyNotes = null;
let reviewSpeech = false;
let listening = {available:false,message:'Checking local listening…'};
let microphone = null;
let transcription = null;
let liveTranscript = null;
let delivery = { ...DEFAULT_DELIVERY };
let referenceVoice = { available:false, message:'Checking local reference voice…' };
let voiceJob = null;
let voiceProgress = 'Ready for an audition.';
try { state = readState(localStorage.getItem(STORAGE_KEY)); }
catch (error) { storageBlocked = true; storageMessage = 'Saved notes could not be opened. The original data has been left untouched; this session will not overwrite it.'; }
if (!storageBlocked) legacyNotes = { notes: state.notes, trash: state.trash };
try {
  const prefs = JSON.parse(localStorage.getItem(PREFS_KEY) || '{}');
  if (['periwinkle','sage','graphite','classic'].includes(prefs.pattern)) state.pattern = prefs.pattern;
  if (typeof prefs.voice === 'boolean') state.voice = prefs.voice;
  reviewSpeech = prefs.reviewSpeech === true;
  delivery = readDelivery(prefs.delivery);
} catch { /* Keep earlier preferences; never overwrite the original notes. */ }

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
  try { localStorage.setItem(PREFS_KEY, JSON.stringify({pattern:next.pattern,voice:next.voice,reviewSpeech,delivery})); state = next; return true; }
  catch { toast('This browser could not save preferences. Your memories have not changed.'); return false; }
}
function applySnapshot(snapshot, showHistory=false) {
  state = {...state, notes:snapshot.notes, trash:snapshot.trash};
  if (showHistory) conversation = snapshot.history.flatMap((t)=>[{who:'You',text:t.user},{who:'Mack',text:t.reply}]);
  if (!conversation.length) conversation = [{who:'Mack',text:'Hello, Bill. My memories live on this Mac. Tell me something you would like me to remember.'}];
  refreshNotes(); renderConversation();
}
async function refreshHealth() {
  try { health = await api('models'); }
  catch (error) { health = {...health,ready:false,message:error.message}; }
  const label=$('#model-status'); if(label) label.textContent=health.message+(health.model?' · '+health.model:'');
  $('.preview-label').textContent=health.ready?'Local AI · '+health.model:'Local AI unavailable';
  if (!busy && !microphone && !transcription && !preview && !voiceJob && mode!=='speaking') setMode(health.ready?'idle':'fault');
  renderModelChoices();
  try { referenceVoice = await api('voice/status'); }
  catch { referenceVoice = {available:false,message:'Local reference voice is unavailable.'}; }
  try { listening=await api('listening/status'); } catch { listening={available:false,message:'Local listening is unavailable.'}; }
  const micStatus=$('#listening-status');if(micStatus)micStatus.textContent=listening.message;
  renderVoiceChoices();
}
async function saveChange(path, payload) {
  if (!connected) { toast('Mack’s memory service is unavailable. Reload to reconnect.'); return false; }
  try { applySnapshot(await api(path,payload)); return true; }
  catch (error) { toast(error.message); return false; }
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
  if(id==='mack'&&(microphone||transcription)){stopCurrent();setMode('idle');}
  const win = windows.get(id); if (!win) return;
  windowSizes.unobserve(win);
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
  win.append(bar,body,foot); $('#windows').append(win); windows.set(id,win); windowSizes.observe(win); focusWindow(win); fit(win);
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

const stateText={idle:'Mack is ready',listening:'Listening · microphone on',opening:'Opening microphone',transcribing:'Transcribing locally',thinking:'Thinking',voicing:'Preparing voice',speaking:'Speaking',resting:'Resting',fault:'Connection unavailable'};
function setMode(next, isPreview=false) {
  mode=next; preview=isPreview; desktop.dataset.state=mode;
  $('#status-label').textContent=stateText[mode]+(preview?' · preview':'');
  const line=$('#mack-state');
  if(line)line.textContent=preview?'Expression preview — '+stateText[mode].toLowerCase()+'. No action is running.':(mode==='thinking'?'Waiting for '+(health.model||'local AI')+'…':mode==='voicing'?'Preparing her voice on this Mac. Escape stops it.':mode==='speaking'?'Reading the reply aloud.':mode==='opening'?'Allow microphone access to talk locally. Escape cancels.':mode==='transcribing'?'Microphone off. Transcribing on this Mac…':mode==='listening'?'Microphone on · '+(microphone?.deviceLabel||'Selected input')+'. Click Finish & send when done; Escape discards.':mode==='resting'?'Taking a little desktop nap. Send a message to wake me.':health.message+(health.model?' · '+health.model:''));
  const fault=$('#fault-banner'); if(fault)fault.hidden=mode!=='fault';
  const input=$('#message-input'); if(input)input.disabled=busy||!connected||!!microphone||!!transcription;
  const send=$('#send-message'); if(send)send.disabled=busy||!connected||!!microphone||!!transcription;
  if(!microphone){const elapsed=$('#recording-time');if(elapsed)elapsed.textContent='Microphone off';const meter=$('#microphone-meter');if(meter)meter.value=0;const signal=$('#microphone-signal');if(signal)signal.textContent='';}
  const dictate=$('#dictate-message'); if(dictate){dictate.disabled=busy||!connected||!!transcription;dictate.textContent=microphone?(mode==='opening'?'Cancel microphone':'Finish & send'):'Talk to Mack';}
  const stop=$('#stop-listening');if(stop)stop.hidden=!microphone&&!transcription;
  document.querySelectorAll('[data-preview-state]').forEach((b)=>b.setAttribute('aria-pressed',String(preview && b.dataset.previewState===mode)));
}
function stopCurrent() {
  turn++; timers.forEach(clearTimeout); timers=[]; busy=false;
  if(request){api('cancel',{id:request.id}).catch(()=>{});request.controller.abort();request=null;}
  microphone?.cancel();microphone=null;
  liveTranscript?.stop(true);liveTranscript=null;
  const transcriptPanel=$('#live-transcript');if(transcriptPanel)transcriptPanel.hidden=true;
  if(transcription){transcription.controller.abort();api('listening/cancel',{id:transcription.id}).catch(()=>{});transcription=null;}
  const dictate=$('#dictate-message');if(dictate)dictate.textContent='Talk to Mack';
  if('speechSynthesis' in window)window.speechSynthesis.cancel();
  stopReferenceVoice();
}
function previewState(next) { stopCurrent(); openMack(); setMode(next,true); }
function renderConversation() {
  const log=$('#conversation'); if(!log)return; log.replaceChildren();
  conversation.forEach(({who,text,tools})=>{
    const row=node('div','message '+(who==='You'?'user':'assistant'));
    row.append(node('span','speaker',who),node('p','',text));
    if(tools?.length){
      const labels={mack_status:'System status',local_time:'Local clock',search_memories:'Saved memories',search_conversations:'Past conversations'};
      row.append(node('p','fine-print','Tools: '+tools.map((tool)=>(labels[tool.name]||'Unavailable tool')+(tool.ok?' — checked':' — failed')).join('; ')));
    }
    if(who==='Mack') {
      const read=button('Read aloud',()=>{if(busy||microphone||transcription)return;stopCurrent();speak(text,turn,true);},'classic-button small read-aloud');
      read.setAttribute('aria-label','Read this reply aloud');row.append(read);
    }
    log.append(row);
  });
  log.scrollTop=log.scrollHeight;
}
function refreshVoices() { localVoices=('speechSynthesis' in window)?window.speechSynthesis.getVoices().filter((voice)=>voice.localService):[]; renderVoiceChoices(); }
if('speechSynthesis' in window){ refreshVoices();window.speechSynthesis.addEventListener('voiceschanged',refreshVoices); }
function speak(text, token, audition=false) {
  if(!state.voice&&!audition){setMode(health.ready?'idle':'fault');return;}
  if(delivery.engine==='reference'){speakReference(text,token);return;}
  refreshVoices();
  const selected = chooseVoice(localVoices, delivery.voiceURI);
  if((!state.voice&&!audition) || !selected) { setMode(health.ready?'idle':'fault'); if(state.voice||audition)toast('The selected local voice is unavailable. Choose another voice in Control Panels.'); return; }
  const speech=new SpeechSynthesisUtterance(text.slice(0,2500));
  speech.voice=selected;
  speech.lang=selected.lang;
  speech.rate=delivery.rate;
  speech.pitch=delivery.pitch;
  speech.onstart=()=>{if(token===turn)setMode('speaking');};
  speech.onend=()=>{if(token===turn)setMode('idle');};
  speech.onerror=()=>{if(token===turn){setMode('idle');toast('Voice playback was unavailable. The reply is here to read.');}};
  window.speechSynthesis.speak(speech);
  const speechDeadline=Math.max(30000,speech.text.split(/\s+/).length*650/delivery.rate);
  timers.push(setTimeout(()=>{if(token===turn&&mode==='speaking'){window.speechSynthesis.cancel();setMode('idle');}},speechDeadline));
}

function stopReferenceVoice() {
  const job=voiceJob;voiceJob=null;
  if(!job)return;
  updateVoiceProgress('Voice stopped.');
  job.controller.abort();api('voice/cancel',{id:job.id}).catch(()=>{});
  if(job.audio){job.audio.pause();job.audio.removeAttribute('src');job.audio.load();}
  if(job.url)URL.revokeObjectURL(job.url);
  job.finish?.();
}

function updateVoiceProgress(message) {
  voiceProgress=message;
  const line=$('#voice-progress');if(line)line.textContent=message;
}

async function speakReference(text, token) {
  if(!referenceVoice.available){setMode(health.ready?'idle':'fault');toast(referenceVoice.message);return;}
  try {
    for(const part of speechChunks(text)) {
      if(token!==turn)return;
      const job={id:crypto.randomUUID(),controller:new AbortController()};voiceJob=job;
      setMode('voicing');
      updateVoiceProgress('Preparing voice on this Mac…');
      try {
        const blob=await speechAudio({id:job.id,text:part,style:delivery.style},job.controller.signal);
        if(token!==turn)return;
        job.url=URL.createObjectURL(blob);job.audio=new Audio(job.url);
        job.audio.onplaying=()=>{if(token===turn){setMode('speaking');updateVoiceProgress('Playing the generated voice.');}};
        await new Promise((resolve,reject)=>{
          job.finish=resolve;
          job.audio.onended=resolve;
          job.audio.onerror=()=>reject(new Error('Voice playback failed. The reply is still here to read.'));
          job.audio.play().catch(()=>reject(new Error('Click Read aloud or Hear voice preview to allow playback.')));
        });
      } finally {
        if(job.audio){job.audio.pause();job.audio.removeAttribute('src');job.audio.load();}
        if(job.url)URL.revokeObjectURL(job.url);
        if(voiceJob===job)voiceJob=null;
      }
    }
    if(token===turn){setMode(health.ready?'idle':'fault');updateVoiceProgress('Voice playback finished.');}
  } catch(error) {
    if(token===turn){setMode(health.ready?'idle':'fault');updateVoiceProgress(error.message);toast(error.message);}
  }
}
async function sendMessage(value) {
  const text=value.trim().slice(0,2000); if(!text||busy)return;
  if(!connected){toast('Reload Mack to reconnect to her memory service.');return;}
  stopCurrent(); const token=turn; busy=true;
  conversation.push({who:'You',text}); if(conversation.length>80)conversation=conversation.slice(-80);
  openMack(); $('#message-input').value=''; renderConversation(); setMode('thinking');
  const pending={id:crypto.randomUUID(),controller:new AbortController()};request=pending;
  try {
    const result=await api('chat',{id:pending.id,text},pending.controller.signal);
    if(token!==turn)return;
    request=null;
    try{const snapshot=await api('state');if(token!==turn)return;applySnapshot(snapshot);}catch{toast('Reply received. Reload to refresh the memory list.');}
    if(token!==turn)return;
    busy=false;conversation.push({who:'Mack',text:result.text,tools:result.tools});renderConversation();
    if(result.model!=='memory service'){health.ready=true;health.message='Local AI ready';health.model=result.model;}
    setMode(health.ready?'idle':'fault');speak(result.text,token);
    $('#message-input')?.focus();
  } catch(error) {
    if(token!==turn)return;
    request=null;busy=false;
    conversation.push({who:'Mack',text:'I couldn’t finish that request. '+error.message});renderConversation();
    health.message=error.message;setMode('fault');
  }
}
async function dictate() {
  if(microphone){if(mode==='opening'){stopCurrent();setMode('idle');}else await finishListening();return;}
  if(busy||transcription)return;
  if(!listening.available){toast(listening.message);openControls();return;}
  stopCurrent();const token=turn;
  let lastSound=-Infinity;
  const capture=new Microphone(()=>finishListening(),(peak,seconds)=>{
    if(token!==turn)return;
    const meter=$('#microphone-meter');if(meter){meter.value=peak;meter.setAttribute('aria-valuetext',Math.round(seconds)+' seconds recorded');}
    const elapsed=$('#recording-time');if(elapsed)elapsed.textContent=Math.floor(seconds)+' / 60 seconds';
    if(peak>.003)lastSound=seconds;
    const signal=$('#microphone-signal');
    if(signal)signal.textContent=seconds-lastSound<1?'Sound detected':seconds>3?'No sound detected — check your microphone.':'Waiting for sound…';
  });microphone=capture;setMode('opening');
  showTranscript('', 'Opening microphone…');
  try{
    if(await capture.start()&&token===turn){
      setMode('listening');showTranscript('', 'Listening · your words will appear here');
      liveTranscript=new LiveTranscript({capture,
        recognize:(audio,id,signal)=>transcribeAudio(audio,id,signal,true),
        cancel:id=>api('listening/cancel',{id}),
        onText:result=>{if(token===turn)showTranscript(result.text,result.text?'Live transcript · words may correct themselves':'Listening · waiting for speech');},
        onError:error=>{if(token===turn){const label=$('#live-transcript-label');if(label)label.textContent='Live words unavailable · '+error.message+' You can still Finish & send.';}}
      });
      liveTranscript.start();
    }
  }catch(error){
    if(token!==turn)return;
    microphone=null;setMode('idle');
    const message=error.name==='NotAllowedError'?'Microphone access was denied. Allow it for Mack in this browser, then try Talk to Mack again.':error.message;
    showTranscript('',message);
    const status=$('#mack-state');if(status)status.textContent=message;toast(message);
  }
}
function showTranscript(text,label){
  const panel=$('#live-transcript');if(!panel)return;
  panel.hidden=false;
  $('#live-transcript-label').textContent=label;
  const words=$('#live-transcript-text');words.textContent=text||'…';words.scrollTop=words.scrollHeight;
}
async function finishListening(){
  const capture=microphone;if(!capture||mode==='opening')return;
  microphone=null;const token=turn;
  try{
    const audio=capture.finish();
    const job={id:crypto.randomUUID(),controller:new AbortController()};transcription=job;setMode('transcribing');
    const label=$('#live-transcript-label');if(label)label.textContent='Checking the complete transcript · microphone off';
    const drafts=liveTranscript;
    await drafts?.stop();
    if(token!==turn)return;
    liveTranscript=null;
    const result=await transcribeAudio(audio,job.id,job.controller.signal);
    if(token!==turn)return;
    transcription=null;
    const input=$('#message-input');if(input)input.value=result.text;
    showTranscript(result.text,'Transcript ready');
    setMode('idle');
    delivery=readDelivery({...delivery,engine:'reference',style:'film'});persist({...state,voice:true});updateVoiceControls();
    if(reviewSpeech){toast('Transcript ready. Edit it if needed, then Send.');input?.focus();}
    else{
      await sendMessage(result.text);
    }
  }catch(error){if(token===turn){liveTranscript?.stop(true);liveTranscript=null;transcription=null;setMode('idle');const status=$('#mack-state');if(status)status.textContent=error.message;const label=$('#live-transcript-label');if(label)label.textContent='Not sent · '+error.message;toast(error.message);}}
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
  const fault=node('div','fault-banner');fault.id='fault-banner';fault.hidden=true;fault.append(node('p','','Memories stay on this Mac when AI is unavailable. Expression previews are labeled separately.'),button('Check connection',refreshHealth,'classic-button small'));
  const form=node('form','composer');form.setAttribute('aria-label','Talk to Mack');
  const input=node('input');input.id='message-input';input.type='text';input.maxLength=2000;input.placeholder='Say something to Mack…';input.autocomplete='off';input.setAttribute('aria-label','Message to Mack');
  const send=node('button','classic-button primary','Send');send.id='send-message';send.type='submit';
  const mic=button('Talk to Mack',dictate);mic.id='dictate-message';mic.title='See a live local transcript as you speak, then Finish & send';
  form.append(input,mic,send);form.addEventListener('submit',(event)=>{event.preventDefault();sendMessage(input.value);});
  const micInfo=node('div','microphone-info');
  const meter=node('meter');meter.id='microphone-meter';meter.min=0;meter.max=1;meter.value=0;meter.setAttribute('aria-label','Microphone level');
  const elapsed=node('span','fine-print','Microphone off');elapsed.id='recording-time';
  const signal=node('span','fine-print');signal.id='microphone-signal';
  const stop=button('Cancel recording',()=>{stopCurrent();setMode('idle');},'classic-button small');stop.id='stop-listening';stop.hidden=true;
  micInfo.append(meter,elapsed,signal,stop);
  const transcriptPanel=node('section','live-transcript');transcriptPanel.id='live-transcript';transcriptPanel.hidden=true;transcriptPanel.setAttribute('aria-label','Live speech transcript');
  const transcriptLabel=node('div','fine-print');transcriptLabel.id='live-transcript-label';
  const transcriptText=node('p','live-transcript-text','…');transcriptText.id='live-transcript-text';transcriptText.setAttribute('aria-live','polite');transcriptText.setAttribute('aria-atomic','true');
  transcriptPanel.append(transcriptLabel,transcriptText);
  content.append(welcome,log,line,suggestions,fault,transcriptPanel,form,micInfo,node('p','fine-print','Offline conversation · speech stays on this Mac · completed exchanges are saved in Conversations.'));
  makeWindow('mack','Mack',560,content,{foot:'M.A.C. Model 04 · Local AI 0.3 · Esc stops a reply'});renderConversation();setMode(mode,preview);
}
function openAbout() {
  const content=node('div','panel');const hero=node('div','about-header');const words=node('div');words.append(node('h3','','M.A.C. Model 04'),node('p','','Mobile Autonomous Computer'));hero.append(face(),words);
  const table=node('table','spec-table');
  [['Known as','Mack · she/her'],['System','Mack Local AI 0.3'],['Personality','SAL-inspired · calm, curious, plain-spoken'],['Conversation',health.model||'No model selected'],['Memories','Local database · survives restarts and model changes'],['Tools','Read-only status, clock, facts and conversation search'],['Body','Desktop now · four-leg Mac planned'],['Long-term','Humanoid body · separate future engineering']].forEach(([key,value])=>{const row=node('tr');row.append(node('th','',key),node('td','',value));table.append(row);});
  content.append(hero,table,node('p','','A little Mac brought to life. This is the first working shell for the RayCue conversion, inspired by the Platinum desktop.'),node('p','fine-print','Original interface and icons. This preview does not run Mac OS 9 or vintage applications.'));
  makeWindow('about','About This Computer',440,content);
}
function openDisk() {
  const content=node('div');const meta=node('div','finder-meta');meta.append(node('span','','6 items'),node('span','','Mackintosh HD'));
  const items=node('div','finder-items');
  [['Mack','mack',openMack],['Memories','memory',openMemories],['Conversations','readme',openConversations],['Control Panels','controls',openControls],['Read Me','readme',openHelp],['About Mack','mack',openAbout]].forEach(([label,image,action])=>items.append(desktopIcon(label,image,action)));
  content.append(meta,items);makeWindow('disk','Mackintosh HD',460,content);
}
function openNewNote(memory=null) {
  if(memory instanceof Event)memory=null;
  closeWindow('new-note');
  const content=node('form','note-editor'); const area=node('textarea');area.maxLength=2000;area.placeholder='Something worth remembering…';area.setAttribute('aria-label','Memory text');area.value=memory?.text||'';
  const actions=node('div','panel-actions');const save=node('button','classic-button primary','Save note');save.type='submit';actions.append(button('Cancel',()=>closeWindow('new-note')),save);
  content.append(area,node('p','fine-print','Saved on this Mac. Active memories help Mack answer future questions. Trash is excluded from her next reply.'),actions);
  content.addEventListener('submit',async(event)=>{event.preventDefault();save.disabled=true;const saved=await saveChange('memory/save',{text:area.value,id:memory?.id});save.disabled=false;if(saved){closeWindow('new-note');openMemories();toast('Saved in Mack’s memory database.');}});
  makeWindow('new-note',memory?'Edit Memory':'New Note',350,content);$('textarea',windows.get('new-note')).focus();
}
function noteList(destination) {
  const panel=node('div','notes-list');panel.dataset.notesList=destination;
  if(!connected){panel.append(node('p','empty-state','Connecting to Mack’s memory database… Reload if the service is unavailable.'));return panel;}
  const count=state[destination].length;
  const toolbar=node('div','notes-toolbar');toolbar.append(node('span','',count+(destination==='notes'?' saved note':' note')+(count===1?'':'s')+(destination==='trash'?' in Trash':'')));
  if(destination==='notes')toolbar.append(button('New note',openNewNote,'classic-button small'));
  panel.append(toolbar);const list=node('div','trash-list');
  if(!state[destination].length)list.append(node('p','empty-state',destination==='notes'?'An empty notebook. A good place to begin.':'The Trash is empty. Removed notes appear here until you restore them.'));
  state[destination].forEach((note)=>{
    const row=node('div','note-row');row.append(node('p','',note.text));
    if(destination==='notes')row.append(button('Edit',()=>openNewNote(note),'classic-button small'));
    row.append(button(destination==='notes'?'Move to Trash':'Restore',async()=>{
      if(await saveChange('memory/move',{id:note.id,trashed:destination==='notes'}))toast(destination==='notes'?'Moved to Trash. Excluded from future AI context.':'Restored to Memories.');
    },'classic-button small'));list.append(row);
  });panel.append(list,node('div','window-note','Saved on this Mac, independent of your browser and chosen model. Up to 100 active memories; the most relevant six inform each reply.'));return panel;
}
function refreshNotes() { document.querySelectorAll('[data-notes-list]').forEach((list)=>list.replaceWith(noteList(list.dataset.notesList))); }
function openMemories(){makeWindow('memories','Memories',420,noteList('notes'));}
function openTrash(){makeWindow('trash','Trash',410,noteList('trash'));}
function toggleVoice() {
  refreshVoices();
  if(!state.voice&&(delivery.engine==='reference'?!referenceVoice.available:!chooseVoice(localVoices,delivery.voiceURI))){toast('The selected voice is unavailable. Check Control Panels.');return;}
  if(persist({...state,voice:!state.voice})){
    if(!state.voice){if(mode==='speaking'||mode==='voicing'){stopCurrent();setMode(health.ready?'idle':'fault');}window.speechSynthesis?.cancel();}
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
  panel.append(node('p','','SAL-inspired personality: calm, candid, curious, and plain-spoken.'),label);
  const voiceChoices=node('div','voice-choices');voiceChoices.id='voice-choices';panel.append(voiceChoices);
  for(const [key,title,min,max] of [['rate','Pace',0.7,1.1],['pitch','Pitch',0.8,1.2]]){
    const row=node('label','stock-delivery');const slider=node('input');slider.type='range';slider.min=min;slider.max=max;slider.step=0.02;slider.value=delivery[key];slider.setAttribute('aria-label','Voice '+title.toLowerCase());
    const value=node('output','',delivery[key].toFixed(2));
    slider.addEventListener('input',()=>{delivery=readDelivery({...delivery,[key]:Number(slider.value)});value.textContent=delivery[key].toFixed(2);});
    slider.addEventListener('change',()=>persist(state));row.append(document.createTextNode(title),slider,value);panel.append(row);
  }
  const auditionLabel=node('label');const auditionText=node('textarea');auditionText.value=AUDITION;auditionText.maxLength=600;auditionText.rows=3;auditionText.setAttribute('aria-label','Voice audition text');auditionLabel.append(document.createTextNode('Audition text'),auditionText);panel.append(auditionLabel);
  panel.append(button('Hear voice preview',()=>{if(busy||microphone||transcription){toast('Finish or stop the current conversation first.');return;}if(!auditionText.value.trim())return;stopCurrent();speak(auditionText.value,turn,true);},'classic-button small'),button('Stop voice',()=>{if(busy||microphone||transcription)return;stopCurrent();setMode(health.ready?'idle':'fault');},'classic-button small'),node('p','fine-print','Voice v1 preserves Bill’s approved light-echo delivery. New speech is generated locally from the chosen SAL reference. Preview text does not enter conversation or memory.'));
  const progress=node('p','fine-print',voiceProgress);progress.id='voice-progress';progress.setAttribute('aria-live','polite');panel.append(progress);
  const micLabel=node('label');const mic=node('input');mic.type='checkbox';mic.checked=reviewSpeech;mic.addEventListener('change',()=>{reviewSpeech=mic.checked;persist(state);});micLabel.append(mic,document.createTextNode('Review transcript before sending'));
  const listeningStatus=node('p','fine-print',listening.message);listeningStatus.id='listening-status';
  panel.append(node('hr'),node('h3','','Local listening'),listeningStatus,micLabel,node('p','fine-print','Talk to Mack shows a live local transcript as you speak. Draft words may correct themselves. Finish & send closes the microphone, checks the full transcript and asks Mack to answer in her approved voice. Escape discards the recording. Maximum 60 seconds. No browser speech service or cloud fallback.'));
  const modelStatus=node('p','fine-print');modelStatus.id='model-status';const modelChoices=node('div','model-choices');modelChoices.id='model-choices';
  panel.append(node('hr'),node('h3','','Local AI model'),modelStatus,modelChoices,button('Check connection',refreshHealth,'classic-button small'),node('p','fine-print','Installed Ollama models only. Switching keeps your memories. Downloads and cloud services are not enabled here.'),node('hr'),node('h3','','Try Mack’s expressions'),node('p','','These buttons preview screen states. They do not start a microphone, AI service, or robot.'));
  const states=node('div','state-buttons');
  [['idle','Ready'],['listening','Listening'],['thinking','Thinking'],['speaking','Speaking'],['resting','Resting'],['fault','Disconnected']].forEach(([name,label])=>{const b=button(label,()=>previewState(name),'classic-button small');b.dataset.previewState=name;b.setAttribute('aria-pressed','false');states.append(b);});
  panel.append(states);const actions=node('div','panel-actions');actions.append(button('Reset expression',()=>{stopCurrent();setMode('idle');}));panel.append(actions);
  makeWindow('controls','Control Panels',420,panel);setMode(mode,preview);renderModelChoices();refreshVoices();refreshHealth();
}
function renderVoiceChoices(){
  const box=$('#voice-choices');if(!box)return;box.replaceChildren();
  const engineLabel=node('label');engineLabel.append(document.createTextNode('Voice engine'));
  const engine=node('select');engine.setAttribute('aria-label','Voice engine');
  for(const [value,title] of [['reference','Mack · approved voice v1'],['browser','Stock Mac voice']]){const option=node('option','',title);option.value=value;engine.append(option);}
  engine.value=delivery.engine;
  engine.addEventListener('change',()=>{if(!busy&&!microphone&&!transcription){stopCurrent();setMode(health.ready?'idle':'fault');}delivery=readDelivery({...delivery,engine:engine.value});persist(state);renderVoiceChoices();});
  engineLabel.append(engine);box.append(engineLabel);
  document.querySelectorAll('.stock-delivery').forEach((row)=>row.hidden=delivery.engine!=='browser');
  if(delivery.engine==='reference'){
    const styleLabel=node('label');styleLabel.append(document.createTextNode('Delivery'));
    const style=node('select');style.setAttribute('aria-label','Reference voice delivery');
    for(const [value,title] of [['film','Approved v1 · light echo'],['natural','Reference · dry (alternative)']]){const option=node('option','',title);option.value=value;style.append(option);}
    style.value=delivery.style;
    style.addEventListener('change',()=>{if(!busy&&!microphone&&!transcription){stopCurrent();setMode(health.ready?'idle':'fault');}delivery=readDelivery({...delivery,style:style.value});persist(state);});
    styleLabel.append(style);box.append(styleLabel,node('p','fine-print',referenceVoice.message));return;
  }
  const label=node('label');label.append(document.createTextNode('Local voice'));
  const select=node('select');select.setAttribute('aria-label','Local speaking voice');
  const automatic=node('option','','Automatic · English');automatic.value='';select.append(automatic);
  for(const voice of localVoices){const option=node('option','',voice.name+' · '+voice.lang);option.value=voice.voiceURI;select.append(option);}
  if(delivery.voiceURI&&!localVoices.some((v)=>v.voiceURI===delivery.voiceURI)){const missing=node('option','','Saved voice unavailable');missing.value=delivery.voiceURI;select.append(missing);}
  select.value=delivery.voiceURI;select.addEventListener('change',()=>{delivery=readDelivery({...delivery,voiceURI:select.value});persist(state);renderVoiceChoices();});
  label.append(select);box.append(label);
  const selected=chooseVoice(localVoices,delivery.voiceURI);box.append(node('p','fine-print',selected?'Current voice: '+selected.name:'No matching local voice is available.'));
}
function renderModelChoices(){
  const box=$('#model-choices');if(!box)return;box.replaceChildren();
  const select=node('select');select.setAttribute('aria-label','Local AI model');
  (health.models||[]).forEach((model)=>{const option=node('option','',model.name);option.value=model.name;select.append(option);});
  select.value=health.model;
  const choose=button('Use model',async()=>{choose.disabled=true;if(await saveChange('model',{model:select.value})){await refreshHealth();toast('Model selected. Mack’s memories stayed in place.');}choose.disabled=false;},'classic-button small');
  choose.disabled=!health.models?.length;box.append(select,choose);
  $('#model-status').textContent=health.message+(health.model?' · '+health.model:'');
}
function openConversations() {
  if(windows.has('conversations')){focusWindow(windows.get('conversations'));return;}
  const panel=node('div','panel');const search=node('input');search.type='search';search.maxLength=200;search.setAttribute('aria-label','Search conversations');
  const list=node('div');let offset=0;let trash=false;let generation=0;
  const count=node('p','fine-print');
  const load=async()=>{
    const current=++generation;
    try{
      const result=await api('conversation/search',{query:search.value,offset,trashed:trash});
      if(current!==generation)return;
      list.replaceChildren();count.textContent=(trash?'Conversation Trash':'Saved conversations')+' · '+(result.exchanges.length ? (offset+1)+'–'+(offset+result.exchanges.length) : 'No exchanges');
      if(!result.exchanges.length)list.append(node('p','','No exchanges found.'));
      for(const exchange of result.exchanges){
        const item=node('article','archive-exchange');item.append(node('p','fine-print',new Date(exchange.created).toLocaleString()),node('strong','','You'),node('p','',exchange.user),node('strong','','Mack'),node('p','',exchange.reply));
        item.append(button(trash?'Restore exchange':'Move exchange to Trash',async()=>{if(await saveChange('conversation/move',{id:exchange.id,trashed:!trash})){applySnapshot(await api('state'),true);await load();}},'classic-button small'));
        list.append(item);
      }
      previous.disabled=offset===0;next.disabled=result.exchanges.length<20;
    }catch(error){toast(error.message);}
  };
  const previous=button('Previous',()=>{offset=Math.max(0,offset-20);load();},'classic-button small');
  const next=button('Next',()=>{offset+=20;load();},'classic-button small');
  const deleted=button('Show Conversation Trash',()=>{trash=!trash;offset=0;deleted.textContent=trash?'Show saved conversations':'Show Conversation Trash';load();},'classic-button small');
  panel.append(node('p','','Completed exchanges stay on this Mac across restarts and model changes. Trash excludes an exchange from recall and can be restored.'),search,button('Search',()=>{offset=0;load();},'classic-button small'),deleted,count,list,previous,next);
  search.addEventListener('keydown',e=>{if(e.key==='Enter'){offset=0;load();}});
  makeWindow('conversations','Conversations',560,panel);load();
}
function openHelp() {
  const panel=node('div','panel');panel.append(node('h3','','Welcome to Mack.'),node('p','','A small desktop to get acquainted with. Click an icon once to open it. Drag a title bar to move a window.'));
  const list=node('ul','help-list');['Talk to Mack: type freely, or try “Remember that I like jazz.” Explicit Remember requests save facts without asking the model to guess what belongs in memory.','Memories: inspect, edit, move notes to Trash, and restore them. They survive browser clearing, restarts, and model changes.','Talk to Mack shows a live local transcript while you speak. Draft words may change. Finish & send closes the microphone, checks the full transcript and plays her answer. Escape cancels. Control Panels offers transcript review before sending.','Completed exchanges stay in the local Conversations archive. New Conversation starts a fresh view without erasing the archive. Move an exchange to Conversation Trash to exclude it from recall. Fact edits create a recall boundary so old dialogue cannot revive corrected facts.','Window controls: close on the left, zoom and collapse on the right. Drag the bottom corner to resize.','Escape dismisses a pending reply or expression preview. Local inference may finish in the background before Mack accepts another request.'].forEach((text)=>list.append(node('li','',text)));
  panel.append(list,node('hr'),node('p','','AI answers can be mistaken. Mack currently has no sensors, motors, web access, or project service connections. Memory lives in runtime/mack/memory.sqlite3 in the project folder; it is excluded from Git. Back up that folder with the server stopped.'),node('p','fine-print','Mack is a new interface inspired by classic Mac OS. It does not include Apple system software, ROMs, sounds, or fonts.'));
  makeWindow('help','Read Me',470,panel);
}
function arrangeWindows(){windows.forEach((win,id)=>{const i=[...windows.keys()].indexOf(id);win.classList.remove('collapsed');Object.assign(win.style,{left:18+i*24+'px',top:18+i*24+'px',height:''});fit(win);});}
async function newConversation(){if(busy){toast('Finish or stop this reply first, then start a new conversation.');return;}if(await saveChange('conversation/new',{})){stopCurrent();conversation=[{who:'Mack',text:'A fresh conversation. Earlier exchanges are still in Conversations, and your saved facts are in Memories.'}];openMack();renderConversation();setMode(health.ready?'idle':'fault');}}
function closeMenus(){document.querySelectorAll('.dropdown').forEach((menu)=>menu.hidden=true);document.querySelectorAll('.menu-trigger').forEach((b)=>b.setAttribute('aria-expanded','false'));}
function buildMenus(){
  const items=[
    ['Mack menu',[['About This Computer…',openAbout],null,['Mack',openMack],['Control Panels…',openControls],['Memories',openMemories]]],
    ['File',[['New Note',openNewNote],['Open Mackintosh HD',openDisk],null,['Close Window',()=>{if(activeWindow)closeWindow(activeWindow.dataset.window);}]]],
    ['Edit',[['New Conversation',newConversation],['Show Saved Notes',openMemories],['Conversations',openConversations]]],
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
[['Mackintosh HD','disk',openDisk],['Memories','memory',openMemories],['Conversations','readme',openConversations],['Control Panels','controls',openControls],['Trash','trash',openTrash]].forEach(([label,image,action])=>$('#desktop-icons').append(desktopIcon(label,image,action)));
document.addEventListener('pointerdown',(event)=>{if(!event.target.closest('.menu-wrap'))closeMenus();});
document.addEventListener('keydown',(event)=>{
  if(event.key==='Escape'){closeMenus();stopCurrent();setMode('idle');}
});
window.addEventListener('resize',()=>windows.forEach(fit));
window.addEventListener('pagehide',()=>stopCurrent());
document.addEventListener('visibilitychange',()=>{if(document.hidden&&microphone){stopCurrent();setMode('idle');}});
window.addEventListener('storage',(event)=>{
  if(event.key!==PREFS_KEY)return;
  try{const prefs=JSON.parse(event.newValue||'{}');if(['periwinkle','sage','graphite','classic'].includes(prefs.pattern))state.pattern=prefs.pattern;if(typeof prefs.voice==='boolean')state.voice=prefs.voice;reviewSpeech=prefs.reviewSpeech===true;delivery=readDelivery(prefs.delivery);desktop.dataset.pattern=state.pattern;updateVoiceControls();renderVoiceChoices();}catch{ /* Ignore malformed browser preferences. */ }
});
window.addEventListener('focus',()=>{if(connected&&!busy)api('state').then((s)=>applySnapshot(s)).catch(()=>{});});
$('#status-control').addEventListener('click',openControls);$('#sound-control').addEventListener('click',toggleVoice);
function updateClock(){const now=new Date();$('#clock').textContent=now.toLocaleTimeString([],{hour:'numeric',minute:'2-digit'});$('#clock').dateTime=now.toISOString();}
updateClock();setInterval(updateClock,15000);updateVoiceControls();openMack();
if(storageMessage)setTimeout(()=>toast(storageMessage),500);
async function initialize(){
  try{
    const snapshot=await connect();connected=true;applySnapshot(snapshot,true);
    if(legacyNotes&&(legacyNotes.notes.length||legacyNotes.trash.length)){
      try{applySnapshot(await api('memory/import',legacyNotes));}catch(error){toast('Old browser notes were preserved but could not be imported: '+error.message);}
    }
    await refreshHealth();
  }catch(error){connected=false;health.message=error.message;setMode('fault');toast(error.message);}
}
initialize();
