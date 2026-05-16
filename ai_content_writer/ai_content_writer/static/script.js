const genBtn = document.getElementById('genBtn');
const topicEl = document.getElementById('topic');
const toneEl = document.getElementById('tone');
const outputEl = document.getElementById('output');
const loader = document.getElementById('loader');

function setLoading(on){ if(on){loader.classList.remove('hidden');genBtn.disabled=true}else{loader.classList.add('hidden');genBtn.disabled=false} }

async function generate(){
  const prompt = topicEl.value.trim();
  const tone = toneEl.value;
  if(!prompt){alert('Enter a topic');return}
  setLoading(true);
  try{
    const resp = await fetch('/api/generate', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({prompt:`Write a ${tone} article about: ${prompt}`})});
    const data = await resp.json();
    if(!resp.ok){outputEl.textContent = data.message||data.detail||'Error'}else{outputEl.textContent = data.content||data.summary||JSON.stringify(data,null,2)}
  }catch(e){console.error(e);outputEl.textContent='Network error'}
  finally{setLoading(false)}
}

genBtn.addEventListener('click',generate);
