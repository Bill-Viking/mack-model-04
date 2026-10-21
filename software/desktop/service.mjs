let token = '';

export async function connect() {
  const response = await fetch('/api/bootstrap', { cache: 'no-store' });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || 'Mack’s local service is unavailable.');
  token = data.token;
  return data.state;
}

export async function api(path, body, signal) {
  const response = await fetch('/api/' + path, {
    method: body === undefined ? 'GET' : 'POST', cache: 'no-store', signal,
    headers: { 'Content-Type': 'application/json', 'X-Mack-Token': token },
    ...(body === undefined ? {} : { body: JSON.stringify(body) })
  });
  let data;
  try { data = await response.json(); }
  catch { throw new Error('Mack’s local service returned an unreadable response.'); }
  if (!response.ok) throw new Error(data.error || 'Mack could not complete that request.');
  return data;
}

export async function speechAudio(body, signal) {
  const response = await fetch('/api/voice/speak', {
    method:'POST', cache:'no-store', signal,
    headers:{'Content-Type':'application/json','X-Mack-Token':token},
    body:JSON.stringify(body),
  });
  if (!response.ok) {
    let data;
    try { data = await response.json(); } catch { /* Keep a readable failure. */ }
    throw new Error(data?.error || 'Local voice could not finish.');
  }
  if (!response.headers.get('Content-Type')?.startsWith('audio/wav')) throw new Error('Local voice returned unreadable audio.');
  return response.blob();
}

export async function transcribeAudio(audio, id, signal) {
  const response=await fetch('/api/listening/transcribe',{
    method:'POST',cache:'no-store',signal,
    headers:{'Content-Type':'audio/wav','X-Mack-Token':token,'X-Mack-Request-Id':id},body:audio
  });
  const data=await response.json();
  if(!response.ok)throw new Error(data.error||'Local transcription failed.');
  return data;
}
