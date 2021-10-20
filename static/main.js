var autorefresh = 0;
var oldtab = "tabmail";
var table = null;
var chart; // global
var chart_interface; // TODO: change this ugly global variable?
var api_url = '/api/v1/';
var chart_seconds = 120;

var fetch_timer = 0;

function request(data, success, api_error, server_error) {
    return $.ajax({
        url: api_url,
        data: data,
        type: "POST",
        cache: false,
        success: success,
        error: function(jqXHR) {
            if (jqXHR.status == 400 && jqXHR.responseJSON) {
                if (api_error)
                    api_error(jqXHR.responseJSON);

                // User is logged out - refresh page
                if (jqXHR.responseJSON.logout)
                    location.reload();
            } else {
                console.error('AJAX request failed!');
                if (server_error) {
                    server_error(jqXHR);
                }
            }
        }
    });
}


function clearFetchInterval() {
    if (fetch_timer) {
        clearInterval(fetch_timer);
    }
    fetch_timer = 0;
}

function requestData() {
    if (!fetch_timer)
        fetch_timer = setInterval(ipstat, 1000);
    ipstat();
}

function ipstat() {
    request(
        {
            action: "ifstat",
            interface: chart_interface
        },
        function(point) {
            if (chart == null) {
                return;
            }
            var series = chart.series[0],
                shift = series.data.length > chart_seconds;
            // shift if the series is longer than chart_seconds
            if (typeof requestData.txbytes != 'undefined') {
                var stampdiff = point.stamp - requestData.stamp;
                var speedtx = (point.txbytes - requestData.txbytes) * 1000 * 8 / stampdiff;
                var speedrx = (point.rxbytes - requestData.rxbytes) * 1000 * 8 / stampdiff;
                // add the point
                chart.series[0].addPoint([point.stamp, speedtx], true, shift);
                chart.series[1].addPoint([point.stamp, speedrx], true, shift);
            }
            requestData.stamp = point.stamp;
            requestData.txbytes = point.txbytes;
            requestData.rxbytes = point.rxbytes;
        }
    );
}

function showchart() {
    var winW = window.innerWidth - 180;
    var winH = window.innerHeight - 180;

    if (winH < 300) {
        winH = 300;
    }

    $("#ifchart").dialog({
        height: winH,
        width: winW,
        modal: true,
        close: function(event, ui) {
            delete requestData.txbytes;
            delete requestData.rxbytes;
            chart.destroy();
            chart = null;
            clearFetchInterval();
        }
    });
    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'ifchart',
            defaultSeriesType: 'spline',
            events: {
                load: requestData
            }
        },
        title: {
            text: 'Interface statistics'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150,
            minRange: chart_seconds * 1000
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'Bps',
                margin: 80
            }
        },
        series: [{
            name: 'TX Speed',
            data: []
        }, {
            name: 'RX Speed',
            data: []
        }]
    });
}


function activateselect() {
    //      $(".act").selectmenu();
    // Deactivate, might make double fire
    $(".act").off();
    $(".act").change(function(e) {
        var username = $(this).closest("tr").children("td:nth-of-type(2)").text();
        var intf = $(this).closest("tr").children("td:nth-of-type(1)").text();
        var op = $(this).val();
        if (op == "watch") {
            $(".act").val('');
            chart_interface = intf;
            console.log('interface ' + intf);
            showchart();
        } else {
            $("#loadingdialog").dialog('open');
            $(".ui-dialog-titlebar").hide();

            var count = 0;

            function do_activate() {
                request(
                    {action: op, interface: intf},
                    function(ret) {
                        setTimeout(function() {
                            $(".act").val('');
                            $("#loadingdialog").dialog('close');
                        }, 1000);
                    }, function(resp) {
                        if (resp.error) {
                            alert(resp.error);
                            $("#loadingdialog").dialog('close');
                        }
                    }, function() {
                        // Server error - try again
                        count++;
                        if (count < 10)
                            setTimeout(do_activate, 1000)
                        else
                            $("#loadingdialog").dialog('close');
                    }
                );
            };

            do_activate();

        }
    });
}

function loadmain() {
    request(
        {action: "stat"},
        function(ret) {
            $("#tabmain pre").html(ret.output);
        }
    );
    if (autorefresh == 1) {
        setTimeout(loadmain, 1000);
    }
}

