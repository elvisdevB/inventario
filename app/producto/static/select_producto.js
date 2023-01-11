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
});
