// Função para exibir imagens de uma página específica de um álbum
function showImages(album, pageNumber, pageSize) {
    $('#' + album + '-content .gallery-item').hide();
    var start = (pageNumber - 1) * pageSize;
    var end = start + pageSize;
    $('#' + album + '-content .gallery-item').slice(start, end).show();
}

// Função para criar links de paginação
function createPagination(album, pageSize) {
    var totalItems = $('#' + album + '-content .gallery-item').length;
    var totalPages = Math.ceil(totalItems / pageSize);
    var html = '';

    for (var i = 1; i <= totalPages; i++) {
        html += '<li class="page-item ' + (i === 1 ? 'active' : '') + '">';
        html += '<a class="page-link" href="#" onclick="navigateToPage(\'' + album + '\', ' + i + ')">' + i + '</a>';
        html += '</li>';
    }

    $('#pagination' + album.slice(-1)).html(html);
}

// Função para navegar para uma página específica
function navigateToPage(album, pageNumber) {
    showImages(album, pageNumber, 3); // Mostra 3 imagens por página
    $('#pagination' + album.slice(-1) + ' .page-item').removeClass('active');
    $('#pagination' + album.slice(-1) + ' .page-item').eq(pageNumber - 1).addClass('active');
}

// Inicialização da página inicial
$(document).ready(function() {
    createPagination('album1', 3);
    navigateToPage('album1', 1);

    createPagination('album2', 3);
    navigateToPage('album2', 1);

    createPagination('album3', 3);
    navigateToPage('album3', 1);
});
