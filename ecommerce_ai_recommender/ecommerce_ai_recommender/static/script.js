const runBtn = document.getElementById('runBtn');
const prefsEl = document.getElementById('prefs');
const respEl = document.getElementById('response');
const loader = document.getElementById('loader');

function setLoading(on){ if(on){loader.classList.remove('hidden');runBtn.disabled=true}else{loader.classList.add('hidden');runBtn.disabled=false} }

async function recommend(){
  const prefs = prefsEl.value.trim();
  if(!prefs){alert('Enter preferences');return}
  setLoading(true);
  try{
    const resp = await fetch('/api/recommend', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user_input:prefs})});
    const data = await resp.json();
    if(!resp.ok){respEl.textContent = data.message||data.detail||'Error'}else{respEl.textContent = data.recommendations||JSON.stringify(data,null,2)}
  }catch(e){console.error(e);respEl.textContent='Network error'}
  finally{setLoading(false)}
}

runBtn.addEventListener('click',recommend);
