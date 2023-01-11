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

function format_repo_producto(repo) {
    if (repo.loading) {
        return repo.text;
    }

    var option = $(
        '<div class="wrapper container">'+
        '<div class="row">' +
        '<div class="col-lg-1">' +
        '<img src="' + repo.imagen + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
        '</div>' +
        '<div class="col-lg-11 text-left shadow-sm">' +
        //'<br>' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.nombre + '<br>' +
        '<b>Precio Unitario:</b> $' + repo.precio_unitario + '<br>' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}

var compra = {
    items :{
        cod_proveedor:'',
        fecha_emision: '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        producto: []
    },

    //Calcular Detalle de Producto
    calcular_detalle_factura: function () {
        var subTotal = 0.00;
        var iva = $('input[name="iva"]').val();
        $.each(this.items.producto, function(pos,dict){
            dict.subtotal = dict.cantidad * parseFloat(dict.precio_unitario);
            subTotal += dict.subtotal;
        });
        this.items.subtotal = subTotal;
        this.items.iva = this.items.subtotal * iva;
        this.items.total = this.items.subtotal + this.items.iva;



        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="ivacalculado"]').val(this.items.iva.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },

    agregar_productos : function(item){
        this.items.producto.push(item);
        this.list();
    },

    list: function () {
        this.calcular_detalle_factura();

        tabla_productos = $('#listProductos').DataTable({
            responsive:true,
            autoWidth:false,
            destroy:true,
            data: this.items.producto,
            columns: [
                {'data':'id'},
                {'data':'nombre'},
                {'data':'cod_proveedor'},
                {'data':'precio_unitario'},
                {'data':'cantidad'},
                {'data':'subtotal'},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class:'tex-center',
                    orderable: false,
                    render: function(data, type, row){
                        return '<a rel="remove" class="btn btn-danger" style="color:white"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable:false,
                    render : function(data, type, row){
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete=off value=' + row.cantidad + '></input>';
                    }
                },
                {
                    targets:[-1],
                    class:'text-center',
                    orderable:false,
                    render: function(data,type,row){
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
            ],

            rowCallback(row, data, displayNum, displayIndex, dataIndex){
                $(row).find('input[name="cant"]').TouchSpin({
                    min:1,
                    max:100000,
                    step:1
                });
            }
        });
    },
}


$(function () {

    $('input[name="iva"]').TouchSpin({
        min: 0,
        max: 100,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%'
    }).on('change', function () {
        compra.calcular_detalle_factura();
    }).val(0.12);

    $('select[name="cod_proveedor"]').select2({
        theme:'bootstrap4',
        lagunge: 'es',
        allowClear: true,
        ajax: {
            dalay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function(params){
                var queryParameters = {
                    term: params.term,
                    action: 'buscarProveedor',
                }
                return queryParameters;
            },
            processResults: function(data){
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese el Codigo del Producto',
        minimumInputLength: 1,
        templateResult: formatRepo
    });

    $('select[name="search"]').select2({
        theme:'bootstrap4',
        lagunge: 'es',
        allowClear: true,
        ajax:{
            delay: 250,
            type:'POST',
            url: window.location.pathname,
            data: function(params) {
                var queryParameters = {
                    term: params.term,
                    action: "buscarProductos",
                }

                return queryParameters;
            },

            processResults: function(data){
                return{
                    results: data
                };
            },
        },
        placeholder: 'Ingrese el Codigo del Producto',
        minimumInputLength: 1,
        templateResult: format_repo_producto
    }).on('select2:select', function (e) {
        e.preventDefault();
        console.clear();

        var data = e.params.data;

        data.cantidad = 1;
        data.subtotal = 0.00;
        console.log(data);

        compra.agregar_productos(data);
        $(this).val('').trigger('change.select2');
    });

    $('#listProductos tbody').on('change', 'input[name="cant"]', function () {
        var cantidad = parseInt($(this).val());
        var tr = tabla_productos.cell($(this).closest('td, li')).index();
        compra.items.producto[tr.row].cantidad = cantidad;
        compra.calcular_detalle_factura();
        $('td:eq(5)', tabla_productos.row(tr.row).node()).html('$' + compra.items.producto[tr.row].subtotal.toFixed(2));
    });

    $('#formAdd').on('submit', function (e) {
        e.preventDefault();
        
        compra.items.cod_proveedor = $('select[name="cod_proveedor"]').val();
        compra.items.fecha_emision = $('input[name="fecha_emision"]').val();
        
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('compra', JSON.stringify(compra.items));

        registrar_informacion_ajax(window.location.pathname, parameters, function (response) {
            alert_action_switalert('Notificacion','¿Desea imprimir la voleta de venta?', function(){
                window.open('/factura/volante/pdf/salida/'+response.id+'/', '_blank')
                location.href = '/factura/listar/factura/compra/';
            }, function(){
                location.href = '/factura/listar/factura/compra/';
            })
        }); 
    });

    compra.list();
});