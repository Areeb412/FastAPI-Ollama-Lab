const runBtn = document.getElementById('runBtn');
const urlEl = document.getElementById('url');
const summaryEl = document.getElementById('summary');
const loader = document.getElementById('loader');

function setLoading(on){ if(on){loader.classList.remove('hidden');runBtn.disabled=true}else{loader.classList.add('hidden');runBtn.disabled=false} }

async function summarize(){
  const url = urlEl.value.trim();
  if(!url){alert('Enter an article URL');return}
  setLoading(true);
  try{
    const resp = await fetch('/api/summarize', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url})});
    const data = await resp.json();
    if(!resp.ok){summaryEl.textContent = data.message||data.detail||'Error'}else{summaryEl.textContent = data.summary||JSON.stringify(data,null,2)}
  }catch(e){console.error(e);summaryEl.textContent='Network error'}
  finally{setLoading(false)}
}

runBtn.addEventListener('click',summarize);
