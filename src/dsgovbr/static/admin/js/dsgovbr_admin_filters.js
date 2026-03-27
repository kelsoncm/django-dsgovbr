// dsgovbr_admin_filters.js

// dsgovbr_admin_filters.js
// Garante execução após DOM pronto, usando jQuery do admin
window.dsgovbrAdminFiltersInit = function() {
    console.log('DSGovBR Admin Filters Initialized2');
    var filterBtn = document.getElementById('button-input-filter');
    var filterBar = document.getElementById('filter-bar');
    var filterDismissBtn = filterBar ? filterBar.querySelector('[data-dismiss="filter"]') : null;
    if (filterBtn && filterBar) {
        filterBtn.addEventListener('click', function() {
            filterBar.hidden = false;
            filterBar.classList.add('active');
            // Optional: close search-bar if open
            var searchBar = document.querySelector('.search-bar');
            if (searchBar) searchBar.hidden = true;
        });
    }
    if (filterDismissBtn && filterBar) {
        filterDismissBtn.addEventListener('click', function() {
            filterBar.hidden = true;
            filterBar.classList.remove('active');
        });
    }

    // --- Filtros DSGovBR ---
    var tagsContainer = document.getElementById('dsgovbr-filter-tags');
    var form = document.getElementById('dsgovbr-filter-form');
    var filterApplyBtn = document.getElementById('dsgovbr-filter-apply');
    // Debug: forçar display dos containers
    if (tagsContainer) tagsContainer.style.display = 'flex';
    if (form) form.style.display = 'block';
    console.log('tagsContainer:', tagsContainer, 'form:', form);

    // Event delegation para .filter_choice
    var filterNav = document.getElementById('changelist-filter');
    if (filterNav) {
        filterNav.addEventListener('click', function(e) {
            // Garante que o clique veio de um .filter_choice ou filho
            var el = e.target;
            while (el && !el.classList.contains('filter_choice')) {
                if (el === filterNav) return; // saiu do nav, não achou
                el = el.parentElement;
            }
            if (!el || !el.classList.contains('filter_choice')) return;
            e.preventDefault();
            var btn = el;
            var fieldName = btn.getAttribute('data-field-name');
            var fieldTitle = btn.getAttribute('data-field-title');
            var value = btn.getAttribute('data-value');
            var display = btn.getAttribute('data-display');
            console.log('Filtro clicado:', fieldName, value, display);
            if (!fieldName || !value) return;

            // Remove tag/input anterior desse campo (permite só um valor por campo)
            var oldTag = tagsContainer.querySelector('.br-tag[data-field-name="' + fieldName + '"]');
            if (oldTag) oldTag.remove();
            var oldInput = form.querySelector('input[name="' + fieldName + '"]');
            if (oldInput) oldInput.remove();

            // Cria tag DSGovBR
            var tag = document.createElement('div');
            tag.className = 'br-tag';
            tag.setAttribute('data-field-name', fieldName);
            tag.innerHTML = '<span class="br-tag__text">' + fieldTitle + ': ' + display + '</span>' +
                '<button type="button" class="br-tag__close" aria-label="Remover filtro">&times;</button>';
            tagsContainer.appendChild(tag);
            console.log('Tag criada:', tag.outerHTML);

            // Cria input hidden
            var input = document.createElement('input');
            input.type = 'hidden';
            input.name = fieldName;
            input.value = value;
            form.appendChild(input);
            console.log('Input criado:', input.outerHTML);

            // Handler para remover tag/input
            tag.querySelector('.br-tag__close').addEventListener('click', function() {
                var btn = el;
                var fieldName = btn.getAttribute('data-field-name');
                var fieldTitle = btn.getAttribute('data-field-title');
                var value = btn.getAttribute('data-value');
                var display = btn.getAttribute('data-display');
                console.log('Filtro clicado:', fieldName, value, display);
                if (!fieldName || !value) return;

                if (!tagsContainer) {
                    console.error('tagsContainer não encontrado!');
                    return;
                }
                if (!form) {
                    console.error('form não encontrado!');
                    return;
                }

                // Remove tag/input anterior desse campo (permite só um valor por campo)
                var oldTag = tagsContainer.querySelector('.br-tag[data-field-name="' + fieldName + '"]');
                if (oldTag) {
                    oldTag.remove();
                    console.log('Tag antiga removida');
                }
                var oldInput = form.querySelector('input[name="' + fieldName + '"]');
                if (oldInput) {
                    oldInput.remove();
                    console.log('Input antigo removido');
                }

                // Cria tag DSGovBR
                var tag = document.createElement('div');
                tag.className = 'br-tag';
                tag.setAttribute('data-field-name', fieldName);
                tag.innerHTML = '<span class="br-tag__text">' + fieldTitle + ': ' + display + '</span>' +
                    '<button type="button" class="br-tag__close" aria-label="Remover filtro">&times;</button>';
                tagsContainer.appendChild(tag);
                console.log('Tag criada:', tag.outerHTML);

                // Cria input hidden
                var input = document.createElement('input');
                input.type = 'hidden';
                input.name = fieldName;
                input.value = value;
                form.appendChild(input);
                console.log('Input criado:', input.outerHTML);

                // Handler para remover tag/input
                tag.querySelector('.br-tag__close').addEventListener('click', function() {
                    tag.remove();
                    input.remove();
                    console.log('Tag e input removidos');
                });
}