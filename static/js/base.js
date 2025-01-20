// static/js/base.js 

// CART | CRUD(Create, Read, Update, Delete) 
// Js/Ajax for add meals to cart
$(document).ready(function() {
    $('#add-to-cart-form').on('submit', function(event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),  // Ensures that the form URL is used
            data: $(this).serialize(),
            success: function(response) {
                alert(response.message);  
                $('#cart-badge').text(response.cart_quantity);  // Updates the badge with the amount
            },
            error: function() {
                alert('Ocorreu um erro ao adicionar ao carrinho.');
            }
        });
    });
});

// Js/Ajax for remove meals from the cart
$(document).on('click', '.remove-from-cart-btn', function(event) {
    event.preventDefault();
    const mealId = $(this).data('meal-id');

    $.ajax({
        type: 'POST',
        url: '/carts/delete/',
        data: {
            'meal_id': mealId,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(response) {
            alert(response.message);
            $('#cart-badge').text(response.cart_quantity);  // Updates the badge with the amount
            location.reload();  // Reloads the page to update the list
        },
        error: function() {
            alert('Ocorreu um erro ao remover a refeição do carrinho.');
        }
    });
});

// Js/Ajax for update the number of meals in the cart
$(document).on('click', '.update-quantity-btn', function(event) {
    event.preventDefault();
    const mealId = $(this).data('meal-id');
    const action = $(this).data('action');

    $.ajax({
        type: 'POST',
        url: '/carts/update/',
        data: {
            'meal_id': mealId,
            'action': action,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(response) {
            alert(response.message);
            location.reload();
        },
        error: function() {
            alert('Ocorreu um erro ao atualizar a quantidade.');
        }
    });
});