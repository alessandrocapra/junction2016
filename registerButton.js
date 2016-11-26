$(document).ready(function(){
    $("#getButtonCode").click(function(){
      $.get("http://127.0.0.1/getButton", function (req, res) {
        $('#generatedCode').val(res);
        $('#generatedCode').css("display", "block");
        $('#copyStuff').css("display", "block");
      });
    });
});
