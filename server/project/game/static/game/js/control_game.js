function Control() {
    this.url_ajax_switch = undefined;
}


Control.prototype.init = function () {
    var self = this;
    console.log(this.url_ajax_switch);

    $(".toogle").click(function () {
        var toogle = $(this).attr("id");
        ajax_switch(toogle, self.url_ajax_switch);
    });
};

function ajax_switch(toggle, url) {
    console.log(url);
    $.ajax({
        method: "POST",
        url: url,
        data: {'toggle': toggle}
        }).done(function (msg) {
             console.log(msg);
            });



}