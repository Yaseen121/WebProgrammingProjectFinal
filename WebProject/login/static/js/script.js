//An AJAX request is made containing the username of the user who is being liked. If the like already exists, the user is notified.
function likeProfile(){
  username =  $(this).attr("id")
  request = {
    url: "/like/",
    type: "POST",
    data: {
      username: username,
      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
    },
    success: function (response) {
      console.log(response)
      if(response=="Already Liked"){
        alert("You've already liked this user")
      } else {
        alert("Like added")
        responseSplit = response.split(" ")
        $("#likes"+username).html(responseSplit[0])
      }
    },
    error: function () {
      alert("There was some error")
    }
  }
  $.ajax(request)
}

//An AJAX request is made to the server including the parameters needed for the appropriate filtering. It is also responsible for displaying the returned results.
function filterProfiles() {
  gender = $("#gender").val()
  minAge = $("#minAge").val()
  maxAge = $("#maxAge").val()
  error=0
  //Input/form validation (error=1 if there is an error)
  if(minAge!="" && maxAge!=""){
    if(parseInt(minAge, 10)>parseInt(maxAge, 10)){
      alert("The minimum age cannot be greater than the maximum age.")
      error=1
    } else if (parseInt(minAge, 10)<0 || parseInt(maxAge, 10)<0){
      alert("Age cannot be negative.")
      error=1
    }
  }
  if (error==1){
    //If there was an error with the form input then dont make any request
  } else {
    request = {
      url: "/filter/",
      type: "POST",
      data: {
        minAge: minAge,
        maxAge: maxAge,
        gender: gender,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val() //Data to pass back + csrf token
      },
      success: function (response) {
        $(".loadProfiles").empty() //If there was a successful response then clear the data currently element id loadProfiles so that it can be filled with the new data
        $(".profiles").remove() // Delete the data that was initially in (The profiles that were lodaed from views.py on loggedIn page)
        console.log(response)
        //For each user in the response append the user profile with the corresponding data to the element with id loadProfiles
        //The html is the same as the profile.html with minor changes to work with this javascript data rather than data based in from views.
        for (i=0; i<response.users.length; i++) {
          var u =response.users[i].username
          var g=response.users[i].gender
          var img=response.users[i].image
          var e=response.users[i].email
          var d=response.users[i].dob
          var h=response.users[i].hobby
          var l=response.users[i].liked
          $(".loadProfiles").append("<div class='container'><div class='container bg-light rounded'><div class='col-12'><hr><div class='row'><div class='col-sm-3'><!--left col   http://ssl.gstatic.com/accounts/ui/avatar_2x.png  -->                  <div class='text-center'><img src='"+img+"' class='img-thumbnail rounded-circle' alt='avatar' height='195px' width='195px'>                    <br><h4>"+u+"</h4></div><hr><br><div class='card'>                    <div class='card-header'>Email</div><div class='card-body'><a href='"+e+"'>"+e+"</a></div></div><br><div class='card'><div class='card-header'>Likes</div><div id='likes"+u+"' class='card-body'>"+l+"</div></div></div><div class='col-sm-9'><ul class='nav nav-tabs'>                    <li class='nav-item'>                      <!--<a class='nav-link active' href=''>Profile</a>-->                      <a class='nav-link active' >Profile</a>                    </li>                    <!--Add new li for messages -->                  </ul><br><table class='table table-striped'><tbody><tr><td>Gender</td><td>"+g+"</td></tr><tr><td>Date of Birth</td><td>"+d+"</td></tr><tr><td>Hobbies</td><td class='hobby"+i+"'></td></tr></tbody></table><button id="+u+" type='button' class='like btn-primary form-control'>Like!</button></div></div><hr></div><br></div></div>")
          for (j=0; j<h.length; j++){
            $(".hobby"+i).append(h[j].name + "<br>")
          }
          $(".loadProfiles").append("<br>")
        }
        $(".like").click(likeProfile)//Once the profiles have all been loaded in again, re add the like functionality
      },
      error: function(response){
        //If there was an error print the error message
        console.log(response)
        alert("There was an error: " + response.responseJSON.message)
      }
    }
    $.ajax(request)
  }
}


//When page loads it adds the filterprofile functionality to the filter button and the like functionality to the like button
$(function() {
  $("#filter").click(filterProfiles)
  $(".like").click(likeProfile)
})
