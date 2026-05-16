const runBtn = document.getElementById('runBtn');
const inputEl = document.getElementById('input');
const modeEl = document.getElementById('mode');
const outputEl = document.getElementById('output');
const loader = document.getElementById('loader');

function setLoading(on){
  if(on){loader.classList.remove('hidden');runBtn.disabled=true}else{loader.classList.add('hidden');runBtn.disabled=false}
}

async function run(){
  const prompt = inputEl.value.trim();
  const mode = modeEl.value;
  if(!prompt){alert('Please enter a prompt or code');return}
  setLoading(true);
  try{
    const resp = await fetch('/api/generate',{
      method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({prompt,mode})
    });
    const data = await resp.json();
    if(!resp.ok){outputEl.textContent = data.message || data.detail || 'Error';}
    else outputEl.textContent = data.code || data.content || JSON.stringify(data,null,2)||'';
  }catch(e){console.error(e);outputEl.textContent='Network error';}
  finally{setLoading(false)}
}

runBtn.addEventListener('click',run);
