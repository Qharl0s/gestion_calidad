$(function () {
  $('.menu_condicion').click(function (e) {
    if (!$(this).parent().hasClass('active')) {
      $(location).attr('href', base_url + 'condiciones/');
    }
  });

  $('.menu_requerimiento').click(function (e) {
    if (!$(this).parent().hasClass('active')) {
      $(location).attr('href', base_url + 'requerimientos/');
    }
  });

  $('.menu_recomendacion').click(function (e) {
    if (!$(this).parent().hasClass('active')) {
      $(location).attr('href', base_url + 'recomendaciones/');
    }
  });

  $('.btnCargarArchivo').click(function () {
    var id = $(this).data('idevidencia');
    $('#idEvidencia').val(id);
    $('#modalCargarArchivo').modal('show');
  });

  $('.btnRevisarArchivo').click(function () {
    $('#idEvidenciaRevision').val(0);
    $('#tBodyRevision').html('');
    var idEvidencia = $(this).data('idevidencia');
    /** Listar Revision por Evidencia */
    $.ajax({
      url: base_url + 'listar_revision/',
      data: {
        idEvidencia: idEvidencia,
      },
      dataType: 'Json',
      type: 'POST',
      success: function (response) {
        var tr =
          '<tr><td>' +
          response.dFecha +
          '</td><td>' +
          response.cComentario +
          '</td><td>' +
          response.cEstado +
          '</td></tr>';
        $('#tBodyRevision').html(tr);
      },
    });
    /**Fin */
    $('#idEvidenciaRevision').val(idEvidencia);
    $('#modalRevisarArchivo').modal('show');
  });

  $('#fileEvidencia').on('change', function () {
    let fileName = $(this).val().split('\\').pop();
    $(this).next('.custom-file-label').addClass('selected').html(fileName);
  });

  /* Revision de Evidencia */
  guardar_revision = function (idEvidencia, idEstado, cComentario) {
    $.ajax({
      url: base_url + 'guardar_revision/',
      data: {
        idEvidencia: idEvidencia,
        idEstado: idEstado,
        cComentario: cComentario,
      },
      dataType: 'Json',
      type: 'POST',
      success: function (response) {
        if (response.state == 'success') {
          notify('Guardar Revisión', response.cMensaje);
          setTimeout(function () {
            location.reload();
          }, 2000);
        } else notify('Guardar Revisión', response.cMensaje, 'danger');
      },
      error: function (jqXhr, textStatus, errorMessage) {
        console.log(errorMessage);
      },
    });
  };

  $('#btnObservarRevision').click(function () {
    guardar_revision(
      $('#idEvidenciaRevision').val(),
      2,
      $('#cComentarioRevision').val()
    );
  });

  $('#btnAprobarRevision').click(function () {
    guardar_revision(
      $('#idEvidenciaRevision').val(),
      3,
      $('#cComentarioRevision').val()
    );
  });

  /** Guardar Archivo Evidencia */
  $('#btnCargarEvidencia').click(function () {
    var fd = new FormData();
    var files = $('#fileEvidencia')[0].files;
    fd.append('idEvidencia', $('#idEvidencia').val());
    fd.append('fileEvidencia', files[0]);
    $.ajax({
      url: base_url + 'guardar_evidencia/',
      data: fd,
      processData: false,
      contentType: false,
      type: 'POST',
      success: function (response) {
        if (response.state == 'success') {
          notify('Guardar Evidencia', response.cMensaje);
          setTimeout(function () {
            location.reload();
          }, 2000);
        } else notify('Guardar Evidencia', response.cMensaje, 'danger');
      },
      error: function (jqXhr, textStatus, errorMessage) {
        console.log(errorMessage);
      },
    });
  });

  $('.btnVerArchivo').click(function (e) {
    window.open($(this).data('urlpdf'), '_blank');
  });
  /************************************************************************ */
  function notify(
    title,
    message,
    type = 'success',
    from = 'top',
    align = 'right',
    icon = 'fa fa-comments',
    animIn = '',
    animOut = ''
  ) {
    $.growl(
      {
        icon: icon,
        title: ' ' + title + ': ',
        message: ' ' + message + ' ',
        url: '',
      },
      {
        element: 'body',
        type: type,
        allow_dismiss: true,
        placement: {
          from: from,
          align: align,
        },
        offset: {
          x: 30,
          y: 30,
        },
        spacing: 10,
        z_index: 999999,
        delay: 2500,
        timer: 1000,
        url_target: '_blank',
        mouse_over: false,
        animate: {
          enter: animIn,
          exit: animOut,
        },
        icon_type: 'class',
        template:
          '<div data-growl="container" class="alert" role="alert">' +
          '<button type="button" class="close" data-growl="dismiss">' +
          '<span aria-hidden="true">&times;</span>' +
          '<span class="sr-only">Close</span>' +
          '</button>' +
          '<span data-growl="icon"></span>' +
          '<span data-growl="title"></span>' +
          '<span data-growl="message"></span>' +
          '<a href="#" data-growl="url"></a>' +
          '</div>',
      }
    );
  }
});
