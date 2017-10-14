/**
* Created by FiLoY on 08.04.17.
*/
function ValidateAndImageUpload() {
    var fuData = document.getElementById('id_avatar');
    var FileUploadPath = fuData.value;

    //To check if user upload any file
    if (FileUploadPath === '') {
        alert("Пожалуйста загрузите изображение");
        console.log('ggg');
    } else {
        var Extension = FileUploadPath.substring(FileUploadPath.lastIndexOf('.') + 1).toLowerCase();
        //The file uploaded is an image
        if (Extension == "png" || Extension == "jpeg" || Extension == "jpg") {
            // To Display
            if (fuData.files && fuData.files[0]) {
                var reader = new FileReader();

                reader.onload = function(e) {
                $('#avatar').attr('src', e.target.result);
                };
                reader.readAsDataURL(fuData.files[0]);
            }
        }
        //The file upload is NOT an image
        else {
            alert("Изображения богут быть только формата png или jpg.");

        }
    }
}


