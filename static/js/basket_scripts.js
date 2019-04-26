// window.onload = function () {
//     $('.basket_list').on('click', 'input[type="number"]', function () {
//         var t_href = event.target;
//         $.ajax({
//             url: "/basket/edit/" + t_href.name + "/" + t_href.value + "/",
//             success: function (data) {
//                 $('.basket_list').html(data.result);
//             },
//         });
//         event.preventDefault();
//     });
// }

// $("basket_list").on( "click",".basket-input-button",function () {
//     var input_object = $(event.target).closest(
//         'div'
//     ).find(
//         '.basket-input-field'
//     );
//
//     var quantity = parseInt(input_object.attr('value'));
//     var cart_id = input_object.attr('name');
//
//     ($(this).val() == "+") ? quantity++ : quantity--;
//     $.ajax(
//         "/basket/edit/" + cart_id + "/" + quantity + "/",
//         {
//             success: function (data) {
//                 $("basket_list").html(data.result);
//             }
//         }
//     );
//     input_object.val(quantity);
// });
//

window.onload = function () {
    $('.basket_list').change( 'input[type="number"]',function (event) {

        let targetHref = event.target;

        $.ajax({
            url: "/basket/edit/" + targetHref.name + "/" + targetHref.value + "/",
            success: function (data) {
                $('.basket_list').html(data.result);
            }
        });

        event.preventDefault();
    });
};
