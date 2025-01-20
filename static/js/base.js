// static/js/base.js 

// JavaScript CRUD do carrinho #Create, Read, Update, Delete.
// Adicionar refeições ao carrinho cart
$(document).ready(function() {
    $('#add-to-cart-form').on('submit', function(event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),  // Garante que a URL do formulário é usada
            data: $(this).serialize(),
            success: function(response) {
                alert(response.message);  // Mostra uma mensagem de sucesso
                $('#cart-badge').text(response.cart_quantity);  // Atualiza a badge com a quantidade
            },
            error: function() {
                alert('Ocorreu um erro ao adicionar ao carrinho.');
            }
        });
    });
});