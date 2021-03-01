function $(x) = { return document.getElementById(x) }

var imageUpload = $("image");
imageUpload.addEventListener("input", () => {
    console.log("Function fired")
    var reader = new FileReader();
    imageUpload.value = reader.readAsDataURL(imageUpload.value);
    console.log(imageUpload.value);
    console.log("function ended")
});