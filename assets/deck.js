"use strict";
async function copyCode(id, button){
 const node=document.getElementById(id);
 const target=button.parentElement.querySelector('.status');
 if(!node){if(target)target.textContent='Command missing';return}
 const text=node.textContent.trim();let copied=false;
 try{if(navigator.clipboard && window.isSecureContext){await navigator.clipboard.writeText(text);copied=true}}catch(e){}
 if(!copied){
  const area=document.createElement('textarea'); area.value=text;area.setAttribute('readonly','');area.style.position='fixed';area.style.left='-9999px';document.body.appendChild(area);area.select();
  try{copied=document.execCommand('copy')}catch(e){} area.remove();
 }
 if(target)target.textContent=copied?'Copied real command':'Copy blocked; select the command manually';
}
document.addEventListener('click',e=>{const b=e.target.closest('[data-copy]');if(b){copyCode(b.dataset.copy,b)}});
