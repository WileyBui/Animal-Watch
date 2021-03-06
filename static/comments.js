$(document).ready(function() {
    var tempCommentUser = getUrlVars()["comment_user"];
    var tempCurrentUser = getUrlVars()["users_id"]

    var commentLinks = getElementsByClassName("hidden-by-user");
    for(var i = 0; i < commentLinks.length; i++)
    {
        if (tempCommentUser == tempCurrentUser) {
            commentLinks[i].style="display:none"
        }
    }
});