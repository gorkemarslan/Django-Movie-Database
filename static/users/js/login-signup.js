var image = new Image();
image.src = "https://images.unsplash.com/photo-1478479405421-ce83c92fb3ba?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=668&q=80";
image.onload = function () {
    $(".login-box").css("background", "url('" + image.src + "') no-repeat center");
}

