function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
};

function cloneMore(selector, prefix) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
    newElement.find(':input').each(function() {
        var name = $(this).attr('name').replace('-' + (total-1) + '-', '-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
    total++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
    return false;
};

function createImageForm() {
    var totalInput = $('#id_image_fields-TOTAL_FORMS');
    var prefixTotal = 'image_fields-' + totalInput.attr('value');
    var orderValue = parseInt(totalInput.attr('value')) + 1;

    $('.images-previews').append('<div class="image-box" id="setup-image" hidden></div>');

    var newImageBox = $('.image-box:last-of-type');

    newImageBox.append('<div class="image_fields-form-row"></div>');
    var inputsDiv = newImageBox.children('.image_fields-form-row');
    inputsDiv.append('<input type="file" name="' + prefixTotal + '-image" id="id_' + prefixTotal + '-image" hidden>');
    inputsDiv.append('<input type="number" name="' + prefixTotal + '-ORDER" id="id_' + prefixTotal + '-ORDER">');
    inputsDiv.append('<input type="checkbox" name="' + prefixTotal + '-DELETE" id="id_' + prefixTotal + '-DELETE">');
    inputsDiv.append('<input type="hidden" name="' + prefixTotal + '-id" id="id_' + prefixTotal + '-id">');
    inputsDiv.append('<input type="hidden" name="' + prefixTotal + '-setup" id="id_' + prefixTotal + '-setup">');

    newImageBox.append('<img src=""/>');
    newImageBox.append('<div class="delete-image" id="delete-' + prefixTotal + '">&times;</div>');

    newImageBox.append('<div class="order-image-arrows"></div>');
    newImageBox.children('.order-image-arrows').append('<i class="order-image fa fa-arrow-up" aria-hidden="true"></i>');
    newImageBox.children('.order-image-arrows').append('<i class="order-image fa fa-arrow-down" aria-hidden="true"></i>');

    newImageBox.find('input[type="file"]').click().one();

    newImageBox.find('input[type="file"]').change( function(){
        newImageBox.find('input[type="number"]').attr('value', orderValue);
        imageInputTumbnail(this);
        $('.images-previews').show();
        $('html, body').animate({
            scrollTop: $("#add-image_fields").offset().top
        }, 750);
        newImageBox.show();
        return false;
    });

    totalInput.attr('value', orderValue);
}


function deleteForm(prefix, btn) {
    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    var formSelector = '.' + prefix + '-form-row';
    if (total > 1){
        btn.closest(formSelector).hide();
        var forms = $(formSelector);
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (var i=0, formCount=forms.length; i<formCount; i++) {
            $(forms.get(i)).find(':input').each(function() {
                updateElementIndex(this, prefix, i);
            });
        }
    }
    return false;
}

function getBrandModels() {
    $('select[name="car_brand"]').change( function(){
        var carBrandId = {'brand_id': $(this).find(':selected').val()};
        var req_url = $(this).attr('data-url');

        $('select[name="car_model"] option:not(:first)').remove();
        $('select[name="car_sub_model"] option:not(:first)').remove();
        $('select[name="car_sub_model"]').prop('disabled', true);

        $.ajax({
              url: req_url,
			  type: "GET",
			  data: carBrandId,
			  dataType: "json",
			  cache: true,
			  success: function(data) {
                  $('select[name="car_model"]').prop('disabled', false);
                  if (data.length > 0) {
                      for (var car_model in data){
                          $('select[name="car_model"]').append('<option value="' + data[car_model].id + '">' + data[car_model].name + '</option>');
                      }
                  } else {
                      $('select[name="car_model"]').append('<option value="">No models here =\\</option>');
                  }
			  },
			  error: function(){
				  console.log('ERROR');
			  }
            });
    });
}


function getModelsSubModels() {
    $('select[name="car_model"]').change( function(){
        var carBrandId = {'car_model_id': $(this).find(':selected').val()};
        var req_url = $(this).attr('data-url');

        $('select[name="car_sub_model"] option:not(:first)').remove();

        $.ajax({
              url: req_url,
			  type: "GET",
			  data: carBrandId,
			  dataType: "json",
			  cache: true,
			  success: function(data) {
                  $('select[name="car_sub_model"]').prop('disabled', false);
                  if (data.length > 0) {
                      for (var car_sub_model in data) {
                          $('select[name="car_sub_model"]').append('<option value="' + data[car_sub_model].id + '">' + data[car_sub_model].name + '</option>');
                      }
                  } else {
                      $('select[name="car_sub_model"]').append('<option value="">No bodies here ==\\</option>');
                  }
			  },
			  error: function(){
				  console.log('ERROR');
			  }
            });
    });
}


function imageInputTumbnail(input) {
    var input_id = $(input).attr('id').replace('-image', '');
    if (input.files) {
        var files = input.files;
        for (var i = 0, f; f = files[i]; i++) {
            // Only process image files.
            if (!f.type.match('image.*')) {
                continue;
            }

            var reader = new FileReader();

            // Closure to capture the file information.
            reader.onload = (function (theFile) {
                return function (e) {
                    $(input).parent().parent('.image-box').show();
                    $(input).parent().parent('.image-box').last().children('img').attr('src', e.target.result);
                    $(input).parent().parent('.image-box').last().children('.delete-image').attr('id', 'delete-' + input_id);
                }
            })(f);

            reader.readAsDataURL(f);
        }
    }
}


$(document).ready(function (){
    $('#id_image_fields-0-ORDER').attr('value', 1);
    getBrandModels();
    getModelsSubModels();
});

$(document).on('click', '.order-image', function() {
        var imageBox = $(this).closest('.image-box');
        var currentOrderInput = $(imageBox).find('input[type="number"]');
        var currentOrderInputValue = parseInt(currentOrderInput.attr('value'));
        console.log(currentOrderInputValue);

        if ($(this).hasClass('fa-arrow-up')){
            $(imageBox).prev().find('input[type="number"]').attr('value', currentOrderInputValue);
            $(imageBox).insertBefore($(imageBox).prev('.image-box'));
            currentOrderInput.attr('value', currentOrderInputValue - 1);
        } else {
            $(imageBox).next().find('input[type="number"]').attr('value', currentOrderInputValue);
            $(imageBox).insertAfter($(imageBox).next('.image-box'));
            currentOrderInput.attr('value', currentOrderInputValue + 1);
        }
    });

$(document).on('click', '.setup-create-form-add-field', function(e){
    e.preventDefault();
    var prefix = $(this).attr('id').replace('add-', '');
    var formSelector = '.' + prefix + '-form-row:last';
    cloneMore(formSelector, prefix);
    return false;
});

$(document).on('click', '.delete-image', function(e){
    e.preventDefault();
    var formId = $(this).attr('id').replace('delete-', '');
    var delete_input = $('input[id=' + formId + '-DELETE]');
    $(delete_input).attr('checked', true);
    var this_image_box = $(this).parent();
    this_image_box.hide();
    return false;
});

$(document).on('click', '.setup-create-form-add-image-container', function(e){
    e.preventDefault();
    createImageForm();
});

$(document).on('click', '.delete-form', function(e){
    e.preventDefault();
    prefix = $(this).attr('id');
    deleteForm(prefix, $(this));
    return false;
});

$(document).on('submit', 'button[type="submit"]', function() {
    $('.popup-background').show();
    $('.loader').show();
});