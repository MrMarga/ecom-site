const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

// Form submission for adding reviews
$("#commentForm").submit(function (e) {
    e.preventDefault(); // prevents the form from refreshing the page

    let dt = new Date();
    let time = (dt.getDay() + 1) + " " + monthNames[dt.getUTCMonth()] + ", " + dt.getUTCFullYear();

    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr('action'),
        dataType: "json",
        success: function (response) {
            console.log("Review Added..!!");

            if (response.bool == true) {
                $("#review-alert").html("Review Added");
                $(".hide-comment").hide();

                // Format the date

                // Construct the new review HTML
                let newReview = '<div class="media mb-4">';
                newReview += '<img src="img/user.jpg" alt="Image" class="img-fluid mr-3 mt-1" style="width: 45px;">';
                newReview += '<div class="media-body">';
                newReview += '<h6>' + response.context.user + '<small> - <i>' + time + '</i></small></h6>';


                for (let i = 0; i < response.context.rating; i++) {
                    newReview += '<i class="fas fa-star text-warning"></i>';
                }

                newReview += '<div class="text-primary mb-2">';
                newReview += '<p>' + response.context.review + '</p>';

                newReview += '</div>';
                newReview += '</div>';
                newReview += '</div>';
                // Prepend the new review to the existing reviews
                $(".review-list").prepend(newReview);
            }
        }
    });
});

//-------------------------Add to Cart-----------------------------------//

// Adding products to cart
$(".add-to-cart-btn").on("click", function () {
    "use strict"; // Add strict mode here

    let this_val = $(this);
    let index = this_val.attr("data-index");

    // Use the class to select the correct quantity input
    let product_quantity_input = $(".product-quantity-input[data-product-id='" + index + "']");
    
    // Get the value from the quantity input
    let product_quantity = product_quantity_input.val();

    // Convert quantity to a number, defaulting to 1 if not a valid number
    let quantity = parseInt(product_quantity, 10) || 1;

    // Retrieve other product information
    let product_title = $(".product-title-" + index).val();
    let product_id = $(".product-id-" + index).val();
    let price_as_float = $(".current-product-price-" + index).text();
    let product_price = parseFloat(price_as_float);
    let product_pid = $(".product-pid-" + index).val();
    let product_image = $(".product-image-" + index).val();

    console.log("Quantity:", quantity);
    console.log("Title:", product_title);
    console.log("ID:", product_id);
    console.log("Price:", product_price);
    console.log("PID:", product_pid);
    console.log("Image:", product_image);
    console.log("Index:", index);
    console.log("Current Element:", this_val);

    $.ajax({
        url: '/add-to-cart',
        data: {
            'id': product_id,
            'pid': product_pid,
            'qty': quantity,
            'title': product_title,
            'price': product_price,
            'image': product_image,
        },
        dataType: 'json',
        beforeSend: function () {
            console.log("Adding Products to Cart.");
        },
        success: function (res) {
            this_val.html("✓");
            console.log("Added Product to cart.");
            console.log("AJAX Response:", res);
            $(".cart-items-count").text(res.totalcartitems); // Update cart count in real-time
            $('#cart-container').html(res.cart_html);
        }
    });
});


// Deleting products to cart
$(".delete-product").on("click", function(){
    "use strict"; // Strict mode is enabled
    
    // Extracting the product ID from the data attribute of the clicked element
    let product_id = $(this).attr("data-product");
    let this_val = $(this);

    console.log("Product ID:", product_id);

    // Making an AJAX request to the server
    $.ajax({
        url: "/delete-from-cart",
        data: {
            'id': product_id
        },
        dataType: 'json',
        beforeSend: function(){
            // Hide the clicked element before sending the request
            this_val.hide();
        },
        success: function(response){
            // Show the clicked element after a successful response
            this_val.show();

            // Update the cart items count and replace the cart list content
            $(".cart-items-count").text(response.totalcartitems);
            $("#cart-list").html(response.data);
    
        },
        
    });
});

//------------------------------------------------------------//
// Function to update quantity






//------------------------------------------------------------//

// Additional functions and event handling
(function ($) {
    "use strict";

    // Dropdown on mouse hover
    $(document).ready(function () {
        function toggleNavbarMethod() {
            if ($(window).width() > 992) {
                $('.navbar .dropdown').on('mouseover', function () {
                    $('.dropdown-toggle', this).trigger('click');
                }).on('mouseout', function () {
                    $('.dropdown-toggle', this).trigger('click').blur();
                });
            } else {
                $('.navbar .dropdown').off('mouseover').off('mouseout');
            }
        }
        toggleNavbarMethod();
        $(window).resize(toggleNavbarMethod);
    });

    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({ scrollTop: 0 }, 1500, 'easeInOutExpo');
        return false;
    });

    // Vendor carousel
    $('.vendor-carousel').owlCarousel({
        loop: true,
        margin: 29,
        nav: false,
        autoplay: true,
        smartSpeed: 1000,
        responsive: {
            0: {
                items: 2
            },
            576: {
                items: 3
            },
            768: {
                items: 4
            },
            992: {
                items: 5
            },
            1200: {
                items: 6
            }
        }
    });

    // Related carousel
    $('.related-carousel').owlCarousel({
        loop: true,
        margin: 29,
        nav: false,
        autoplay: true,
        smartSpeed: 1000,
        responsive: {
            0: {
                items: 1
            },
            576: {
                items: 2
            },
            768: {
                items: 3
            },
            992: {
                items: 4
            }
        }
    });

    // Product Quantity
    $('.quantity button').on('click', function () {
        var button = $(this);
        var oldValue = button.parent().parent().find('input').val();
        if (button.hasClass('btn-plus')) {
            var newVal = parseFloat(oldValue) + 1;
        } else {
            if (oldValue > 0) {
                var newVal = parseFloat(oldValue) - 1;
            } else {
                newVal = 0;
            }
        }
        button.parent().parent().find('input').val(newVal);
    });

})(jQuery);
