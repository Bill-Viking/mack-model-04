// Delivery settings are separate from Mack's identity, model, and saved memories.
export const DEFAULT_DELIVERY = Object.freeze({ voiceURI: '', rate: 0.88, pitch: 0.98, engine: 'browser', style: 'natural' });
export const AUDITION = "Hello. I'm Mack. We can take this one step at a time. If I am not certain, I will tell you.";

export function readDelivery(value) {
  const source = value && typeof value === 'object' ? value : {};
  const bounded = (key, low, high) => typeof source[key] === 'number' && Number.isFinite(source[key])
    ? Math.max(low, Math.min(high, source[key])) : DEFAULT_DELIVERY[key];
  return {
    voiceURI: typeof source.voiceURI === 'string' ? source.voiceURI.slice(0, 500) : '',
    rate: bounded('rate', 0.7, 1.1), pitch: bounded('pitch', 0.8, 1.2),
    engine: source.engine === 'reference' ? 'reference' : 'browser',
    style: source.style === 'film' ? 'film' : 'natural',
  };
}

export function speechChunks(text, limit=600) {
  const chunks=[];
  let remaining=text.trim();
  while(remaining.length>limit) {
    const head=remaining.slice(0,limit+1);
    const boundary=Math.max(head.lastIndexOf('. '),head.lastIndexOf('? '),head.lastIndexOf('! '));
    const end=boundary>limit/3?boundary+1:head.lastIndexOf(' ');
    const cut=end>0?end:limit;
    chunks.push(remaining.slice(0,cut).trim());remaining=remaining.slice(cut).trim();
  }
  if(remaining)chunks.push(remaining);
  return chunks;
}

export function chooseVoice(voices, preferredURI = '') {
  const local = voices.filter((voice) => voice.localService === true);
  if (preferredURI) return local.find((voice) => voice.voiceURI === preferredURI) || null;
  const english = local.filter((voice) => /^en(?:[-_]|$)/i.test(voice.lang));
  for (const name of ['Samantha', 'Ava', 'Allison', 'Susan', 'Victoria', 'Karen', 'Moira']) {
    const preferred = english.find((voice) => voice.name.includes(name));
    if (preferred) return preferred;
  }
  return english[0] || null;
}
