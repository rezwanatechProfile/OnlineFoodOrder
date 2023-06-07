// custom javascript to add and delete item in the cart.

$(document).ready(function(){
  // add to cart
  $('.add_to_cart').on('click', function(e){
      e.preventDefault()

     
  
      food_id = $(this).attr('data-id');
      url = $(this).attr('data-url');

     
      $.ajax({
          type: 'GET',
          url: url,
          success: function(response){

            if (response.status == "login_required") {
              swal(response.message, "", "info").then(function () {
                window.location = "/accounts/login";
              });
            } else if (response.status == "Failed") {
              // error class will show red alert
              swal(response.message, "", "error");
            } else {
              $("#cart_counter").html(response.cart_counter["cart_count"]
              );
              $("#qty-" + food_id).html(response.qty);

              // subtotal, tax and grand total
              // applyCartAmounts(
              //   response.cart_amount["subtotal"],
              //   response.cart_amount["tax_dict"],
              //   response.cart_amount["grand_total"]
              // );
            }
           }
      })

     
         
    
  })

   // place the cart item quantity on load
  $('.item_qty').each(function(){
    let the_id = $(this).attr('id')
    let qty = $(this).attr('data-qty')
    // append the value
    console.log(qty)
    $('#'+the_id).html(qty)

  })


  // decrease Cart
  $('.decrease_cart').on('click', function(e){
    e.preventDefault()

   

    food_id = $(this).attr('data-id');
    url = $(this).attr('data-url');

    $.ajax({
      type: 'GET',
      url: url,
      success: function(response){

        if (response.status == "login_required") {
          //configure sweet alert as swal("title", "subtitle", "info") info is the color here
          swal(response.message, "", "info").then(function () {
            window.location = "/login";
          });
        } else if (response.status == "Failed") {
          swal(response.message, "", "error");
        } else {
          $("#cart_counter").html(response.cart_counter["cart_count"]
          );
          $("#qty-" + food_id).html(response.qty);

          // subtotal, tax and grand total
          // applyCartAmounts(
          //   response.cart_amount["subtotal"],
          //   response.cart_amount["tax_dict"],
          //   response.cart_amount["grand_total"]
          // );
        }
       }
    })

    // place the cart item quantity on load
       
  
})


});