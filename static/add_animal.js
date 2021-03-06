function $(x) { return document.getElementById(x) }

$("image-upload-option-1").addEventListener("click", () => {
    if ($("image-upload-option-1").checked) {
        $("aligned-image-file").style.visibility = "hidden";
        $("aligned-image-URL").style.visibility = "visible";
    } else {
        $("aligned-image-URL").visibility = "hidden";
        $("aligned-image-file").visibility = "visible";
    }
})

$("image-upload-option-2").addEventListener("click", () => {
    if ($("image-upload-option-2").checked) {
        $("aligned-image-URL").style.visibility = "hidden";
        $("aligned-image-file").style.visibility = "visible";     
    } else {
        $("aligned-image-file").style.visibility = "hidden";
        $("aligned-image-URL").style.visibility = "visible";
    }
})