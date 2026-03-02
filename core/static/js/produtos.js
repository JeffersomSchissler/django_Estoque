/**
 * Produtos - JavaScript
 * Funções para manipulação de modais e interações HTMX
 */

function openModal(id, nome) {
  document.getElementById('modal-product-name').textContent = '"' + nome + '"';
  const btn = document.getElementById('modal-delete-btn');
  btn.setAttribute('hx-delete', '/produtos/' + id + '/excluir/');
  btn.setAttribute('hx-target', '#row-' + id);
  htmx.process(btn); // re-processa os atributos hx-* após alteração dinâmica
  document.getElementById('delete-modal').classList.add('open');
}

function closeModal() {
  document.getElementById('delete-modal').classList.remove('open');
}

// Fecha ao clicar fora do modal
document.getElementById('delete-modal').addEventListener('click', function(e) {
  if (e.target === this) closeModal();
});

// Suporte a fechamento com ESC
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') closeModal();
});
