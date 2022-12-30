$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax:{
            url: window.location.pathname,
            type: 'POST',
            data:{
                'action':'buscar_usuarios'
            },
            dataSrc:''
        },
        columns:[
            {'data':'id'},
            {'data':'full_name'},
            {'data':'username'},
            {'data':'date_joined'},
            {'data':'img'},
            {'data':'groups'},
            {'data':'butons'},
        ],
        columnDefs:[
            {
                targets : [-1],
                class : "text-center",
                orderable: false,
                render: function (data, type, row){
                    return '<a href="/usuario/editar/usuarios/'+row.id+'/" class="btn btn-warning"><i class="fas fa-edit"></i></a>'+
                    '<a href="" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a>';
                }
            },
            {
                targets : [-2],
                class : "text-center",
                orderable: false,
                render: function (data, type, row){
                    var html = '';
                    $.each(row.groups, function (key, value){
                        html += '<span class="badge badge-success">'+ value.nombre +'</span>';
                    });
                    return html;
                }
            },
            {
                targets: [-3],
                class: "text-center",
                orderable: false,
                render: function(data, type, row){
                    return '<img src="'+row.img+'" class="img-fluid mx-auto d-block" style="width:20px; height:20px">';
                }
            },
        ]
    });
});