$(document).ready(function () {
   $('#byAverage').show();
   $('#byPrice').hide();
   $('#byQuality').hide();
   $('#byAtmosphere').hide();
   $('#byWaitingTimes').hide();
   $('#byService').hide();
});
$(document).ready(function () {
    $("#Price").click(function () {
        $('#byAverage').hide();
        $('#byPrice').show();
        $('#byQuality').hide();
        $('#byAtmosphere').hide();
        $('#byWaitingTimes').hide();
        $('#byService').hide();
    });
    $("#Quality").click(function () {
        $('#byAverage').hide();
        $('#byPrice').hide();
        $('#byQuality').show();
        $('#byAtmosphere').hide();
        $('#byWaitingTimes').hide();
        $('#byService').hide();
    });
    $("#Atmosphere").click(function () {
        $('#byAverage').hide();
        $('#byPrice').hide();
        $('#byQuality').hide();
        $('#byAtmosphere').show();
        $('#byWaitingTimes').hide();
        $('#byService').hide();
    });
    $("#Service").click(function () {
        $('#byAverage').hide();
        $('#byPrice').hide();
        $('#byQuality').hide();
        $('#byAtmosphere').hide();
        $('#byWaitingTimes').hide();
        $('#byService').show();
    });
    $("#WaitingTimes").click(function () {
        $('#byAverage').hide();
        $('#byPrice').hide();
        $('#byQuality').hide();
        $('#byAtmosphere').hide();
        $('#byWaitingTimes').show();
        $('#byService').hide();
    });
});
