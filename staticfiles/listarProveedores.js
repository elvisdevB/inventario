$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax:{
            url : window.location.pathname,
            type: 'POST',
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
                    '<a href="/proveedor/eliminar/'+row.id+'/" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a>';
                }
            },
        ],
        initComplete: function(settings, json){

        }
    });
});