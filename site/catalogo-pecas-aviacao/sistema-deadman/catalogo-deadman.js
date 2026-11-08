(function(){
  const root = document.querySelector('.fts-catalogo-embed');
  if(!root || root.dataset.filtersReady === 'true') return;
  root.dataset.filtersReady = 'true';

  const grid = root.querySelector('.fts-grid');
  const cards = Array.from(root.querySelectorAll('.fts-card'));
  const search = root.querySelector('#fts-search-input');
  const clearSearch = root.querySelector('.fts-search__clear');
  const sort = root.querySelector('#fts-sort');
  const chips = Array.from(root.querySelectorAll('.fts-chip'));
  const resetButtons = Array.from(root.querySelectorAll('.fts-reset, .fts-no-results__reset'));
  const resultCount = root.querySelector('#fts-result-count');
  const noResults = root.querySelector('.fts-no-results');

  let activeFilter = 'all';

  const normalize = (value) => (value || '')
    .toLocaleLowerCase('pt-BR')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .trim();

  cards.forEach(card => {
    card.dataset.normalizedSearch = normalize(card.dataset.search);
    card.dataset.normalizedTitle = normalize(card.dataset.title);
  });

  function sortCards(){
    const mode = sort.value;
    const ordered = [...cards].sort((a,b) => {
      if(mode === 'az') return a.dataset.normalizedTitle.localeCompare(b.dataset.normalizedTitle, 'pt-BR');
      if(mode === 'za') return b.dataset.normalizedTitle.localeCompare(a.dataset.normalizedTitle, 'pt-BR');
      return Number(a.dataset.index) - Number(b.dataset.index);
    });
    ordered.forEach(card => grid.appendChild(card));
  }

  function applyFilters(){
    const term = normalize(search.value);
    let visible = 0;

    cards.forEach(card => {
      const matchesCategory = activeFilter === 'all' || card.dataset.category === activeFilter;
      const matchesSearch = !term || card.dataset.normalizedSearch.includes(term);
      const show = matchesCategory && matchesSearch;

      card.hidden = !show;
      card.classList.remove('fts-enter');

      if(show){
        visible++;
        requestAnimationFrame(() => card.classList.add('fts-enter'));
      }
    });

    resultCount.textContent = visible === 1
      ? '1 produto encontrado'
      : visible + ' produtos encontrados';

    noResults.hidden = visible !== 0;
    grid.hidden = visible === 0;
    clearSearch.classList.toggle('is-visible', search.value.length > 0);
  }

  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      activeFilter = chip.dataset.filter;
      chips.forEach(item => {
        const selected = item === chip;
        item.classList.toggle('is-active', selected);
        item.setAttribute('aria-pressed', selected ? 'true' : 'false');
      });
      applyFilters();
    });
  });

  search.addEventListener('input', applyFilters);

  clearSearch.addEventListener('click', () => {
    search.value = '';
    search.focus();
    applyFilters();
  });

  sort.addEventListener('change', () => {
    sortCards();
    applyFilters();
  });

  resetButtons.forEach(button => {
    button.addEventListener('click', () => {
      activeFilter = 'all';
      search.value = '';
      sort.value = 'original';
      chips.forEach(chip => {
        const selected = chip.dataset.filter === 'all';
        chip.classList.toggle('is-active', selected);
        chip.setAttribute('aria-pressed', selected ? 'true' : 'false');
      });
      sortCards();
      applyFilters();
      search.focus({preventScroll:true});
    });
  });

  sortCards();
  applyFilters();
})();
