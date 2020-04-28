$(function(){

  $('#data-remove-info-button').click(function () {
    let title = $("#title").val()
    let firstname = $("#firstname").val()
    let lastname = $("#lastname").val()
    let suffix= $("#suffix").val()
    let email = $("#email").val()
    let phonenum = $("#phonenum").val()
    let city = $("#city").val()
    let street = $("#street").val()
    let apt = $("#apt").val()
    let state = $("#state").val()
    let country = $("#country").val()
    let zipcode = $("#zipcode").val()
    let cclast4 = $("#cclast4").val()
    let datadelmsg = $("#datadelmsg").val()
    let deviceadid =  $("#deviceadid").val()
    let privacyreg = =  $("#privacyreg").val()
    let emailpw =  $("#emailpw").val()
    $.ajax(
      { url:"http://localhost:5000/data_remove",
        type: "POST",
        data: {"title": title, "firstname": firstname, "lastname": lastname, "suffix": suffix, "email": email, "phonenum": phonenum, "city": city, "street": street, "apt": apt, "state": state, "country": country, "zipcode": zipcode, "cclast4": cclast4, "datadelmsg": datadelmsg, "deviceadid": deviceadid, "privacyreg": privacyreg, "emailpw": emailpw},
      })
      .done(function (data){
        console.log(data.answer)
        $("#add-answer").val(data.answer);
      });
  });
});
