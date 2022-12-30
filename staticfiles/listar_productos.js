var tablaProductos;

$(function () {
    tablaProductos = $('#data').DataTable({
        responsive:true,
        autoWidth:false,
        destroy:true,
        deferRender: true,
        ajax:{
            url:window.location.pathname,
            type:'POST',
            data:{
                'action':'verProductos'
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
            {'data':'buttons'},
        ],
        columnDefs:[
            {
                targets : [-1],
                class : "text-center",
                orderable: false,
                render: function (data, type, row){
                    return '<a href="/producto/editar/'+ row.id +'/" class="btn btn-warning"><i class="fas fa-edit"></i></a>'+
                    '<a href="/proveedor/eliminar/'+row.id+'/" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a>';
                }
            },
            {
                targets : [-2],
                class : "text-center",
                orderable: false,
                render: function (data, type, row){
                    return '<a rel="stock" class="btn btn-success" style="cursor:pointer; color:white;"><i class="fas fa-truck"></i> Ver</a>';
                }
            },
        ],
        initComplete: function(settings, json){

        }
    });

    $('#data tbody').on('click', 'a[rel="stock"]', function () {
        var tr = tablaProductos.cell($(this).closest('td , li')).index();
        var data = tablaProductos.row(tr.row).data();
        $('#tableDetalle').DataTable({
            responsive:true,
            autoWidth:false,
            destroy:true,
            deferRender:true,
            ajax:{
                url:window.location.pathname,
                type:'POST',
                data:{
                    'action':'ver_stock',
                    'id':data.id
                },
                dataSrc:''
            },
            columns:[
                {'data':'cod_producto'},
                {'data':'cant_stock'},
                {'data':'fecha_ingreso'}
            ],
            initComplete: function(settings, json){
        
            }
        });
        $('#miModalDetalle').modal('show');
    });

});