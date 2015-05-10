var data = require('sdk/self').data;
var pageMod = require('sdk/page-mod');

pageMod.PageMod({
    include: '*',
    contentScriptFile: [
        data.url('jquery-2.1.3.min.js'),
        data.url('jquery-ui-1.11.4.min.js'),
        data.url('fetch_descriptions.js')
    ]
});
