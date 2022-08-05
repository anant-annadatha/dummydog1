$("form[name=signup_form]").submit(function(e){

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/signup",
        type: "POST",
        data: data,
        dataType: "json",
        success:function(resp){
            console.log(resp);
            window.location.href = "/dashboard/";
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    })
    e.preventDefault();
});

$("form[name=signin_form]").submit(function(e){

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/signin",
        type: "POST",
        data: data,
        dataType: "json",
        success:function(resp){
            console.log(resp);
            window.location.href = "/dashboard/";
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    })
    e.preventDefault();
});

$("form[name=checkoutform]").submit(function(e){

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/dashboard/checkout",
        type: "POST",
        data: data,
        dataType: "json",
        success:function(resp){
            console.log(resp);
            $("#success-alert").show();
            setTimeout(function() { 
                $("#success-alert").hide(); 
                window.location.href = "/dashboard/";
            }, 2000);
            
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
            setTimeout(function() { 
            window.location.href = "/dashboard/";
            }, 4000);
        }
    })
    e.preventDefault();
});

$("form[name=checkinform]").submit(function(e){

    var $form = $(this);
    var $error = $form.find(".errorCI");
    var data = $form.serialize();

    $.ajax({
        url: "/dashboard/checkin",
        type: "POST",
        data: data,
        dataType: "json",
        success:function(resp){
            console.log(resp);
            $("#success-alertCI").show();
            setTimeout(function() { 
                $("#success-alertCI").hide(); 
                window.location.href = "/dashboard/";
            }, 2000);
            
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
            setTimeout(function() { 
            window.location.href = "/dashboard/";
            }, 4000);
        }
    })
    e.preventDefault();
});

$("form[name=project_create]").submit(function(e){

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/project/create",
        type: "POST",
        data: data,
        dataType: "json",
        success:function(resp){
            console.log(resp);
            window.location.href = "/project/";
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    })
    e.preventDefault();
});

$("form[name=project_retrieve]").submit(function(e){

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/project/retr",
        type: "POST",
        data: data,
        dataType: "json",
        success:function(resp){
            console.log(resp);
            window.location.href = "/project/";
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    })
    e.preventDefault();
});