$(function () {

  $('#form_guardar_datos').submit(function (e) {
    e.preventDefault();
    if ($('#email').val() == "") {
      notify('Guardar Datos', 'El campo email es obligatorio.', 'danger');
      return;
    }
    if ($('#nombres').val() == "") {
      notify('Guardar Datos', 'El campo nombres es obligatorio.', 'danger');
      return;
    }

    $.ajax({
      url: base_url + 'guardar_datos/',
      data: {
        email: $('#email').val(),
        nombres: $('#nombres').val(),
      },
      dataType: 'Json',
      type: 'POST',
      success: function (response) {
        if (response.state == 'success') {
          notify('Guardar Datos', response.cMensaje);
          setTimeout(function () {
            location.reload();
          }, 2000);
        } else notify('Guardar Datos', response.cMensaje, 'danger');
      },
    });
  });

  $('#form_actualizar_password').submit(function (e) {
    e.preventDefault();
    if ($('#password_actual').val() == "") {
      notify('Guardar Datos', 'El campo password actual es obligatorio.', 'danger');
      return;
    }
    if ($('#nuevo_password1').val() == "") {
      notify('Guardar Datos', 'El campo de nuevo password es obligatorio.', 'danger');
      return;
    }
    if ($('#nuevo_password2').val() == "") {
      notify('Guardar Datos', 'El campo para repetir password es obligatorio.', 'danger');
      return;
    }

    $.ajax({
      url: base_url + 'actualizar_password/',
      data: {
        password_actual: $('#password_actual').val(),
        nuevo_password1: $('#nuevo_password1').val(),
        nuevo_password2: $('#nuevo_password2').val(),
      },
      dataType: 'Json',
      type: 'POST',
      success: function (response) {
        if (response.state == 'success') {
          notify('Actualizar Password', response.cMensaje);
          setTimeout(function () {
            location.reload();
          }, 2000);
        } else notify('Actualizar Password', response.cMensaje, 'danger');
      },
    });
  });

  $('.menu_estandar').click(function (e) {
    var id_oficina = $(this).data('idoficina');
    if (!$(this).parent().hasClass('active')) {
      $(location).attr('href', base_url + 'estandares/' + id_oficina + '/');
    }
  });

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

  $('.menu_renovacion').click(function (e) {
    if (!$(this).parent().hasClass('active')) {
      $(location).attr('href', base_url + 'renovaciones/');
    }
  });

  $('.btnModalCargarDetalleEvidencia').click(function () {
    var id = $(this).data('medioverificacion');
    var id_periodo = $(this).data('idperiodo');
    $.ajax({
      url: base_url + 'obtener_evidencia/',
      data: {
        idMedioVerificacion: id,
        idPeriodo: id_periodo,
      },
      dataType: 'Json',
      type: 'POST',
      success: function (response) {
        $('#idMedioVerificacion').val(id);
        $('#idPeriodoEvi').val(id_periodo);
        if (response.state == 'success') {
          $('#detalle1').Editor('setText', response.cDetalle1 === undefined ? '' : response.cDetalle1);
          $('#detalle2').Editor('setText', response.cDetalle2 === undefined ? '' : response.cDetalle2);
        }
        else {
          $('#detalle1').Editor('setText', '');
          $('#detalle2').Editor('setText', '');
        }
      },
    });
    if ($(this).data('editar') == 1)
      $('.footer_detalles').show();
    else
      $('.footer_detalles').hide();
    $('#modalDetalleEvidencia').modal('show');
  });


  $('.btnModalCargarArchivo').click(function () {
    var id = $(this).data('medioverificacion');
    var id_periodo = $(this).data('idperiodo');
    var lEditar = $(this).data('editar');
    $('#idMedioVerificacionArchivo').val(id);
    $('#idPeriodoArchivo').val(id_periodo);
    $.ajax({
      url: base_url + 'listar_archivos/',
      data: {
        idMedioVerificacion: id,
        idPeriodo: id_periodo,
      },
      dataType: 'Json',
      type: 'POST',
      success: function (response) {
        var tBody = '';
        for (var i = 0; i < response.archivos.length; i++) {
          var mydate = new Date(response.archivos[i].dFecha);
          var btnEliminar = '<button type="button" class="btn btn-danger btnEliminarArchivo" data-id="' + response.archivos[i].id + '"><i class="fa fa-trash" aria-hidden="true"></i></button>';
          if (lEditar == 0)
            btnEliminar = '';
          tBody +=
            '<tr>' +
            '<td><a target="_blank" href="' + base_url + 'media/' + response.archivos[i].archivoPdf + '">' + (response.archivos[i].archivoPdf).substring(4, 40) + '</a></td>' +
            '<td>' + mydate.toLocaleDateString() + '</td>' +
            '<td>' + response.archivos[i].usuario__username + '</td>' +
            '<td>' +
            '<div class="btn-group btn-group-sm text_body">' +
            '<button type="button" class="btn btn-primary btnCopiarLink" data-urlpdf="' + response.archivos[i].archivoPdf + '">' +
            '<i class="fa fa-link" aria-hidden="true"></i>' +
            '</button>' + btnEliminar +
            '</div>' +
            '</td>' +
            '</tr>';
        }
        $('#tBodyArchivos').html(tBody);
        $('#cantidadArchivos').html(response.archivos.length);
      },
    });
    if ($(this).data('editar') == 1)
      $('#formCargarArchivo').show();
    else
      $('#formCargarArchivo').hide();
    $('#modalCargarArchivo').modal('show');
  });

  // Funcion para guardar archivo al seleccionar
  $('#fileEvidencia').change(function () {
    $this = $(this);
    $this.attr('disabled', 'disabled');
    var parametros = new FormData();
    parametros.append('idMedioVerificacion', $('#idMedioVerificacionArchivo').val());
    parametros.append('idPeriodo', $('#idPeriodoArchivo').val());
    parametros.append('fileEvidencia', $('#fileEvidencia')[0].files[0]);
    $('#lblFileEvidencia').html('Guardando archivo..');

    $.ajax({
      url: base_url + 'guardar_archivo/',
      data: parametros,
      // dataType: 'Json',
      processData: false,
      contentType: false,
      type: 'POST',
      success: function (response) {
        if (response.state == 'success') {
          notify('Guardar Archivo', response.cMensaje);
          setTimeout(function () {
            location.reload();
          }, 2000);

        } else {
          notify('Guardar Revisión', response.cMensaje, 'danger');
          $this.removeAttr('disabled');
        }
      },
      error: function (jqXhr, textStatus, errorMessage) {
        console.log(errorMessage);
        $this.removeAttr('disabled');
      },
    });

    $('#fileEvidencia').val('');
  });

  $('.btnRevisarEvidencia').click(function () {
    $('#idMedioRevision').val(0);
    $('#idPeriodoRevision').val(0);
    $('#tBodyRevision').html('');
    var idMedio = $(this).data('medioverificacion');
    var idPeriodo = $(this).data('idperiodo');
    /** Listar Revision por Evidencia */
    $.ajax({
      url: base_url + 'listar_revision/',
      data: {
        'idMedio': idMedio,
        'idPeriodo': idPeriodo,
      },
      dataType: 'Json',
      type: 'POST',
      success: function (response) {
        if (response.state == "success") {
          var tBody = '';
          for (var i = 0; i < response.revisiones.length; i++) {
            // var td = ''
            // if (response.lRevisor) {
            //   td = '<td>' +
            //     '<div class="btn-group btn-group-sm text_body">' +
            //     '<button type="button" class="btn btn-danger btnEliminarRevision" data-id="' + response.revisiones[i].id + '">' +
            //     '<i class="fa fa-trash" aria-hidden="true"></i>' +
            //     '</button>' +
            //     '</div>' +
            //     '</td>';
            // }

            var estado = '<span class="text-danger">' + response.revisiones[i].idEstado + '</span>';
            if (response.revisiones[i].idEstado == 'Aprobado')
              estado = '<span class="text-success">' + response.revisiones[i].idEstado + '</span>';

            var mydate = new Date(response.revisiones[i].dFecha);
            tBody +=
              '<tr>' +
              '<td>' + estado + '</td>' +
              '<td>' + mydate.toLocaleDateString() + '</td>' +
              '<td>' + response.revisiones[i].usuario__username + '</td>' +
              '<td>' + response.revisiones[i].cRevision + '</td>' +
              // td +
              '</tr>';
          }


          $('#tBodyRevision').html(tBody);
        }
      },
    });
    /**Fin */
    $('#idMedioRevision').val(idMedio);
    $('#idPeriodoRevision').val(idPeriodo);
    $('#modalRevisarEvidencia').modal('show');
  });

  $('#fileEvidencia').on('change', function () {
    let fileName = $(this).val().split('\\').pop();
    $(this).next('.custom-file-label').addClass('selected').html(fileName);
  });

  /* Revision de Evidencia */
  guardar_revision = function (idMedio, idPeriodo, cEstado, cComentario, $this) {
    $this.prop("disabled", true);
    $.ajax({
      url: base_url + 'guardar_revision/',
      data: {
        idMedio: idMedio,
        idPeriodo: idPeriodo,
        cEstado: cEstado,
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
        } else {
          notify('Guardar Revisión', response.cMensaje, 'danger');
          $this.prop("disabled", false);
        }
      },
      error: function (jqXhr, textStatus, errorMessage) {
        console.log(errorMessage);
        $this.prop("disabled", false);
      },
    });
  };

  $('#btnObservarRevision').click(function () {
    guardar_revision(
      $('#idMedioRevision').val(),
      $('#idPeriodoRevision').val(),
      'Observado',
      $(
        $('#txtEditorContentRevision').text(
          $('#cComentarioRevision').Editor('getText')
        )[0]
      ).val(),
      $(this)
    );
  });

  $('#btnAprobarRevision').click(function () {
    guardar_revision(
      $('#idMedioRevision').val(),
      $('#idPeriodoRevision').val(),
      'Aprobado',
      $(
        $('#txtEditorContentRevision').text(
          $('#cComentarioRevision').Editor('getText')
        )[0]
      ).val(),
      $(this)
    );
  });

  /** Guardar Archivo Evidencia */
  $('#btnGuardarDetalleEvi').click(function () {
    var $this = $(this);
    $this.prop("disabled", true);
    var fd = new FormData();
    // var files = $('#fileEvidencia')[0].files;
    fd.append('idMedioVerificacion', $('#idMedioVerificacion').val());
    fd.append('idPeriodo', $('#idPeriodoEvi').val());
    fd.append(
      'cDetalle1',
      $($('#txtEditorContent1').text($('#detalle1').Editor('getText'))[0]).val()
    );
    fd.append(
      'cDetalle2',
      $($('#txtEditorContent2').text($('#detalle2').Editor('getText'))[0]).val()
    );

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
        } else {
          notify('Guardar Evidencia', response.cMensaje, 'danger');
          $this.prop("disabled", false);
        }

      },
      error: function (jqXhr, textStatus, errorMessage) {
        $this.prop("disabled", false);
        console.log(errorMessage);
      },
    });
  });

  $(document).on('click', '.btnEliminarArchivo', function () {
    var $this = $(this);
    $this.prop("disabled", true);
    console.log($this.prop("disabled"));

    var id_archivo = $(this).data('id');
    $.ajax({
      url: base_url + 'eliminar_archivo/',
      data: {
        idArchivo: id_archivo,
      },
      dataType: 'Json',
      type: 'POST',
      success: function (response) {
        if (response.state == 'success') {
          notify('Eliminar Archivo', response.cMensaje);
          setTimeout(function () {
            location.reload();
          }, 2000);
        } else {
          notify('Eliminar Archivo', response.cMensaje, 'danger');
          $this.prop("disabled", false);
        }

      },
      error: function (jqXhr, textStatus, errorMessage) {
        console.log(errorMessage);
        $this.prop("disabled", false);
      },
    });

  });

  $(document).on('click', '.btnCopiarLink', function () {
    var url = $(this).data('urlpdf');
    console.log(url);
    unsecuredCopyToClipboard(base_url + 'media/' + url, $(this));
  });

  function unsecuredCopyToClipboard(text, $this) {
    var textArea = $('#link_file');
    textArea.val(text);
    textArea.focus();
    textArea.select();
    $this.focus();
    try {
      document.execCommand('copy');
      notify('Copiado', 'el link del archivo fue copiado.');
    } catch (err) {
      notify('Copiado', 'No se pudo copiar, intento de nuevo.', 'danger');
    }
    setTimeout(() => {
      textArea.val("");
    }, "3000");
  }

  $('.btnVerArchivo').click(function (e) {
    window.open(base_url + 'media/' + $(this).data('urlpdf'), '_blank');
    // var id = $(this).data('medioverificacion');
    // $.ajax({
    //   url: base_url + 'obtener_evidencia/',
    //   data: {
    //     idMedioVerificacion: id,
    //   },
    //   dataType: 'Json',
    //   type: 'POST',
    //   success: function (response) {
    //     console.log(response);
    //     if(response.cArchivoName ===undefined)
    //     {}
    //     else{
    //       window.open(base_url+'media/'+response.cArchivoName, '_blank');
    //     }
    //   },
    // });

  });

  $('#detalle1').Editor({
    fonts: null,
    styles: null,
    font_size: null,
    block_quote: false,
    insert_img: false,
    undo: false,
    redo: false,
    insert_link: false,
    strikeout: false,
    print: false,
    unlink: false,
    hr_line: false,
    source: false,
    insert_table: false,
    select_all: false,
  });
  $('#detalle2').Editor({
    fonts: null,
    styles: null,
    font_size: null,
    block_quote: false,
    insert_img: false,
    undo: false,
    redo: false,
    insert_link: false,
    strikeout: false,
    print: false,
    unlink: false,
    hr_line: false,
    source: false,
    insert_table: false,
    select_all: false,
  });
  $('#cComentarioRevision').Editor({
    fonts: null,
    styles: null,
    font_size: null,
    block_quote: false,
    insert_img: false,
    undo: false,
    redo: false,
    insert_link: false,
    strikeout: false,
    print: false,
    unlink: false,
    hr_line: false,
    source: false,
    insert_table: false,
    select_all: false,
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
