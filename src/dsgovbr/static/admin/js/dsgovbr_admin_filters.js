window.dsgovbrAdminFiltersInit = function() {
    var filterBtn = document.getElementById('button-input-filter');
    var filterBar = document.getElementById('filter-bar');


    var filterDismissBtn = filterBar ? filterBar.querySelector('[data-dismiss="filter"]') : null;
    if (filterBtn && filterBar) {
        filterBtn.addEventListener('click', function() {
            filterBar.hidden = false;
            filterBar.classList.add('active');
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
    var tagsContainer = document.getElementById('filter-tags');
    var form = document.getElementById('changelist-form');
    if (tagsContainer) tagsContainer.style.display = 'flex';
    if (form) form.style.display = 'block';

    // Event delegation para .filter_choice
    var filterNav = document.getElementById('changelist-filter');
    if (filterNav) {
        filterNav.addEventListener('click', function(e) {
            e.preventDefault();
            var el = e.target;
            while (el && !el.classList.contains('filter_choice')) {
                if (el === filterNav) return;
                el = el.parentElement;
            }
            if (!el || !el.classList.contains('filter_choice')) return;
            var fieldName = el.getAttribute('data-field-name');
            var fieldTitle = el.getAttribute('data-field-title');
            var value = el.getAttribute('data-value');
            var display = el.getAttribute('data-display');
            if (!fieldName || !value) {
                return;
            };

            var tag = document.createElement('span');
            tag.className = 'br-tag interaction small';
            tag.setAttribute('data-field-name', fieldName);
            tag.setAttribute('style', "padding-right: 0;");
            tag.innerHTML = '<span class="br-tag__text">' + fieldTitle + ': ' + display + '</span>' +
            '<button class="br-button inverted" type="button" aria-label="Fechar" aria-describedby="interactivetag1" data-dismiss="interaction01"><i class="fas fa-times" aria-hidden="true"></i></button>';
            tagsContainer.appendChild(tag);

            var input = document.createElement('input');
            input.type = 'hidden';
            input.name = fieldName;
            input.value = value;
            form.appendChild(input);

            tag.querySelector('.br-tag__close').addEventListener('click', function() {
                var fieldName = el.getAttribute('data-field-name');
                var fieldTitle = el.getAttribute('data-field-title');
                var value = el.getAttribute('data-value');
                var display = el.getAttribute('data-display');
                if (!fieldName || !value) return;

                if (!tagsContainer) {
                    return;
                }
                if (!form) {
                    return;
                }

                var oldTag = tagsContainer.querySelector('.br-tag[data-field-name="' + fieldName + '"]');
                if (oldTag) {
                    oldTag.remove();
                }
                var oldInput = form.querySelector('input[name="' + fieldName + '"]');
                if (oldInput) {
                    oldInput.remove();
                }

                var tag = document.createElement('div');
                tag.className = 'br-tag';
                tag.setAttribute('data-field-name', fieldName);
                tag.innerHTML = '<span class="br-tag__text">' + fieldTitle + ': ' + display + '</span>' +
                    '<button type="button" class="br-tag__close" aria-label="Remover filtro">&times;</button>';
                tagsContainer.appendChild(tag);

                var input = document.createElement('input');
                input.type = 'hidden';
                input.name = fieldName;
                input.value = value;
                form.appendChild(input);

                tag.querySelector('.br-tag__close').addEventListener('click', function() {
                    tag.remove();
                    input.remove();
                });
            });
        });
    }
}

// Inicializa automaticamente ao carregar o script
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', window.dsgovbrAdminFiltersInit);
} else {
    window.dsgovbrAdminFiltersInit();
}