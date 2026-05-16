const runBtn = document.getElementById('runBtn');
const inputEl = document.getElementById('text');
const outputEl = document.getElementById('output');
const loader = document.getElementById('loader');

function setLoading(on){ if(on){loader.classList.remove('hidden');runBtn.disabled=true}else{loader.classList.add('hidden');runBtn.disabled=false} }

async function proofread(){
  const text = inputEl.value.trim();
  if(!text){alert('Enter text');return}
  setLoading(true);
  try{
    const resp = await fetch('/api/proofread', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text})});
    const data = await resp.json();
    if(!resp.ok){outputEl.textContent = data.message||data.detail||'Error'}else{outputEl.textContent = data.proofread||JSON.stringify(data,null,2)}
  }catch(e){console.error(e);outputEl.textContent='Network error'}
  finally{setLoading(false)}
}

runBtn.addEventListener('click',proofread);
