window.onload = function () {
    var _quantity, _price, orderitemNum, deltaQuantity, orderitemQuantity, deltaCost;
    quantityArr = [];
    priceArr = [];

    var totalForms = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());
    var orderTotalQuantity = parseInt($('.order_total_quantity').text()) || 0;
    var orderTotalCost = parseFloat($('.order_total_cost').text().replace(',', '.')) || 0;
    var $orderForm = $('.order_form');

    for (i = 0; i < totalForms; i++) {
        _quantity = parseInt($('input[name="orderitems-' + i + '-quantity"]').val());
        _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));
        quantityArr[i] = _quantity;
        priceArr[i] = (_price) ? _price : 0;
    }

    function orderSummaryUpdate(orderitemPrice, deltaQuantity) {
        deltaCost = orderitemPrice * deltaQuantity;
        orderTotalCost = Number((orderTotalCost + deltaCost).toFixed(2));
        orderTotalQuantity = orderTotalQuantity + deltaQuantity;

        $('.order_total_cost').html(orderTotalCost.toString());
        $('.order_total_quantity').html(orderTotalQuantity.toString());
    }

    function deleteOrderItem(row) {
        var targetName = row[0].querySelector('input[type="number"]').name;
        orderitemNum = parseInt(targetName.replace('orderitems-', '').replace('-quantity', ''));
        deltaQuantity = -quantityArr[orderitemNum];
        quantityArr[orderitemNum] = 0;
        if (!isNaN(priceArr[orderitemNum]) && !isNaN(deltaQuantity)) {
            orderSummaryUpdate(priceArr[orderitemNum], deltaQuantity);
        }
    }

    if (!orderTotalQuantity) {
        orderSummaryRecalc();
    }

    function orderSummaryRecalc() {
        orderTotalQuantity = 0;
        orderTotalCost = 0;

        for (i = 0; i < totalForms; i++) {
            orderTotalQuantity += quantityArr[i];
            orderTotalCost += quantityArr[i] * priceArr[i];
        }
        $('.order_total_quantity').html(orderTotalQuantity.toString());
        $('.order_total_cost').html(Number(orderTotalCost.toFixed(2)).toString());
    }

    $orderForm.on('change', 'input[type="number"]', function (event) {
        orderitemNum = parseInt(event.target.name.replace('orderitems-', '').replace('-quantity', ''));
        if (priceArr[orderitemNum]) {
            orderitemQuantity = parseInt(event.target.value);
            deltaQuantity = orderitemQuantity - quantityArr[orderitemNum];
            quantityArr[orderitemNum] = orderitemQuantity;
            orderSummaryUpdate(priceArr[orderitemNum], deltaQuantity);
        }
    });

    $orderForm.on('change', 'input[type="checkbox"]', function (event) {
        orderitemNum = parseInt(event.target.name.replace('orderitems-', '').replace('-DELETE', ''));
        if (event.target.checked) {
            deltaQuantity = -quantityArr[orderitemNum];
        } else {
            deltaQuantity = quantityArr[orderitemNum];
        }
        orderSummaryUpdate(priceArr[orderitemNum], deltaQuantity);
    });

    $('.formset_row').formset({
        addText: 'add new product',
        deleteText: 'delete',
        prefix: 'orderitems',
        removed: deleteOrderItem
    });

    $orderForm.on('change', 'select', function (event) {
        orderitemNum = parseInt(event.target.name.replace('orderitems-', '').replace('-product', ''));

        if (event.target.value) {
            $.ajax({
                url: "/order/update/product/" + event.target.value,
                success: function (data) {
                    if (data.price) {
                        priceArr[orderitemNum] = parseFloat(data.price);
                        if (isNaN(quantityArr[orderitemNum])) {
                            quantityArr[orderitemNum] = 0;
                        }
                        var currentTr = $orderForm.find('tr:eq(' + (orderitemNum + 1) + ')');
                        currentTr.find('td:eq(2)').html(data.price);

                        if (isNaN(currentTr.find('input[type="number"]').val())) {
                            currentTr.find('input[type="number"]').val(0);
                        }
                        orderSummaryRecalc();
                    }
                },
            });
        }
    });
};
