function Control() {
    this.url_ajax_switch = undefined;
}


Control.prototype.init = function () {
    var self = this;
    console.log(this.url_ajax_switch);

    $(".w").click(function () {
        ajax_switch('w', self.url_ajax_switch);
    });

    $(".s").click(function () {
        ajax_switch('s', self.url_ajax_switch);
    });

    $(".a").click(function () {
        ajax_switch('a', self.url_ajax_switch);
    });
    $(".d").click(function () {
        ajax_switch('d', self.url_ajax_switch);
    });
    $(".brake").click(function () {
        ajax_switch(' ', self.url_ajax_switch);
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