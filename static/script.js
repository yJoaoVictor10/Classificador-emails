
const form = document.getElementById('form');
const fileInput = document.getElementById('email_file');
const textArea = document.getElementById('email_text');


fileInput.addEventListener('change', ()=>{
if(fileInput.files.length){
textArea.disabled = true;
textArea.placeholder = 'Arquivo selecionado — o texto do arquivo será usado.';
} else {
textArea.disabled = false;
textArea.placeholder = 'Cole o conteúdo do email...';
}
});