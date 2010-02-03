var MinutiaeTools = window.MinutiaeTools || {};
MinutiaeTools.page_refresh = function() {
    jQuery("a img").parent("a").css("border","none");
};
MinutiaeTools.supports_input_placeholder = function() {
    var i = document.createElement('input');
    return 'placeholder' in i;
};


jQuery(function() {
    MinutiaeTools.page_refresh();
    
    if (MinutiaeTools.supports_input_placeholder !== true) {
        jQuery(".sitesearch input[name=q]").focus(function(){ 
            if(jQuery(this).val() == jQuery(this).attr('placeholder')) {
                jQuery(this).css('color',"#222");
                jQuery(this).val('');
            }
        }).blur(function(){ 
            if(jQuery(this).val() == '') {
                jQuery(this).css('color',"#888");
                jQuery(this).val(jQuery(this).attr('placeholder'));
            }
        });
        jQuery(".sitesearch input[name=q]").val(jQuery(".sitesearch input[name=q]").attr('placeholder')).css('color',"#888");
    }
});

if(window.addEventListener){var kkeys=[],k="38,38,40,40,37,39,37,39,66,65";window.addEventListener("keydown",function(a){kkeys.push(a.keyCode);if(kkeys.toString().indexOf(k)>=0){window.location="http://www.youtube.com/watch?v=oHg5SJYRHA0&fmt=18"}},true)};
