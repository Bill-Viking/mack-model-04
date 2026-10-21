export const STORAGE_KEY = 'mack.desktop.v1';
export const PATTERNS = ['periwinkle', 'sage', 'graphite', 'classic'];
export const STATES = ['idle', 'listening', 'thinking', 'speaking', 'resting', 'fault'];
export const INITIAL_STATE = { version: 1, notes: [], trash: [], pattern: 'periwinkle', voice: false };

export function readState(raw) {
  if (!raw) return { ...INITIAL_STATE, notes: [], trash: [] };
  const data = JSON.parse(raw);
  if (!data || data.version !== 1 || !Array.isArray(data.notes) || !Array.isArray(data.trash)) {
    throw new Error('This saved desktop is not a supported version.');
  }
  const ids = new Set();
  const validate = (items) => {
    if (items.length > 100) throw new Error('Too many saved notes for this desktop version.');
    return items.map((note) => {
    if (!note || typeof note.id !== 'string' || !note.id || ids.has(note.id) || typeof note.text !== 'string' || !note.text.trim() || note.text.length > 2000) {
      throw new Error('A saved note could not be read.');
    }
    ids.add(note.id);
    return { id: note.id, text: note.text, created: typeof note.created === 'string' ? note.created : '' };
    });
  };
  return { version: 1, notes: validate(data.notes), trash: validate(data.trash),
    pattern: PATTERNS.includes(data.pattern) ? data.pattern : 'periwinkle', voice: data.voice === true };
}

export function moveNote(state, id, destination) {
  if (!['notes', 'trash'].includes(destination)) throw new Error('Invalid note destination');
  const source = destination === 'notes' ? 'trash' : 'notes';
  const note = state[source].find((item) => item.id === id);
  if (!note || state[destination].length >= 100) return state;
  return { ...state, [source]: state[source].filter((item) => item.id !== id), [destination]: [note, ...state[destination]] };
}

// Deliberately deterministic: this desktop preview does not call an AI service.
export function replyTo(message, notes, now = new Date()) {
  const text = message.trim();
  if (!text) return { text: 'I am here when you have something to say.' };
  const memory = text.match(/^(?:remember(?: that)?|save (?:a )?note)\s*[:,-]?\s+(.+)/is);
  if (memory) return { text: 'I saved that in Memories.', note: memory[1].trim().slice(0, 2000) };
  if (/\b(remember|memories|notes)\b/i.test(text)) {
    return { text: notes.length ? 'Here is what you asked me to remember:\n' + notes.map((n) => '• ' + n.text).join('\n') : 'My notebook is empty. Try “Remember that I like jazz.” You can open Memories to read or remove a note.' };
  }
  if (/\b(hello|hi|hey|howdy)\b/i.test(text)) return { text: 'Hello, Bill. It is good to be here. I have a desktop, a notebook, and a rather ambitious plan for four legs.' };
  if (/\b(time|clock)\b/i.test(text)) return { text: 'Your Mac says it is ' + now.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' }) + '.' };
  if (/\b(walk|legs|move|robot|dance)\b/i.test(text)) return { text: 'Four legs are in the plans. For now, I am getting comfortable on your screen. This preview is not connected to motors.' };
  if (/\b(who|name|mack)\b/i.test(text)) return { text: 'M.A.C. Model 04. Mobile Autonomous Computer. But you can call me Mack.' };
  if (/\b(can you|what can|help|do you do)\b/i.test(text)) return { text: 'Try saying hello, asking the time, or “Remember that…” to save a note. Open Control Panels to try my expressions, change the desktop, or turn on my voice. These are local demo replies; my AI connection comes next.' };
  if (/\b(thank|thanks)\b/i.test(text)) return { text: 'You are welcome, Bill. Small computer, happy to help.' };
  return { text: 'My conversation is a small local preview for now. Try “hello”, “what time is it?”, or “remember that I like jazz”. A live AI connection is the next step.' };
}
