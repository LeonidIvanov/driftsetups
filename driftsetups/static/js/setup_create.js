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

function deleteForm(prefix, btn) {
    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    var formSelector = '.' + prefix + '-form-row';
    if (total > 1){
        btn.closest(formSelector).remove();
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

function openImageUploadInput() {
    $('.setup-create-form-add-image-container').click( function () {
        $('#id_image').click()
    })
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


$(document).ready(function (){
    openImageUploadInput();
    getBrandModels();
    getModelsSubModels();

    $('#id_image').change( function(){
        imageInputTumbnail(this);
    });
});


function imageInputTumbnail(input) {
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
                    var images_box = $('.images-previews');
                    images_box.append('<div class="image-box" id="setup-image"></div>');
                    $('.image-box').last().append('<img src="' + e.target.result + '"\>');
                    $('.image-box').last().append('<div class="delete-image">&times;</div>');
                    $('.delete-image').click(function () {
                        var this_image_box = $(this).parent();
                        this_image_box.remove();
                    });
                }
            })(f);

            reader.readAsDataURL(f);
        }
    }
}


$(document).on('click', '.setup-create-form-add-field', function(e){
    e.preventDefault();
    var prefix = $(this).attr('id').replace('add-', '');
    var formSelector = '.' + prefix + '-form-row:last';
    cloneMore(formSelector, prefix);
    return false;
});

$(document).on('click', '.delete-form', function(e){
    e.preventDefault();
    prefix = $(this).attr('id');
    deleteForm(prefix, $(this));
    return false;
});
