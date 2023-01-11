function message_error(obj) {
    var html = '';
    if (typeof (obj) === 'object') {
        html = '<ul style="text-align: left;">';
        $.each(obj, function (key, value) {
            html += '<li>' + key + ': ' + value + '</li>';
        });
        html += '</ul>';
    } else {
        html = '<p>' + obj + '</p>';
    }
    Swal.fire({
        title: 'Error!',
        html: html,
        icon: 'error'
    });
}

function registrar_informacion_ajax(url, parameters, callback){
    Swal.fire({
        title: 'Procesando...',
    });
    Swal.showLoading();
    $.ajax({
        url: url, //window.location.pathname
        type: 'POST',
        data: parameters,
        dataType: 'json',
        processData: false,
        contentType: false,
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            callback(data);
            console.log(data);
            return false;
        }
        message_error(data.error);
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ': ' + errorThrown);
    }).always(function (data) {

    });
}

function actions_switalert_ajax(url, title, content, parameters, callback) {
    Swal.fire({
        title:title,
        text: content,
        icon: 'question',
        showCancelButton:true,
        confirmButtonText:"Si",
        confirmButtonColor:'btn btn-success btn-lg btn-block',
        cancelButtonColor:'btn btn-danger btn-lg btn-block',
        backdrop:true,
        showLoaderOnConfirm:true,
        preConfirm: () => {
            Swal.fire({
                title: 'Procesando...',
            });
            Swal.showLoading();
            $.ajax({
                url: url, //window.location.pathname
                type: 'POST',
                data: parameters,
                dataType: 'json',
                processData: false,
                contentType: false,
            }).done(function (data) {
                if (!data.hasOwnProperty('error')) {
                    callback(data);
                    console.log(data);
                    return false;
                }
                message_error(data.error);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {

            });
        },
        allowOutsideClick:() => false,
    });
}

function alert_action_switalert(title, content, callback, cancel){
    Swal.fire({
        title:title,
        text: content,
        icon: 'question',
        showCancelButton:true,
        confirmButtonText:"Si",
        cancelButtonText:"No",
        confirmButtonColor:'btn btn-success btn-lg btn-block',
        cancelButtonColor:'btn btn-danger btn-lg btn-block',
        backdrop:true,
        showLoaderOnConfirm:true,
        preConfirm: () => {
            callback();
        },
        allowOutsideClick:() => false,
    }).then(function(result){
        if(result.dismiss){
            window.location.href = '/factura/listar/factura/compra'
        }
    });
}
