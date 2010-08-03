var MinutiaeTools = window.MinutiaeTools || {};
MinutiaeTools.page_refresh = function() {
    jQuery("a img").parent("a").css("border","none");
};

jQuery(function() {
    MinutiaeTools.page_refresh();
});

if(window.addEventListener){var kkeys=[],k="38,38,40,40,37,39,37,39,66,65";window.addEventListener("keydown",function(a){kkeys.push(a.keyCode);if(kkeys.toString().indexOf(k)>=0){window.location="http://www.youtube.com/watch?v=oHg5SJYRHA0&fmt=18"}},true)};
