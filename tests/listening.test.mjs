import test from 'node:test';
import assert from 'node:assert/strict';
import {encodeWav,Microphone} from '../software/desktop/listening.mjs';

function fakeEnvironment({pending=false,failModule=false}={}){
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
  return {tracks,timers,grant:()=>grant(stream),
    env:{navigator:{mediaDevices:{getUserMedia:()=>pending?new Promise(resolve=>grant=resolve):Promise.resolve(stream)}},
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
