const runBtn = document.getElementById('runBtn');
const queryEl = document.getElementById('query');
const responseEl = document.getElementById('response');
const loader = document.getElementById('loader');

function setLoading(on){ if(on){loader.classList.remove('hidden');runBtn.disabled=true}else{loader.classList.add('hidden');runBtn.disabled=false} }

async function ask(){
  const q = queryEl.value.trim();
  if(!q){alert('Enter a question');return}
  setLoading(true);
  try{
    const resp = await fetch('/api/chat', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:q})});
    const data = await resp.json();
    if(!resp.ok){responseEl.textContent = data.message||data.detail||'Error'}else{responseEl.textContent = data.reply||JSON.stringify(data,null,2)}
  }catch(e){console.error(e);responseEl.textContent='Network error'}
  finally{setLoading(false)}
}

runBtn.addEventListener('click',ask);
