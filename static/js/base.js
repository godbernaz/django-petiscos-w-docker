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

document.addEventListener('DOMContentLoaded', function () {
    function formatPostalCodeInput(input) {
        input.addEventListener('input', function () {
            let value = input.value.replace(/\D/g, ''); // Remove non-numeric characters
            if (value.length > 7) value = value.slice(0, 7);

            // Format as XXXX-XXX
            input.value = value.length > 4 
                ? value.slice(0, 4) + '-' + value.slice(4) 
                : value;
        });
    }

    function limitToDigits(input, maxLength) {
        input.addEventListener('input', function () {
            let value = input.value.replace(/\D/g, ''); // Remove non-numeric characters
            input.value = value.slice(0, maxLength);    // Limit length
        });
    }

    // Select and apply formatting to the Postcode field
    const postalCodeInput = document.querySelector('#id_postal_code');
    if (postalCodeInput) formatPostalCodeInput(postalCodeInput);

    // Select and apply validation to the TaxNumber field
    const nifInput = document.querySelector('#id_nif');
    if (nifInput) limitToDigits(nifInput, 9);

    // Selects and applies validation to the Phone Number field
    const phoneInput = document.querySelector('#id_phone');
    if (phoneInput) limitToDigits(phoneInput, 9);
});