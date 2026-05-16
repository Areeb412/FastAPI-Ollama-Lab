const runBtn = document.getElementById('runBtn');
const symptomsEl = document.getElementById('symptoms');
const respEl = document.getElementById('response');
const loader = document.getElementById('loader');

function setLoading(on){ if(on){loader.classList.remove('hidden');runBtn.disabled=true}else{loader.classList.add('hidden');runBtn.disabled=false} }

async function analyze(){
  const symptoms = symptomsEl.value.trim();
  if(!symptoms){alert('Enter symptoms');return}
  setLoading(true);
  try{
    const resp = await fetch('/api/diagnose', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({symptoms})});
    const data = await resp.json();
    if(!resp.ok){respEl.textContent = data.message||data.detail||'Error'}else{respEl.textContent = data.diagnosis||JSON.stringify(data,null,2)}
  }catch(e){console.error(e);respEl.textContent='Network error'}
  finally{setLoading(false)}
}

runBtn.addEventListener('click',analyze);
