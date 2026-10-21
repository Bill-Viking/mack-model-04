export const MAX_SECONDS = 60;

export function encodeWav(chunks, rate) {
  if (!Number.isFinite(rate) || rate < 16000 || rate > 192000) throw new Error('Unsupported microphone sample rate.');
  const length = chunks.reduce((n,c)=>n+c.length,0);
  if (length < rate*0.2 || length > rate*MAX_SECONDS) throw new Error('Speak for between 0.2 and 60 seconds.');
  const source = new Float32Array(length);
  let offset=0;for(const chunk of chunks){source.set(chunk,offset);offset+=chunk.length;}
  const frames=Math.floor(length*16000/rate), buffer=new ArrayBuffer(44+frames*2), view=new DataView(buffer);
  const label=(at,text)=>[...text].forEach((c,i)=>view.setUint8(at+i,c.charCodeAt(0)));
  label(0,'RIFF');view.setUint32(4,36+frames*2,true);label(8,'WAVE');label(12,'fmt ');
  view.setUint32(16,16,true);view.setUint16(20,1,true);view.setUint16(22,1,true);
  view.setUint32(24,16000,true);view.setUint32(28,32000,true);view.setUint16(32,2,true);view.setUint16(34,16,true);
  label(36,'data');view.setUint32(40,frames*2,true);
  // Average each output interval, reducing aliasing when downsampling browser PCM.
  for(let i=0;i<frames;i++){
    const start=Math.floor(i*rate/16000),end=Math.floor((i+1)*rate/16000);
    let sum=0;for(let j=start;j<end;j++)sum+=source[j];
    const value=Math.max(-1,Math.min(1,sum/(end-start)));
    if(!Number.isFinite(value))throw new Error('Invalid microphone audio.');
    view.setInt16(44+i*2,Math.round(value*(value<0?32768:32767)),true);
  }
  return new Blob([buffer],{type:'audio/wav'});
}

export class Microphone {
  constructor(onLimit, onLevel=()=>{}, env=globalThis) {
    this.env=env;this.onLimit=onLimit;this.onLevel=onLevel;this.closed=false;
    this.chunks=[];this.samples=0;
  }
  async start() {
    if(!this.env.navigator?.mediaDevices?.getUserMedia)throw new Error('This browser cannot access a microphone. Open Mack in Safari or Chrome on this Mac.');
    let openingTimer;
    try {
      this.context=new this.env.AudioContext();
      const resumed=this.context.resume();
      const permission=this.env.navigator.mediaDevices.getUserMedia({audio:{channelCount:1,echoCancellation:true,noiseSuppression:true,autoGainControl:true},video:false}).then(stream=>{
        if(this.closed)stream.getTracks().forEach(t=>t.stop());
        else this.stream=stream;
      });
      await Promise.race([Promise.all([resumed,permission]),new Promise((_,reject)=>{
        openingTimer=this.env.setTimeout(()=>reject(new Error('Microphone did not open. Allow microphone access, or open Mack in Safari or Chrome on this Mac.')),30000);
      })]);
      this.env.clearTimeout(openingTimer);
      if(this.closed)return false;
      this.deviceLabel=this.stream.getAudioTracks?.()[0]?.label || 'Selected microphone';
      await this.context.audioWorklet.addModule('/microphone-worklet.js');
      if(this.closed)return false;
      this.source=this.context.createMediaStreamSource(this.stream);
      this.worklet=new this.env.AudioWorkletNode(this.context,'mack-microphone');
      this.worklet.port.onmessage=({data})=>{
        if(this.closed)return;
        const room=Math.floor(this.context.sampleRate*MAX_SECONDS)-this.samples;
        const chunk=data.slice(0,room);this.chunks.push(chunk);this.samples+=chunk.length;
        let peak=0;for(const sample of chunk)peak=Math.max(peak,Math.abs(sample));
        this.meterPeak=Math.max(this.meterPeak||0,peak);
        if(this.samples-(this.lastMeterSample||0)>=this.context.sampleRate/10){
          this.lastMeterSample=this.samples;this.onLevel(this.meterPeak,this.samples/this.context.sampleRate);this.meterPeak=0;
        }
        if(this.samples>=this.context.sampleRate*MAX_SECONDS&&!this.limitReached){this.limitReached=true;this.onLimit();}
      };
      // The worklet's output is silence; microphone sound never feeds the speakers.
      this.source.connect(this.worklet);this.worklet.connect(this.context.destination);
      this.timer=this.env.setTimeout(()=>this.onLimit(),MAX_SECONDS*1000);
      return true;
    } catch(error){this.cancel();throw error;}
    finally{this.env.clearTimeout(openingTimer);}
  }
  release() {
    this.closed=true;this.env.clearTimeout(this.timer);
    this.stream?.getTracks().forEach(t=>t.stop());
    this.source?.disconnect();this.worklet?.disconnect();
    if(this.worklet)this.worklet.port.onmessage=null;
    if(this.context&&this.context.state!=='closed')this.context.close().catch(()=>{});
  }
  snapshot() {
    if(this.closed || !this.context || this.samples < this.context.sampleRate*.8)return null;
    return encodeWav(this.chunks,this.context.sampleRate);
  }
  finish() {
    const rate=this.context?.sampleRate;this.release();
    try{return encodeWav(this.chunks,rate);}finally{this.chunks=[];}
  }
  cancel(){this.release();this.chunks=[];}
}

// Full-prefix drafts can correct earlier words. Never queue overlapping inference
// or append duplicate snippets, and never let a late result revive a cancelled turn.
export class LiveTranscript {
  constructor({capture,recognize,cancel,onText,onError,env=globalThis,interval=1000}) {
    Object.assign(this,{capture,recognize,cancel,onText,onError,env,interval});
    this.closed=false;this.active=null;this.pending=null;
  }
  start(){this.schedule(this.interval);}
  schedule(delay){if(!this.closed)this.timer=this.env.setTimeout(()=>this.tick(),delay);}
  tick(){
    if(this.closed||this.pending)return;
    const started=Date.now();
    this.pending=this.update().finally(()=>{
      this.pending=null;
      this.schedule(Math.max(100,this.interval-(Date.now()-started)));
    });
    return this.pending;
  }
  async update(){
    try{
      const audio=this.capture.snapshot();if(!audio)return;
      const job={id:this.env.crypto.randomUUID(),controller:new this.env.AbortController()};
      this.active=job;
      const result=await this.recognize(audio,job.id,job.controller.signal);
      if(!this.closed)this.onText(result);
    }catch(error){if(!this.closed)this.onError(error);}
    finally{this.active=null;}
  }
  stop(discard=false){
    this.closed=true;this.env.clearTimeout(this.timer);
    if(discard&&this.active){
      const {id,controller}=this.active;controller.abort();
      this.cancel(id).catch(()=>{});
    }
    return this.pending||Promise.resolve();
  }
}
