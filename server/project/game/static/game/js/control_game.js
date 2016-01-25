function Control() {
    this.url_ajax_switch = undefined;
}


Control.prototype.init = function () {
    var self = this;
    console.log(this.url_ajax_switch);

    $(".on").click(function () {
        ajax_switch('o', self.url_ajax_switch);
    });

    $(".off").click(function () {
        ajax_switch('f', self.url_ajax_switch);
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