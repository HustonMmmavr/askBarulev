function readURL(input) {

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#img_signup_settings').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}

$(document).ready(function() {
	$( "input[type='file']" ).change(function() {
		console.log("1");
		readURL(this);
	  // Check input( $( this ).val() ) for validity here
	});
});

$("#upload-img").change(function(){
	console.log("1");
    readURL(this);
});