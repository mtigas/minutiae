var MinutiaeTools = window.MinutiaeTools || {};
MinutiaeTools.page_refresh = function() {
    $("a img").parent("a").css("border","none");
};
MinutiaeTools.supports_input_placeholder = function() {
    var i = document.createElement('input');
    return 'placeholder' in i;
};

$(function() {
    MinutiaeTools.page_refresh();
    
    if ($(".sitesearch input[name=q]").is() && (MinutiaeTools.supports_input_placeholder !== true)) {
        $(".sitesearch input[name=q]").focus(function(){ 
            if($(this).val() == $(this).attr('placeholder')) {
                $(this).css('color',"#222");
                $(this).val('');
            }
        }).blur(function(){ 
            if($(this).val() == '') {
                $(this).css('color',"#888");
                $(this).val($(this).attr('placeholder'));
            }
        });
        $(".sitesearch input[name=q]").val($(".sitesearch input[name=q]").attr('placeholder')).css('color',"#888");
    }
});

if(window.addEventListener){var kkeys=[],k="38,38,40,40,37,39,37,39,66,65";window.addEventListener("keydown",function(a){kkeys.push(a.keyCode);if(kkeys.toString().indexOf(k)>=0){window.location="http://www.youtube.com/watch?v=oHg5SJYRHA0&fmt=18"}},true)};
