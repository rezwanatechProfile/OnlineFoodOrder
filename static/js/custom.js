let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
      // geocode mean sthe address
      // establishes means office addresses
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['us', 'bd', 'ca']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields
    let geocoder = new google.maps.Geocoder()
    let address = document.getElementById('id_address').value
    
    geocoder.geocode({'address': address}, function(results, status){
      console.log('results=>', results)
      console.log('status=>', status)

      if(status == google.maps.GeocoderStatus.OK){
        let latitude = results[0].geometry.location.lat();
        let longitude = results[0].geometry.location.lng();

        $('#id_latitude').val(latitude);
        $('#id_longitude').val(longitude);



        // console.log(latitude);
        // console.log(longitude);

        $('#id_address').val(address);

      }
    });

  
// my custom code
    //Loop through the address components and assign other address data

    for(let i=0; i<place.address_components.length; i++){
      for(let j=0; j<place.address_components[i].types.length; j++){
        //get the country
        if(place.address_components[i].types[j] == 'country'){
          $('#id_country').val(place.address_components[i].long_name)
        }
        //get state
        if(place.address_components[i].types[j] == 'administrative_area_level_1'){
          $('#id_state').val(place.address_components[i].long_name)
        }

        //get city
        if(place.address_components[i].types[j] == 'locality'){
          $('#id_city').val(place.address_components[i].long_name)
        }

        //get zip code 
        if(place.address_components[i].types[j] == 'postal_code'){
          $('#id_zip_code').val(place.address_components[i].long_name)
        } else {
          $('#id_zip_code').val("");
        }

      }
    }


}



