import test from 'node:test';
import assert from 'node:assert/strict';
import { chooseVoice, readDelivery, DEFAULT_DELIVERY, speechChunks } from '../software/desktop/voice.mjs';

const local = (name, lang='en-US') => ({name, lang, voiceURI:name, localService:true});

test('automatic delivery prefers an available local Samantha over the old male fallback', () => {
  const samantha=local('Samantha (English (US))');
  assert.equal(chooseVoice([local('Daniel','en-GB'),samantha]),samantha);
});
test('neither an explicit choice nor automatic fallback can select an online voice', () => {
  const remote={...local('Samantha'),localService:false};
  assert.equal(chooseVoice([remote]),null);
  assert.equal(chooseVoice([remote,local('Karen')],'Samantha'),null);
});
test('a missing saved voice does not silently change the character voice', () => {
  assert.equal(chooseVoice([local('Samantha')],'Ava'),null);
  assert.equal(chooseVoice([local('Daniel')],'Daniel').name,'Daniel');
  assert.equal(chooseVoice([local('Anna','de-DE')]),null);
});
test('old and malformed browser preferences keep usable delivery defaults', () => {
  for(const value of [null,undefined,[],{}, {rate:'fast',pitch:Infinity,voiceURI:34}]) {
    assert.deepEqual(readDelivery(value),DEFAULT_DELIVERY);
  }
  assert.deepEqual(readDelivery({rate:-3,pitch:40,voiceURI:'local'}),{rate:0.7,pitch:1.2,voiceURI:'local',engine:'reference',style:'film'});
});
test('reference selection survives preferences; unknown engines cannot select a network path',()=>{
  assert.equal(readDelivery({engine:'reference'}).engine,'reference');
  assert.equal(readDelivery({engine:'https://remote.example'}).engine,'reference');
  assert.equal(readDelivery({style:'film'}).style,'film');
  assert.equal(readDelivery({style:'unavailable'}).style,'film');
});
test('fresh preferences use the approved voice while explicit alternatives survive reload',()=>{
  assert.equal(readDelivery().engine,'reference');
  assert.equal(readDelivery().style,'film');
  const alternative=readDelivery({engine:'browser',style:'natural'});
  assert.equal(readDelivery(JSON.parse(JSON.stringify(alternative))).engine,'browser');
  assert.equal(readDelivery(alternative).style,'natural');
});
test('long replies are spoken in bounded chunks without losing words',()=>{
  const text=('One complete sentence. Another thought follows. ').repeat(50).trim();
  const chunks=speechChunks(text);
  assert.ok(chunks.length>1);
  assert.ok(chunks.every(c=>c.length<=600));
  assert.equal(chunks.join(' '),text);
  assert.deepEqual(speechChunks(''),[]);
  assert.deepEqual(speechChunks('x'.repeat(1300)).map(c=>c.length),[600,600,100]);
});
