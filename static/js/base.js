// static/js/base.js 

// templates/carts/cart_detail.html
// CRUD functionality for Cart
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

// Remove Meals from the cart and update the quantity and badge.
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

// Updates the quantity for the cart and badge.
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

// templates/account/profile.html
// Makes the form for Adress and Receipt only visible when toggled by the user. 
function toggleAddressForm() {
    var form = document.getElementById('address-form');
    if (form.style.display === 'none') {
        form.style.display = 'block';
    } else {
        form.style.display = 'none';
    }
}

// For the Zip Code field. Formatted for Portuguese ZipCode.
document.addEventListener('DOMContentLoaded', function() {
    var postalCodeInput = document.querySelector('#id_postal_code');

    postalCodeInput.addEventListener('input', function(e) {
        var value = postalCodeInput.value.replace(/\D/g, ''); // Remove non-numeric characters
        if (value.length > 7) {
            value = value.slice(0, 7);
        }

        if (value.length > 4) {
            postalCodeInput.value = value.slice(0, 4) + '-' + value.slice(4);
        } else {
            postalCodeInput.value = value;
        }
    });
});

// For the NIF (Portuguese stuff)
document.addEventListener('DOMContentLoaded', function () {
    var nifInput = document.querySelector('#id_nif');
    
    nifInput.addEventListener('input', function (event) {
        // Remove any non-digit characters
        var value = event.target.value.replace(/\D/g, '');

        // Limit to 9 digits
        if (value.length > 9) {
            value = value.slice(0, 9);
        }

        event.target.value = value;
    });
});