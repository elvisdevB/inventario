var tabla_compras;

$(function () {
    tabla_compras = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax:{
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action':'listar_factura'
            },
            dataSrc:''
        },
        columns: [
            {'data':'cod_proveedor'},
            {'data':'fecha_emision'},
            {'data':'subtotal'},
            {'data':'iva'},
            {'data':'total'},
            {'data':'detalle'}
        ],
        columnDefs:[
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function(data, type, row){
                    return '<a rel="stock" class="btn btn-success" style="cursor:pointer; color:white;"><i class="fas fa-shopping-cart"></i> Ver</a>';
                }
            }
        ]
    });

    $('#data tbody').on('click', 'a[rel="stock"]', function () {
        var tr = tabla_compras.cell($(this).closest('td , li')).index();
        var data = tabla_compras.row(tr.row).data();
        $('#tableDetalle').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax:{
                url: window.location.pathname,
                type: 'POST',
                data:{
                    'action':'ver_detalle_compra',
                    'id':data.id
                },
                dataSrc: ''
            },
            columns:[
                {'data':'fecha_ingreso'},
                {'data':'cod_producto.nombre'},
                {'data':'cantidad_ingreso_stock'},
                {'data':'subtotal'}
            ]
        });
        $('#miModalDetalle').modal('show');
    });
});