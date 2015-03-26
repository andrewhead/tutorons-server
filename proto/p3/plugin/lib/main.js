var pageMod = require("sdk/page-mod");
var self = require("sdk/self");
var contextMenu = require("sdk/context-menu");
var notifications = require("sdk/notifications");
var currentWorker;

pageMod.PageMod({
    include: '*',
    contentScriptFile: [self.data.url("jquery.min.js"), self.data.url("control.js")],
    contentStyleFile: self.data.url("style.css"),
    onAttach: function(worker) {
        currentWorker = worker;
        worker.port.on("share", function() {
            notifications.notify({
                title: "Thanks for your insight",
                text: "Insights: 5 (+1!);  L.O.C.: 1",
                iconURL: self.data.url("Ubuntu-Geek.png")
            });
        });
    }
});

var menuItem = contextMenu.Item({
    label: "Share Insight",
    context: contextMenu.SelectionContext(),
    contentScript: 'self.on("click", function() {' +
                   '  self.postMessage();' +
                   '});',
    onMessage: function() { 
        currentWorker.port.emit("write", true); 
    }
});
