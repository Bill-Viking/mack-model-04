import test from 'node:test';
import assert from 'node:assert/strict';
import {encodeWav,Microphone,LiveTranscript} from '../software/desktop/listening.mjs';

function fakeEnvironment({pending=false,failModule=false,mediaError=null}={}){
  let grant;const tracks=[{stopped:false,stop(){this.stopped=true;}}];
  const stream={getTracks:()=>tracks};
  const timers=new Map();let serial=0;
  class AudioContext {
    constructor(){this.sampleRate=48000;this.state='running';this.destination={};this.audioWorklet={addModule:async()=>{if(failModule)throw Error('worklet failed');}};}
    resume(){return Promise.resolve();}
    close(){this.state='closed';return Promise.resolve();}
    createMediaStreamSource(){return{connect(){},disconnect(){}};}
  }
  class AudioWorkletNode{constructor(){this.port={onmessage:null};}connect(){}disconnect(){}}
  const requests=[];
  return {tracks,timers,requests,grant:()=>grant(stream),
    env:{navigator:{mediaDevices:{getUserMedia:constraints=>{requests.push(constraints);return mediaError?Promise.reject(mediaError):pending?new Promise(resolve=>grant=resolve):Promise.resolve(stream);}}},
      AudioContext,AudioWorkletNode,setTimeout:(fn,ms)=>{const id=++serial;timers.set(id,{fn,ms});return id;},clearTimeout:id=>timers.delete(id)}};
}

test('browser PCM is bounded, downsampled and encoded as mono 16k PCM16',async()=>{
  const samples=new Float32Array(48000).fill(.5);
  const data=new DataView(await encodeWav([samples],48000).arrayBuffer());
  assert.equal(data.byteLength,32044);assert.equal(data.getUint32(24,true),16000);
  assert.equal(data.getUint16(22,true),1);assert.equal(data.getUint16(34,true),16);
  assert.equal(data.getInt16(44,true),16384);
  for(const [input,rate] of [[[],48000],[[new Float32Array(100)],48000],[[samples],0],[[new Float32Array(16000*61)],16000]]){
    assert.throws(()=>encodeWav(input,rate));
  }
  samples[0]=NaN;assert.throws(()=>encodeWav([samples],48000));
});
test('finish releases all microphone tracks before returning upload audio',async()=>{
  const f=fakeEnvironment(),mic=new Microphone(()=>{},()=>{},f.env);
  await mic.start();mic.worklet.port.onmessage({data:new Float32Array(48000).fill(.1)});
  const blob=mic.finish();assert.equal(blob.type,'audio/wav');
  assert.ok(f.tracks.every(t=>t.stopped));assert.equal(mic.context.state,'closed');
  assert.equal(mic.chunks.length,0);assert.equal(f.timers.size,0);
});
test('a chosen microphone is required exactly, while default leaves the browser choice open',async()=>{
  const chosen=fakeEnvironment(),mic=new Microphone(()=>{},()=>{},chosen.env);
  await mic.start('studio-display-device');
  assert.deepEqual(chosen.requests[0].audio.deviceId,{exact:'studio-display-device'});
  mic.cancel();
  const automatic=fakeEnvironment(),other=new Microphone(()=>{},()=>{},automatic.env);
  await other.start();assert.equal(automatic.requests[0].audio.deviceId,undefined);other.cancel();
});
test('a missing selected input closes audio and never retries with another microphone',async()=>{
  for(const name of ['NotFoundError','OverconstrainedError']){
    const f=fakeEnvironment({mediaError:Object.assign(new Error('gone'),{name})});
    const mic=new Microphone(()=>{},()=>{},f.env);
    await assert.rejects(mic.start('disconnected-device'),/selected microphone is unavailable/);
    assert.equal(f.requests.length,1);assert.equal(mic.context.state,'closed');assert.equal(f.timers.size,0);
  }
});
test('cancel before permission resolves stops a late microphone stream',async()=>{
  const f=fakeEnvironment({pending:true}),mic=new Microphone(()=>{},()=>{},f.env);
  const opening=mic.start();mic.cancel();f.grant();
  assert.equal(await opening,false);assert.ok(f.tracks.every(t=>t.stopped));
  assert.equal(f.timers.size,0);
});
test('worklet failure releases microphone and leaves no recording timer',async()=>{
  const f=fakeEnvironment({failModule:true}),mic=new Microphone(()=>{},()=>{},f.env);
  await assert.rejects(mic.start(),/worklet failed/);
  assert.ok(f.tracks.every(t=>t.stopped));assert.equal(f.timers.size,0);
});
test('permission timeout releases context and stops a stream granted later',async()=>{
  const f=fakeEnvironment({pending:true}),mic=new Microphone(()=>{},()=>{},f.env);
  const opening=mic.start();[...f.timers.values()].find(t=>t.ms===30000).fn();
  await assert.rejects(opening,/Microphone did not open/);
  f.grant();await Promise.resolve();
  assert.ok(f.tracks.every(t=>t.stopped));assert.equal(mic.context.state,'closed');
});
test('recording limit cannot capture beyond sixty seconds',async()=>{
  const f=fakeEnvironment();let completed;
  const mic=new Microphone(()=>{completed=mic.finish();},()=>{},f.env);
  await mic.start();mic.worklet.port.onmessage({data:new Float32Array(48000*61).fill(.1)});
  assert.equal(completed.size,1920044);assert.ok(f.tracks.every(t=>t.stopped));
});

