// Allow adding multiple “Split With” fields dynamically
window.addEventListener('DOMContentLoaded', () => {
  const addBtn = document.getElementById('addNameBtn');
  if (!addBtn) return; // Only present on split.html

  const container = document.getElementById('namesContainer');
  addBtn.addEventListener('click', () => {
    const idx = container.querySelectorAll('input[name="split_with"]').length;
    const wrapper = document.createElement('label');
    wrapper.innerHTML = `Split With
      <input type="text" name="split_with" placeholder="Name" required />`;
    container.appendChild(wrapper);
  });
});