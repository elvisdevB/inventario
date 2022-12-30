function formatRepo(repo) {
    if (repo.loading) {
        return repo.text;
    }

    var option = $(
        '<div class="wrapper container">'+
        '<div class="row">' +
        '<div class="col-lg-11 text-left shadow-sm">' +
        //'<br>' +
        '<p style="margin-bottom: 0;">' +
        '<b>Identificacion:</b> ' + repo.cod_proveedor + '<br>' +
        '<b>Nombre Proveedor:</b> ' + repo.nombre + '<br>' +
        '<b>Telefono:</b> ' + repo.telefono+ '<br>' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}

var producto = {
    product:{
        cod_producto:'',
        cod_proveedor:'',
        nombre:'',
        precio_unitario:'',
        fecha_creacion:'',
        cant_stock:'',
    }
}

$(function () {
    /* Select - Autocomplete */
    $('select[name="cod_proveedor"]').select2({
        theme: 'bootstrap4',
        lagunge: 'es',
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'buscarproveedor',
                }

                return queryParameters;
            },

            processResults: function(data){
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese el numero de Cedula del Proveedor',
        minimumInputLength: 1,
        templateResult: formatRepo

    });

    /* Enviar Datos */
    $('#form').on('submit', function (e) {
        e.preventDefault();
        
        producto.product.cod_producto = $('input[name="cod_producto"]').val();
        producto.product.cod_proveedor = $('select[name="cod_proveedor"]').val();
        producto.product.nombre = $('input[name="nombre"]').val();
        producto.product.precio_unitario = $('input[name="precio_unitario"]').val();
        producto.product.fecha_creacion= $('input[name = "fecha_creacion"]').val();
        producto.product.cant_stock = $('input[name="cant_stock"]').val();

        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('producto', JSON.stringify(producto.product));

        submit_switalert_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            location.href = '/producto/listar/';
        }); 
    });

});
