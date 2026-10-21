import test from 'node:test';
import assert from 'node:assert/strict';
import { readState, moveNote, replyTo } from '../software/desktop/model.mjs';

test('saved notes round-trip without executing or changing their text', () => {
  const state=readState(null);
  state.notes.push({id:'one',text:'<img src=x onerror=alert(1)> & tea',created:'2026-10-20'});
  assert.deepEqual(readState(JSON.stringify(state)),state);
});
test('corrupt or newer saved data is refused instead of silently overwritten', () => {
  for (const raw of ['{','null',JSON.stringify({version:2,notes:[],trash:[]}),JSON.stringify({version:1,notes:[{id:'x'}],trash:[]})]) {
    assert.throws(()=>readState(raw));
  }
});
test('duplicate identifiers cannot remove a different note', () => {
  const note={id:'x',text:'Keep me'};
  assert.throws(()=>readState(JSON.stringify({version:1,notes:[note],trash:[note]})));
});
test('oversized saved collections are refused rather than silently truncated', () => {
  const state=readState(null);state.notes=Array.from({length:101},(_,i)=>({id:String(i),text:'keep'}));
  assert.throws(()=>readState(JSON.stringify(state)));
});
test('Trash moves are reversible and do not mutate the previous state', () => {
  const original=readState(null);original.notes.push({id:'one',text:'I like jazz',created:''});
  const trashed=moveNote(original,'one','trash');
  assert.equal(original.notes.length,1);assert.equal(trashed.notes.length,0);assert.equal(trashed.trash.length,1);
  assert.deepEqual(moveNote(trashed,'one','notes'),original);
  assert.equal(moveNote(original,'missing','trash'),original);
});
test('a full destination keeps the source note', () => {
  const state=readState(null);state.notes=[{id:'keep',text:'keep'}];state.trash=Array.from({length:100},(_,i)=>({id:String(i),text:'old'}));
  assert.equal(moveNote(state,'keep','trash'),state);
});
test('only explicit remember requests propose saved memory', () => {
  assert.equal(replyTo('Remember that I like jazz',[]).note,'I like jazz');
  assert.equal(replyTo('remember: my cat is named Ada',[]).note,'my cat is named Ada');
  assert.equal(replyTo('What do you remember?',[]).note,undefined);
  assert.equal(replyTo('Do you remember that I like jazz?',[]).note,undefined);
  assert.equal(replyTo('hello',[]).note,undefined);
});
test('recall comes from supplied notes and unknown prompts disclose the preview', () => {
  assert.match(replyTo('What do you remember?',[{text:'I like jazz'}]).text,/I like jazz/);
  assert.match(replyTo('Explain quantum gravity',[]).text,/local preview/);
  assert.match(replyTo('Can you walk?',[]).text,/not connected to motors/);
});
