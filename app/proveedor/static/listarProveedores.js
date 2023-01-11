
var tabla_proveedores;

$(function () {
    tabla_proveedores = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax:{
            url : window.location.pathname,
            type: 'POST',
            data:{
                'action':'listar_proveedores'
            },
            dataSrc:''
        },
        columns:[
            {'data':'cod_proveedor'},
            {'data':'nombre'},
            {'data':'direccion'},
            {'data':'email'},
            {'data':'telefono'},
            {'data':'buttons'},
        ],
        columnDefs:[
            {
                targets : [-1],
                class : "text-center",
                orderable: false,
                render: function (data, type, row){
                    return '<a href="/proveedor/listar/'+ row.id +'/" class="btn btn-warning"><i class="fas fa-edit"></i></a>'+
                    '<a href="#" rel="delete" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a>';
                }
            },
        ],
        initComplete: function(settings, json){

        }
    });

    $('#data tbody').on('click', 'a[rel="delete"]', function () {
        var tr = tabla_proveedores.cell($(this).closest('td , li')).index();
        var data = tabla_proveedores.row(tr.row).data();
        var parametros = new FormData();
        parametros.append('action', 'delete');
        parametros.append('id', data.id)
        actions_switalert_ajax(window.location.pathname, 'Notificación', '¿Desea eliminar el siguiente registro?', parametros, function () {
            location.href = window.location.pathname;
        });
    });
});