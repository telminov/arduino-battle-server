function Control() {
    this.url_ajax_switch = undefined;
    this.url_ajax_get_port_data = undefined;
}


Control.prototype.init = function () {
    var self = this;
    console.log(this.url_ajax_switch);
    console.log(this.url_ajax_get_port_data);

    $(".toogle").click(function () {
        var toogle = $(this).attr("id");
        ajax_switch(toogle, self.url_ajax_switch);
    });

    $(".get_data").click(function () {
        console.log(self.url_ajax_get_port_data);
        $.get(self.url_ajax_get_port_data, {},
            function(data){
                    console.log(data);
               //$('#like_count').html(data);
               //$('#likes').hide();
           });
        //ajax_get_port_data(self.url_ajax_get_port_data);
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

function ajax_get_port_data(url) {
    console.log(url);
    $.ajax({
        url: self.map_url,
        dataType: 'json',
        success: function (data) {
            console.log(data);
        }
    });
}