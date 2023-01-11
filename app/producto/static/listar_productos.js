var tabla_productos;

$(function () {
    tabla_productos = $('#data').DataTable({
        responsive:true,
        autoWidth:false,
        destroy:true,
        deferRender: true,
        ajax:{
            url:window.location.pathname,
            type:'POST',
            data:{
                'action':'ver_productos'
            },
            dataSrc:''
        },
        columns:[
            {'data':'cod_proveedor'},
            {'data':'cod_producto'},
            {'data':'nombre'},
            {'data':'precio_unitario'},
            {'data':'fecha_creacion'},
            {'data':'stock'},
            {'data':'buttons'}
        ],
        columnDefs:[
            {
                targets : [-1],
                class : "text-center",
                orderable: false,
                render: function (data, type, row){
                    return '<a href="/producto/editar/'+ row.id +'/" class="btn btn-warning"><i class="fas fa-edit"></i></a>'+
                    '<a href="#" rel="delete" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a>';
                }
            },
        ],
        initComplete: function(settings, json){

        }
    });

    $('#data tbody').on('click', 'a[rel="delete"]', function () {
        var tr = tabla_productos.cell($(this).closest('td , li')).index();
        var data = tabla_productos.row(tr.row).data();
        var parametros = new FormData();
        parametros.append('action', 'delete');
        parametros.append('id', data.id)
        actions_switalert_ajax(window.location.pathname, 'Notificación', '¿Desea eliminar el siguiente registro?', parametros, function () {
            location.href = window.location.pathname;
        });
    });
});