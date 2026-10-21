import test from 'node:test';
import assert from 'node:assert/strict';
import { chooseVoice, readDelivery, DEFAULT_DELIVERY } from '../software/desktop/voice.mjs';

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
  assert.deepEqual(readDelivery({rate:-3,pitch:40,voiceURI:'local'}),{rate:0.7,pitch:1.2,voiceURI:'local'});
});