function refreshUserTable() {
        $("#loadingdialog").dialog('open');
        $(".ui-dialog-titlebar").hide();
        var displayLen = $('#tusers_length select').val() || 10;
        request({action: "users"}, function(ret) {
            //console.log(ret.output);
            $("#tabusers").html(ret.output);
            $("#tabusers").prepend('<button id="refreshusers">Refresh<\/button>');
            $("#refreshusers").button().click(refreshUserTable);
            // Burp... ugly, but quick hack to remove +++---++ and so
            $("tr:eq(1)").remove();
            // and also th for better styling
            $("tr:first-child td").each(function() {
                $(this).replaceWith('<th>' + $(this).text() + '<\/th>');
            });
            // fix and add thead, datatables love it and need it
            $("#tusers").prepend($('<thead><\/thead>').append($('#tusers tr:first').remove()));

            // Add action column
            $("#tusers tr:eq(0)").append('<th>Operation<\/th>');
            $("#tusers tr:gt(0)").append('<td><select class="act" name="act"><option selected><\/option><option value="killhard">Terminate(hard)<\/option><option value="killsoft">Terminate(soft)<\/option><option value="watch">Watch live<\/option><\/select><\/td>');

            $("#tusers tr").click(function() {
                // We can do something on row click... later.
                //var username = $(this).children("td:nth-of-type(2)").text();
            });


            table = $("#tusers").dataTable({
                "iDisplayLength": displayLen,
                "stateSave": true
            }).on('draw.dt', function(e, settings) {
                activateselect();
            });
            // Because draw is not fired on first event, we will fire manually
            activateselect();
            //$(".act").selectmenu();

            // Get user detailed info

        }).always(function(){ $("#loadingdialog").dialog('close');});
}

function activator(event, ui) {
    var tabname = ui.newPanel.attr('id');

    console.log('Activating tab ' + tabname);
    if (tabname == "tablogout") {
        request({action: "logout"}, function() {
            location.reload();
        });
    }
    if (oldtab == "tabusers") {
        table.clear();
        table.destroy();
        table = null;
        $("#tabusers").html('');
    }
    if (tabname == "tabmain") {
        loadmain();
    }
    if (tabname == "tabusers") {
        refreshUserTable();
    }
}

function showmainscreen() {
    $("#mainscreen").show().tabs({
        activate: activator
    });
    loadmain();
    $("#autorefresh").button().click(function(ev) {
        ev.preventDefault();
        if (autorefresh == 0) {
            $("#autorefresh").prop('value', 'Autorefresh: ON');
            autorefresh = 1;
            setTimeout(loadmain, 1000);
        } else {
            $("#autorefresh").prop('value', 'Autorefresh: OFF');
            autorefresh = 0;
        }
    });
}


function loginError(text) {
    $("#message").html(text).css('color', 'red');
    $("#flogin").hide();
    // Remove message after while
    setTimeout(function() {
        $("#message").html('');
        $("#flogin").show();
    }, 1000);
}


function trylogin(event) {
    event.preventDefault();
    var data = $('#flogin').serializeArray();
    request(data, function(returned) {
        $("#logindialog").dialog("close");
        showmainscreen();
    }, function(data) {
        loginError(data.error);
    }, function() {
        loginError('Server error, try later');
    });
}

function prelogin(data) {
    if (data.authenticated == 1) {
        // We are already authenticated
        showmainscreen();
    } else {
        if (data.login) {
            $("#login").val(data.login);
        }
        $("#logindialog").dialog('open');
    }
}


function try_prelogin() {
    request({action: "prelogin"}, prelogin, null, function() {
        setTimeout(try_prelogin, 2000);
    });
}


$(document).ready(function() {
    $("#mainscreen").hide();
    $("#logindialog").dialog({
        autoOpen: false,
        buttons: [{
            text: "Login",
            click: trylogin
        }],
        title: "accel-ppp login"
    });
    $("#loadingdialog").dialog({
        autoOpen: false,
        modal: true
    });

    try_prelogin();

//    $.post(api_url, {
//        action: "prelogin"
//    }, prelogin);
});