test('live snapshots preserve capture and include the full growing prefix',async()=>{
  const f=fakeEnvironment(),mic=new Microphone(()=>{},()=>{},f.env);
  await mic.start();assert.equal(mic.snapshot(),null);
  mic.worklet.port.onmessage({data:new Float32Array(48000).fill(.1)});
  const first=mic.snapshot();
  mic.worklet.port.onmessage({data:new Float32Array(48000).fill(.2)});
  const second=mic.snapshot();
  assert.equal(first.size,32044);assert.equal(second.size,64044);
  assert.ok(f.tracks.every(t=>!t.stopped));assert.equal(mic.chunks.length,2);
  mic.cancel();assert.equal(mic.snapshot(),null);
});

function previewFixture(){
  const timers=new Map(),calls=[],updates=[],errors=[],cancels=[];let sequence=0;
  const env={crypto:{randomUUID:()=>`preview-${++sequence}`},AbortController,
    setTimeout:(fn,delay)=>{const id=++sequence;timers.set(id,{fn,delay});return id;},clearTimeout:id=>timers.delete(id)};
  const preview=new LiveTranscript({capture:{snapshot:()=>new Blob(['audio'])},env,
    recognize:(audio,id,signal)=>new Promise((resolve,reject)=>calls.push({id,signal,resolve,reject})),
    cancel:async id=>{cancels.push(id);},onText:r=>updates.push(r.text),onError:e=>errors.push(e.message)});
  return {preview,timers,calls,updates,errors,cancels};
}
test('live recognition never overlaps and replaces drafts with corrected full text',async()=>{
  const f=previewFixture();
  const first=f.preview.tick();f.preview.tick();assert.equal(f.calls.length,1);
  f.calls[0].resolve({text:'Hello, Max'});await first;
  const second=f.preview.tick();f.calls[1].resolve({text:'Hello, Mack. This is Bill.'});await second;
  assert.deepEqual(f.updates,['Hello, Max','Hello, Mack. This is Bill.']);
  await f.preview.stop();
});
test('finish drains the current draft while cancellation rejects stale updates',async()=>{
  const f=previewFixture();const current=f.preview.tick();
  let done=false;const finishing=f.preview.stop().then(()=>{done=true;});
  await Promise.resolve();assert.equal(done,false);assert.equal(f.calls[0].signal.aborted,false);
  f.preview.stop(true);assert.equal(f.calls[0].signal.aborted,true);
  f.calls[0].resolve({text:'This late text must not appear.'});await current;await finishing;
  assert.deepEqual(f.updates,[]);assert.deepEqual(f.cancels,[f.calls[0].id]);
  assert.equal(f.timers.size,0);
});
test('preview failure is visible, and a later update can recover',async()=>{
  const f=previewFixture();const failed=f.preview.tick();f.calls[0].reject(Error('Recognizer busy'));await failed;
  const next=f.preview.tick();f.calls[1].resolve({text:'Now working'});await next;
  assert.deepEqual(f.errors,['Recognizer busy']);assert.deepEqual(f.updates,['Now working']);
  await f.preview.stop();
});
